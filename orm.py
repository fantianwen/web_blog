#!/usr/bin/env python3
# coding:utf-8

from utils import mylog
import asyncio
import aiomysql


# TODO  连接池对象重复生成，效率很低
@asyncio.coroutine
def create_pool(loop=None):
    # 初始化数据库连接池
    # host = config.get('HOST')
    host = '127.0.0.1'
    print('host is : %s ' % host)

    # port = config.get('PORT')
    port = 3306
    # user = config.get('USER')
    user = 'root'
    # password = config.get('PASSWORD')
    password = 'Fantianwen09'
    # db = config.get('DB')
    db = 'awesome'
    global pool
    # 获取数据库连接池的对象
    if loop is None:
        pool = yield from aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db)
    else:
        pool = yield from aiomysql.create_pool(host=host, port=port, user=user, password=password, db=db, loop=loop)
    mylog.info('yield success!')


# insert操作
@asyncio.coroutine
def insert(sql, args):
    mylog.info('begin.....inserting user data')
    stmt = sql.replace('?', '%s')
    mylog.info(stmt)
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(stmt, args)
        print(cur.affected)
        yield from cur.close()
        yield from conn.commit()


@asyncio.coroutine
def find():
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute('select * from Users;')
        re = yield from cur.fetchall()
        print(re)


class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type


class IntergerField(Field):
    def __init__(self, name):
        super(IntergerField, self).__init__(name, 'bigint')


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(30)')


# 定义一个model的元类，要定义原类的时候，必须要使用type来进行继承
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            # 如果是Model基类，及直接返回
            return type.__new__(cls, name, bases, attrs)
        print('Found Model: %s' % (name))
        # 如果不是Model基类，就需要收集收集attrs.items()中的属性信息，将是上述Field中定义的属性封装到dict中
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v

        # 将类属性中的Filed类属性删除（动态语言，类属性和实例属性是可以进行动态的增删的）
        for k in mappings.keys():
            attrs.pop(k)

        # 创建类属性保存数据
        attrs['__mappings__'] = mappings
        attrs['__tableName__'] = name

        # 最后创建类的实例
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('no this key exists')

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    @asyncio.coroutine
    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            print('%s ====> %s' % (k, v))
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__tableName__, ','.join(fields), ','.join(params))
        mylog.info(sql)
        print('arg is %s' % (str(args)))
        yield from insert(sql=sql, args=args)

    @classmethod
    @asyncio.coroutine
    def find_all(self):
        yield from find()


class Users(Model):
    username = StringField('username')
    password = StringField('password')

#
# @asyncio.coroutine
# def test_save():
#     yield from create_pool()
#     user = Users(username='test2', password='4444')
#     yield from user.save()
#
#
# @asyncio.coroutine
# def haha():
#     yield from create_pool()
#     with (yield from pool) as conn:
#         cur = yield from conn.cursor()
#         yield from cur.execute("select * from student;")
#         re = yield from cur.fetchall()
#         print(re)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_save())
# loop.run_forever()

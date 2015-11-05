#!/usr/bin/env python3
# coding:utf-8

from utils import mylog
import pymysql


def create_connection():
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='Fantianwen09',
                                 db='awesome',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def insert(sql, args):
    stmt = sql.replace('?', '%s')
    print(stmt)
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(stmt, tuple(args))
        conn.commit()
    finally:
        conn.close()


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ','.join(L)


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class IntergerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntergerField, self).__init__(name, 'bigint', primary_key, default)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super(StringField, self).__init__(name, ddl, primary_key, default)


# boolean型的数据不可能是primary_key
class BooleanField(Field):
    def __init__(self, name=None, default=None):
        super(BooleanField, self).__init__(name, 'boolean', False, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(FloatField, self).__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


# 定义一个model的元类，要定义原类的时候，必须要使用type来进行继承
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            # 如果是Model基类，及直接返回
            return type.__new__(cls, name, bases, attrs)
        print('Found Model: %s' % (name))
        # 如果不是Model基类，就需要收集收集attrs.items()中的属性信息，将是上述Field中定义的属性封装到dict中
        mappings = dict()
        fields = []
        primarykey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    primarykey = k
                else:
                    fields.append(k)

        # 将类属性中的Filed类属性删除（动态语言，类属性和实例属性是可以进行动态的增删的）
        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda s: '`%s`' % s, fields))
        # 创建类属性保存数据
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        attrs['__primary_key__'] = primarykey
        attrs['__fields__'] = fields
        # select语句
        attrs['__select__'] = 'select `%s`,%s from `%s`' % (primarykey, ','.join(escaped_fields), name)
        # insert
        attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values (%s)' % (
            name, ','.join(escaped_fields), primarykey, create_args_string(len(fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primarykey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (name, primarykey)
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
        insert(sql=sql, args=args)


class Users(Model):
    username = StringField('username')
    password = StringField('password')

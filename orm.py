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

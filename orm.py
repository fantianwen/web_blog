#!/usr/bin/env python3
# coding:utf-8


class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type


class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(20)')


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__tableName__', None) or name
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__tableName__'] = table_name
        return type.__new__(cls, name, bases, attrs)


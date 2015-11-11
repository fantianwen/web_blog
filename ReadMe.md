# web_blog项目学习

##一、项目结构和文件配置

其中：
	config：项目的基本配置，包括：数据库的配置，flask的配置，jinja2的配置。
	static和templates：放置flask的前端文件
	tests：测试使用
	utils：工具类
	
###项目的基本配置
####1、运行环境的配置：
希望通过一个参数的改变来完成整体项目的degub和release模式的切换（flask中debug的改变）

在config文件夹下，我们通过定义default.py,development.py,production.py中定义的Config类中定义的配置参数来得到不同的发布环境

例如：(development环境的配置)

```
class DevelopmentConfig(Config):

    '''
    web的访问地址
    '''

    WEB_URL = 'http://127.0.0.1:5000'

    SECRET_KEY = 'hahah'

    '''
    mysql的相关配置
    '''

    HOST = '127.0.0.1'

    PORT = 3306

    USER = 'root'

    PASSWORD = 'Fantianwen09'

    DB = 'awesome'

```

其中:`DevelopmentConfig`继承自`default.py`中的`Config`类

####2、如何获取不同环境中的配置文件

在`__init__.py`文件中定义函数：

```python
def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'DEVELOPMENT':
            from .development import DevelopmentConfig
            return DevelopmentConfig
        elif mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        else:
            from .testing import TestingConfig
            return TestingConfig
    except ImportError as e:
        logging.info('import Config file error', e)
        from .default import Config
        return Config
```

其中，os.environ在发布的时候进行某些参数的配置（例如：`MODE`）：

```python
def change_environ():
    os.environ['MODE'] = 'DEVELOPMENT'
```

因此，每当需要改变环境的时候，只需要改变这里的值就行了。

###3、基本log类的配置

如同android中自己定制Log类，在python中也能这样配置：

```python
import logging

logging.basicConfig(level=logging.INFO, format='van===>%(levelname)s : %(message)s')


def info(msg):
    logging.info(msg)

```

每当别的.py需要的时候，只要引入这个文件就可以了。

##二、准备工作
###1、数据库

###2、orm

###3、flask

###4、css静态库和html模板

##三、初步运行




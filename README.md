 个人博客.....以及其他乱七八糟的功能
=======

------
## 开始前

- 此项目使用腾讯COS对象存储服务，如果要使用阿里OSS服务需要自行修改相关代码
  

- 代码不含有关于腾讯COS以及数据库的配置文件。在运行以前请确保你已经新建了所有需要的配置文件


- 代码运行环境为python3.6(不支持python2.x)

--------
## COS配置

- 在根目录下新建`tencent_config.py`文件，并写入以下内容：

```
TENCENT_SECRET_ID = 'TENCENT_SECRET_ID'
TENCENT_SECRET_KEY = 'TENCENT_SECRET_KEY'
TENCENT_REGION = 'TENCENT_REGION'
TENCENT_TOKEN = 'TENCENT_TOKEN'
TENCENT_SCHEME = 'TENCENT_SCHEME'
TENCENT_URL = 'TENCENT_URL'
TENCENT_DIRNAME = 'TENCENT_DIRNAME'
TENCENT_BUCKET = 'TENCENT_BUCKET'
```
其中`TENCENT_SECRET_ID`,`TENCENT_SECRET_KEY`,
`TENCENT_REGION`,`TENCENT_TOKEN`,`TENCENT_SCHEME`，
`TENCENT_BUCKET`
均为腾讯COS基本配置项(可以参考[这里](https://cloud.tencent.com/developer/article/1774343))

而`TENCENT_URL`为储存桶的url地址，`TENCENT_DIRNAME`为希望储存文件在bucket中的文件地址

--------
## 数据库配置

- 在`settings`目录下新建`config.py`文件，写入数据库配置，如下：
```
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'HOST': 'db_host',
        'PORT': '3306',
        'USER': 'db_user',
        'PASSWORD': 'db_pwd'
    }
 }
```

------
## 运行！

- 执行以下语句运行项目!
  
`python manage.py runserver --settings=settings.config 127.0.0.1:port`
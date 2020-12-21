# B2C商城

与淘宝、小米商城类似的购物平台实现。整体分为前台与后台，前台功能为用户使用，后台功能为管理员使用。

## 1.需求分析

- 商城前台
  - 商品展示
    - 商品详情
    - 商品分类
    - 商品图片
  - 广告位
  - 消息设置
  - 商品评论
  - 购物车
    - 显示定价
    - 商品列表
    - 商品的链接
    - 购物车内商品修改数量，删除
  - 订单
    - 显示价格
    - 商品列表
    - 商品详情链接
  - 结算系统
  - 用户注册
    - 注册表单
    - 防止机器人图片
  - 用户状态
    - 用户信息显示
    - 用户信息修改
- 商城后台
  - 前台各种信息对应的管理界面
  - 控制界面等，比如权限等 
## 2.确定相应模块
- 项目可以根据逻辑或者业务，将需求进行相应归类
- 根据业务：比如新闻类，商品类，用户管理，订单系统
- 根据逻辑：前台、后台
- 本系统采用前后台模块
- 一个app负责前台，一个app负责后台
## 3.确定数据库信息
- 找出对应名词，对应成数据库表格
- 确定相互之间关系
- 需要的表可能有：用户，商品，订单，新闻
## 4.确定后的程序结构
/bjtlxy/
 ├── manage.py
   ├── bjtlxy
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── myadmin 
   │   ├── admin.py
   │   ├── apps.py
   │   ├── __init__.py
   │   ├── migrations
   │   │   └── __init__.py
   │   ├── models.py
   │   ├── tests.py
   │   ├── urls.py
   │   └── views.py 后台管理视图
   │   └── viewsgoods.py 商品管理视图
   │   └── viewsorders.py 订单管理视图
   └── myweb  
   │    ├── admin.py
   │    ├── apps.py
   │    ├── __init__.py
   │    ├── migrations
   │    │   └── __init__.py
   │    ├── models.py
   │    ├── tests.py
   │    ├── urls.py
   │    └── views.py 网站首页，商品列表与详情
   │    └── viewsusers.py 会员相关操作视图
   │    └── viewsorders.py 购物车和订单处理视图
   |
   ├── templates 模板目录
   |    |--myadmin 后台模板总目录
   |    |    |--users/ 后台会员管理
   |    |    |    |--index.html         
   |    |    |    |--add.html         
   |    |    |    |--edit.html         
   |    |    |    |--repass.html         
   |    |    |--type/ 后台类别管理模板
   |    |    |    |--index.html         
   |    |    |    |--add.html         
   |    |    |    |--edit.html         
   |    |    |--goods/ 商品信息管理模板
   |    |    |    |--index.html         
   |    |    |    |--add.html         
   |    |    |    |--edit.html          
   |    |    |--orders/ 订单信息管理模板
   |    |    |    |--index.html                 
   |    |    |    |--edit.html         
   |    |    |--index.html
   |    |    |--login.html
   |    |    |--base.html
   |    |
   |    |--myweb 前台模板目录
   |
   ├── static 静态资源目录
   |    |--myadmin 后台静态资源 
   |    |    |--
   |    |    |--
   |    |
   |    |
   |    |--myweb 网站前台静态资源
   |    |    |--
   |    |    |--

## 5.操作步骤
### 5.1创建环境

```shell
conda create -n beijing_tuling python=3.5
source activate beijing_tuling
pip install django==1.11.18
```

### 5.2创建空系统并测试
- 创建空系统
  - ```
    django-admin startproject bjtlxy
    ```

- 配置系统

  - 1.创建相应文件和文件夹

  - ```
    //创建两个app：myweb、myadmin
    python manage.py startapp myadmin
    python manage.py startapp myweb
    //创建模板和静态文件文件夹，并分别为每个app创建相应的子文件夹
    mkdir templates
    cd templates
    mkdir myweb
    mkdir myadmin
    cd ..
    mkdir static
    cd static
    mkdir myweb
    mkdir myadmin
    ```

  - 2.拷贝子路由文件
  
  - ```
    # 拷贝bjtlxy/urls.py 到 myadmin和myweb 文件夹下
    # 本操作可以手动操作，也可以在pycharm中操作
    # 也可以使用命令行cp命令
    cp bjtlxy/urls.py myadmin/urls.py
    ```
    
  - 3.配置pycharm环境
  
  - 4.配置项目运行环境 manage.py
    
    - runserver 127.0.0.1:7852
    
  - 5.settings设置
    
    - app中加入myweb、myadmin
    - 静态文件设置
    ```
    STATICFILES_DIRS = [
        # BASE_DIR 是本文件最开始配置的根目录
        os.path.join(BASE_DIR, 'static')
    ]
    ```
  - 6.主路由设置
  
  - ```
    from django.conf.urls import url, include
    from django.contrib import admin
    urlpatterns = [
       url(r'^admin/', admin.site.urls),
       url(r'^myweb/', include('myweb.urls')),
       url(r'^myadmin/', include('myadmin.urls')),
       url(r'^', include('myweb.urls')),
    ]
    ```
  
  - 7.myweb/urls.py 和 myadmin/urls.py 中分别设置
  
  - ```
    from django.conf.urls import url, include
    from django.contrib import admin
    
    from .views import t
    
    urlpatterns = [
        url(r'^', t),
    ]
    ```
  - 8.myweb/views.py 和 myadmin/views.py中分别设置返回测试函数
  - ```
    from django.shortcuts import render
    from django.http.response import HttpResponse
    def t(request):
        return HttpResponse("Hello world")
    ```
  - 9.测试模板系统
    - 1. 在模板文件夹下的myweb添加模板test.html
    - 2. test.html是一个完整的html页面
         
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
            <h1>你好，北京图灵学院！！！</h1>
            </body>
            </html>
    - 3.myweb/views下编写返回函数 t2
    - ```
      from django.http.response import HttpResponse
      from django.shortcuts import render_to_response
      def t2(reqest):
          return render_to_response("./myweb/test.html")

      def t(request):
          return HttpResponse("Hello world")
      ```
    - 4.配置settings.TEMPLATES.DIRS
    - ```
      'DIRS': [os.path.join(BASE_DIR, "templates")],
      ```
    - 5.myweb/urls配置更改
    - ```
      from django.conf.urls import url, include
      from django.contrib import admin

      from .views import *

      urlpatterns = [
          url(r'^/', t),
          url(r'^t2/', t2),
      ]
      ```
- 测试系统
  
  - 测试输入不同url，返回的内容

### 5.3用户系统
- 过程
  - 确定数据库表
  - 确定对数据库表的操作
  - 确定路由和对应视图内容
  - 编写视图实现
  - 确定相应界面
  - 测试
#### 5.3.1确定用户表
- myadmin/models文件编辑
- 代码

        class Users(models.Model):
            username = models.CharField(max_length=32)
            name = models.CharField(max_length=16)
            password = models.CharField(max_length=32)
            gender = models.IntegerField(default=1)
            address = models.CharField(max_length=255)
            phone = models.CharField(max_length=16)
            email = models.CharField(max_length=50)
            state = models.IntegerField(default=1)
            # 需要留意 auto_now, auto_now_add的区别
            # http://blog.sina.com.cn/s/blog_9e2e84050101iltd.html
            update_time = models.DateTimeField(auto_created=True, auto_now=True)
            create_time = models.DateTimeField(auto_created=True, auto_now_add=True)

            class Meta:
                db_table = "tlxy_users"  # 更改表名
#### 5.3.2确定数据库表操作
- 增删改查，作为后台必须的
- 用户注册需不需要？？？如果需要，属于前台还是后台

#### 5.3.3确定路由和视图内容
- 见路由文件
- 原则：
    - 返回网页一个路由
    - 网页提交内容一个路由，由post中的action确定
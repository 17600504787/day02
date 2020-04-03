# day02
第2天作业
⼀：Web框架的设计逻辑
2：以此设计逻辑分析django框架
分析之前再看来看⼀眼django的项⽬的⽬录结构
$ tree devops/
devops/
├── devops
│ ├── __init__.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── manage.py
⼆：从hello world启程
1：创建⼀个APP(应⽤)
Django框架的组织架构：⼀个项⽬(Project)下可以有多个应⽤(APP),每个应⽤
下⾯都五脏俱全的MTV模块(就是以py结尾的⽂件)，每个模块各司其职。
$ python manage.py startapp hello
$ tree hello
hello
├── admin.py # 后台管理⽂件
├── apps.py # app命名⽂件
├── __init__.py # 初始化⽂件，有他表示这是⼀个包
├── migrations # 数据迁移⽂件
│ └── __init__.py
├── models.py # 模型⽂件
├── tests.py
├── urls.py # 定义路由，默认没有，⾃⼰加的
└── views.py # 逻辑处理，即控制器
2：配置APP
2.1：在全局配置⽂件中注册新创建的APP
$ cat devops/settings.py
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'hello.apps.HelloConfig', ]
2.2：编写处理逻辑代码（控制器）
$ cat hello/view.py
from django.http import HttpResponse
def index(request):
 return HttpResponse("<p>Hello World,Hello, Django</p>")
2.3：编写提供给⽤户访问的路由URL
URL的设计有两种模式：1、所有URL都在⼊⼝路由表注册；2：每个APP定义
⾃⼰的url,然后在全局统⼀⼊⼝的url⽂件中引⼊，最终访问的URL为全局
url+APP URL
路由表图例
⽤户访问链接 全局⼊⼝URL APP⾃定义URL
http://192.168.1.10:/
hello/
path('hello/',views.i
ndex) 不定义
http://192.168.1.10:/
hello/
path('hello/', includ
e('hello.urls')),
path('', views.index, name='i
ndex')
http://192.168.1.10:/
hello/userlist/
path('hello/', includ
e('hello.urls')),
path('userlist/', views.userlis
t, name='userlist')
以⽤户访问http://ip:8001/hello/为例分析两种理由访问⽅式
# 设计⾃⼰的url, ⽤户访问/hello就会把请求发给views模块中的index⽅法
$ cat hello/urls.py 
from django.urls import path
from hello import views
urlpatterns = [
 path('', views.index, name='index') ]
# 在统⼀访问url⼊⼝将hello的url引⼊进来
$ cat devops/urls.py 
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
 path('admin/', admin.site.urls),
 # 当你访问hello的时候，我不知道具体点⽅法，⽽是告诉你去找hello的app的
urls.py,
 path('hello/', include('hello.urls')), 
]
# 访问结果
$ curl http://ip:8001/hello/
Hello World,Hello, Django
可以直接在路由统⼀⼊⼝直接定义路由（不建议）
from django.contrib import admin
from django.urls import path
from django.urls import path,include
# ⽤户输⼊ http://ip:8001/hello/
# 从hello app中定⼀个叫views.py模块index函数来处理hello这个⽤户请求
from hello import views
urlpatterns = [
 path('admin/', admin.site.urls),
 # 如果路由是hello，总⼊⼝直接指向具体app的具体⽅法，⼀旦app过多，路由过
多，主⼊⼝会⽐较乱
 path('hello/',views.index) ]
# 访问结果
$ curl http://ip:8000/hello/
Hello World,Hello, Django
⼩结
以上这个⼩栗⼦其实只⽤到了MTV中的View以及URL(url是view的指引，这两
个会⼀起出现,统称为V),数据库和模板都没⽤上，故⽽体验不好，功能也简
单，好⽍是跑通了。接下来⼀个完整的项⽬。在此之前把V和URL的最佳实战
知识学习下
三：MTV之视图(URL&&View)
hello的⼩栗⼦主要实现了⽤户发起请求，然后Django根据⽤户发起的url路径
找到对应的处理函数，然后将内容简单返回⽽已。但现实中⽤户的请求可不是
这么简单。⽤户都会有那些请求呢，⼤致可以分为两类读和写，读有带参数和
不带参数两种场景，写肯定是带参数了
1、Request && Response
官⽅⽂档
1.1、Request——⽤户有2⼤类，5⼩类对服务器发起请求
- GET请求
 - 不带参数 
 - 带参数
 - ？参数—— url 
 - 位置参数——url设计 
 - 关键字参数——url设计 
- POST请求(正常情况下都会带参数)常⽤语表单场景
1.2、Django定义了两种url来承接5种请求
# get不带参数 get通过？加参数 post请求的url格式如下
path('hello/', views.index, name='index'),
# 关键字传参数 (?<参数名>参数类型)——视图中直接通过参数名获取值（最常⽤）
re_path('hello/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/',
views.index, name='index') ] 2：Response——2⼤类3⼩类获取到数据
- request.method —— 判断请求的⽅式
- request.body —— 第⼀种获取数据数据的⽅式
 - print(type(request.body)) # byte
 - print(QueryDict(request.body)) # QueryDict
 - print(QueryDict(request.body).dict) # dict
 
- request.GET # 第⼆种⽅式获取GET QueryDict 
 - request.GET.get('name','devops') - request.POST # 第⼆种获取post数据⽅式 <QueryDict: {'year':
['2019']
 - request.POST.getlist('id')
 
- kwargs.get('year', 2018) # 第三种获取GET 只适⽤关键字请求的数据
3：不带参数的读——get
⽤户请求带参数的url
http://123.56.73.115:8000/hello/
配置对应的url规则
$ cat hello/urls.py 
from django.urls import path
from . import views
urlpatterns = [
 path('', views.index, name='index')
后端view编写对应的处理⽅法
$ cat hello/view.py
from django.http import HttpResponse
def index(request):
 return HttpResponse("<p>Hello World,Hello, Django</p>") 4：带参数的读——get
⽤户请求带参数的url
场景的有三种场景：
# 普通参数
http://123.56.73.115:8000/hello/?year=2019&month=06
# 位置参数
http://123.56.73.115:8000/hello/2019/06
配置对应的url规则
from django.urls import path, re_path
from . import views
app_name = 'hello'
urlpatterns = [
 # 2.1: 普通传参url基本和⽆参数⼀样
 path('', views.index, name='index'),
 # If the paths and converters syntax isn't sufficient for
defining your URL patterns,
 # you can also use regular expressions. To do so, use re_path()
instead of path(). 正则⽤re_path
 # URL中每个位置数值和view中定义的参数顺序⼀⼀对应（代码可读性不好，不推荐）
 
 # 2.2：位置匹配
 re_path('([0-9]{4})/([0-9]{2})/', views.index, name='index'),
 # 2.3：关键字匹配(最优雅) (?<参数名>参数类型)??视图中直接通过参数名获取
值（最常⽤）
 re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.index,
name='index') ]
后端view编写对应的处理⽅法
# 2.1：普通参数的接收⽅法
$ cat hello/view.py
from django.http import HttpResponse
def index(request):
 # 设置默认值的⽅式获取数据更优雅
 year = request.GET.get("year","2019") 
 # 直接获取数据，没有传会报错，不建议
 month = request.GET["month"] 
 return HttpResponse("year is %s,month is %s" % (year,month))
$ http://123.56.73.115:8000/hello/?year=2019&month=06
year is 2019,month is 06
# 2.2：位置参数的接收⽅法——函数中的参数和URL中的位置⼀⼀对应（严重依赖参数顺序
且代码可读性不好，不推荐）
$ cat hello/view.py
from django.http import HttpResponse
def index(request,year,month):
 return HttpResponse("year is %s,month is %s" % (year,month))
$ http://123.56.73.115:8000/hello/2019/06/
year is 2019,month is 06
# 3：关键字传参数(?<参数名>参数类型)——视图中直接通过参数名获取值（最常⽤）
$ cat hello/view.py
from django.http import HttpResponse
def index(request, **kwargs):
 print(kwargs)
 year = kwargs.get('year', 2018)
 month = kwargs.get('month', 7)
 return HttpResponse("year is %s,month is %s" % (year,month))
# 另⼀种写法——函数参数位置⽆关，以关键字为准
def index(request,year=2018,month=8):
 return HttpResponse("year is %s,month is %s" % (year,month))
$ http://123.56.73.115:8000/hello/2019/06/
year is 2019,month is 06
5：带参数的写——post
# url最普通的就好
$ cat hello/urls.py 
from django.urls import path, re_path
from . import views
app_name = 'hello'
urlpatterns = [
 path('hello/', views.index, name='index'),
] 
# 视图通过request.POST⽅法获取数据
# 视图通过request.POST⽅法获取数据
# 模拟django表单POST提交数据
$ curl -X POST http://123.56.73.115:8000/hello/ -d
'year=2019&month=06'
year is 2019,month is 06
$ cat hello/view.py
from django.http import HttpResponse, QueryDict
# 请求参数接收,默认为GET请求，通过method判断POST请求
def index(request):
 print(request.scheme) # http
 print(request.method) # GET
 print(request.headers) # {'Content-Length': '', 'Content￾Type': 'text/plain', ……}
 print(request.path) # /hello/hello/
 print(request.META) # {'REMOTE_ADDR': '1.119.56.6',
'HTTP_HOST': '123.56.73.115:8000',……}
 print(request.GET) # <QueryDict: {'year': ['2019'], 'month': ['06']}>: 获取相应信息中get发送的数据, request.GET.getlist('id'), 适⽤于
复选框的场景，如：id=1&id=2,结果存为列表
 data = request.GET
 year = data.get("year", "2019")
 month = data.get("month", "10")
 if request.method == "POST":
 print(request.method) # POST
 print(request.body) # b'year=2019&month=06'
 print(QueryDict(request.body).dict())
 print(request.POST) # <QueryDict: {'year': ['2019'],
'month': ['06']}> 获取相应信息中post发送的数据,
request.POST.getlist('id')
 data = request.POST
 year = data.get("year","2018")
 month = data.get("month", "07")
 return HttpResponse("year is %s,month is %s" % (year,month))
6：QueryDict介绍
通过上⾯演示我们知道⽆论GET/POST请求，接受参数的数据类型都是
QueryDict。QueryDict到底做了什么事情呢
在HttpRequest 对象中，GET 和POST 属性是django.http.QueryDict 的实例，
它是⼀个⾃定义的类似字典的类，⽤来处理同⼀个键带有多个值。⽆论使⽤
GET,POST⽅式，他们最终都是通过QueryDict⽅法对传⼊的参数进⾏处理
# QueryDict常⽤⽅法
>>> from django.http import QueryDict 
>>> QueryDict('a=1&a=2&c=3') # 对⽤户请求的数据处理
<QueryDict: {'a': ['1', '2'], 'c': ['3']}>
>>> QueryDict.get(key, default=None) # 获取数据
>>> q = QueryDict('a=1&a=2&a=3')
>>> q.lists()
[('a', ['1', '2', '3'])]
>>> q = QueryDict('a=1&b=3&c=5')
>>> q.dict()
{'a': '1','b':'3','c':'5'}



⼀：MTV之模板(Templates)
官⽅介绍
⽤户通过URL发起的各种请求，我们都可以通过View中定义的处理⽅法返回给
了相应的数据，但是，返回给⽤户的界⾯体验太差了，这个时候模板就该出场
了。模板主要负责将视图返回的数据渲染到⻚⾯，更加优雅的展示给⽤户
1: 全局配置⽂件中配置模板路径
$ cat devops/settings.py
TEMPLATES = [
 {
 'BACKEND':
'django.template.backends.django.DjangoTemplates',
 'DIRS': [BASE_DIR+"/templates"],
 'APP_DIRS': True,
 'OPTIONS': {
 # ... some options here ...
 },
 },
]
# 配置解释
BACKEND 是⼀个指向实现了Django模板后端API的模板引擎类的带点的Python路径。内置
的后有django.template.backends.django.DjangoTemplates 和
django.template.backends.jinja2.Jinja2.两个模板差不多
DIRS 定义了⼀个⽬录列表，模板引擎按列表顺序搜索这些⽬录以查找模板源⽂件。默认会
先找templates⽬录
APP_DIRS 告诉模板引擎是否应该进⼊每个已安装的应⽤中查找模板。每种模板引擎后端都
定义了⼀个惯⽤的名称作为应⽤内部存放模板的⼦⽬录名
2：常⽤语法
以hello APP为例，测试常⻅数据类型的渲染⽤法
# 创建公共模板templates⽬录
$ mkdir -p devops/templates/hello
# 最简单的URL即可
$ cat hello/urls.py
from django.urls import path,re_path
from hello import views
app_name = 'hello'
urlpatterns = [
 path('', views.index, name='index')
 
]
# 编写view,模拟django常⽤的数据类型，并传给模板
$ cat hello/views.py
from django.shortcuts import render
# template渲染数据到html
def index(request):
 classname = "DevOps"
 books = ['Python','Java','Django']
 user = {'name':'kk','age':18}
 userlist = [ {'name':'kk','age':18}, {'name':'rock','age':19},
{'name':'mage','age':20}]
 return render(request, 'hello/hello.html', \
 {'classname': classname,"books":books,
"user":user, "userlist":userlist })
# 模板接收到数据并渲染⻚⾯
$ cat hello/templates/hello/hello.html
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head>
 <meta http-equiv="Content-Type" content="text/html;charset=UTF-
8" />
<title>DevOps</title> 
<head> <body> <p> {{ name }} </p> {#接受视图中的⼀般变量值#}
<li>{{ books.0 }}</li> {# 接受列表中的值#}
<li>{{ books.1 }}</li> <li>{{ books.2 }}</li>
{# 接受字典中的定义的值 #}
<div color = blue>hello my name is {{ user.name }} </br>
 my age is {{ user.age }}
</div>
{# if标签使⽤，判断user是否存在 #}
{% if user %}
 <p> name:{{ user.name }} </p>
{%else%}
 ⽤户不存在
{% endif %}
{# for循环标签，渲染books列表 #}
{% for book in books %}
<li>{{ book }}</li>
{% endfor %}
{# for循环输出列表嵌套字典数据 #}
{% for user in userlist %}
<li>{{ user.name }}-->{{ user.age }}</li>
{% endfor %}
</body>
</html>
# 结果如下：
Python
Java
Django
hello my name is kk
my age is 18
name:kk
Python
Java
Django
kk-->18
rock-->19
mage-->20


Template模板继承——简化代码
Django 使⽤了“模板继承”的概念,模板继承让你在模板间⼤⼤减少冗余内容：
每⼀个模板只需要定义它独特的部分即可。
如下图：⼤部分⽹址的布局的类型，其中变化的是中间部分，周边基本保持不
变。我们把公共不变的地⽅抽出来作为公共模版，各个⼦⻚⾯继承模版直接引
⽤公共部分，同时对变对部分进⾏重写。这种设计代码得到最⼤程度的复⽤，
并且使得添加内容更加简单
⼀、⽤户需求
⽤户访问http://192.168.1.10:8001/hello/list，返回⼀个⽤户列表，以表格形式
呈现
⼆、定义URL和Views
正常情况下我们需要startapp新建⼀个app, 本例我们以现有的hello app来练
习。
第⼀步：定义⽤户访问⼊⼝——url
$ cat hello/urls.py
app_name = 'hello'
urlpatterns = [
 path('list/', views.list, name = 'list'),
]
第⼆步：编写对于url的view,l来处理⽤户的请求
$ cat hello/views.py
from django.shortcuts import render
def list(request):
 users = [
 {'username': 'kk1', 'name_cn': 'kk1', 'age': 18},
 {'username': 'kk2', 'name_cn': 'kk2', 'age': 19},
 {'username': 'kk3', 'name_cn': 'kk3', 'age': 20},
 ]
 return render(request,'list.html',{'users':users})
三、编写template⽂件
1、常规写法
cat templates/userlist.html
<html> <head>
 <title>⾃动化运维平台</title>
</head> <body>
<!-- 每个⻚⾯都有个标题且样式基本不会变，可以抽象出来。变的标题内容做成变量 -->
<p style="background-color:yellow;">⽤户列表</p>
<!-- ⻚⾯都内容往往是变化的这⼀块，做成变量即可 -->
<table border="1"> <thead>
 <tr>
 <th>⽤户名</th>
 <th>姓名</th>
 <th>年龄</th>
 </tr>
</thead> <tbody>
 {% for user in users %}
 <tr>
 <td>{{ user.username }}</td>
 <td>{{ user.name_cn }}</td>
 <td>{{ user.age }}</td>
 </tr>
 {% endfor %}
</tbody>
</table>
<!-- 每个⻚⾯都有个底部且样式基本不会变，可以抽象出来 -->
<p style="background-color:red;">版权所有：⻢哥教育</p>
</body>
</html> 2、模板继承及渲染
定义⺟版
$ cat templates/base.html 
……
<html> <head>
 <title>⾃动化运维平台</title>
</head> <body>
<!-- 每个⻚⾯都有个标题且样式基本不会变，可以抽象出来。变的标题内容做成变量 -->
<p style="background-color:yellow;">
 {% block title %} ⽤户列表 {% endblock %}
</p>
<!-- ⻚⾯都内容往往是变化的这⼀块，做成变量即可 -->
 {% block content %}
 {% endblock %}
<!-- 每个⻚⾯都有个底部且样式基本不会变，可以抽象出来 -->
<p style="background-color:red;">版权所有：⻢哥教育</p>
</body>
</html>
⼦⻚⾯继承
$ cat templates/userlist.html 
<!-- 继承⺟版不变的部分 -->
{% extends "base.html" %}
<!-- 重写⺟版变的部分-->
{% block title %} ⽤户的列表 {% endblock %}
<!-- 重写⺟版变的部分-->
{% block content %}
<table border="1"> <thead>
 <tr>
 <th>⽤户名</th>
 <th>姓名</th>
 <th>年龄</th>
 </tr>
</thead> <tbody>
 {% for user in users %}
 <tr>
 <td>{{ user.username }}</td>
 <td>{{ user.name_cn }}</td>
 <td>{{ user.age }}</td>
 </tr>
 {% endfor %}
</tbody>
</table>
{% endblock %}
Template过滤器——前端处理数据
⼀、Django⾃带常⽤过滤器
1：传⼊参数的⻓度
{% if messages|length >= 3 %}
 You have lots of messages today!
{% else %}
 You have not messages today!
{% endif %}
2：default——传⼊的值为false则显示默认值
{{ value|default:"nothing" }}
3：first/last——只展示列表中的第⼀/最后元素
{{ value|first }}
# 如果值是列表['a'， 'b'， 'c'] ，输出将为'a'。
{{ value|last }} 同上取最后⼀个
4：join——将列表转为字符串，同Python的 str.join(list)
{{ value|join:" // " }}
# 如果value是列表['a'， 'b'， 'c']，输出将是字符串“a // b // c“。
5：length——判断字符串和列表的⻓度
{{ value|length }}
如果value是['a'， 'b'， 'c'， 'd']或"abcd"，输出将为4。
{{ value|length_is:"4" }}
如果value是['a'， 'b'， 'c'， 'd']或"abcd"，输出将为True。 6：static 要链接保存在STATIC_ROOT中的静态⽂件，Django附带了static模板
标记。⽆论是否使⽤RequestContext，您都可以使⽤此⽅法。
{% load static %}
<img src="{% static "images/hi.jpg" %}" alt="Hi!" />
{% load static %}
{% static "images/hi.jpg" as myphoto %}
<img src="{{ myphoto }}"></img>
7：date
# 如果 value=datetime.datetime.now()，将返回当前时间的年-⽉-⽇格式
{{ value|date:"Y-m-d" }}
8：safe
Django的模板中会对HTML标签和JS等语法标签进⾏⾃动转义，原因显⽽易
⻅，这样是为了安全。但是有的时候我们可能不希望这些HTML元素被转义，
⽐如我们做⼀个内容管理系统，后台添加的⽂章中是经过修饰的，这些修饰可
能是通过⼀个类似于FCKeditor编辑加注了HTML修饰符的⽂本，如果⾃动转义
的话显示的就是保护HTML标签的源⽂件。为了在Django中关闭HTML的⾃动
转义有两种⽅式，如果是⼀个单独的变量我们可以通过过滤器“|safe”的⽅式告
诉Django这段代码是安全的不必转义。
⽐如：
value="<a href="">点击</a>"
{{ value|safe}}
9：csrf_token
这个标签⽤于跨站请求伪造保护
<form action="/login/" method="post">
 {% csrf_token %} #加上这个才能正常POST请求
 <p><input type="text" name="user"></p>
 <input type="submit">
</form>
10：slice——切⽚
使⽤形式：{{some_list | slice:":2"}}
作⽤：与python语法中的slice相同，:2表示第⼀的第⼆个元素
⼆、⾃定义模版标签和过滤器
Python中，你可以通过⾃定义标签或过滤器的⽅式扩展模板引擎的功能，并使
⽤{{ load }}标签在你的模板中进⾏调⽤。
1：⾃定义标签和过滤器的代码布局
⾃定义模板标签和过滤器必须位于Django 的某个应⽤中。如果它们与某个已
存在的应⽤相关，那么将其与应⽤绑在⼀起才有意义。
1.1：⾃定义标签/过滤器在⼀个名为mytag.py的⽂件中，那么app⽬录结构看起
来应该是这样的：
hello/
 __init__.py
 models.py
 templatetags/
 __init__.py
 mytag.py
 views.py
1.2：可以在模板中像如下这样使⽤： {% load mytag %}
1.3：需要注意的点
为了让{{ load }} 标签⼯作，包含⾃定义标签的应⽤(hello)必须在
INSTALLED_APPS中注册。 在 templatetags 包中放多少个模块没有限制。只
需要记住{% load 标签名 %} 声明将会载⼊给定模块名中的标签/过滤器名，⽽
不是应⽤的名称。 在模板⾥使⽤标签或过滤器之前你将需要重启服务器。
1.4 ⼩例⼦
A、定义标签 $ cat hello/templatetags/mytag.py
from django import template
register = template.Library()
@register.filter
def sssss(x,y): # 接收两个参数
 return int(x)*2+int(y)
B、 模版调⽤标签
$ cat hello/templates/hello.html
{% load mytag %}
# 管道符前⾯为第⼀个参数，后⾯为第⼆个参数
<p>{{ "2" |sssss:'1' }}</p> 





⼀、模型概念
官⽅⽂档
模型准确且唯⼀的描述了数据。它包含您储存的数据的重要字段和⾏为。⼀般
来说，每⼀个模型都映射⼀张数据库表。
1、常⽤字段类型
<1> CharField
 #字符串字段, ⽤于较短的字符串.
 #CharField 要求必须有⼀个参数 maxlength, ⽤于从数据库层和Django校
验层限制该字段所允许的最⼤字符数.
<2> IntegerField
 #⽤于保存⼀个整数.
<3> FloatField
 # ⼀个浮点数. 必须 提供两个参数:
 #
 # 参数 描述
 # max_digits 总位数(不包括⼩数点和符号)
 # decimal_places ⼩数位数
 # 举例来说, 要保存最⼤值为 999 (⼩数点后保存2位),你要这样定
义字段:
 #
 # models.FloatField(..., max_digits=5,
decimal_places=2)
 # 要保存最⼤值⼀百万(⼩数点后保存10位)的话,你要这样定义:
 #
 # models.FloatField(..., max_digits=19,
decimal_places=10)
 # admin ⽤⼀个⽂本框(<input type="text">)表示该字段保存
的数据.
<4> AutoField
 # ⼀个 IntegerField, 添加记录时它会⾃动增⻓. 你通常不需要直接使⽤这
个字段; 
 # ⾃定义⼀个主键：my_id=models.AutoField(primary_key=True)
 # 如果你不指定主键的话,系统会⾃动添加⼀个主键字段到你的 model.
<5> BooleanField
 # A true/false field. admin ⽤ checkbox 来表示此类字段.
 # A true/false field. admin ⽤ checkbox 来表示此类字段.
<6> TextField
 # ⼀个容量很⼤的⽂本字段.
 # admin ⽤⼀个 <textarea> (⽂本区域)表示该字段数据.(⼀个多⾏编辑
框).
<7> EmailField
 # ⼀个带有检查Email合法性的 CharField,不接受 maxlength 参数.
<8> DateField
 # ⼀个⽇期字段. 共有下列额外的可选参数:
 # Argument 描述
 # auto_now 当对象被保存时,⾃动将该字段的值设置为当前时间.通常⽤于
表示 "last-modified" 时间戳.
 # auto_now_add 当对象⾸次被创建时,⾃动将该字段的值设置为当前时间.
通常⽤于表示对象创建时间.
 #（仅仅在admin中有意义...)
<9> DateTimeField
 # ⼀个⽇期时间字段. 类似 DateField ⽀持同样的附加选项.
<10> ImageField
 # 类似 FileField, 不过要校验上传对象是否是⼀个合法图⽚.#它有两个可选
参数:height_field和width_field,
 # 如果提供这两个参数,则图⽚将按提供的⾼度和宽度规格保存. 
<11> FileField
 # ⼀个⽂件上传字段.
 #要求⼀个必须有的参数: upload_to, ⼀个⽤于保存上载⽂件的本地⽂件系统路
径. 这个路径必须包含 strftime #formatting, 
 #该格式将被上载⽂件的 date/time 
 #替换(so that uploaded files don't fill up the given
directory).
 # admin ⽤⼀个<input type="file">部件表示该字段保存的数据(⼀个⽂件上传
部件) .
 #注意：在⼀个 model 中使⽤ FileField 或 ImageField 需要以下步骤:
 #（1）在你的 settings ⽂件中, 定义⼀个完整路径给 MEDIA_ROOT 以
便让 Django在此处保存上传⽂件. 
 # (出于性能考虑,这些⽂件并不保存到数据库.) 定义MEDIA_URL 作为该
⽬录的公共 URL. 要确保该⽬录对
 # WEB服务器⽤户帐号是可写的.
 #（2） 在你的 model 中添加 FileField 或 ImageField, 并确保定
义了 upload_to 选项,以告诉 Django
 # 使⽤ MEDIA_ROOT 的哪个⼦⽬录保存上传⽂件.你的数据库中要保存的
只是⽂件的路径(相对于 MEDIA_ROOT). 
 # 出于习惯你⼀定很想使⽤ Django 提供的 get_<#fieldname>_url
函数.举例来说,如果你的 ImageField 
函数.举例来说,如果你的 ImageField 
 # 叫作 mug_shot, 你就可以在模板中以 {{
object.#get_mug_shot_url }} 这样的⽅式得到图像的绝对路径. 2、常⽤字段参数
null
 如果为True，Django将在数据库中存储⼀个空值NULL。默认为 False。
 
blank
 如果为True，则允许该字段为空⽩。默认为False。
 注意，该项与null是不同的，null纯粹是与数据库相关的。⽽blank则与验证相关。
如果⼀个字段设置为blank=True，表单验证时允许输⼊⼀个空值。⽽blank=False，则该
项必需输⼊数据。
 
unique
 如果为True，该字段必需是整个表中唯⼀的。
 
primary_key
 如果为true，那么这个字段为模型的主键
 
default=""
 可以定义某个字段的默认值
 
verbose_name
 只有ForeignKey、ManyToManyField 和 OneToOneField 的备注信息需要这个
参数，普通字段直接写描述即可
⼆、建模及同步
1、设计模型——以⼀个简单的⽤户表为例
$ cat hello/models.py
from django.db import models
class User(models.Model): # 建⽴创建表的类
 SEX = (
 ('0', '男'),
 ('1', '⼥'),
 )
 name = models.CharField(max_length = 20, 
 help_text="⽤户名") 
 password = models.CharField(max_length = 32, help_text="密码") 
 sex = models.IntegerField(choices = SEX, null=True, blank=True) 
# 数据库存0,1，展示男⼥
 
 def __str__(self): # 当对象以字符串返回时。把name返回 
 return self.name
2、同步模型内容到数据库
⽣成迁移脚本
$ python manage.py makemigrations hello
Migrations for 'hello':
 hello/migrations/0001_initial.py
 - Create model User
 
$ cat hello/migrations/0001_initial.py
# Generated by Django 2.2 on 2020-03-27 14:46
from django.db import migrations, models
class Migration(migrations.Migration):
 initial = True
 dependencies = [
 ]
 operations = [
 migrations.CreateModel(
 name='User',
 fields=[
 ('id', models.AutoField(auto_created=True,
primary_key=True, serialize=False, verbose_name='ID'
)),
 ('name', models.CharField(help_text='⽤户名',
max_length=20)),
 ('password', models.CharField(help_text='密码',
max_length=6)),
 ('sex', models.IntegerField(choices=[('0', '男'),
('1', '⼥')])),
 ],
 ),
 ]
展示迁移的sql语句
$ python manage.py sqlmigrate hello 0001 
BEGIN;
--
-- Create model User
--
CREATE TABLE `hello_user` (`id` integer AUTO_INCREMENT NOT NULL
PRIMARY KEY, `name` varchar(20) NOT NULL, `pass
word` varchar(6) NOT NULL, `sex` integer NOT NULL);
COMMIT;
执⾏数据库命令
$ python manage.py migrate hello 
Operations to perform:
 Apply all migrations: hello
Running migrations:
 Applying hello.0001_initial... OK
 
# 查看数据表已经创建
mysql> show tables;
+----------------------------+
| Tables_in_devops |
+----------------------------+
| auth_group |
| auth_group_permissions |
| auth_permission |
| auth_user |
| auth_user_groups |
| auth_user_user_permissions |
| django_admin_log |
| django_content_type |
| django_migrations |
| django_session |
| hello_user |
+----------------------------+
11 rows in set (0.00 sec)
常⽤命令：
 python manage.py makemigrations appname # ⽣成迁移脚本
 python manage.py sqlmigrate appname 0001 # 展示迁移的sql语句
 python manage.py migrate # 执⾏数据库命令
 python manage.py showmigrations # 所有的app及对应的
已经⽣效的migration
 # 将某个app的migration重置，出现冲突时这么⼲，
 python manage.py migrate --fake appname hello
 # 强制执⾏某个版本的迁移脚本
 python manage.py migrate --fake hello
 python manage.py migrate --fake hello 0003
三、ORM实现简单的增删改查（命令⾏模式）
1、ORM是什么
ORM是对数据抽象建模并提供访问接⼝的编程⽅式
模型中的⼀个类就表示⼀个表
每⼀个属性，就对应数据表中的⼀个字段
调⽤数据表，就是实例化类的对象
基于包的调⽤⽅式： from package import models
基于模块的调⽤⽅式：from package.models import classname
2、进⼊命令⾏交互
 $ python manage.py shell # 进⼊命令模式
>>> from hello.models import User # 导⼊模型⾥⾯的User
表
>>> result = User.objects.all() # 实例化User对象，查
询数据
或者
>>> from hello import models # 直接把定义模型的模块
导⼊
>>> result = models.User.objects.all() # 通过models.实例
化User对象，查询数据
3：增
A、实例化类对象的⽅式创建
>>> from hello.models import User
>>> User # 调⽤类,及
实例化对象
 <class 'hello.models.User'>
>>> u = User() # 实例化⼀个
类对象
>>> u.name = 'kk' # 通过实例化
的对象⽅式赋值
>>> u.password = '123456' 
>>> u.save(） # 将数据保存
到数据库
等价：
>>> u = User(name='kk', password="kk2020")
>>> u.save(） B、直接通过object⽅式创建（最常⽤）
# 指定字段的插⼊
>>> User.objects.create(name='kk'，password="123456") 
# 不定⻓字段的插⼊⽅式——⽣产环境中最实⽤,设计带外键的要特殊处理
>>> data = {'name':'kk','password':'123456'}
>>> User.objects.create(**data)
C、objects.get_or_create⽅式
# 这种⽅法是防⽌重复很好的⽅法，但是速度要相对慢些.
# 返回⼀个元组，第⼀个为User对象，第⼆个为True或False, 新建时返回的是True, 已
经存在时返回False.
>>> User.objects.get_or_create(name="WZT",)
2、删
 >>> u = User.objects.get(name='kk') # 删除⼀条
 >>> u.delete()
 
 >>> u.objects.filter(name='k').delete() # 删除匹配的所
有
等价：
 >>> data = {'name':'kk'}
 >>> u.objects.filter(**data).delete()
 
 >>> u.objects.all().delete() # 删除所有
3、改
A：原始⽅法——查出某个数据然后修改
>>> from hello.models import User
>>> u = User.objects.get(name='kk')
>>> u.name = 'yangmi'
>>> u.set_password('new password') # django的密码是加密的，需要
调⽤加密的⽅法
>>> u.save()
B：⾼效的⽅法
# 指定列更新
>>> user.objects.filter(id=52).update(name="cjk",password='123') 
# 不定⻓的更新
>>> data = {'name':'cjk','password':'123456'}
>>> publisher.objects.filter(id=52).update(**data)
4、查
2.1、查询多条数据——返回结果为列表嵌套字典
>>> users = User.objects.all() # 以列表显示表定义显示的字段
>>> users # 返回Queryset列表，列表中的每个元
素都为⼀个对象
[<User: fengjie>, <User: cjk>, <User: Alen>, <User: tom>,
>>> users[0] # 每个结果都是⼀个对象
<User: fengjie> 
>>> users[0].name # 获取对象的属性值 
<User: fengjie> 
>>> User.objects.all()[:1] # 切⽚获取前2条数据，不⽀持负索
引，切⽚可以节约内存
<User: fengjie>, <User: cjk>
>>> for user in users: # 遍历查询的数据
 print(user.name) # 通过列表获取对应的值
>>> User.objects.all().values_list('name', 'password') # 返回
指定的字段的值，
>>> User.objects.all().values('name', 'password') # 返回
指定的字段的值
2.2、查询⼀条数据——get条件,返回结果为⼀个Queryset对象
>>> res = User.objects.get(name="cjk"); # 返回⼀个对象，name
相当于where条件
>>> res.name # 通过属性获取对应的
值
>>> res.password
等价于
>>> data = {'name':'cjk'}
>>> res = User.objects.get(**data); 
>>> res.name 
2.3、过滤查询——filter过滤，相当于where，返回结果是列表
2.3.1、简单实例
>>> User.objects.filter(name="cjk"); 
等价于
>>> User.objects.filter(**data);
2.3.2、常⽤过滤⽅法
# 不区分⼤⼩写过滤
 >>> User.objects.filter(name__iexact="abc") # name为abc
但是不区分⼤⼩写，
# 包含过滤
 >>> User.objects.filter(name__contains="abc") # 名称中包含
"abc"的⼈
 >>> User.objects.filter(name__icontains="abc") # 名称中包含
"abc"，且abc不区分⼤⼩写
 
# 正则模糊查询
 >>> User.objects.filter(name__regex="^abc") # 正则表达式
查询
 >>> User.objects.filter(name__iregex="^abc") # 正则表达式
不区分⼤⼩写
# 排除过滤
 >>> User.objects.exclude(name__contains="WZ") 
# 排除包含 WZ 的数据
 >>> User.objects.filter(name__contains="abc").exclude(age=23) 
# 找出名称含有abc, 但是排除年龄是23岁的
# filter其他常⽤过滤查询⽅法
 __exact 精确等于 like ‘aaa’
 __iexact 精确等于 忽略⼤⼩写 ilike ‘aaa’
 __contains 包含 like ‘%aaa%’
 __icontains 包含 忽略⼤⼩写 ilike ‘%aaa%’，但是对于sqlite来
说，contains的作⽤效果等同于icontains。
 __gt ⼤于
 __gte ⼤于等于
 __lt ⼩于
 __lte ⼩于等于
 __in 存在于⼀个list范围内
 __startswith 以…开头
 __istartswith 以…开头 忽略⼤⼩写
 __endswith 以…结尾
 __iendswith 以…结尾，忽略⼤⼩写
 __range 在…范围内
 __year ⽇期字段的年份
 __month ⽇期字段的⽉份
 __day ⽇期字段的⽇
 __isnull=True/False
 __isnull=True 与 __exact=None的区别
2.3.3、get和filter的区别是什么呢？
get 和 filter都可以获取指定条件的数据对象
get适⽤于只有返回唯⼀数据的场景，即主键ID的场景，返回结果为⼀个
Queryset对象
filter适⽤于任何场景，返回结果为列表嵌套Queryset对象
2.4、values——返回所有列的k/v值或者指定的列
 >>> User.objects.filter(id=1) 
 >>> User.objects.filter(id=1).values() # 查出全部结
果以列表嵌套字典形式显示
 >>> User.objects.filter(id=1).values('id','name') # 只列出指定
的列
2.5、排序查询
 >>> User.objects.all().order_by('name')
 >>> User.objects.all().order_by('-name') # 在name 前加⼀个负
号，可以实现倒序
2.6、raw执⾏原⽣sql
In [12]: from hello.models import User 
In [13]: res = User.objects.raw('select * from hello_user') 
In [14]: for user in res: 
 ...: print(user.name) 
 ...: 
rock
mage
kk555
kk
kk
kkk
四、打通MTV
1： 创建模型(同上)
$ cat hello/models.py
from django.db import models
class User(models.Model): # 建
⽴创建表的类
 SEX = (
 ('0', '男'),
 ('1', '⼥'),
 )
 name = models.CharField(max_length = 20, 
 help_text="⽤户名") 
 password = models.CharField(max_length = 32, help_text="密码") 
 sex = models.IntegerField(choices = SEX, null=True, blank=True) 
# 数据库存0,1，展示男⼥
 
 def __str__(self): # 当对象以字符串返回时。把name返回 
 return self.name
2：创建视图
$ cat hello/views.py
from django.shortcuts import render
from hello.models import User
def userlist(request):
 users = User.objects.all() 
 return render(request ,'index.html',{'users':users})
3： 创建模版
$ cat hello/templates/index.html
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head>
 <meta http-equiv="Content-Type" content="text/html;charset=UTF-
8" />
 <title>title</title> <head> <body>
{% for user in users %}
<div> {{forloop.counter}}{{user.name}} </div> # 循环输出，并显示序
列号
{% endfor %}
</body>
</html> 4： 修改urls.py, 启动web功能测试即可
$ cat hello/urls.py
app_name = 'hello'
urlpatterns = [
 path('userlist/', views.userlist, name = 'list'),
]

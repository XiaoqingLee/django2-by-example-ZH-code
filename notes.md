Django版本
```
import django
django.get_version()
'3.0.6'
```
# 1. 创建博客应用

## 1.1 创建第一个Django项目
```
django-admin startproject mysite
```

project结构：
```
manage.py：是一个命令行工具，可以通过这个文件管理项目。其实是一个django-admin.py的包装器，这个文件在创建项目过程中不需要编辑。
mysite/：这是项目目录，由以下文件组成：
    __init__.py：一个空文件，告诉Python将mysite看成一个包。
    settings.py：这是当前项目的设置文件，包含一些初始设置
    urls.py：这是URL patterns的所在地，其中的每一行URL，表示URL地址与视图的一对一映射关系。
    wsgi.py：这是自动生成的当前项目的WSGI程序，用于将项目作为一个WSGI程序启动。
```

为了完成项目创建，还必须在数据库里创建起INSTALLED_APPS中的应用所需的数据表，打开系统命令行输入下列命令：
```
cd mysite
python manage.py migrate
```

在命令行中输入下列命令就可以启动站点：
```
python manage.py runserver
```

在启动站点的时候，还可以指定具体的主机地址和端口，或者使用另外一个配置文件，例如：
```
python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings
```

settings.py内的变量
```
DEBUG是一个布尔值，控制DEBUG模式的开启或关闭。当设置为True时，Django会将所有的日志和错误信息都打印在窗口中。在生产环境中则必须设置为False，否则会导致信息泄露。
ALLOWED_HOSTS在本地开发的时候，无需设置。在生产环境中，DEBUG设置为False时，必须将主机名/IP地址填入该列表中，以让Django为该主机/IP提供服务。
INSTALLED_APPS列出了每个项目当前激活的应用，Django默认包含下列应用：
    django.contrib.admin：管理后台应用
    django.contrib.auth：用户身份认证
    django.contrib.contenttypes：追踪ORM模型与应用的对应关系
    django.contrib.sessions：session应用
    django.contrib.messages：消息应用
    django.contrib.staticfiles：管理站点静态文件
MIDDLEWARE是中间件列表。
ROOT_URLCONF指定项目的根URL patterns配置文件。
DATABASE是一个字典，包含不同名称的数据库及其具体设置，必须始终有一个名称为default的数据库，默认使用SQLite 3数据库。
LANGUAGE_CODE站点默认的语言代码。
USE_TZ是否启用时区支持，Django可以支持根据时区自动切换时间显示。如果通过startproject命令创建站点，该项默认被设置为True。
```

## 1.2 创建应用

项目（projects）包含多个应用（applications）：
```
你可以将一个项目理解为一个站点，站点中包含很多功能，比如博客，wiki，论坛，每一种功能都可以看作是一个应用。
```

进入项目根目录（manage.py文件所在的路径），在系统命令行中输入以下命令创建第一个Django应用：
```
python manage.py startapp blog
```

应用blog的目录：
```
blog/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py

admin.py：用于将模型注册到管理后台，以便在Django的管理后台（Django administration site）查看。管理后台也是一个可选的应用。
apps.py：当前应用的主要配置文件
migrations这个目录包含应用的数据迁移记录，用来追踪数据模型的变化然后和数据库同步。
models.py：当前应用的数据模型，所有的应用必须包含一个models.py文件，但其中内容可以是空白。
test.py：为应用增加测试代码的文件
views.py：应用的业务逻辑部分，每一个视图接受一个HTTP请求，处理这个请求然后返回一个HTTP响应。
```

## 1.3 设计博客应用的数据架构（data schema）
```
一个数据模型，是指一个继承了django.db.models.Model的Python 类。Django会为在models.py文件中定义的每一个类，在数据库中创建对应的数据表。
```

为了让Django可以为应用中的数据模型创建数据表并追踪数据模型的变化，必须在项目里激活应用。要激活应用，编辑settings.py文件，添加blog.apps.BlogConfig到INSTALLED_APPS设置中：
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]
```
BlogConfig类是我们应用的配置类。现在Django就已经知道项目中包含了一个新应用，可以载入这个应用的数据模型了。

我们首先来定义一个Post类，在blog应用下的models.py文件中添加代码。

创建好了博客文章的数据模型，之后需要将其变成数据库中的数据表。Django提供数据迁移系统，用于追踪数据模型的变动，然后将变化写入到数据库中。我们之前执行过的migrate命令会对INSTALLED_APPS中的所有应用进行扫描，根据数据模型和已经存在的迁移数据执行数据库同步操作。

首先，我们需要来为Post模型创建迁移数据，进入项目根目录，输入下列命令：
```
python manage.py makemigrations blog
```

会看到如下输出：
```
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Post
```

该命令执行后会在blog应用下的migrations目录里新增一个0001_initial.py文件，可以打开该文件看一下迁移数据是什么样子的。一个迁移数据文件里包含了与其他迁移数据的依赖关系，以及实际要对数据库执行的操作。

为了了解Django实际执行的SQL语句，可以使用sqlmigrate加上迁移文件名，会列出要执行的SQL语句，但不会实际执行。在命令行中输入下列命令然后观察数据迁移的指令：
```
python manage.py sqlmigrate blog 0001
```

输出应该如下所示：
```
BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"title" varchar(250) NOT NULL, "slug" varchar(250) NOT NULL, "body" text NOT
NULL, "publish" datetime NOT NULL, "created" datetime NOT NULL, "updated"
datetime NOT NULL, "status" varchar(10) NOT NULL, "author_id" integer NOT
NULL REFERENCES "auth_user" ("id"));
CREATE INDEX "blog_post_slug_b95473f2" ON "blog_post" ("slug");
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
COMMIT;
```
具体的输出根据你使用的数据库会有变化。上边的输出针对SQLite数据库。可以看到表名被设置为应用名加上小写的类名（blog_post）也可以通过在Meta类中使用db_table属性设置表名。Django自动为每个模型创建了主键，也可以通过设置某个模型字段参数primary_key=True来指定主键。默认的主键列名叫做id，和这个列同名的id字段会自动添加到你的数据模型上。（即Post类被Django添加了Post.id属性）。

然后来让数据库与新的数据模型进行同步，在命令行中输入下列命令：
```
python manage.py migrate
```

会看到如下输出：
```
Applying blog.0001_initial... OK
```

这样就对INSTALLED_APPS中的所有应用执行完了数据迁移过程，包括我们的blog应用。在执行完迁移之后，数据库中的数据表就反映了我们此时的数据模型。

如果之后又编辑了models.py文件，对已经存在的数据模型进行了增删改，或者又添加了新的数据模型，必须重新执行makemigrations创建新的数据迁移文件然后执行migrate命令同步数据库。

定义了Post数据模型之后，可以为方便的管理其中的数据创建一个简单的管理后台。Django内置了一个管理后台，这个管理后台动态的读入数据模型，然后创建一个完备的管理界面，从而可以方便的管理数据。这是一个可以“拿来就用”的方便工具。

管理后台功能其实也是一个应用叫做django.contrib.admin，默认包含在INSTALLED_APPS设置中。

## 1.4 创建管理后台站点

要使用管理后台，需要先注册一个超级用户，输入下列命令：
```
python manage.py createsuperuser
```

会看到下列输出，输入用户名、密码和邮件：
```
Username (leave blank to use 'admin'): admin
Email address: admin@admin.com
Password: admin
Password (again): admin
Superuser created successfully.
```

使用python manage.py runserver启动站点，然后打开<http://127.0.0.1:8000/admin/>，可以看到管理后台登录页面

Group和User已经存在于管理后台中，这是因为设置中默认启用了django.contrib.auth应用的原因。

## 1.5 自定义模型在管理后台的显示

还记得blog应用的Post模型与User模型通过author字段产生外键关联吗？我们把Post模型添加到管理后台中，编辑blog应用的admin.py文件为如下这样：
```
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
然后刷新页面，可以看到Post类。

现在我们来看一下如何自定义管理后台，编辑blog应用的admin.py，修改成如下：
```
from django.contrib import admin
from .models import Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
```
这段代码的意思是将我们的模型注册到管理后台中，并且创建了一个类继承admin.ModelAdmin用于自定义模型的展示方式和行为。list_display属性指定那些字段在详情页中显示出来。@admin.register()装饰器的功能与之前的admin.site.register()一样，用于将PostAdmin类注册成Post的管理类。

再继续添加一些自定义设置，如下所示：
```
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)
```
回到浏览器，刷新一下posts的列表页。

可以看到在该页面上显示的字段就是list_display中的字段。页面出现了一个右侧边栏用于筛选结果，这个功能由list_filter属性控制。页面上方出现了一个搜索栏，这是因为在search_fields中定义了可搜索的字段。在搜索栏的下方，出现了时间层级导航条，这是在date_hierarchy中定义的。还可以看到文章默认通过Status和Publish字段进行排序，这是由ordering属性设置的。

这个时候点击Add Post，可以发现也有变化。当输入文章标题时，slug字段会根据标题自动填充，这是因为设置了prepopulated_fields属性中slug字段与title字段的对应关系。现在author字段旁边出现了一个搜索图标，并且可以按照ID来查找和显示作者，如果在用户数量很大的时候，这就方便太多了。

## 1.6 使用QuerySet和模型管理器（managers）


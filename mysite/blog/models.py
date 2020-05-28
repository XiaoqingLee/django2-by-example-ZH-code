from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):

    # Django提供了很多不同类型的字段可以用于数据模型，具体可以参考：https://docs.djangoproject.com/en/2.0/ref/models/fields/。

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    # title：这是文章标题字段。
    # 这个字段被设置为Charfield类型，在SQL数据库中对应VARCHAR数据类型
    title = models.CharField(max_length=250)

    # slug：该字段通常在URL中使用。
    # slug是一个短的字符串，只能包含字母，数字，下划线和减号。
    # 将使用slug字段构成优美的URL，也方便搜索引擎搜索。
    # 其中的unique_for_date参数表示不允许两条记录的publish字段日期和title字段全都相同，
    # 这样就可以使用文章发布的日期与slug字段共同生成一个唯一的URL标识该文章。
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # author：是一个外键字段。
    # 通过这个外键，告诉Django一篇文章只有一个作者，一个作者可以写多篇文章。
    # 对于这个字段，Django会在数据库中使用外键关联到相关数据表的主键上。
    # 在这个例子中，这个外键关联到Django内置用户验证模块的User数据模型上。

    # on_delete参数表示删除外键关联的内容时候的操作，
    # 这个并不是Django特有的定义，
    # 而是SQL 数据库的标准操作；
    # 将其设置为CASCADE意味着如果删除一个作者，
    # 将自动删除所有与这个作者关联的文章。

    # related_name参数设置了从User到Post的反向关联关系，
    # 用blog_posts为这个反向关联关系命名。

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # body：是文章的正文部分。
    # 这个字段是一个文本域，对应SQL数据库的TEXT数据类型。
    body = models.TextField()

    # publish：文章发布的时间。
    # 使用了django.utils.timezone.now作为默认值，
    # 这是一个包含时区的时间对象，
    # 可以将其认为是带有时区功能的Python标准库中的datetime.now方法。
    publish = models.DateTimeField(default=timezone.now)

    # created：表示创建该文章的时间。
    # auto_now_add表示当创建一行数据的时候，自动用创建数据的时间填充。
    created = models.DateTimeField(auto_now_add=True)

    # updated：表示文章最后一次修改的时间，
    # auto_now表示每次更新数据的时候，都会用当前的时间填充该字段。
    updated = models.DateTimeField(auto_now=True)

    # statues：这个字段表示该文章的状态，
    # 使用了一个choices参数，
    # 所以这个字段的值只能为一系列选项中的值。
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:

        # 在数据模型中的Meta类表示存放模型的元数据。
        # 通过定义ordering = ('-publish',)，
        # 指定了Django在进行数据库查询的时候，
        # 默认按照发布时间的逆序将查询结果排序。
        # 逆序通过加在字段名前的减号表示。
        # 这样最近发布的文章就会排在前边。
        ordering = ('-publish',)

    def __str__(self):
        return self.title





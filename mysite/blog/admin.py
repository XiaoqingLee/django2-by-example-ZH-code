from django.contrib import admin
from .models import Post

# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)

    # 当输入文章标题时，slug字段会根据标题自动填充，
    # 这是因为设置了prepopulated_fields属性中slug字段与title字段的对应关系
    prepopulated_fields = {'slug': ('title',)}

    # 现在author字段旁边出现了一个搜索图标，
    # 并且可以按照ID来查找和显示作者，
    # 如果在用户数量很大的时候，这就方便太多了。
    raw_id_fields = ('author',)

    # 在搜索栏的下方，出现了时间层级导航条，
    # 这是在date_hierarchy中定义的。
    date_hierarchy = 'publish'

    # 还可以看到文章默认通过Status和Publish字段进行排序，
    # 这是由ordering属性设置的。
    ordering = ('status', 'publish',)



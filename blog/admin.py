from django.contrib import admin
from .models import Article, ArticleType

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "article_type", "content", "get_read_num", "created_time", "last_updated_time",)
    ordering = ("id", )

@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name", )
    ordering = ("id",)


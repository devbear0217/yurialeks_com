from django.contrib import admin
from .models import Article, ArticleTag, ArticleCategory, AboutMe
# Register your models here.

admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(ArticleTag)
admin.site.register(AboutMe)

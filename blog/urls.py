from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.articles_list,
         name='articles_list',),
    path('<int:pk>/',
         views.article_by_id,
         name='article_by_id',),
    path('tags/<slug:slug>/',
         views.articles_by_tag,
         name='articles_by_tag'),
    path('<slug:slug>/',
         views.article_by_slug,
         name='article_by_slug',),
    path('categories/<slug:slug>/',
         views.articles_by_category,
         name='articles_by_category'),
    path('about/about_me/',
         views.about_me_view,
         name='about_me'),
    path('contact/contactme',
         views.contact_me,
         name='contact')
]

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms

# Create your models here.


class ArticleCategory(models.Model):
    name = models.CharField(verbose_name='Имя категории',
                            max_length=64,
                            unique=True,
                            default=None)

    slug_category = models.SlugField(verbose_name='Транслит',
                                     max_length=64,
                                     unique=True,
                                     default='',
                                     blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статей'


class ArticleTag(models.Model):
    name = models.CharField(verbose_name='Название тэга',
                            max_length=64,
                            unique=True)

    slug_tag = models.SlugField(verbose_name='Транслит',
                                max_length=64,
                                unique=True,
                                default='',
                                blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг статьи'
        verbose_name_plural = 'Тэги статей'

    def save(self, *args, **kwargs):
        self.slug_tag = slugify(self.slug_tag)
        super(ArticleTag, self).save(*args, **kwargs)


class Article(models.Model):
    author = models.ForeignKey('auth.User',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    titleru = models.CharField(max_length=200,
                               default=None)
    category = models.ForeignKey(ArticleCategory,
                                 related_name='articles',
                                 on_delete=models.CASCADE,
                                 default=None)
    preview_image = models.ImageField(upload_to='media/previews',
                                      default=None,
                                      null=True)
    short_text = RichTextField(blank=True,
                               null=True)
    text = RichTextUploadingField(blank=True,
                                  null=True)
    slug = models.SlugField(default='',
                            blank=True)
    tags = models.ManyToManyField(ArticleTag,
                                  verbose_name='Тэги')
    created_date = models.DateTimeField(blank=True,
                                        null=True)
    published_date = models.DateTimeField(blank=True,
                                          null=True)
    is_active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        self.slug = slugify(self.title)
        self.save()
        return self.slug

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Статья сайта'
        verbose_name_plural = 'Статьи сайта'


class AboutMe(models.Model):
    my_photo = models.ImageField(upload_to='media/uploads',
                                 default=None,
                                 null=True)
    my_description = RichTextField(blank=True,
                                   null=True)

    class Meta:
        verbose_name = 'Данные страницы обо мне'
        verbose_name_plural = 'Данные страницы обо мне'

class ContactMeForm(forms.Form):
    contact_name = forms.CharField(required=True,
                                   label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Представьтесь пожалуйста',
                                                                 'class': 'form-control'}))
    contact_email = forms.EmailField(required=True,
                                     label='',
                                     widget=forms.TextInput(attrs={'placeholder': 'Ваша почта для связи',
                                                                   'class': 'form-control'}))
    contact_subject = forms.CharField(label='',
                                      widget=forms.TextInput(attrs={'placeholder': 'Тема сообщения',
                                                                    'class': 'form-control'}))
    contact_content = forms.CharField(required=True,
                                      label='',
                                      widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение. И помните: доброта и уважение - наше всё!',
                                                                   'class': 'form-control'}))


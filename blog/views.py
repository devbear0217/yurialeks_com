from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Article, ArticleTag, ArticleCategory, AboutMe, ContactMeForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template

# Create your views here.


def articles_list(request):
    articles = Article.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'all_articles.html', {'articles': articles})


def article_by_id(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'single_article.html', {'article': article})


def article_by_slug(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'single_article.html', {'article': article})


def articles_by_tag(request, slug):
    tag = ArticleTag.objects.get(slug_tag=slug)
    articles = Article.objects.filter(tags=tag)
    return render(request, 'all_articles.html', {'articles': articles})


def articles_by_category(request, slug_category=None):
    category = None
    categories = ArticleCategory.objects.all()
    articles = Article.objects.filter(is_active=True)
    if slug_category:
        category = get_object_or_404(ArticleCategory,
                                     slug_category=slug_category)
        articles = articles.filter(category=category)
    return render(request,
                  'navbar.html', {'categories': categories,
                                  'category': category,
                                  'articles': articles, })


def about_me_view(request):
    information = get_object_or_404(AboutMe)
    return render(request, 'about_me.html',
                  {'information': information, })


def contact_me(request):
    form_class = ContactMeForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name',
                                            '')
            contact_email = request.POST.get('contact_email',
                                             '')
            contact_topic = request.POST.get('contact_subject',
                                             '')
            contact_content = request.POST.get('contact_content',
                                               '')

            context = {'contact_name': contact_name,
                       'contact_email': contact_email,
                       'contact_topic': contact_topic,
                       'contact_content': contact_content, }
            contact_message = get_template('contact_template.txt').render(context)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]
            try:
                send_mail('Получена контактная форма',
                          contact_message,
                          from_email,
                          to_email,
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Ошибка')
            return redirect('contact')
    return render(request,
                  'contact_me.html',
                  {'form': form_class, })

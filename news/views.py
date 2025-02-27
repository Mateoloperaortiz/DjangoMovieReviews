from django.shortcuts import render
from .models import News

def news(request):
    # Order by date in descending order
    all_news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news_list': all_news})

from django.contrib import admin
from django.urls import path, include
from movie import views as movieViews
from django.conf.urls.static import static # Importa 'static'
from django.conf import settings # Importa 'settings'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movieViews.home, name='home'),
    path('about/', movieViews.about, name='about'),
    path('movie/<int:movie_id>/', movieViews.movie_detail, name='movie_detail'),
    path('news/', include('news.urls')),
    path('statistics/', movieViews.statistics_view, name='statistics'),
    path('signup/', movieViews.signup_view, name='signup'),
    path('login/', movieViews.login_view, name='login'),
    path('logout/', movieViews.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path
from movie import views as movieViews
from django.conf.urls.static import static # Importa 'static'
from django.conf import settings # Importa 'settings'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movieViews.home, name='home'),
    path('about/', movieViews.about, name='about'),
    path('movie/<int:movie_id>/', movieViews.movie_detail, name='movie_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
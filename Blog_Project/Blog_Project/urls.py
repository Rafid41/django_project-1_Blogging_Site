from django.contrib import admin
from django.urls import path, include
from . import views    # . means same directory tei views.py ache j directory te ei file(urls.py) ache

# showing images
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('App_Login.urls')),
    path('blog/',include('App_Blog.urls')),
    path('', views.Index, name='index'),
]


# showing image
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

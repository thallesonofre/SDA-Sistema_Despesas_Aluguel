from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from paginas.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Pagina Inicial
    path('', Index.as_view(), name="index"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^aboutvol/', views.aboutvol, name='aboutvol'),
    url(r'^aboutcorr/', views.aboutcorr, name='aboutcorr'),
    url(r'^volcalculator/', views.engine, name='engine'),
    url(r'^corrcalculator/', views.correlation, name='correlation'),
]

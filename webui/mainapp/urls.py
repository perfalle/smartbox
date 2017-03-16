from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^show/', views.show, name='show'),
    url(r'^service/', views.service, name='service'),
    url(r'^add/', views.add, name='add'),
    url(r'^remove/', views.remove, name='remove'),
    url(r'^start/', views.start, name='start'),
    url(r'^stop/', views.stop, name='stop')
]

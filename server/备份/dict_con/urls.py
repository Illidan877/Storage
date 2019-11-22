from django.conf.urls import url, include

from dict_con import views

urlpatterns = [
    url(r'^/class', views.DictConClass.as_view()),
    url(r'^/type', views.DictConType.as_view()),
]

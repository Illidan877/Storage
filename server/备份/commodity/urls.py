from django.conf.urls import url, include

from dict_con import views

urlpatterns = [
    url(r'^$', views.DictConClass.as_view()),
]

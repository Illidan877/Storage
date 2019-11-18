from django.conf.urls import url, include

from users import views

urlpatterns = [
    url(r'^/user', views.TUser_View.as_view()),
]

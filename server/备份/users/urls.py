from django.conf.urls import url, include

from users import views

urlpatterns = [
    url(r'^/user', views.TUser_View.as_view()),
    url(r'^/role', views.TRole_View.as_view()),
    url(r'^/right', views.TRight_View.as_view()),

]

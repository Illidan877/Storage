from django.conf.urls import url

from base_dict import views

urlpatterns = [
    url(r'^/type', views.BaseType_View.as_view()),
    url(r'^/jurisdiction', views.Jurisdiction_View.as_view()),
    url(r'^/ofroles', views.Roles_View.as_view()),
    url(r'^/users', views.Users_View.as_view()),
]

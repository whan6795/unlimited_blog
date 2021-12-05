from django.conf.urls import url
from model_user import views

urlpatterns = [
    url('^login', views.LoginView.as_view()),
    url('^check', views.CheckLoginView.as_view()),
    url('^logout', views.LogOutView.as_view()),
    url('^info', views.ShowUserInfoHandler.as_view()),
    url('^reset', views.ChangePasswordHandler.as_view()),
]

from django.conf.urls import url
from model_blog import views

urlpatterns = [
    url('^test', views.Test.as_view()),
]

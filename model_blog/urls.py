from django.conf.urls import url
from model_blog import views

urlpatterns = [
    url('^manage', views.BlogManageHandler.as_view()),
    # url('^test', views.Test.as_view()),
]

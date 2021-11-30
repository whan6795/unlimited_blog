from django.conf.urls import url
from model_blog import views

urlpatterns = [
    url('^', views.BlogPortalHandler.as_view()),
    url('^/<int:user_id>', views.BlogManageHandler.as_view()),
    # url('^test', views.Test.as_view()),
]

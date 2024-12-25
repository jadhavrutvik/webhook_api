
from django.urls import path,include
from webhook.views import webhook,admin_interface,reply_to_user

urlpatterns = [
    path("webhook/",webhook,name="webhook"),
    path("",admin_interface,name="admin_interface"),
    path("reply_to_user/",reply_to_user,name="reply_to_user"),

]

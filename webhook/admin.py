from django.contrib import admin
from webhook.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=("sender","receiver","content","timestamp","mobile_no","status")
    search_fields=("sender","receiver","mobile_no")
    list_filter=("status","timestamp")




# Register your models here.

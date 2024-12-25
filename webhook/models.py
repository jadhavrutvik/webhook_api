from django.db import models

# Create your models here.
class Message(models.Model):
    sender=models.CharField(max_length=50)
    receiver=models.CharField(max_length=20)
    content=models.TextField()
    status=models.CharField(max_length=20)
    timestamp=models.DateTimeField(auto_now_add=True)
    mobile_no=models.CharField(max_length=20,null=True)
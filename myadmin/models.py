from django.db import models

# Create your models here.
# 起名比较重要,不要跟系统重复
class Users(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    gender = models.IntegerField(default=1)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50)
    state = models.IntegerField(default=1)
    update_time = models.DateTimeField(auto_created=True, auto_now=True)
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        db_table = "tlxy_users"  # 更改表名
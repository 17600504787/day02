from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('0','男'),
        ('1','女'),
    )
    name = models.CharField(max_length= 20,help_text="用户名")
    password = models.CharField(max_length = 32, help_text="密码")
    sex = models.IntegerField(choices = SEX, null=True,blank=True)

    def _str_(self):
        return self.name

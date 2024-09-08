from django.db import models

class Member(models.Model):
    uname = models.CharField(max_length=40)
    email = models.EmailField(max_length=100)
    passwd = models.CharField(max_length=50)
    repasswd = models.CharField(max_length=50)

    def __str__(self):
        return self.uname

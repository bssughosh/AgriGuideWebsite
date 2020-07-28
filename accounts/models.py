from django.db import models


# Create your models here.
class UserData(models.Model):
    aadhar = models.BigIntegerField(null=True)
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField(null=True)
    add1 = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    pincode = models.BigIntegerField()

    def __str__(self):
        return self.name

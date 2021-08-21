from django.db import models
from django.contrib.auth.models import User
from django.conf.urls.static import static


# Create your models here.
class TblRegistration(models.Model):
    id = models.BigAutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    userType = models.CharField(max_length=8)
    userGender = models.CharField(max_length=6)
    userContactNo = models.CharField(max_length=10)
    userEmail = models.EmailField()
    userAddress = models.CharField(max_length=300)
    userCity = models.CharField(max_length=50)
    userPassword = models.CharField(max_length=30)
    userCreationTime = models.TimeField()
    userCreationDate = models.DateField()
    userStatus = models.CharField(max_length=8)


class TblCustomerDetails(models.Model):
    Customerid = models.ForeignKey(TblRegistration, on_delete=models.CASCADE)
    customerBalance = models.IntegerField()


class TblSheetDetails(models.Model):
    id = models.BigAutoField(primary_key = True)
    uTime = models.TimeField()
    uDate = models.DateField()
    sheet = models.FileField(upload_to="uploads/")


class TblSheetData(models.Model):
    id = models.BigAutoField(primary_key=True)
    orderId = models.IntegerField()
    userId = models.ForeignKey(TblCustomerDetails, on_delete=models.CASCADE)
    orderAmount = models.IntegerField()
    orderCreationDate = models.DateField()
    agentId = models.ForeignKey(TblRegistration, on_delete=models.CASCADE)
    amountPaid = models.IntegerField(null=True, blank=True)
    serialNo = models.IntegerField(null=True, blank=True)
    modificationDate = models.DateField()
    orderStatus = models.CharField(max_length=15)





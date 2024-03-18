from django.db import models

# Create your models here.
class AllSecretsApi(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1,unique=True)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
    

class LastSecretApiUsing(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
    
# Create your models here.
class SupportAllSecretsApi(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1,unique=True)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
    

class SupportLastSecretApiUsing(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
    
class ExamAllSecretsApi(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1,unique=True)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
    
class ExamLastSecretApiUsing(models.Model):
    user_name = models.CharField(max_length=200)
    turn_number = models.IntegerField(default=1)
    api_key = models.CharField(max_length=200,unique=True)
    secret_key = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.user_name
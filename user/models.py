from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,AbstractUser,Group, 
Permission,PermissionsMixin)

# Create your models here.

#For MainSite (Al-Nafi) User:
class AlNafi_User(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    isMentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Al-Nafi User"



#For Islamic Academy User/Customer:
class IslamicAcademy_User(models.Model):
    id = models.IntegerField(primary_key=True)
    is_paying_customer = models.BooleanField(default=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Islamic Academy User"


#FOR MERGE USERS TABLES MAIN_USER:
class Main_User(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    source = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    isMentor = models.BooleanField(default=False)
    is_paying_customer = models.BooleanField(default=False)
    role = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        managed = True
        verbose_name = "Main User"
        ordering = ['-created_at']



class PSWFormRecords(models.Model):
    hear_about_us = models.CharField(max_length=100, blank=True, null=True)
    know_about_alnafi = models.CharField(max_length=100,default='No')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    study_field = models.CharField(max_length=255,blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    university_name = models.CharField(max_length=255,blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True, null=True)
    title_of_degree = models.CharField(max_length=100, blank=True, null=True)
    user_status_of_PSW = models.CharField(max_length=100, blank=True, null=True)
    student_visa_expiry = models.CharField(max_length=100, blank=True, null=True)
    skillset = models.CharField(max_length=255,blank=True, null=True)
    language = models.CharField(max_length=255,blank=True, null=True)
    nationality = models.CharField(max_length=255,blank=True, null=True)
    move_another_country = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="media/psw_form/resumes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def _str_(self):
        return self.full_name



#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name,phone,department, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            department=department,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='users')
    user_permissions = models.ManyToManyField(Permission, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True
    
    
class NavbarLink(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    path = models.CharField(max_length=100,null=True, blank=True)
    image = models.CharField(max_length=100,null=True, blank=True)
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name
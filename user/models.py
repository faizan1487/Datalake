from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,AbstractUser,Group, 
Permission,PermissionsMixin)
import datetime


# Create your models here.

#For MainSite (Al-Nafi) User:
class AlNafi_User(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    isMentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    assigned_date = models.DateTimeField(null=True, blank=True)
    login_source = models.CharField(max_length=100, null=True, blank=True)
    academy_demo_access = models.BooleanField(default=False)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    form = models.CharField(max_length=255,blank=True, null=True)
    advert = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        managed = True
        verbose_name = "Al-Nafi User"

#For New Al-Nafi Main Site Users Table:
class New_AlNafi_User(models.Model):
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=255, unique=True)
    student_email = models.CharField(max_length=255, null=True, blank=True)
    student_email_status = models.CharField(max_length=50, null=True, blank=True)
    verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    meta_data = models.JSONField(null=True, blank=True)
    facebook_user_id = models.CharField(null=True, blank=True, max_length=50)
    google_user_id = models.CharField(null=True, blank=True, max_length=50)
    provider = models.CharField(null=True, blank=True, max_length=50)
    affiliate_code = models.CharField(max_length=30, null=True, blank=True)
    source = models.CharField(max_length=30, null=True, blank=True,default='alnafi.edu.pk')
    easypaisa_number = models.CharField(max_length=15, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)



    def _str_(self):
        return f"{self.email or self.username}"
    
    class Meta:
        managed = True
        verbose_name = "New Al-Nafi User"




#For Islamic Academy User/Customer:
class IslamicAcademy_User(models.Model):
    id = models.IntegerField(primary_key=True)
    is_paying_customer = models.BooleanField(default=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
    
    
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
    internal_source = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    modified_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    isAffiliate = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.CharField(max_length=255, null=True, blank=True)
    affiliate_code = models.CharField(max_length=255, null=True, blank=True)
    isMentor = models.BooleanField(default=False)
    is_paying_customer = models.BooleanField(default=False)
    role = models.CharField(max_length=255, null=True, blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    student_email = models.CharField(max_length=255, null=True, blank=True)
    student_email_status = models.CharField(max_length=50, null=True, blank=True)
    verified = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    meta_data = models.JSONField(null=True, blank=True)
    facebook_user_id = models.CharField(null=True, blank=True, max_length=50)
    google_user_id = models.CharField(null=True, blank=True, max_length=50)
    provider = models.CharField(null=True, blank=True, max_length=50)
    easypaisa_number = models.CharField(max_length=15, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    academy_demo_access = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.email}"
    
    
    class Meta:
        managed = True
        verbose_name = "Main User"
        ordering = ['-created_at']



class PSWFormRecords(models.Model):
    hear_about_us = models.CharField(max_length=100, blank=True, null=True)
    know_about_alnafi = models.CharField(max_length=100,default='No')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    study_field = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    university_name = models.CharField(max_length=255,blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True, null=True)
    title_of_degree = models.CharField(max_length=100, blank=True, null=True)
    user_status_of_PSW = models.CharField(max_length=100, blank=True, null=True)
    student_visa_expiry = models.CharField(max_length=100, blank=True, null=True)
    skillset = models.CharField(max_length=255,blank=True, null=True)
    language = models.CharField(max_length=255,blank=True, null=True)
    nationality = models.CharField(max_length=255,blank=True, null=True)
    move_another_country = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="media/psw_form/resumes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return f"{self.email}"
    

class Marketing_PKR_Form(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    study_field = models.CharField(max_length=255,blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True, null=True)
    university_name = models.CharField(max_length=255,blank=True, null=True)
    # university_name_othe = models.CharField(max_length=255,blank=True, null=True)
    title_of_degree = models.CharField(max_length=100, blank=True, null=True)
    move_another_country = models.CharField(max_length=100, blank=True, null=True)
    skillset = models.CharField(max_length=255,blank=True, null=True)
    skillset_budget = models.CharField(max_length=255,blank=True, null=True)
    language = models.CharField(max_length=255,blank=True, null=True)
    financial_sponsorship = models.BooleanField(default=False,blank=True, null=True)
    resume = models.FileField(upload_to="media/marketing_pkr/resumes", blank=True, null=True)
    communication = models.CharField(max_length=255,blank=True, null=True)
    know_about_alnafi = models.BooleanField(default=False,blank=True, null=True)
    hear_about_us = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return f"{self.email}"
    


class Moc_Leads(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    form = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    login_source = models.CharField(max_length=255, null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    interest = models.CharField(max_length=255, null=True, blank=True)
    cv_link = models.CharField(max_length=255, null=True, blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    advert = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        managed = True
        verbose_name = "MOC Lead"


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

    def create_superuser(self, email, name, password=None,phone=None,department=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            department=department,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#Albaseer Users
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
        return f"{self.email}"
    

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

class CvForms(models.Model):
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.CharField(max_length=50,null=True, blank=True)
    nationality = models.CharField(max_length=100,null=True, blank=True)
    cnic_no = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=100,null=True, blank=True)
    martial_status = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    province = models.CharField(max_length=100,null=True, blank=True)
    zip_code = models.CharField(max_length=100,null=True, blank=True)
    phone_number_1 = models.CharField(max_length=100,null=True, blank=True)
    phone_number_2 = models.CharField(max_length=100,null=True, blank=True)
    updated_resume = models.FileField(upload_to="cv/resume_uploads",null=True, blank=True)
    your_picture = models.ImageField(upload_to="cv/profile_pic",null=True, blank=True)
    job = models.JSONField(null= True, blank= True)
    qualification = models.JSONField(null= True, blank= True)
    certificate = models.JSONField(null=True, blank=True)
    certificate = models.JSONField(null=True, blank=True)
    work_history =  models.JSONField(null=True, blank=True)
    skills = models.JSONField(null=True, blank=True)
    refrences = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.email


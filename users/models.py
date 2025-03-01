from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)


# Create your models here.

user_types = (
                ("medical_practitioner","medical_practitioner"),
                ("other","other"),
                )
gender = (
                ("male","male"),
                ("female","female"),
                )
class UserManager(BaseUserManager):
    def create_user(self,phone_number, full_name='null',
                    user_type="medical_practitioner",email=None,
                    specialization='doctor',image=None,
                    patient_count=0,work_experience=0,
                    gender=None,biography=None,date_of_birth=None,
                    password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if email:
            email =self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          full_name=full_name,
                          user_type=user_type,email=email,
                          specialization=specialization,
                          image=image,patient_count=patient_count,
                          work_experience=work_experience,
                          gender=gender,biography=biography,
                          date_of_birth=date_of_birth
                           )
        user.set_password(password)
        user.save(using=self._db)
        return user 
  
    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number,password=password,full_name="SITE CREATOR")
        user.is_admin = True
        user.staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    full_name = models.CharField(verbose_name='full_name', max_length=255,
                                 default='Name not set',
                                 null=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=20,unique=True)
    user_type = models.CharField(max_length=20, choices = user_types,default='medical_practitioner')
    email = models.EmailField(verbose_name='email address',max_length=255,null=True,
                              blank=True,unique=True)
    specialization = models.CharField(verbose_name='specialization', max_length=50)
    image = models.ImageField("image", upload_to='profile_images/', height_field=None, 
                              width_field=None, max_length=None,null=True)
    patient_count = models.IntegerField(verbose_name="patient_count",default=0)
    work_experience = models.IntegerField(verbose_name="work_experience",default=1)
    gender = models.CharField(verbose_name='gender',max_length=7, 
                              choices = gender,null=True)
    biography  = models.TextField(verbose_name='biography',null=True)
    date_of_birth = models.DateField(verbose_name="date_of_birth",blank=True,null=True)
    verified_number=models.BooleanField(default=False)
    verified_email=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_general_admin = models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    
    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        if not self.is_admin and self.staff:
            if perm =="Users.add_user" or perm=="Users.change_user" or perm=="Users.delete_user":
                return False
            else:
                return True
        else:
            return True

    # remember to set appropriate permissions.
    def has_module_perms(self, app_label):
        if not self.is_admin and self.staff:
            if app_label =="knox" or app_label=="auth" :
                return False
            else:
                return True
        else:
            return True
    @property

    def is_staff(self):
        return self.staff


class Patient(models.Model):
    """Model definition for Patient."""

    # TODO: Define fields here
    full_name = models.CharField(verbose_name='full_name', max_length=150)
    identifier = models.CharField(verbose_name='identifier', max_length=20)
    whatsapp_number = models.CharField(verbose_name='whatsapp_number', max_length=20,
                                       unique=True)
    medical_practitioner = models.ForeignKey(User, verbose_name="medical_practitioner",
                                             on_delete=models.CASCADE, related_name='patient_medical_practitioner')
    image = models.ImageField("image", upload_to='patients_profile_images/', height_field=None, 
                              width_field=None, max_length=None,null=True)
    address = models.CharField("address", max_length=250,default='Not Set', null=True,blank=True)
    date = models.DateField('date', auto_now=False, auto_now_add=True)
    
    

    class Meta:
        """Meta definition for Patient."""

        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        """Unicode representation of Patient."""
        return f"{self.full_name} --- {self.identifier}"

class Medical_practitional_Meta_Data(models.Model):
    """Model definition for Medical_practitional_Meta_Data."""

    # TODO: Define fields here
    medical_practitioner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_practitioner_meta')
    current_patient  = models.CharField(max_length = 50, default='none')
    status = models.CharField(verbose_name='status', max_length=6, default='closed')
    notified = models.BooleanField(default=False)
    otp = models.IntegerField(verbose_name="otp",default=0,blank=True)
    otp_created = models.DateTimeField(verbose_name="otp_created", auto_now=False, auto_now_add=False,null=True)
    last_opened = models.DateTimeField(verbose_name="last_opened", auto_now=False, auto_now_add=False,null=True)
    
    class Meta:
        """Meta definition for Medical_practitional_Meta_Data."""

        verbose_name = 'Medical_practitional_Meta_Data'
        verbose_name_plural = 'Medical_practitional_Meta_Datas'

    def __str__(self):
        """Unicode representation of Medical_practitional_Meta_Data."""
        return f"{self.medical_practitioner} --- {self.last_opened} --- {self.status}"

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)


# Create your models here.

user_types = (
                ("medical_practitioner","medical_practitioner"),
                ("other","other"),
                )

class UserManager(BaseUserManager):
    def create_user(self,phone_number, 
                    first_name='null',last_name='null',
                    user_type="individual",email=None,password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if email:
            email =self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          first_name=first_name,last_name=last_name,
                          user_type=user_type,email=email
                           )
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number,password=password,first_name="SITE",last_name="CREATOR",)
        user.is_admin = True
        user.staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    first_name =models.CharField(verbose_name='first name', max_length=255)
    last_name =models.CharField(verbose_name='last name', max_length=255)
    phone_number = models.CharField(verbose_name='phone number', max_length=20,unique=True)
    user_type = models.CharField(max_length=20, choices = user_types,default='medical_practitioner')
    email = models.EmailField(verbose_name='email address',max_length=255,null=True,blank=True)
    specialization = models.CharField(verbose_name='specialization', max_length=50,unique=True)
    verified_number=models.BooleanField(default=False)
    verified_email=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_general_admin = models.BooleanField(default=False)
    is_double = models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

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
    whatspp_number = models.CharField(verbose_name='whatspp_number', max_length=20)
    medical_practitioner = models.ForeignKey(User, verbose_name="medical_practitioner",
                                             on_delete=models.CASCADE, related_name='patient_medical_practitioner')
    

    class Meta:
        """Meta definition for Patient."""

        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        """Unicode representation of Patient."""
        return f"{self.full_name} --- {self.identifier}"


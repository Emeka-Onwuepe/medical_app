from django import forms
from django.contrib.auth import get_user_model
User=get_user_model()

# from django.db import models

class UserModelForm(forms.ModelForm):
    """Form definition for UserModel."""
    class Meta:
        """Meta definition for UserModelform."""
        model = User
        fields = ('full_name','phone_number',
                  'email','specialization',
                  'image','work_experience',
                    'gender','biography','date_of_birth',
                    )   
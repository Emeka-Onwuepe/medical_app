from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Patient
User=get_user_model()
from django.contrib.auth import authenticate

class Get_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude=["password","last_login","is_active","is_admin","staff",
                    "is_superuser","groups","user_permissions","is_general_admin",]

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email","phone_number",
                  'specialization',"password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data["phone_number"],validated_data["full_name"],
                                        'medical_practitioner',
                                        validated_data["email"],validated_data["specialization"],
                                        password=validated_data["password"]
                                        )
        user.save()
        return user      
    
    
class Edit_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name','phone_number','email','specialization',
                  'image','work_experience','gender','biography',
                    'date_of_birth',]

        # def create(self, validated_data):
        #     user = User.objects.create_user(validated_data["phone_number"],validated_data["full_name"],
        #                                     'medical_practitioner',
        #                                     validated_data["email"],validated_data["specialization"],
        #                                     validated_data["password"]
        #                                     )
        #     user.save()
        #     return user            


class Login_Serializer(serializers.Serializer):
    phone_number= serializers.CharField()
    password= serializers.CharField()
    
    def validate(self,data):
        user= authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Credentials")  
    
class Patient_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        
class Patient_Serializer_init(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id','full_name')
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model



User = get_user_model()


class AccountsSerializer(serializers.ModelSerializer):

    # either this have to be done or 
    # password2 have to added in the password2 also
    password2           = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

        extra_kwargs = {'password': {'write_only': True}}


    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists")
        return value


    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2') # using pop here from the data cause password2 is not a field in model
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data


    # the data.pop in validate was not that much nessesary cause
    # the model value assigning, we're handling that in this create
    # method where the default create method
    # assigns the values as it is, we are not 
    # we are handling the user creating and password set
    
    def create(self, validated_data):  
        #print(validated_data)
        user_obj = User(
                username=validated_data.get('username'), 
                email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
import datetime
from django.utils import timezone


# proper way of getting the data from the jwt configs, 
# (out overwritten payload handler is referenced here)
# cause we overriten it in the settings file

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta                    = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()


class AccountsSerializer(serializers.ModelSerializer):

    # either this have to be done or 
    # password2 have to added in the password2 also
    password2                       = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    token                           = serializers.SerializerMethodField()
    expiry                          = serializers.SerializerMethodField() 
    # token_with_custom_handler       = serializers.SerializerMethodField()
    is_authenticated                = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expiry',
            # 'token_with_custom_handler',
            'is_authenticated',
        ]

        extra_kwargs = {'password': {'write_only': True}}


    def get_is_authenticated(self, obj):
        context = self.context
        request = context['request']

        return  request.user.is_authenticated

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    
    def get_expiry(self, obj):
        expires = timezone.now() + expire_delta - datetime.timedelta(seconds=200)
        return expires

    # def get_token_with_custom_handler(self, obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     response = jwt_response_payload_handler(token, user, request=None)
    #     return response


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
        
        # by default the user is not activated
        user_obj.is_active = False
        user_obj.save()
        return user_obj
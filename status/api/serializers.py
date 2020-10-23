from rest_framework import serializers
from status.models import StatusModel
from accounts.api.serializers import UserPublicSerializer


class UserStatusSerializer(serializers.ModelSerializer):
    uri             = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StatusModel
        fields = [
            'id',
            'content',
            'image',
            'uri'
        ] 

    def get_uri(self, obj):
        return "/api/status/{id}/".format(id=obj.id)



class StatusSerializer(serializers.ModelSerializer):
    user            = UserPublicSerializer(read_only=True)
    uri             = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StatusModel
        fields = [
            'user',
            'id',
            'content',
            'image',
            'uri'
        ]

        read_only_fields = ['user']

    

    def get_uri(self, obj):
        return "/api/status/{id}/".format(id=obj.id)


    def validate_content(self, value):
        content  = value

        if content == "":
            content = None

        if content is not None:
            if len(content) > 240:
                raise serializers.ValidationError('Content too long')
        else:
            raise serializers.ValidationError('Content can\'t be empty')

        return content

    # def validate(self, data):

    #     image = data.get('image', None)

    #     if image is None:
    #         raise serializers.ValidationError("Image Required !!!!")

    #     return data




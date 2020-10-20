from rest_framework import serializers
from status.models import StatusModel


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = [
            'user',
            'id',
            'content',
            'image',
        ]

        read_only_fields = ['user']


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




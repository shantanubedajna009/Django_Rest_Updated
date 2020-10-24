from rest_framework import serializers
from rest_framework.reverse import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
import datetime
from django.utils import timezone

from status.api.serializers import UserStatusSerializer

User = get_user_model()


class CustomHyperlinkMethoedField(serializers.HyperlinkedRelatedField):

    def __init__(self, *args, **kwargs):
        super(CustomHyperlinkMethoedField, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(CustomHyperlinkMethoedField, self).get_queryset(*args, **kwargs)

        return qs[:3]


class UserDetailSerializer(serializers.ModelSerializer):
    uri                 = serializers.SerializerMethodField(read_only=True)
    recent_status       = serializers.SerializerMethodField(read_only=True)
    statuses            = CustomHyperlinkMethoedField(source='statusmodel_set', # basically specifying
                                                                                   # the reverse queryset
                                                                                   # since this is the user obj
                                                                                   # so user_obj.statusmodel_set 
                                                            view_name='status-api:detail',
                                                            lookup_field='id',
                                                            many=True,
                                                            read_only=True,

                                                            )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'recent_status',
            'statuses',
        ]

    def get_uri(self, obj):
        return reverse("api-user:detail", kwargs={'username': obj.username}, request=self.context['request'])

    def get_recent_status(self, obj):

        request = self.context['request']
        
        limit = 1
        limit = request.GET.get('status_limit')

        try:
            limit = int(limit)
        except:
            limit = 1
        
        qs = obj.statusmodel_set.order_by('-timestamp')[:limit]

        serialized_data = UserStatusSerializer(qs, context={'request': request}, many=True).data

        data = {
            'status_endpoint': reverse("api-user:status-list", kwargs={'username': obj.username}, request=self.context['request']),
            'list': serialized_data,
        }

        return data



from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer
from status.api.serializers import UserStatusSerializer
from status.models import StatusModel

User = get_user_model()

class UserDetailApiView(RetrieveAPIView):
    serializer_class    = UserDetailSerializer
    queryset            = User.objects.filter(is_active=True)
    lookup_field        = 'username'


    def get_serializer_context(self, *args, **kwargs):
        context = super(UserDetailApiView, self).get_serializer_context(*args, **kwargs)

        context['request'] = self.request
        return context



class UserStatusListView(ListAPIView):
    serializer_class        = UserStatusSerializer
    queryset                = StatusModel.objects.all()


    def get_queryset(self, *args, **kwargs):
                    # always use self.kwargs, cause we are accesing the global one
        username = self.kwargs.get('username', None) # This can be used here cause 
                                                     # django urlparametrs can be 
                                                     # at place at the endpoint
                                                     # it not nessesarily need to be at the end
                                                     # so the username can be get from this also
                                                     # api/user/(?P<username>\w+)/status/

        qs = StatusModel.objects.filter(user__username=username)

        return qs

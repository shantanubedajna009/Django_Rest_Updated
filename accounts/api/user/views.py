from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserDetailSerializer
from status.api.serializers import UserStatusSerializer
from status.models import StatusModel
from status.api.views import StatusListAPIView


User = get_user_model()

class UserDetailApiView(RetrieveAPIView):
    serializer_class    = UserDetailSerializer
    queryset            = User.objects.filter(is_active=True)
    lookup_field        = 'username'


    def get_serializer_context(self, *args, **kwargs):
        context = super(UserDetailApiView, self).get_serializer_context(*args, **kwargs)

        context['request'] = self.request
        return context



class UserStatusListView(StatusListAPIView):
    serializer_class        = UserStatusSerializer
    queryset                = StatusModel.objects.all()




    # inherited get_queryset either from other class or a generic view
    # doesn't get overwritten, they get combinedin this case the 
    # StatusListApiView Search fields and ordering fields gets combined
    #  with the current one
    # the overwritten tasks gets executed first and whatever queryset is returned the 
    # previus get_queryset tasks gets executed after that
    
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

    def post(self, *args, **kwargs):
        return Response({'detail': 'This is Not Allowed Here'})


    def get_serializer_context(self, *args, **kwargs):
        context = super(UserStatusListView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request

        return context
from rest_framework.generics import (
                                        ListAPIView, 
                                        CreateAPIView, 
                                        DestroyAPIView, 
                                        RetrieveAPIView, 
                                        UpdateAPIView,
                                        RetrieveUpdateDestroyAPIView,
                                    )
from rest_framework.views import APIView
from rest_framework.response import Response
from status.models import StatusModel
from .serializers import StatusSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import (
                                    CreateModelMixin, 
                                    UpdateModelMixin, 
                                    DestroyModelMixin, 
                                    RetrieveModelMixin,
                                    )

from status.utils import is_json
import json




class StatusListAPIView(CreateModelMixin, ListAPIView):
    
    #overriding global permisson and authentication classes
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    
    serializer_class = StatusSerializer
    queryset = StatusModel.objects.all()

    
    # works as a Createview with the help of the Mixin
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

    def get_queryset(self, *args, **kwargs):
        request = self.request

        print('\n\n\n\n', request.user, '\n\n\n\n')

        q = request.GET.get('q', None)

        if q:
            # qs = (  
            #         Q(content__icontains=q) |
            #         Q(user__username__icontains=q)
            #      )
            
            qs = StatusModel.objects.filter(  
                    Q(content__icontains=q) |
                    Q(user__username__icontains=q)
                 )

            if qs.exists():
                return qs

        return super(StatusListAPIView, self).get_queryset(*args, **kwargs)
        # same as return StatusModel.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)



class StatusDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = []
    
    serializer_class = StatusSerializer
    queryset = StatusModel.objects.all()
    lookup_field = 'id'


    # these views under the hood calls
    # perform_create/perform/update/perform_destroy   respectively

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


    # def get_object(self, *args, **kwargs):

    #     # have to use self.kwargs to get the id here as all insted class based viuew methods
    #     # this locally passed kwargs is empty
    #     id_ = self.kwargs.get('id', None)

    #     if id_:
    #         #etai 404 raise korbe
    #         obj = get_object_or_404(StatusModel, id=id_)

    #         return obj
    #     else:
    #         return super(StatusDetailAPIView, self).get_object(*args, **kwargs)




# # class StatusCreateAPIView(CreateAPIView):
# #     permission_classes = []
# #     authentication_classes = []
# #     serializer_class = StatusSerializer
# #     queryset = StatusModel.objects.all()
# #     #lookup_field = 'id'

# #     # to set the user as current requested one if not selected
# #     # def perform_create(self, serializer):
# #     #     serializer.save(user=self.request.user)




# # this does the same thing as the mixins for the DetailView
# class StatusDetailAPIView(RetrieveUpdateDestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer
#     queryset = StatusModel.objects.all()
#     lookup_field = 'id'



# class StatusUpdateAPIView(UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer
#     queryset = StatusModel.objects.all()
#     lookup_field = 'id'


# class StatusDeleteAPIView(DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     serializer_class = StatusSerializer
#     queryset = StatusModel.objects.all()
#     lookup_field = 'id'


































































































""" first by default the get() method calls the get queryset
    
    GET_QUERYSET():
    by default the get method in a listview calls the get_queryset
    we are ovverwriding the geet method to call retrieve
    which calls the get_object whicch gets get_queryset() as a query and 
    passes to queryset itself to get_object_or_404(this takes a queryset also like a model)
    which also processes the "q" argument cause we are essentially calling the get_queryset itself


    GET() and then GET_OBJECT():
    but we are ovveriding the get() methood and getting the idd from the url
    or we get the id from the request.body as data
    then we parse the json if it is valid
    then we call the retrieve method which calls the get_object
    
    POST:
    the post method does not anything extra for the create

    PUT/PATCH:
    the put/ patch method gets called first and we get the id 
    from request body or the url itself, then assigns as the 
    class cariable pased_id, then it calls the update method which calls the get_object()

    a new record is created if the parsed id not assigned in the put or patch 
    is because if the id is not passed then it acts as a post method(CreateAPIView)

    so long story short in case of put or patch the get() is bypassed and the update()
    calls directly the get_object then it does it's thing

    DELETE:
    delete method does the same thing , delete is called and it assigns the pased_id
    and calls destroy method which uses as usual get_object to get the data
    and deletes the object after that


"""

# class StatusListAPIView(
#     CreateModelMixin, 
#     RetrieveModelMixin,
#     UpdateModelMixin,
#     DestroyModelMixin,
#     ListAPIView): 
#     permission_classes          = []
#     authentication_classes      = []
#     serializer_class            = StatusSerializer
#     passed_id                   = None

#     def get_queryset(self):
#         request = self.request
#         qs = StatusModel.objects.all()
#         query = request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(
#                             Q(content__icontains=query) |
#                             Q(user__username=query)
#                           )
#         return qs

#     def get_object(self):
#         print('\nget object is executed...\n')
#         request         = self.request
#         passed_id       = request.GET.get('id', None) or self.passed_id
#         queryset        = self.get_queryset()
#         obj = None
#         if passed_id is not None:
#             obj = get_object_or_404(queryset, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj

#     # def perform_destroy(self, instance):
#     #     if instance is not None:
#     #         return instance.delete()
#     #     return None

#     def get(self, request, *args, **kwargs):
#         print('\nget is executed...\n')

#         url_passed_id    = request.GET.get('id', None)
#         json_data        = {}
#         body_            = request.body
        
#         if is_json(body_):
#             json_data        = json.loads(request.body)
        
#         new_passed_id    = json_data.get('id', None)
        
#         #print(request.body)
#         #request.data
        
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
        
#         if passed_id is not None:# or passed_id is not "":
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         print('\n\nput is executed...\n\n')
        
#         url_passed_id    = request.GET.get('id', None)
#         json_data        = {}
#         body_            = request.body
#         if is_json(body_):
#             json_data        = json.loads(request.body)
#         new_passed_id    = json_data.get('id', None)
#         #print(request.body)
#         #request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id

#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         print('\npatch is executed...\n')
        
#         url_passed_id    = request.GET.get('id', None)
#         json_data        = {}
#         body_            = request.body
#         if is_json(body_):
#             json_data        = json.loads(request.body)
#         new_passed_id    = json_data.get('id', None)
#         #print(request.body)
#         #request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
        
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         print('\ndelete method executed....\n')

#         url_passed_id    = request.GET.get('id', None)
#         json_data        = {}
#         body_            = request.body
#         if is_json(body_):
#             json_data        = json.loads(request.body)
#         new_passed_id    = json_data.get('id', None)
#         #print(request.body)
#         #request.data
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
        
#         return self.destroy(request, *args, **kwargs)

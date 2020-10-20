from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import json


def json_response(request):
    
    data = {
        'count': 1000,
        'content': 'some new content',
    }

    data = json.dumps(data)


    return HttpResponse(data, content_type="application/json")


class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        pass

    



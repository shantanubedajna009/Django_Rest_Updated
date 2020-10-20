from django.contrib import admin
from .models import StatusModel
from .forms import StatusModelForm

# Register your models here.


class StatusAdmin(admin.ModelAdmin):
    list_display =  ['user', '__str__', 'image']
    form = StatusModelForm
    # class Meta:
    #     model = StatusModel




admin.site.register(StatusModel, StatusAdmin)


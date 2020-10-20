from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class StatusCustomQueryset(models.query.QuerySet):
    pass


class StatusModelManager(models.Manager):
    def get_queryset(self):
        return StatusCustomQueryset(self.model, using=self._db)



def upload_image_path_function(instance, filename):
    return "status/{user}/{filename}".format(user=instance.user, filename=filename)


class StatusModel(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    content         = models.TextField(blank=True, null=True)
    image           = models.ImageField(upload_to=upload_image_path_function, blank=True, null=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = StatusModelManager()

    
    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    
    def __str__(self):
        if  self.content:
            return self.content[:50]
        else:
            return ""


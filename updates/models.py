from django.db import models

from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


def upload_path_setter(instance, filename):
    return 'updates/{user}/{filename}'.format(user=instance.user, filename=filename)


class Update(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    content         = models.TextField(blank=True, null=True)
    image           = models.ImageField(upload_to=upload_path_setter, blank=True, null=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content or ""

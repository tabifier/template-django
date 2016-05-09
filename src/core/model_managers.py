from django.db import models


class ActiveModelManager(models.Manager):

    def filter(self, *args, **kwargs):
        kwargs.update({'is_active': True})
        return self.filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs.update({'is_active': True})
        return self.get(*args, **kwargs)

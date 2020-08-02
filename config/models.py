from django.db import models


class Deletable(models.Model):
    deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.deleted = True
        return self.save()

    class Meta:
        abstract = True

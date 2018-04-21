from django.db import models


class Cow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    number = models.TextField()
    sex = models.TextField()
    birthday = models.DateTimeField(null=True, blank=True)
    mother = models.ForeignKey('cowapp.Cow', related_name='children', on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='cows', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

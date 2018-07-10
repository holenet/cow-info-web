from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Cow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=20)
    sex = models.TextField()
    birthday = models.DateField(null=True, blank=True)
    mother_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='cows', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('birthday', 'created',)
        unique_together = ('user', 'number')

    @property
    def summary(self):
        return f'{self.number.split("-")[2]}{"♂" if self.sex=="male" else "♀"}'

    def __str__(self):
        return self.number


class Record(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey('cowapp.Cow', related_name='records', on_delete=models.CASCADE)
    content = models.TextField()
    etc = models.TextField(null=True, blank=True)
    day = models.DateField()
    user = models.ForeignKey('auth.User', related_name='records', on_delete=models.CASCADE)

    class Meta:
        ordering = ('day', 'created',)

    def __str__(self):
        return "{}: {}".format(self.cow.number, self.content)

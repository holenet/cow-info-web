from django.db import models


class Cow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    number = models.TextField(unique=True)
    sex = models.TextField()
    birthday = models.DateField(null=True, blank=True)
    mother = models.ForeignKey('cowapp.Cow', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='cows', on_delete=models.CASCADE)

    class Meta:
        ordering = ('birthday', 'created',)

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

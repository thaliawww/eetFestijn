from django.core.exceptions import ValidationError
from django.db import models


class List(models.Model):
    wbw_id = models.CharField(unique=True, max_length=40)
    name = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        List.objects.all().update(active=False)
        super(List, self).save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        if (self.pk and List.objects.filter(
                active=True).exclude(pk=self.pk).count() > 0 and self.active):
            raise ValidationError(
                {'active': 'Je mag maar een actieve lijst hebben.'}
            )
        return super().validate_unique(exclude)

    def __str__(self):
        return self.name


class Participant(models.Model):
    wbw_id = models.CharField(unique=True, max_length=40)
    list = models.ForeignKey(List)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

from django.db import models

from wiebetaaltwat.models import Participant


class Bystander(models.Model):
    name = models.CharField(max_length=200)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class Meal(models.Model):
    price = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    description = models.CharField(max_length=200, blank=True)

    participants = models.ManyToManyField(Participant, blank=True)
    bystanders = models.ManyToManyField(Bystander, blank=True)
    payer = models.ForeignKey(Participant, null=True, blank=True, related_name='paymeal', on_delete=models.SET_NULL)

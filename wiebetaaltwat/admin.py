from django.contrib import admin

from .models import Participant, List


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


class ListAdmin(admin.ModelAdmin):
    inlines = (ParticipantInline, )

admin.site.register(List, ListAdmin)

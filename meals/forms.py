from django.forms import ModelForm, widgets
import django.forms as forms
from meals.models import Meal, Bystander
from wiebetaaltwat.models import Participant


class EuroWidget(widgets.NumberInput):

    def render(self, name, value, attrs=None):
        return ('<div class="input-group">\
                 <span class="input-group-addon">€-cent</span>' +
                super(EuroWidget, self).render(name, value, attrs) +
                '</div>')

    def value_from_datadict(self, data, files, name):
        return data[name]


class ParticipantForm(forms.Form):
    participant = forms.ModelChoiceField(label='Participant',
                                         queryset=Participant.objects.all())


class BystanderForm(ModelForm):
    class Meta:
        model = Bystander
        fields = ['name']
        labels = {'name': 'Name bystander'}


class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['description', 'price', 'payer']
        labels = {'description': 'Description',
                  'price': 'Price'}
        widgets = {'price': EuroWidget()}

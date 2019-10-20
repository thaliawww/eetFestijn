import math
from datetime import datetime
from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import localtime

from meals.forms import MealForm, ParticipantForm, BystanderForm
from meals.models import Meal, Participant, Bystander
from wiebetaaltwat.views import _create_wbw_session


def meal(request):
    context = {}
    try:
        meal = context['meal'] = Meal.objects.get(completed=False)
        context['participant_form'] = ParticipantForm()
        context['bystander_form'] = BystanderForm()
        context['form'] = MealForm(instance=meal)
        context['eaters'] = eaters = []
        for p in meal.participants.all():
            eaters.append({'participant': p})
        for b in meal.bystanders.all():
            eaters.append({'bystander': b, 'participant': b.participant})

        # add warning for eaters not in the wbw list
        context['warning_externals'] = settings.WARNING_EXTERNALS

        # these should probably be split into different view functions
        if 'update' in request.POST:
            context['form'] = form = MealForm(request.POST, instance=meal)
            if form.is_valid():
                form.save()
                return redirect('meal')
        elif 'participate' in request.POST:
            pk = int(request.POST['participant'])
            meal.participants.add(Participant.objects.get(pk=pk))
            meal.save()
            return redirect('meal')
        elif 'bystand' in request.POST:
            pk = int(request.POST['participant'])
            form = BystanderForm(request.POST)
            form.instance.participant = Participant.objects.get(pk=pk)
            form.save()
            meal.bystanders.add(form.instance)
            meal.save()
            return redirect('meal')
        elif 'unbystand' in request.POST:
            pk = int(request.POST['unbystand'])
            meal.bystanders.remove(Bystander.objects.get(pk=pk))
            meal.save()
            return redirect('meal')
        elif 'unparticipate' in request.POST:
            pk = int(request.POST['unparticipate'])
            meal.participants.remove(Participant.objects.get(pk=pk))
            meal.save()
            return redirect('meal')
        elif 'abort' in request.POST:
            meal.delete()
            return redirect('meal')
        elif 'finalise' in request.POST:
            context['form'] = form = MealForm(request.POST, instance=meal)
            if form.is_valid():
                form.save()
            errors = False  # surely there's a more elegant way to do this
            if not meal.payer:
                context['form'].add_error('payer', "You cannot process anything without a payer.")
                errors = True
            if not meal.price > 0:
                context['form'].add_error('price', "You cannot process anything without a price.")
                errors = True
            if not meal.participants.all() and not meal.bystanders.all():
                messages.error(request, "There is nothing to process without participants.")
                errors = True
            if not errors:
                session, response = _create_wbw_session()
                date = datetime.strftime(localtime(meal.date), "%Y-%m-%d")
                desc = []
                for b in meal.bystanders.all():
                    desc.append("{} via {}".format(b.name, b.participant.name))
                desc = "{} ({})".format(meal.description, ', '.join(desc))

                payload = {'expense': {
                    'payed_by_id': meal.payer.wbw_id,
                    'name': desc,
                    'payed_on': date,
                    'amount': 0,
                    'shares_attributes': []}}

                participants = list(chain(meal.participants.all(),
                                          [b.participant for b in
                                           meal.bystanders.all()]))
                amount_per_p = math.ceil(meal.price / len(participants))
                for p in participants:
                    payload['expense']['shares_attributes'].append({
                        'member_id': p.wbw_id,
                        'multiplier': 1,
                        'amount': amount_per_p
                    })
                    # Wiebetaaltwat does not like to share beyond decimals
                    # so we ensure that the total amount is the sum of parts.
                    payload['expense']['amount'] += amount_per_p

                # We must remove duplicate shares
                shares = {}
                for share in list(payload['expense']['shares_attributes']):
                    if share['member_id'] not in shares:
                        shares[share['member_id']] = share
                    else:
                        shares[share['member_id']]['multiplier'] += 1
                        # Since multiplier and amount seem to be unrelated..
                        shares[share['member_id']]['amount'] += amount_per_p
                        payload['expense']['shares_attributes'].remove(share)

                url = ('https://api.wiebetaaltwat.nl/api/lists/{}/expenses'
                       .format(settings.WBW_LIST_ID))
                session.post(url,
                             json=payload,
                             headers={'Accept-Version': '6'},
                             cookies=response.cookies)
                meal.completed = True
                meal.save()
                messages.success(request, "The meal has been processed!")
                return redirect('meal')

    except Meal.DoesNotExist:
        if 'startmeal' in request.POST:
            Meal.objects.create()
            return redirect('meal')

    return render(request, 'meals/meal.html', context)

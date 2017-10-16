import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from orders.models import Order
from .models import Participant, List


def update_lists(request):
    if Order.objects.count() <= 0:
        session, response = _create_wbw_session()
        response = session.get('https://api.wiebetaaltwat.nl/api/lists/',
                               headers={'Accept-Version': '1'},
                               cookies=response.cookies)
        data = response.json()

        List.objects.all().delete()
        for item in data['data']:
            list_id = item['list']['id']
            list_name = item['list']['name']
            list_obj, _ = List.objects.get_or_create(wbw_id=list_id)
            list_obj.name = list_name
            list_obj.save()

            url = ('https://api.wiebetaaltwat.nl/api/lists/{list_id}/members'
                   .format(list_id=list_id))
            response = session.get(url,
                                   headers={'Accept-Version': '1'},
                                   cookies=response.cookies)
            data = response.json()
            Participant.objects.filter(list=list_obj).delete()
            for user_item in data['data']:
                uid = user_item['member']['id']
                if uid == settings.WBW_UID:
                    continue
                name = user_item['member']['nickname']
                p, _ = Participant.objects.get_or_create(wbw_id=uid, list=list_obj)
                p.name = name
                p.save()
        messages.success(request, "Lijsten succesvol bijgewerkt!")
    else:
        messages.error(request, "Lijsten konden niet worden bijgewerkt.")
    return redirect(reverse('index'))


def _create_wbw_session():
    session = requests.Session()
    payload = {'user': {
        'email': settings.WBW_EMAIL,
        'password': settings.WBW_PASSWORD,
        }
    }
    response = session.post('https://api.wiebetaaltwat.nl/api/users/sign_in',
                            json=payload,
                            headers={'Accept-Version': '1'})
    return session, response

# coding=utf-8
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import Client
from orders.models import Item, Order, ItemOrder, Discount
from django.utils import timezone

from wiebetaaltwat.models import List


class ListTestCase(TestCase):
    def test_validate_unique(self):
        list1 = List.objects.create(wbw_id="id1")
        list2 = List.objects.create(wbw_id="id2")

        list1.full_clean()
        list2.full_clean()

        list1.active = True
        list1.save()

        list2.active = True

        list1.full_clean()
        with self.assertRaises(ValidationError):
            list2.full_clean()

    def test_save(self):
        list1 = List.objects.create(wbw_id="id1", active=True)
        list2 = List.objects.create(wbw_id="id2", active=False)

        self.assertEqual(list1.active, True)
        self.assertEqual(list2.active, False)

        list2.active = True
        list2.save()

        list1.refresh_from_db()
        list2.refresh_from_db()

        self.assertEqual(list1.active, False)
        self.assertEqual(list2.active, True)

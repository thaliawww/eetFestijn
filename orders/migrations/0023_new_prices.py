# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def new_prices(apps, schema_editor):
    """New prices as of 2018-06-19"""
    Item = apps.get_model("orders", "Item")
    Category = apps.get_model("orders", "Category")

    def set_price(name, price):
        item = Item.objects.get(name=name)
        item.price = price
        item.save()

    set_price("Pizza Campagnola (nr. 23)", 900)
    set_price("Pizza Roma (nr. 24)", 750)
    set_price("Pizza Carbonara (nr. 25)", 850)
    set_price("Pizza Funghi e pesce (nr. 26)", 900)
    set_price("Pizza Mafiosa (nr. 27)", 900)
    set_price("Friet zonder", 170)
    set_price("Friet mayonaise (groot)", 250)
    set_price("Friet super (klein)", 400)
    set_price("Friet super (groot)", 450)
    set_price("Friet super saté (klein)", 400)
    set_price("Friet super saté (groot)", 450)
    set_price("Friet super oorlog (klein)", 425)
    set_price("Friet super oorlog (groot)", 475)
    set_price("Friet waterfiets (klein)", 475)
    set_price("Friet waterfiets (groot)", 525)
    set_price("Friet waterfiets met kroketten (klein)", 475)
    set_price("Friet waterfiets met kroketten (groot)", 525)
    set_price("Gezinszak friet", 550)
    set_price("Frikandel", 160)
    set_price("Kroket", 160)
    set_price("Goulash kroket", 170)
    set_price("Satékroket", 170)
    set_price("Bamischijf", 170)
    set_price("Nasischijf", 170)
    set_price("Gehaktbal", 220)
    snack = Item.objects.get(name="Kwekkerboom")
    snack.price = 200
    snack.name = "Kwekkeboom"
    snack.save()
    set_price("Pikanto", 220)
    set_price("Kipcorn", 190)
    set_price("Mexicano", 220)
    set_price("Lihanboutje", 170)
    set_price("Viandel", 220)
    set_price("Braadworst", 220)
    set_price("Knakworst", 220)
    set_price("Sitostick", 220)
    set_price("Berenklauw", 250)
    set_price("Smulrol", 250)
    set_price("Loempia klein", 170)
    set_price("Loempia groot", 300)
    set_price("Nasi vegetarisch", 200)
    set_price("Bami vegetarisch", 200)
    set_price("Cheese crack", 200)
    set_price("Kaassoufflé", 170)
    set_price("Broodje kroket", 210)
    set_price("Broodje frikandel", 210)
    set_price("Broodje viandel", 270)
    set_price("Broodje kipkorn", 250)
    set_price("Broodje gehaktbal", 270)
    set_price("Broodje braadworst", 270)
    set_price("Broodje knakworst", 270)
    set_price("Broodje pikanto", 270)
    set_price("Broodje mexicano", 270)
    set_price("Broodje visstick", 300)
    set_price("Broodje goulashkroket", 220)
    set_price("Broodje satékroket", 220)
    Item.objects.get(name="Broodje ham").delete()
    Item.objects.get(name="Broodje ham en kaas").delete()

    lunch = Category.objects.create(name="Lunch")
    lunch.items.add(Item.objects.create(name="Pistolet hete kip", price=495))
    lunch.items.add(Item.objects.create(name="Pistolet gezond", price=350))
    lunch.items.add(Item.objects.create(name="Pistolet Brie", price=350))
    lunch.items.add(Item.objects.create(name="Pistolet tonijn", price=350))
    lunch.items.add(Item.objects.create(name="Pistolet ei", price=250))
    lunch.items.add(Item.objects.create(name="Pistolet ham", price=350))
    lunch.items.add(Item.objects.create(name="Pistolet kaas", price=350))
    lunch.items.add(Item.objects.create(name="Pistolet filet American", price=350))

    tosti = Category.objects.create(name="Tosti")
    tosti.items.add(Item.objects.create(name="Tosti gehakt", price=250))
    tosti.items.add(Item.objects.create(name="Tosti kaas", price=250))
    tosti.items.add(Item.objects.create(name="Tosti ham", price=275))
    tosti.items.add(Item.objects.create(name="Tosti ham en kaas", price=275))
    tosti.items.add(Item.objects.create(name="Tosti mozzarella", price=300))
    tosti.items.add(Item.objects.create(name="Tosti De Fest", price=400))

    # Rename small kapsalon to medium and add new small
    kapsalons = Category.objects.get(name="Kapsalons")
    for kapsalon in kapsalons.items.all():
        if "klein" in kapsalon.name:
            kapsalons.items.add(Item.objects.create(name=kapsalon.name, price=450))
            kapsalon.name = kapsalon.name.replace("klein", "middel")
            kapsalon.save()

    set_price("Lahmacun met döner", 550)
    set_price("Lahmacun met shoarma", 550)
    set_price("Lahmacun met kipdöner", 550)


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20180620_1442'),
    ]

    operations = [
        migrations.RunPython(new_prices)
    ]

from django.utils import timezone
from faker import Factory as FakerFactory


def insert_all_permissions():
    from django.contrib.auth.models import Group, Permission
    from core.models.general import SiteConfiguration
    from core.models.shop import Delivery, DeliveryPoint

    make_permissions(Group, Permission)
    add_permissions_for_prod_stock_and_conf(Group, Permission)
    create_farmers_group(Group)
    save_site_configuration(SiteConfiguration)
    create_one_year_deliveries_for_deliverypoint(DeliveryPoint, Delivery)


def make_permissions(Group, Permission):
    managers_group = Group(name="managers")
    managers_group.save()
    managers_group.permissions.add(
        Permission.objects.get(codename='add_news'),
        Permission.objects.get(codename='change_news'),
        Permission.objects.get(codename='delete_news')
    )


def add_permissions_for_prod_stock_and_conf(Group, Permission):
    managers_group = Group.objects.get(name="managers")
    managers_group.permissions.add(
        Permission.objects.get(codename='change_siteconfiguration'),

        Permission.objects.get(codename='add_product'),
        Permission.objects.get(codename='change_product'),
        Permission.objects.get(codename='delete_product'),

        Permission.objects.get(codename='add_productcategory'),
        Permission.objects.get(codename='change_productcategory'),
        Permission.objects.get(codename='delete_productcategory'),

        Permission.objects.get(codename='add_stock'),
        Permission.objects.get(codename='change_stock'),
        Permission.objects.get(codename='delete_stock'),
    )


def create_farmers_group(Group):
    farmers_group = Group(name="farmers")
    farmers_group.save()


def save_site_configuration(SiteConfiguration):
    conf, created = SiteConfiguration.objects.get_or_create(pk=1)
    if created:
        faker = FakerFactory.create('fr_FR')
        conf.news_count = 4
        conf.homepage_content = "<p>{}</p>".format("</p><p>".join(faker.paragraphs()))
        conf.save()


def create_base_deliverypoints_and_deliveries(DeliveryPoint, Delivery):
    counter = 1
    for town in ['Douala', 'Yaoundé', 'Tayap']:
        point, created = DeliveryPoint.objects.get_or_create(
            pk=counter, defaults={'name': town, 'description': "Livraison à {}".format(town)})
        create_one_year_deliveries_for_deliverypoint(Delivery, point)
        counter += 1


def create_one_year_deliveries_for_deliverypoint(Delivery, delivery_point):
    next_friday = timezone.now()
    while next_friday.weekday() != 4:
        next_friday += timezone.timedelta(1)

    for i in range(0, 51):
        date = next_friday + timezone.timedelta(i * 7)
        Delivery.objects.get_or_create(date=date, delivery_point=delivery_point)
        print("Created delivery for {} at {}".format(date, delivery_point.name))

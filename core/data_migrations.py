from faker import Factory as FakerFactory

def insert_all_permissions():
    from django.contrib.auth.models import Group, Permission
    from core.models import SiteConfiguration
    make_permissions(Group, Permission)
    add_permissions_for_prod_stock_and_conf(Group, Permission)
    create_farmers_group(Group)
    save_site_configuration(SiteConfiguration)


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

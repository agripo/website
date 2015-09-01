def make_permissions(Group, Permission):
    managers_group = Group(name="managers")
    managers_group.save()
    managers_group.permissions.add(
        Permission.objects.get(codename='add_news'),
        Permission.objects.get(codename='change_news'),
        Permission.objects.get(codename='delete_news')
    )


def create_farmers_group(Group):
    farmers_group = Group(name="farmers")
    farmers_group.save()

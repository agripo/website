from django.contrib.auth.models import User, Group

class AgripoUser(User):

    def add_to_group(self, group_name):
        group = Group.objects.get(name=group_name)
        group.user_set.add(self)
        pass

    class Meta:
        proxy = True

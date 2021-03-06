from .models import MyUsers
from django.contrib.auth.models import Group, Permission


def createGroup():
    new_group, created = Group.objects.get_or_create(name='admin')
    perm = Permission.objects.all()
    new_group.permissions.set(perm)

    new_group, created = Group.objects.get_or_create(name='user')
    perm = [
        Permission.objects.get(codename='view_myusers'),
        Permission.objects.get(codename='add_myusers'),
        Permission.objects.get(codename='change_myusers'),
        Permission.objects.get(codename='delete_myusers'),

    ]
    new_group.permissions.set(perm)


def user_permission(id, perm):
    user = MyUsers.objects.get(pk=id)
    user.groups.add(Group.objects.get(name=perm))
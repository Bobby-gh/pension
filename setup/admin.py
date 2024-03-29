from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from dashboard.models import ApplicationDocumentType, Rank
from setup.models import SysConfig

# Register your models here.
admin.site.register(ApplicationDocumentType)
admin.site.register(Rank)

try:
    if not ApplicationDocumentType.objects.all():
        types = ["Pay Slip", "Pension Form One", "Record of Service"]
        for t in types:
            ApplicationDocumentType.objects.get_or_create(name=t)
except Exception as e:
    pass

# Create default groups if empty
try:
    if not Group.objects.all():
        reg_group, created = Group.objects.get_or_create(name='regional')
        nat_group, created = Group.objects.get_or_create(name='national')
        permission = Permission.objects.get(codename='can_setup_system')
        can_generate_letter = Permission.objects.get(
            codename='can_generate_letter')
        can_review_application = Permission.objects.get(
            codename='can_review_application')
        nat_group.permissions.add(permission)
        nat_group.permissions.add(can_generate_letter)
        nat_group.permissions.add(can_review_application)
except Exception as e:
    pass

# Default
try:
    if not SysConfig.objects.all():
        SysConfig.objects.create()
except Exception as e:
    pass

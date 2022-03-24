from django.contrib import admin

from dashboard.models import Application, ApplicationRank, Notification, Rank, ApplicationDocumentType, ApplicationDocument

admin.site.register(Application)
admin.site.register(ApplicationDocument)
admin.site.register(ApplicationDocumentType)
admin.site.register(Rank)
admin.site.register(ApplicationRank)
admin.site.register(Notification)

# TEMP
try:
    types = ["Pay Slip", "Pension Form One", "Record of Service"]
    for t in types:
        ApplicationDocumentType.objects.get_or_create(name=t)
except Exception as e:
    print(e)

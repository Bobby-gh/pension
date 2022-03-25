from django.contrib import admin

from dashboard.models import (Application, ApplicationDocument,
                              ApplicationRank, Notification)

admin.site.register(Application)
admin.site.register(ApplicationDocument)
admin.site.register(ApplicationRank)
admin.site.register(Notification)


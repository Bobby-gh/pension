from django.contrib import admin

from dashboard.models import Application, ApplicationRank, Rank

admin.site.register(Application)
admin.site.register(Rank)
admin.site.register(ApplicationRank)


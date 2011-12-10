from django.contrib import admin

from consent.models import Privilege, Consent


class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ConsentAdmin(admin.ModelAdmin):
    list_display = ('user', 'privilege', 'granted_on', 'revoked_on', )
    list_filter = ('privilege', 'revoked', )


admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(Consent, ConsentAdmin)

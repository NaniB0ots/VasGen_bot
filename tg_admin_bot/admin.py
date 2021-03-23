from django.contrib import admin

from tg_admin_bot import models


@admin.register(models.AdminUserToken)
class AdminUserTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TgAdminUser)
class TgAdminUserAdmin(admin.ModelAdmin):
    pass

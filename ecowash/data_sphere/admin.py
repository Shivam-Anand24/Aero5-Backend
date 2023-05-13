
from django.contrib import admin
from django.utils.crypto import get_random_string
from .models import User, Role

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)

    def save_model(self, request, obj, form, change):
        # Generate a random token if creating a new user
        if not change:
            obj.token = get_random_string(length=10)

        super().save_model(request, obj, form, change)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentGenre, Major, Profession


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('genre', 'profession', 'activated')}),
    ) + UserAdmin.fieldsets

    add_fieldsets = UserAdmin.add_fieldsets + (
                    (None, {'fields': ('genre', 'profession')}),
                )

# Register your models here.


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentGenre)
admin.site.register(Profession)

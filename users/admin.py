from django.contrib import admin
from .models import NewUser, Council, Service, Notification, Transaction, Issue, Business
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', )
    list_filter = ('email', 'user_name','user_type', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name','user_type',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name','user_type', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Council)
admin.site.register(Service)
admin.site.register(Notification)
admin.site.register(Transaction)
admin.site.register(Issue)
admin.site.register(Business)

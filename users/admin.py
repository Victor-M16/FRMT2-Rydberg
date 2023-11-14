from django.contrib import admin
from .models import NewUser, Revenue, Transaction,Collection_instance
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

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'user_type':
            kwargs['choices'] = (
                ('Collector', 'collector'),
                ('Revenue Creator', 'revenue creator'),
                ('Council Official', 'council official'),
                ('Admin', 'admin')
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)

admin.site.site_header = 'FRTM Admin Dashboard'

class UsersAdminArea(admin.AdminSite):
    site_header = 'Users Admin Area'




admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Revenue)
admin.site.register(Transaction)
admin.site.register(Collection_instance)
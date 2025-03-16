from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Account, Role, AccountMember, Destination, Log
from django.utils import timezone

admin.site.site_header = "Broadcaster"
admin.site.index_title = "Broadcaster"
admin.site.site_title = "Admin"

# Unregister Group from admin
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("email", "is_superuser", "is_active", "created_at")
    search_fields = ("email",)
    ordering = ("email",)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active")}
        ),
    )
    
    readonly_fields = ("created_at", "updated_at")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'website')
    search_fields = ('account_name',)
    readonly_fields = ('app_secret_token', 'created_at', 'updated_at', 'created_by', 'updated_by')
    fields = ('account_name', 'website', 'app_secret_token', 'created_at', 'updated_at', 'created_by', 'updated_by')
    
    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser or request.user.account_memberships.filter(account=obj).exists()
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(members__user=request.user)
    
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('account_name',)
        return self.readonly_fields

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        obj = form.save(commit=False)
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()
        obj.updated_by = request.user
        obj.updated_at = timezone.now()
        return obj

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()
        
        if not change:  # If this is a new object
            # Create an AccountMember for the creator with Admin role
            Role.objects.get_or_create(role_name="Admin")  # Ensure Admin role exists
            admin_role = Role.objects.get(role_name="Admin")
            AccountMember.objects.create(
                user=request.user,
                account=obj,
                role=admin_role,
                created_by=request.user,
                updated_by=request.user
            )


class AccountMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'account')
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fields = ('user', 'role', 'account', 'created_at', 'updated_at')
    
    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account__members__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            kwargs["queryset"] = Role.objects.filter(role_name__in=["Admin", "User"])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('account', 'url', 'http_method')
    search_fields = ('url',)
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
    fields = ('account', 'url', 'http_method', 'headers', 'created_at', 'updated_at')
    
    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return request.user.is_superuser or request.user.account_memberships.filter(account=obj.account).exists()
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account__members__user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "account":
            if not request.user.is_superuser:
                kwargs["queryset"] = Account.objects.filter(members__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['headers'].required = False
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        if not obj.headers:
            obj.headers = {}
        super().save_model(request, obj, form, change)


class LogAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'account', 'destination', 'status', 'received_timestamp')
    search_fields = ('event_id', 'status')
    readonly_fields = ('event_id', 'account', 'destination', 'status', 'received_timestamp', 
                      'processed_timestamp', 'received_data')
    fields = ('event_id', 'account', 'destination', 'status', 'received_timestamp', 
             'processed_timestamp', 'received_data')
    
    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account__members__user=request.user)

# Register models with the admin site
admin.site.register(Account, AccountAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(AccountMember, AccountMemberAdmin)
admin.site.register(Log, LogAdmin)

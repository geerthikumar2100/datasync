from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account, Role, AccountMember, Destination, Log

# @admin.register(User)
# class CustomUserAdmin(BaseUserAdmin):
#     list_display = ("email", "is_staff", "is_active")
#     search_fields = ("email",)
#     ordering = ("email",)
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
#         ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("email", "password1", "password2", "is_staff", "is_active")}
#         ),
#     )

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_name", "created_by", "updated_by", "created_at")
    search_fields = ("account_name",)
    ordering = ("account_name",)
    readonly_fields = ("app_secret_token", "created_at")  

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user  
        obj.updated_by = request.user  
        super().save_model(request, obj, form, change)

@admin.register(AccountMember)
class AccountMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "role")  
    list_filter = ("role",)  
    search_fields = ("user__email", "role__role_name")  # ✅ Fix: search by email, not username

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            kwargs["queryset"] = Role.objects.filter(role_name__in=["Admin", "User"])  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("account", "url", "http_method")
    search_fields = ("url",)
    ordering = ("account",)
    exclude = ("created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("event_id", "account", "destination", "status", "received_timestamp")
    search_fields = ("event_id", "status")
    ordering = ("received_timestamp",)
    readonly_fields = ("received_timestamp",)

    def has_add_permission(self, request):
        return False  # Disable manual log creation in Django Admin

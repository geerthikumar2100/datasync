from django.db import migrations
from django.utils import timezone

def create_default_roles(apps, schema_editor):
    Role = apps.get_model('core', 'Role')
    
    # Create roles only if they don't exist
    if Role.objects.count() == 0:
        now = timezone.now()
        Role.objects.bulk_create([
            Role(id=1, role_name="Admin", created_at=now, updated_at=now),
            Role(id=2, role_name="User", created_at=now, updated_at=now)
        ])

def remove_default_roles(apps, schema_editor):
    Role = apps.get_model('core', 'Role')
    Role.objects.filter(role_name__in=["Admin", "User"]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),  # Make sure this matches your previous migration
    ]

    operations = [
        migrations.RunPython(create_default_roles, remove_default_roles),
    ] 
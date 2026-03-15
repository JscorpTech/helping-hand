import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from core.apps.chat.models import GroupModel

try:
    group = GroupModel.objects.get(id=1)
    print(f"Group 1: name={group.name}, is_public={group.is_public}")
    print(f"Users in Group 1: {[u.username for u in group.users.all()]}")
except GroupModel.DoesNotExist:
    print("Group 1 does not exist")
except Exception as e:
    print(f"Error: {e}")

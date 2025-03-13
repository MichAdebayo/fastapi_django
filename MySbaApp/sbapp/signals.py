import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

def sync_admin_user_to_fastapi(user):
    fastapi_url = "http://http://ussba-fastapi.francecentral.azurecontainer.io/sync/users"
    user_data = {
        "email": user.email,
        "username": user.username,
        "password": user.password,  # Send the hashed password
        "role": "admin" if user.is_staff else "user",
    }
    response = requests.post(fastapi_url, json=user_data)
    if response.status_code == 200:
        print("User synced successfully.")
    else:
        print("Failed to sync user.")

@receiver(post_save, sender=User)
def sync_user_on_create_or_update(sender, instance, created, **kwargs):
    if instance.is_staff:  # Only sync admin users
        sync_admin_user_to_fastapi(instance)
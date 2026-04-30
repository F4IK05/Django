import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
import cloudinary.uploader

from accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def set_default_avatar(sender, instance, created, **kwargs):
    if created and not instance.avatar:
        dicebear_url = f"https://api.dicebear.com/7.x/identicon/png?seed={instance.username}"

        try:
            upload_result = cloudinary.uploader.upload(
                dicebear_url,
                folder='user_avatars/',
                public_id=f"user_{instance.id}_default",
                overwrite=True,
            )

            CustomUser.objects.filter(pk = instance.id).update(avatar=upload_result['public_id'])

        except Exception as e:
            print(f"Ошибка при автоматической генерации аватара: {e}")
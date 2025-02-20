from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
      Tạo profile mới khi người dùng tạo mới tài khoản
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Cập nhật profile nếu người dùng đã tồn tại
    instance.userprofile.save()

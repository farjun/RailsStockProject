#__author__ = Mohammad Abdin

from .models import Profile
<<<<<<< HEAD
from django.dispatch import receiver
=======

from django.dispatch import receiver
# from django.core.signals import post_save
>>>>>>> master
from django.db.models.signals import post_save
from django.contrib.auth.models import User


<<<<<<< HEAD

@receiver(post_save, sender = User)
def create_profile(sender, instance , created , **kwargs):
    """ here we want a user profile to be created automatically after an account is being created """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender = User)
def save_profile(sender, instance , **kwargs):
    """
    receives the signal that askes for saving the profile
    :param sender: User Model
    :type sender: Model
    """
    instance.profile.save()


=======
# here we want a user profile to be created automatically after an account is being created
@receiver(post_save, sender = User)
def create_profile(sender, instance , created , **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save the profile
@receiver(post_save, sender = User)
def save_profile(sender, instance , **kwargs):
    instance.profile.save()
>>>>>>> master

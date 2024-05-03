from django.db.models.signals import post_save
from django.dispatch import receiver

from glasses.orders.models import Basket
from glasses.users.models import User


@receiver(post_save, sender=User)
def create_user_basket(
    sender,
    instance: User,
    created=False,
    **kwargs,
):
    if not created or instance.is_admin or instance.is_staff:
        return

    basket = Basket.objects.create(user=instance)
    instance.basket = basket  # type: ignore
    instance.save()

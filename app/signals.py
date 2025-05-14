from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import CartItem, Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_save, sender=CartItem)
def update_product_stock(sender, instance, **kwargs):
    if not instance.pk:
        # New CartItem
        if instance.product.stock < instance.quantity:
            raise ValueError("There is not enough product stock available.")
        instance.product.stock -= instance.quantity
    else:
        # Existing CartItem being updated
        old_quantity = CartItem.objects.get(pk=instance.pk).quantity
        difference = instance.quantity - old_quantity
        if instance.product.stock < difference:
            raise ValueError("There is not enough product stock.")
        instance.product.stock -= difference
    instance.product.save()

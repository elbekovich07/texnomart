from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import CartItem, Cart


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_save, sender=CartItem)
def update_product_stock(sender, instance, **kwargs):
    if not instance.pk:
        if instance.product.stock < instance.quantity:
            raise ValueError("There is not enough product stock available.")
        instance.product.stock -= instance.quantity
    else:
        old_quantity = CartItem.objects.get(pk=instance.pk).quantity
        difference = instance.quantity - old_quantity
        if instance.product.stock < difference:
            raise ValueError("There is not enough product stock.")
        instance.product.stock -= difference
    instance.product.save()

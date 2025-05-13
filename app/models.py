from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


# Category
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='category/images/')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name', 'slug']),
        ]
        ordering = ['name']


# Product
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        images = self.images.all().order_by('order')
        if images.exists():
            return images[0].image.url
        return ""

    def total_likes(self):
        return sum(product.likes_product.count() for product in self.product_set.all())


# Image
class Image(models.Model):
    image = models.ImageField(upload_to='product/images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} {self.image.url}'

    class Meta:
        verbose_name_plural = 'Images'


# Like
class Like(models.Model):
    user = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes_product")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.user} liked {self.product}"


# Favorite
class Favorite(models.Model):
    user = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_favorite')
        ]


# Comment
class Comment(models.Model):
    user = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Like, related_name="liked_comments", blank=True)

    def __str__(self):
        return f"{self.user} commented on {self.product}"


# Cart
class Cart(models.Model):
    user = models.ForeignKey('app.CustomUser', on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())


# CartItem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_item')
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity


class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, db_index=True)
    phone = models.CharField(max_length=15, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.username

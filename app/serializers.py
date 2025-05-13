from rest_framework import serializers

from app.models import Category, Product, Like, Favorite, Comment, CartItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_category_name(self, obj):
        return obj.name.upper()


class ProductSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False

        return any(like.user_id == user.id for like in obj.likes_product.all())

    def get_like_count(self, obj):
        return getattr(obj, 'like_count', obj.likes_product.count())


class LikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'product', 'created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'added_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'comment', 'created_at', 'like_count', 'is_liked']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return obj.likes.filter(user=user).exists() if user.is_authenticated else False


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return obj.total_price()

from django.db.models import Count, Prefetch
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from app.pagination import CustomPagination
from app.serializers import *


# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category') \
        .prefetch_related('likes_product') \
        .annotate(like_count=Count('likes_product'))
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(user=user, product=product)
        if created:
            product.likes_product.add(like)
            return Response({"liked": True}, status=status.HTTP_201_CREATED)
        return Response({"liked": True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        product = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, product=product).first()
        if like:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)
        return Response({"error": "Like not found."}, status=status.HTTP_400_BAD_REQUEST)


class LikedViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Like.objects.select_related('user', 'product', 'product__category') \
            .filter(user=self.request.user) \
            .prefetch_related(
            Prefetch('product__likes_product', queryset=Like.objects.select_related('user'))
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user) \
            .select_related('product', 'product__category') \
            .prefetch_related('product__likes_product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Comment.objects.select_related('user', 'product', 'product__category')

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def by_product(self, request):
        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(product_id=product_id).select_related('user', 'product')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user) \
            .prefetch_related('items', 'items__product', 'items__product__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def clear_cart(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return CartItem.objects.select_related('cart', 'product', 'product__category') \
            .filter(cart__user=self.request.user)

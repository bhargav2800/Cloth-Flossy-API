from django.urls import path,include
from .views import ViewAllProducts, ViewProductDetail, ViewSearchedProduct, ViewTrendingProduct, CartAddRemoveUpdateView, WishListAddRemoveUpdateView, ProductReviewAddUpdateDelete, FavouriteBrands, OrderBuyCartCod, OrderDetail, ReturnProduct, ReplaceProduct, OrderBuyCartRazorpay, PaymentHandler
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('view_all_products', ViewAllProducts, basename='view_all_products')


urlpatterns = [
    path('', include(router.urls)),
    path('fav_brands/<int:id>/', FavouriteBrands.as_view(), name='fav_brand_section'),
    path('product/<int:id>', ViewProductDetail.as_view(), name='product_view'),
    path('product/review/<int:id>/', ProductReviewAddUpdateDelete.as_view(), name='product_reviews'),
    path('search/<str:search_value>/', ViewSearchedProduct.as_view(), name='search_view'),
    path('product/trending/', ViewTrendingProduct.as_view(), name='trending_product_view'),
    path('view_cart/', CartAddRemoveUpdateView.as_view(), name='view_cart'),
    path('cart/product/<int:id>/', CartAddRemoveUpdateView.as_view(), name='add_to_cart'),
    path('view_wishlist/', WishListAddRemoveUpdateView.as_view(), name='view_wishlist'),
    path('wishlist/product/<int:id>/', WishListAddRemoveUpdateView.as_view(), name='WishlistCrud'),
    path('order/', OrderBuyCartCod.as_view(), name='order'),
    path('order_razorpay/', OrderBuyCartRazorpay.as_view(), name='order_razorpay'),
    path('paymentHandler/', PaymentHandler.as_view(), name="PaytmentHandler"),
    path('order/view/<int:id>/', OrderDetail.as_view(), name='vieworderdetails'),
    path('order/cancel/<int:id>/', OrderDetail.as_view(), name='Cancelorder'),
    path('order/return_products/', ReturnProduct.as_view(), name='Return Products'),
    path('order/return_product/<int:id>/', ReturnProduct.as_view(), name='return_products'),
    path('order/replace_products/', ReplaceProduct.as_view(), name='Replace Products'),
    path('order/replace_product/<int:id>/', ReplaceProduct.as_view(), name='replace_products'),
]
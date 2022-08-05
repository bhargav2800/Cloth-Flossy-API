from django.urls import path,include
from .views import ViewAllProducts, ProductUpdateDeleteViewCreate, ViewProductReviews, ViewOrders, ReturnOrders, ReplaceOrders
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('view_all_products', ViewAllProducts, basename='view_all_products')

urlpatterns = [
    path('view_all_products/', ViewAllProducts.as_view(), name="view_self_products"),
    path('product/', ProductUpdateDeleteViewCreate.as_view(), name='product_seller'),
    path('product/view_all_reviews/<int:id>/', ViewProductReviews.as_view(), name='view_product_reviews'),
    path('view_orders/', ViewOrders.as_view(), name='view_orders'),
    path('InvoiceOrder/UpdateStatus/<int:id>/', ViewOrders.as_view(), name='invoice_order_update_status'),
    path('view_return_orders/', ReturnOrders.as_view(), name='view_return_orders'),
    path('ReturnOrder/UpdateStatus/<int:id>/', ReturnOrders.as_view(), name='return_order_update_status'),
    path('view_replace_orders/', ReplaceOrders.as_view(), name='view_replace_orders'),
    path('ReplaceOrder/UpdateStatus/<int:id>/', ReplaceOrders.as_view(), name='replace_order_update_status'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('', views.mobile_input, name="mobile"),
    path('verify-otp/', views.verify_otp, name="verify_otp"),
    path('order-already-done/', views.order_already_done, name="order_already_done"),
    path('welcome/', views.welcome, name="welcome"),
    path('spin/', views.spin_wheel, name="spin"),
    path('already-spin/', views.already_spin, name="already_spin"),
    path('products/', views.products, name='products'),
    path('select-product/<int:product_id>/', views.select_product, name="select_product"),
    path('address/', views.address, name="address"),
    path('order-success/', views.order_success, name='order_success'),

]

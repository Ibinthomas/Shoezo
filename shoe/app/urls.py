from django.urls import path
from . import views


urlpatterns = [
    path('',views.e_shop_login),
    path('shop_home',views.shop_home),
    path('add_pro',views.add_product),
    path('logout',views.e_shop_logout),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),
    path('view_bookings',views.view_bookings),
    # path('edit_phone/<id>',views.edit_phone),
    # path('add_accessories',views.add_accessories),

    
# -------------user----------
    path('register',views.register),
    path('contact',views.contact),
    path('about',views.about),
    path('user_home',views.user_home),
    path('view_product/<pid>',views.view_product),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart/',views.view_cart),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('bookings',views.bookings),
    path('cancel_order/<pid>',views.cancel_order),
    path('pro_buy/<pid>',views.pro_buy),


]
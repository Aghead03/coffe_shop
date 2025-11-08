from django.urls import path
from . import views

urlpatterns = [
    path('sign_in',views.sign_in,name='sign_in'),
    path('logout',views.logout,name='logout'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('profile' ,views.profile, name='profile'),
    path('product_favorites/<int:pro_id>',views.product_favorites , name = 'product_favorites'),
    path('show_product_favorites',views.show_product_favorites , name = 'show_product_favorites'),
]

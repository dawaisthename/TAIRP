from django.shortcuts import redirect
from django.urls import path
from . import views as view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
urlpatterns=[
    path('',view.Home,name='home'),
    path('about_us/',view.about_us,name='about_us'),
    path('register/',view.Customer_register,name='Customer_register'),
    path('login/',auth_view.LoginView.as_view(template_name="login.html"),name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name="logout.html"),name='logout'),
    path('profile/',view.profile,name='profile'),
    path ('update_profile/',view.update_profile,name='update_profile'),
    path('cart/',view.cart,name='cart'),
    path('update_item/',view.updateItem,name='update_item'),
     path('product/<int:product_id>/', view.detail, name='product'),
    path('all/<slug:cata>',view.all,name='all'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

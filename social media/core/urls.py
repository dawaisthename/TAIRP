from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
    path('setting/',views.setting,name='setting'),
    path('search',views.search,name='search'),
    path('upload/',views.upload,name='upload'),
    path('delete_post/<str:pk>',views.delete_post,name='delete_post'),
    path('addcomment',views.addcomment,name='addcomment'),
    path('followers_list/',views.followers_list,name='followers_list'),
    path('like_post/',views.like_post,name='like_post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('list_comment/<str:pk>',views.list_comment,name='list_comment'),
    path('follow',views.follow,name='follow'),
    
]

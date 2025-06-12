from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('post-approval/', views.post_approval_list, name='post_approval_list'),
    path('approve-post/<int:pk>/', views.approve_post, name='approve_post'),
    path('reject-post/<int:pk>/', views.reject_post, name='reject_post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('comments/', views.comment_list_or_create, name='comments'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('logout/', views.logout_view, name='logout'),
]
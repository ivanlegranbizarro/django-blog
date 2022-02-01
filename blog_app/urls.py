from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/create', views.CreatePost.as_view(), name='create_post'),
    path('posts/update/<slug:slug>', views.UpdatePost.as_view(), name='update_post'),
    path('posts/detail/<slug:slug>',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/delete/<slug:slug>', views.delete_post, name='delete_post'),
    path('category/create', views.CreateCategory.as_view(), name='create_category'),
    path('category/<slug:slug>', views.post_by_category, name='post_by_category'),
    path('posts/like', views.like_post, name='like_post'),
    path('users/create', views.RegisterUserView.as_view(),
         name='register_user'),
    path('users/update', views.UpdateUserView.as_view(), name='update_user'),
    path('users/change-password', views.UpdatePasswordView.as_view(), name='change_password'),
    path('users/profile', views.UserProfileView.as_view(), name='user_profile'),
    path('users/create-profile', views.create_user_profile, name='create_profile'),
    path('users/update-profile', views.UpdateProfileView.as_view(), name='update_profile'),
    path('comments/create/<slug:slug>', views.AddNewComment.as_view(), name='create_comment'),
]

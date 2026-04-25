from django.urls import path  # Import path for URL routing
from .views import (
    PostListView,
    PostDetailView,
    PostEditView,
    PostDeleteView,
    CommentDeleteView,
    ProfileView,
    ProfileEditView,
    AddFollower,
    RemoveFollower,
    AddLike,
    AddDislike,
    UserSearch
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),  # Route for the post list view
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Route for viewing a single post
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),  # Route for editing a post
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),  # Route for deleting a post
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),  # Route for deleting a comment
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),  # Route for liking a post
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),  # Route for disliking a post
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),  # Route for viewing a user profile
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),  # Route for editing a user profile
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),  # Route for adding a follower
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),  # Route for removing a follower
    path('search/', UserSearch.as_view(), name='profile-search'),  # Route for searching user profiles
]

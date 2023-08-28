from django.urls import path
# from .views import api_detail_blog_view, api_update_blog_view, api_delete_blog_view, api_create_blog_view, ApiBlogListView
from . import views


urlpatterns = [
    path('home/', views.HomeAPIView.as_view(), name='home-api'),
    path('article/<int:pk>/', views.ArticleAPIView.as_view(), name='article-api'),
    path('add/', views.AddPostAPIView.as_view(), name='add-api'),
    path('update/<int:pk>/', views.UpdatePostAPIView.as_view(), name='update-api'),
    path('delete/<int:pk>/', views.DeletePostAPIView.as_view(), name='delete-api'),
    path('category-list/', views.CategoryListAPIView.as_view(), name='category-list-api'),
    path('category/<str:cat>/', views.CategoryAPIView.as_view(), name='category-api'),
    path('add-category/', views.AddCategoryAPIView.as_view(), name='add-category'),
    path('like/<int:pk>', views.LikeAPIView.as_view(), name='like-api'),
    # path('api/posts/<int:pk>/like/', api_views.LikeAPIView.as_view(), name='like-api'),
    path('article/<int:pk>/comment', views.AddCommentAPIView.as_view(), name='add-comment'),
]
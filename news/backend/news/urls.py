from django.urls import path
from .views import NewsListView, NewsDetailView, RegisterView, LoginView, NewsCreateView, NewsDeleteView, NewsUpdateView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/update/<int:pk>/', NewsUpdateView.as_view(), name='news-update'),
    path('news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news-delete'),
]

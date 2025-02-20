from django.urls import path
from .views import NewListView, NewDetailView, RegisterView, LoginView, NewCreateView, NewDeleteView, NewUpdateView
from . import views
urlpatterns = [
    path('news/', NewListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewDetailView.as_view(), name='news-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('news/create/', NewCreateView.as_view(), name='news-create'),
    path('news/update/<int:pk>/', NewUpdateView.as_view(), name='news-update'),
    path('news/delete/<int:pk>/', NewDeleteView.as_view(), name='news-delete'),

    path('', views.ProductView.as_view(), name='home'),
]

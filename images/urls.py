from django.urls import path
from .views import AddImageView, ImagesListView, LoginView

urlpatterns = [
    path('', AddImageView.as_view(), name='image-add'),
    path('list/', ImagesListView.as_view(), name='image-list'),
    path('api-login', LoginView.as_view(), name='api-login'),
]

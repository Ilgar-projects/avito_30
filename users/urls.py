from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import *

router = SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),

    path('token/', TokenObtainPairView.as_view()), # получение токена
    path('token/refresh/', TokenRefreshView.as_view()), # обновление токена
]
urlpatterns += router.urls


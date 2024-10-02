from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, TransactionViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
]
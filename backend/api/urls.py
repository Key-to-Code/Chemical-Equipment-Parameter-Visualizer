from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, upload_csv

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('', include(router.urls)),
]

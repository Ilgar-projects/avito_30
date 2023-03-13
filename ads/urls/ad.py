from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views.ad import *

router = SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
    path('<int:pk>/upload_image/', AdImageUpload.as_view()),
]
urlpatterns += router.urls

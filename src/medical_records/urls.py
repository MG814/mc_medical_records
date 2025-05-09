from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import MedicalRecordViewSet

router = SimpleRouter()
router.register('', MedicalRecordViewSet, basename='medical-records-create')

urlpatterns = [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls

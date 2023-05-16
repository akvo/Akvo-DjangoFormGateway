from django.urls import path, include
from .views import AkvoFormViewSet, CheckView, TwilioViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'forms', AkvoFormViewSet, basename='forms')
router.register(r'twilio', TwilioViewSet, basename='twilio')
urlpatterns = [
    path('', include(router.urls)),
    path('check/', CheckView.as_view()),
]

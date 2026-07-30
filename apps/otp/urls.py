from django.urls import path
from .views import OTPMessageListCreateView, OTPMessageDetailView, HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('otp-messages/', OTPMessageListCreateView.as_view(), name='otp-message-list-create'),
    path('otp-messages/<uuid:id>/', OTPMessageDetailView.as_view(), name='otp-message-detail'),
]

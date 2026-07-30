from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import OTPMessage
from .serializers import OTPMessageSerializer

class HealthCheckView(APIView):
    """
    Health Check Endpoint.
    """
    permission_classes = []
    
    @extend_schema(responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}})
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})

class OTPMessageListCreateView(generics.ListCreateAPIView):
    """
    List all OTP messages or create a new one.
    """
    queryset = OTPMessage.objects.all()
    serializer_class = OTPMessageSerializer
    permission_classes = []
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Alphanumeric Sender (bKash)',
                summary='Alphanumeric Sender (bKash)',
                description='Example with alphanumeric sender ID like bKash.',
                value={
                    "otp": "483921",
                    "sender": "bKash",
                    "receiver_number": "+88017XXXXXXXX",
                    "message_body": "Your OTP is 483921",
                    "received_at": "2026-07-30T12:00:00Z",
                    "metadata": {
                        "sender_type": "ALPHANUMERIC",
                        "carrier": "Grameenphone",
                        "sim_slot": 0
                    },
                    "raw_payload": {
                        "android_version": 16,
                        "device_model": "Pixel 8"
                    }
                },
                request_only=True,
            ),
            OpenApiExample(
                'Phone Number Sender',
                summary='Phone Number Sender',
                description='Example with an actual phone number.',
                value={
                    "otp": "123456",
                    "sender": "+8801712345678",
                    "receiver_number": "+88017XXXXXXXX",
                    "message_body": "Your verification code is 123456",
                    "received_at": "2026-07-30T12:05:00Z",
                    "metadata": {},
                    "raw_payload": {}
                },
                request_only=True,
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OTPMessageDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific OTP message by UUID.
    """
    queryset = OTPMessage.objects.all()
    serializer_class = OTPMessageSerializer
    permission_classes = []
    lookup_field = 'id'

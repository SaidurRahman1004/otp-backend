import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class OTPMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID")
    )
    
    # Core Fields
    otp = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name=_("OTP"),
        help_text=_("Extracted OTP. Null if extraction failed.")
    )
    sender = models.CharField(
        max_length=255, 
        verbose_name=_("Sender")
    )
    receiver_number = models.CharField(
        max_length=255, 
        verbose_name=_("Receiver Number")
    )
    message_body = models.TextField(
        verbose_name=_("Message Body")
    )
    received_at = models.DateTimeField(
        verbose_name=_("Received At")
    )
    
    # Flexible Fields
    metadata = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Flexible JSON metadata for future fields from Android without schema changes.")
    )
    raw_payload = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name=_("Raw Payload"),
        help_text=_("The original raw JSON payload received from the Android device.")
    )
    
    # System Fields
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("OTP Message")
        verbose_name_plural = _("OTP Messages")
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver_number} (OTP: {self.otp or 'N/A'})"

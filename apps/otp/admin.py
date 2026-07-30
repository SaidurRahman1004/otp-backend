from django.contrib import admin
from .models import OTPMessage

@admin.register(OTPMessage)
class OTPMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver_number', 'otp', 'received_at', 'created_at')
    list_filter = ('sender', 'received_at', 'created_at')
    search_fields = ('sender', 'receiver_number', 'otp', 'message_body')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Core Details', {
            'fields': ('id', 'otp', 'sender', 'receiver_number', 'message_body', 'received_at')
        }),
        ('Flexible Fields', {
            'fields': ('metadata', 'raw_payload')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at')
        }),
    )

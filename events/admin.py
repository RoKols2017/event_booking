# events/admin.py

from django.contrib import admin
from .models import Event, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'genre', 'price', 'capacity', 'available_tickets')
    search_fields = ('title', 'location', 'genre')
    list_filter = ('date', 'location', 'genre')
    readonly_fields = ('available_tickets',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'image',
                ('date', 'location'),
                'genre', 'price', 'capacity', 'available_tickets'
            )
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'booking_date', 'confirmed')
    search_fields = ('name', 'email')
    list_filter = ('event', 'confirmed')

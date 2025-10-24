from django.contrib import admin
from .models import Bus, Seat, Booking

class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'bus_number', 'origin', 'destination', 'start_time', 'end_time', 'price')
    search_fields = ('bus_name', 'bus_number', 'origin', 'destination')

class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'bus', 'is_available')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'seat', 'booking_time', 'origin', 'destination', 'price')

admin.site.register(Bus, BusAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Booking, BookingAdmin)  



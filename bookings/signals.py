from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Bus, Seat, Booking

# Create seats for new bus
@receiver(post_save, sender=Bus)
def create_seats_for_bus(sender, instance, created, **kwargs):
    if created:
        seats = [Seat(bus=instance, seat_number=str(i)) for i in range(1, instance.no_of_seats + 1)]
        Seat.objects.bulk_create(seats)  # bulk create all seats in one query

# Mark seat unavailable on new booking
@receiver(post_save, sender=Booking)
def mark_seat_unavailable(sender, instance, created, **kwargs):
    if created:
        seat = instance.seat
        if seat.is_available:
            with transaction.atomic():
                seat.is_available = False
                seat.save(update_fields=['is_available'])

# Mark seat available on booking deletion
@receiver(post_delete, sender=Booking)
def mark_seat_available(sender, instance, **kwargs):
    seat = instance.seat
    if not seat.is_available:
        with transaction.atomic():
            seat.is_available = True
            seat.save(update_fields=['is_available'])

# Handle seat change on booking update
@receiver(pre_save, sender=Booking)
def handle_seat_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New booking, handled by post_save

    previous = Booking.objects.get(pk=instance.pk)
    new_seat = instance.seat

    if previous.seat != new_seat:
        with transaction.atomic():
            # Make previous seat available if needed
            if not previous.seat.is_available:
                previous.seat.is_available = True
                previous.seat.save(update_fields=['is_available'])
            # Make new seat unavailable if available
            if new_seat.is_available:
                new_seat.is_available = False
                new_seat.save(update_fields=['is_available'])
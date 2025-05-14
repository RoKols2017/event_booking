# events/models.py

from django.db import models
from django.contrib.auth.models import User

# events/models.py

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.available_tickets:
            self.available_tickets = self.capacity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.date.strftime('%d.%m.%Y %H:%M')}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=True)
    ticket_pdf = models.FileField(upload_to='tickets/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} — {self.event.title}"

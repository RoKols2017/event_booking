# events/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Event

class EventTests(TestCase):
    def setUp(self):
        Event.objects.create(title="Тест", description="Описание", date="2025-12-12T18:00",
                             location="Москва", genre="Концерт", price=1000, capacity=50, available_tickets=50)

    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тест")

    def test_booking_flow(self):
        event = Event.objects.first()
        response = self.client.post(reverse('book_event', args=[event.pk]), {
            "name": "Иван",
            "email": "ivan@example.com"
        })
        self.assertEqual(response.status_code, 302)  # redirect to confirmation

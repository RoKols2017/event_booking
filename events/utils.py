# events/utils.py

import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import qrcode
from django.core.mail import EmailMessage

def generate_pdf_ticket(booking):
    qr = qrcode.make(f"Booking ID: {booking.id}, Event: {booking.event.title}")
    qr_path = os.path.join(settings.MEDIA_ROOT, f'qr_{booking.id}.png')
    qr.save(qr_path)

    pdf_path = os.path.join(settings.MEDIA_ROOT, f'ticket_{booking.id}.pdf')
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, f"Билет на мероприятие: {booking.event.title}")
    c.drawString(100, 780, f"Имя: {booking.name}")
    c.drawString(100, 760, f"Email: {booking.email}")
    c.drawImage(qr_path, 100, 600, width=150, height=150)
    c.save()
    return f'tickets/ticket_{booking.id}.pdf'

def send_booking_email(booking):
    subject = f"Подтверждение бронирования: {booking.event.title}"
    body = f"Здравствуйте, {booking.name}!\n\nВы успешно забронировали билет на: {booking.event.title}"
    email = EmailMessage(
        subject,
        body,
        'noreply@eventbooking.ru',
        [booking.email],
    )
    if booking.ticket_pdf:
        pdf_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(booking.ticket_pdf.name))
        email.attach_file(pdf_path)
    email.send(fail_silently=True)

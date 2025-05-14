# events/views.py

import csv
from io import TextIOWrapper
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Booking
from .forms import BookingForm, EventFilterForm, UserRegisterForm, EventForm
from django.contrib import messages
from .utils import generate_pdf_ticket, send_booking_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.utils.dateparse import parse_datetime


def event_list(request):
    events = Event.objects.all()
    form = EventFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['date']:
            events = events.filter(date__date=form.cleaned_data['date'])
        if form.cleaned_data['location']:
            events = events.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['genre']:
            events = events.filter(genre__icontains=form.cleaned_data['genre'])
    return render(request, 'events/event_list.html', {'events': events, 'form': form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.available_tickets <= 0:
        messages.error(request, "Свободных билетов нет.")
        return redirect('events/event_list')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.event = event
            booking.save()
            event.available_tickets -= 1
            event.save()

            # PDF + email
            pdf_path = generate_pdf_ticket(booking)
            booking.ticket_pdf = pdf_path
            booking.save()
            send_booking_email(booking)

            messages.success(request, "Бронирование успешно! Подтверждение отправлено.")
            return redirect('events/booking_confirmation')
    else:
        form = BookingForm()
    return render(request, 'events/booking_form.html', {'form': form, 'event': event})


def booking_confirmation(request):
    return render(request, 'events/booking_confirmation.html')


@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/dashboard.html', {'bookings': bookings})


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect('events/event_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.available_tickets = event.capacity
            event.save()
            messages.success(request, "Мероприятие успешно добавлено.")
            return redirect('admin_panel')

    events = Event.objects.all().order_by('-date')
    return render(request, 'events/admin_panel.html', {
        'form': form,
        'events': events
    })

@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    form = EventForm()
    if request.method == 'POST':
        if 'manual_submit' in request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.available_tickets = event.capacity
                event.save()
                messages.success(request, "Мероприятие успешно добавлено.")
                return redirect('admin_panel')

        elif 'csv_submit' in request.POST and request.FILES.get('csv_file'):
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    Event.objects.create(
                        title=row['Название'],
                        description=row['Описание'],
                        date=parse_datetime(row['Дата']),
                        location=row['Место'],
                        genre=row['Жанр'],
                        price=float(row['Цена']),
                        capacity=int(row['Мест']),
                        available_tickets=int(row['Мест']),
                    )
                except Exception as e:
                    messages.error(request, f"Ошибка в строке: {row['Название']}: {e}")
            messages.success(request, "CSV-файл успешно загружен.")
            return redirect('admin_panel')

    events = Event.objects.all().order_by('-date')
    return render(request, 'events/admin_panel.html', {
        'form': form,
        'events': events
    })
from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Agent, TourSchedule, Booking
from .forms import BookingForm
from telegram_bot.drive_uploader import upload_file
from telegram_bot.sheet_writer import write_to_sheet
import os
import requests
from django.contrib import messages


def booking_view(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    bookings = agent.booking_set.all()
    tours = TourSchedule.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.agent = agent
            booking.commission = booking.tour.commission_per_client
            booking.save()

            # Joyni kamaytirish
            booking.tour.booked_seats += 1
            booking.tour.save()

            # Telegramga yuborish
            bot_token = '7927590527:AAHu1eG-cDV_DHoiHim78G00VxaDl06a_84'
            chat_id = '-1002406229679'
            text = f"""📌 Yangi bron:
👤 Agent: {agent.name}
👥 Mijoz: {booking.client_name}
📞 Telefon: {booking.phone}
🗺 Yo‘nalish: {booking.route}"""
            try:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={'chat_id': chat_id, 'text': text}
                )
            except Exception as e:
                print("Telegram xabari yuborishda xatolik:", e)

            # Fayllarni Telegramga yuborish
            for file_path in [
                booking.passports.path if booking.passports else None,
                booking.photos.path if booking.photos else None,
                booking.receipts.path if booking.receipts else None
            ]:
                if file_path and os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            requests.post(
                                f"https://api.telegram.org/bot{bot_token}/sendDocument",
                                data={'chat_id': chat_id},
                                files={'document': f}
                            )
                    except Exception as e:
                        print("Telegram fayl yuborishda xatolik:", e)

            # Google Drive yuklash
            passport_link = upload_file(booking.passports.path, 'passport.jpg', settings.PASSPORTS_FOLDER_ID) if booking.passports else ''
            photo_link = upload_file(booking.photos.path, 'photo_3x4.jpg', settings.PHOTOS_FOLDER_ID) if booking.photos else ''
            receipt_link = upload_file(booking.receipts.path, 'payment_receipt.jpg', settings.RECEIPTS_FOLDER_ID) if booking.receipts else ''

            # Google Sheets
            sheet_data = {
                'client_name': booking.client_name,
                'phone': booking.phone,
                'route': booking.route,
                'passport_link': passport_link,
                'photo_link': photo_link,
                'receipt_link': receipt_link,
            }
            write_to_sheet(sheet_data)

            # Muvaffaqiyatli xabar
            messages.success(request, "✅ Mijoz ro'yxatdan o'tkazildi. Tez orada menejerlar siz bilan bog'lanadi.")
            return redirect(request.path)
    else:
        form = BookingForm()

    return render(request, 'booking/agent_dashboard.html', {
        'agent': agent,
        'form': form,
        'bookings': bookings,
        'tours': tours,
    })


def home_view(request):
    return render(request, 'booking/home.html')


def contact_view(request):
    return render(request, 'booking/contact.html')


def tour_list_view(request):
    tours = TourSchedule.objects.all()
    return render(request, 'booking/tour_list.html', {'tours': tours})


def routes_view(request):
    tours = TourSchedule.objects.all()
    return render(request, 'booking/routes.html', {'tours': tours})


def set_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang:
            activate(lang)
            request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                agent = Agent.objects.get(user=user)
                return redirect(f'/agent/{agent.id}/')
            except Agent.DoesNotExist:
                return redirect('home')
        else:
            return render(request, 'booking/login.html', {'error': "Login yoki parol noto‘g‘ri"})
    return render(request, 'booking/login.html')
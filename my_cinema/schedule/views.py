from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from .decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import Seat, Ticket, Screening, Movie, User, Genre
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def convert_youtube_url(url):
    if "youtube.com/watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    return url


def show_schedule(request):
    current_time = timezone.now()
    screenings = Screening.objects.filter(start_time__gt=current_time)

    sort_by = request.GET.get('sort_by')
    genre = request.GET.get('genre')

    if sort_by == 'date':
        screenings = screenings.order_by('start_time')
    elif sort_by == 'price':
        screenings = screenings.order_by('price')

    if genre:
        screenings = screenings.filter(movie__genres__name=genre)

    genres = Genre.objects.all()
    return render(request, 'schedule/schedule.html', {'screenings': screenings, 'genres': genres})
def show_main(request):
    current_time = timezone.now()
    active_screenings = Screening.objects.filter(end_time__gte=current_time)
    unique_movies = {screening.movie for screening in active_screenings}
    return render(request, 'schedule/main.html', {'unique_movies': unique_movies})

@csrf_exempt
@login_required(login_url='/login/')
def profile(request, user_id):
    user=request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'schedule/profile.html', {'user': user, 'tickets': tickets})

@csrf_exempt
def refund_ticket(request, ticket_id):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            seat = Seat.objects.get(screening_id=ticket.screening.id, number=ticket.seat_number)
            seat.is_available = True
            seat.save()
            ticket.delete()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket does not exist'})
        except Seat.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Seat does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
@csrf_exempt
@login_required(login_url='/login/')
def select_seats(request, screening_id):
    screening = get_object_or_404(Screening, id=screening_id)
    return render(request, 'schedule/select_seats.html', {'screening': screening})


def get_seats(request, screening_id):
    seats = Seat.objects.filter(screening_id=screening_id)
    seat_data = [{'id': seat.id, 'number': seat.number, 'busy': not seat.is_available} for seat in seats]
    return JsonResponse({'seats': seat_data})


@csrf_exempt
@login_required(login_url='/login/')
def buy_seats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        seat_ids = data.get('seat_ids', [])
        screening_id = data.get('screening_id')
        user_id = request.user.id
        seats = Seat.objects.filter(id__in=seat_ids, is_available=True)
        if not seats.exists():
            return JsonResponse({'status': 'error', 'message': 'No seats available'})

        for seat in seats:
            seat.is_available = False
            seat.save()
            Ticket.objects.create(screening_id=screening_id, user_id=user_id, seat_number=seat.number)

        return JsonResponse({'status': 'success', 'message': 'Seats purchased successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def movie_info(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.trailer = convert_youtube_url(movie.trailer)
    return render(request, 'schedule/movie_info.html', {'movie': movie})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserRegistrationForm()
    return render(request, 'schedule/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'schedule/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

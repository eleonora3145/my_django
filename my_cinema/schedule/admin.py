from django.contrib import admin
from .models import User, Movie, Screening, Ticket, Seat, Genre

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Ticket)
admin.site.register(Seat)
admin.site.register(Genre)

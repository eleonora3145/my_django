from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=80)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='schedule_user_set',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='schedule_user_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )

    def __str__(self):
        return self.email

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Movie(models.Model):
    title = models.CharField(max_length=150)
    director = models.CharField(max_length=100, blank=True, null=True)
    photo = models.URLField(max_length=200, blank=True, null=True)
    trailer = models.URLField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.movie.title} - {self.start_time}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Seat.objects.filter(screening=self).exists():
            seats = [Seat(number=i+1, screening=self) for i in range(50)]
            Seat.objects.bulk_create(seats)

class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    def __str__(self):
        return f'Ticket {self.id} for {self.screening.movie.title}'

class Seat(models.Model):
    number = models.IntegerField()
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Seat {self.number} for {self.screening.movie.title}'

from django.db import models
from django.contrib.auth.models import User

class TourSchedule(models.Model):
    direction = models.CharField(max_length=100)
    date = models.DateField()
    max_seats = models.IntegerField(default=0)  # default qo‘shildi
    booked_seats = models.IntegerField(default=0)
    commission_per_client = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='tours/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def remaining_seats(self):
        return self.max_seats - self.booked_seats

    def __str__(self):
        return f"{self.direction} — {self.date}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    telegram_id = models.BigIntegerField(null=True, blank=True)  # qo‘shildi

    def __str__(self):
        return self.name


class Booking(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    tour = models.ForeignKey(TourSchedule, on_delete=models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    route = models.CharField(max_length=100)
    passports = models.FileField(upload_to='passports/', null=True, blank=True)
    photos = models.FileField(upload_to='photos/', null=True, blank=True)
    receipts = models.FileField(upload_to='receipts/', null=True, blank=True)
    tracking_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    STATUS_CHOICES = (
    ('new', 'Yangi'),
    ('viewed', 'Ko‘rib chiqildi'),
    ('approved', 'Tasdiqlandi'),
    ('rejected', 'Rad etildi'),
)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Yangi')
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ '-id']

    def __str__(self):
        return f"{self.client_name} — {self.route}"

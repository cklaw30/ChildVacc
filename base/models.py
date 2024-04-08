from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    contact = models.CharField(max_length=12, null=True)
    address1 = models.CharField(max_length=30)
    address2 = models.CharField(max_length=30)
    postcode = models.CharField(max_length=5)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)

    class Types(models.TextChoices):
        PARENT = "PARENT", "Parent"
        HOSPITAL = "HOSPITAL", "Hospital"
        ADMIN = "ADMIN", "Admin"
        VACCINESUPPLIER = "VACCINESUPPLIER", "VaccineSupplier"

    type = models.CharField(max_length=50, choices=Types.choices, default=Types.ADMIN)

    class Status(models.TextChoices):
        APPROVED = "APPROVED", "Approved"
        PENDING = "PENDING", "Pending"
        RESTRICTED = "RESTRICTED", "Restricted"

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['username']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'type']

class ParentManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(type=User.Types.PARENT)

class HospitalManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(type=User.Types.HOSPITAL)
    
class AdminManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(type=User.Types.ADMIN)
    
class VaccineSupplierManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(type=User.Types.VACCINESUPPLIER)

class Parent(User):
    objects = ParentManager()

    class Meta:
        proxy = True

class Hospital(User):
    objects = HospitalManager()

    class Meta:
        proxy = True

class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True

class VaccineSupplier(User):
    objects = VaccineSupplierManager()

    class Meta:
        proxy = True

class Child(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(default=0)
    ic = models.CharField(max_length=12, unique=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default="avatar.svg")

    class Meta:
        ordering = ['age', 'name']

    def __str__(self):
        return self.name
    
class Vaccine(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    startage = models.IntegerField()
    endage = models.IntegerField()

    def __str__(self):
        return self.name

class HospitalVaccine(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    stored = models.IntegerField()
    booked = models.IntegerField(default=0)
    expiry = models.DateField(null=True)

    class Status(models.TextChoices):
        TOSHIP = "TOSHIP", "ToShip"
        TORECEIVE = "TORECEIVE", "ToReceive"
        COMPLETED = "COMPLETED", "Completed"
        EXPIRED = "EXPIRED", "Expired"

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.TOSHIP)

    class Meta:
        ordering = ['expiry', 'status', 'vaccine']

    def __str__(self):
        return str(self.hospital) + " " + str(self.vaccine) + " " + str(self.expiry)

class Appointment(models.Model):
    hospitalvaccine = models.ForeignKey(HospitalVaccine, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        VACCINATED = "VACCINATED", "Vaccinated"

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.SCHEDULED)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return str(self.child) + " " + str(self.hospitalvaccine)
    
class HealthInfo(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    healthinfo = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.topic
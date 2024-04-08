from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Hospital, Child, Appointment, HealthInfo, HospitalVaccine, Vaccine

class MyUserCreationForm(UserCreationForm):
    TYPE_CHOICES = [
        ('PARENT', 'Parent'),
        ('HOSPITAL', 'Hospital'),
    ]

    type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'type']

class ChildCreationForm(ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'ic', 'age']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'contact', 'address1', 'address2', 'postcode', 'city', 'state', 'avatar']

class AdminForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'contact', 'avatar']

class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'avatar']

class HospitalStatusForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['status']

class HealthInfoForm(ModelForm):
    class Meta:
        model = HealthInfo
        fields = ['topic', 'healthinfo']

class AppointmentStatusForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']

class HospitalVaccineOrderForm(ModelForm):
    class Meta:
        model = HospitalVaccine
        fields = ['vaccine', 'stored']

class VaccineForm(ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name', 'startage', 'endage', 'description']

class OrderForm(ModelForm):
    class Meta:
        model = HospitalVaccine
        fields = ['status']
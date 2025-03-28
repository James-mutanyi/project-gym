from django import forms
from .models import *



class TrainerLoginForm(forms.ModelForm):
    class Meta:
        model=Trainer
        fields=('username', 'psw',)

class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=[]
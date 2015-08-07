from django import forms
from bookings.models import Bookings
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.extras.widgets import SelectDateWidget

TREADMILL_CHOICES=(
    ('TREADMILL1','1'),
    ('TREADMILL2','2'),
    ('TREADMILL3','3'),
)


ROWING_MACHINE_CHOICE=(
    ('ROWINGMACHINE1', '1'),
    ('ROWINGMACHINE2', '2'),
    ('ROWINGMACHINE3', '3'),
)

STAIRS_MACHINE_CHOICE=(
    ('STAIRSMACHINE1', '1'),
    ('STAIRSMACHINE2', '2'),
    ('STAIRSMACHINE3', '3'),
)


class TreadmillForm(forms.ModelForm):
   # machine_name=forms.ChoiceField(choices=TREAMILL_CHOICES)
    #booked_info=forms.DateTimeField(widget=forms.DateTimeInput())
    #username=forms.
    class Meta:
        model= Bookings
        exclude=('username',)

class Rowing_Machine_Form(forms.ModelForm):
    class Meta:
       model= Bookings
       exclude=('username',)

class Stair_Machine_Form(forms.ModelForm):
    class Meta:
       model= Bookings
       exclude=('username',)


class BookedMachineForm(forms.ModelForm):
    class Meta:
        model= Bookings






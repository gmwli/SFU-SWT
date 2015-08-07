from django import forms
from bookings.models import Bookings
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple


OPEN_TIMES = (
	('6', '6:00-7:00'),
	('7', '7:00-8:00'),
	('8', '8:00-9:00'),
	('9', '9:00-10:00'),
	('10', '10:00-11:00'),
	('11', '11:00-12:00'),
	('12', '12:00-13:00'),
	('13', '13:00-14:00'),
	('14', '14:00-15:00'),
	('15', '15:00-16:00'),
	('16', '16:00-17:00'),
	('17', '17:00-18:00'),
	('18', '18:00-19:00'),
	('19', '19:00-20:00'),
	('20', '20:00-21:00'),
)

MACHINE_TYPES = (
	('rowing', 'Rowing Machine'),
	('stairs', 'Stairs Machine'),
	('treadmill', 'Treadmill'),
)


class AddBookingForm(forms.ModelForm):
	machine_name = forms.ChoiceField(choices=MACHINE_TYPES)
	treadmill_time = forms.ChoiceField(choices=OPEN_TIMES)
	stairs_time = forms.ChoiceField(choices=OPEN_TIMES)
	rowing_time = forms.ChoiceField(choices=OPEN_TIMES)

	class Meta:
		model = Bookings
		fields = ('machine_name', 'treadmill_time', 'stairs_time', 'rowing_time',)

	def __init__(self, *args, **kwargs):
		super(AddBookingForm, self).__init__(*args, **kwargs)
		#treadmill_time= kwargs.pop("treadmill_time")
		for field_name in self.fields:
			field = self.fields[field_name]
			field.widget.attrs.update({
				'class': 'form-control input-sm'
			})
		#self.fields['treadmill_time']= forms.ChoiceFields(choices=treadmill_time)


class DeleteBookingsForm(forms.ModelForm):
       class Meta:
           model= Bookings
           fields=('machine_name','booked_time','booked_date',)
	   exclude=('username',)        


class AddBookingFormTomorrow(forms.ModelForm):
	machine_name_tmr = forms.ChoiceField(choices=MACHINE_TYPES)
        treadmill_time_tmr = forms.ChoiceField(choices=OPEN_TIMES)
        stairs_time_tmr = forms.ChoiceField(choices=OPEN_TIMES)
        rowing_time_tmr = forms.ChoiceField(choices=OPEN_TIMES)

        class Meta:
                model = Bookings
                fields = ('machine_name_tmr', 'treadmill_time_tmr', 'stairs_time_tmr', 'rowing_time_tmr',)

        def __init__(self, *args, **kwargs):
                super(AddBookingFormTomorrow, self).__init__(*args, **kwargs)
                #treadmill_time= kwargs.pop("treadmill_time")
                for field_name in self.fields:
                        field = self.fields[field_name]
                        field.widget.attrs.update({
                                'class': 'form-control input-sm'
                        })


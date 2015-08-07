from django import forms
from workouts.models import Workout, FilterPreference, chartrequest
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

#for drop down box choice for weight workouts
WEIGHT_TYPE_CHOICES = (
	('LEGS', 'Legs'),
	('CHEST', 'Chest'),
	('BACK', 'Back'),
)

#for drop down box choice for years
WORKOUT_YEAR_CHOICES = ( '2013', '2012', '2011', '2010' ) 

#for drop down box choice for months
WORKOUT_MONTH_CHOICES = (
	('1', 'January'),
	('2', 'February'),
	('3', 'March'),
	('4', 'April'),
	('5', 'May'),
	('6', 'June'),
	('7', 'July'),
	('8', 'Augsut'),
	('9', 'September'),
	('10', 'October'),
	('11', 'November'),
	('12', 'December'),
)

#for drop down box choice for workout types
WORKOUT_TYPE_CHOICES = (
	('Cardio Workout', 'Cardio Workouts'),
	('Weights Workout', 'Weights Workouts')
)

#cardio workout types
CARDIO_TYPE_CHOICES = (
	('TREADMILL', 'Treadmill'),
	('STAIRS', 'Stairs'),
	('ROWING', 'Rowing'),
)

#date filters
DATE_FILTER_CHOICES = (
	('LAST1MONTH', 'Last Month'),
	('LAST6MONTH', 'Last 6 Months'),
	('OVERALL', 'Overall'),
)

#form for user to add workout to database
class AddWorkoutForm(forms.ModelForm):
	cardio_type = forms.ChoiceField(choices=CARDIO_TYPE_CHOICES)
	weights_type = forms.ChoiceField(choices=WEIGHT_TYPE_CHOICES)
	date = forms.DateField(widget=SelectDateWidget(years=WORKOUT_YEAR_CHOICES))
	
	class Meta:
		model = Workout
		fields = ('style', 'cardio_type', 'weights_type', 'date', 'speed', 'time', 'weight', 'sets', 'reps',)

	def __init__(self, *args, **kwargs):
		super(AddWorkoutForm, self).__init__(*args, **kwargs)
		for field_name in self.fields:
			field = self.fields[field_name]
			field.widget.attrs.update({
				'class': 'form-control input-sm',	
			})

#form for gathering information for generating a social workout report
class CommunityStatsForm(forms.ModelForm):
	social_time_period = forms.ChoiceField(choices=DATE_FILTER_CHOICES)
	
	class Meta:
		model = FilterPreference
		fields = ('social_time_period',)

			
#form for users to request graph summary of workouts
class graphrequestform(forms.ModelForm):
	style = forms.ChoiceField(choices=WORKOUT_TYPE_CHOICES)
	month = forms.ChoiceField(choices=WORKOUT_MONTH_CHOICES)
	class Meta:	
		model = chartrequest
		fields = ('style', 'month',)
		exclude = ('username',)




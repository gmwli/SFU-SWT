from django.db import models
from django.core.exceptions import ValidationError


# Workout model.
class Workout(models.Model):
	username = models.CharField(max_length=50)
	#style can be 'cardio workout' or 'weights workout'
	style = models.CharField(max_length=50)
	#keep track of type of cardio workout
	cardio_type = models.CharField(max_length=50, null=True, blank=True)
	#keep track of type of weights workout
	weights_type = models.CharField(max_length=50, null=True, blank=True)
	#date storage
	date = models.DateField()
	month = models.IntegerField(null=True, blank=True)
	day = models.IntegerField(null=True, blank=True)

	# Cardio Workout Metrics
	speed = models.IntegerField(null=True, blank = True)
	time = models.IntegerField(null=True, blank=True)

	# Weights Workout Metrics
	weight = models.IntegerField(null=True, blank = True)
	sets = models.IntegerField(null=True, blank = True)
	reps = models.IntegerField(null=True, blank=True)

#model for setting preference for length of workout history
class FilterPreference(models.Model):
	username = models.CharField(max_length=50)
	social_time_period = models.CharField(max_length=50, default="OVERALL")

#model for a chartrequest information
class chartrequest(models.Model):
	username= models.CharField(max_length=50)
	month = models.IntegerField(null=True, blank=True)
	style = models.CharField(max_length=50)


from django.db import models
from django.core.signing import Signer
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.conf import settings


def validate_positive(value):
	if value < 1:
		raise ValidationError('%s must be positive.' % value)

def validate_length(value):
	if len(value) < 1:
		raise ValidationError('Please enter a valid value.')


# Create your models here.
class Profile(models.Model):
	username = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50, validators=[validate_length])
	last_name = models.CharField(max_length=50, validators=[validate_length])
	weight = models.IntegerField(blank=True, null=True, validators=[validate_positive])
	height = models.IntegerField(blank=True, null=True, validators=[validate_positive])
	bio = models.TextField(blank=True, null=True)
	quote = models.TextField(blank=True, null=True)
	profile_pic = models.URLField(blank=True)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.first_name + " " + self.last_name


class FriendList(models.Model):
    sender_id = models.CharField(max_length=50)
    receiver_id = models.CharField(max_length=50)
    accepted = models.BooleanField(default=False)
	

class GymStatus(models.Model):
	gym_area = models.CharField(max_length=50)
	status = models.CharField(max_length=50)
	last_modified_by = models.CharField(max_length=50)

from django import forms
from profiles.models import Profile, FriendList, GymStatus


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('first_name', 'last_name', 'weight', 'height', 'bio', 'quote', 'profile_pic')

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		for field_name in self.fields:
			field = self.fields[field_name]
			field.widget.attrs.update({
				'class': 'form-control input-sm'
			})


class FriendsForm(forms.ModelForm):	
	class Meta:
		model = FriendList
		fields = ('receiver_id',)

	def __init__(self, *args, **kwargs):
		super(FriendsForm, self).__init__(*args, **kwargs)
		self.fields['receiver_id'].widget.attrs.update({
			'class': 'form-control input-sm',
			'id': 'inputSmall'
		})
	
	
class GymStatusForm(forms.ModelForm):
	class Meta:
		model = GymStatus
		fields = ('gym_area', 'status')
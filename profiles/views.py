import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.signing import Signer
from time import strftime
import urllib

from chartit import DataPool, Chart

from profiles.models import Profile, FriendList, GymStatus
from profiles.forms import ProfileForm, FriendsForm
from profiles.declarators import swtLoginReq

from workouts.models import Workout, FilterPreference
from workouts.forms import graphrequestform


@swtLoginReq
def home(request):
	user = request.user.username
	user_exists = Profile.objects.filter(username=user)
	user_profile = Profile.objects.filter(username=user, completed=False)
	
	# Verify if New User
	if user_exists.count() < 1:
		profile = Profile(username=user)
		user_prefs = FilterPreference(username=user)
		profile.save()
		user_prefs.save()
		
		return HttpResponseRedirect('/swt/profiles/new/')
	# Verify if Incomplete User Profile
	elif user_profile.count() > 0:
		return HttpResponseRedirect('/swt/profiles/new/')
	else:
		profile = Profile.objects.get(username=user)    
  
	args = {}
	args.update(csrf(request))
	args['profile'] = profile

    # WORKOUTS ARGUMENTS
	args['workouts'] = Workout.objects.filter(username=user).order_by('-date')[0:5]

    # FRIENDLIST ARGUMENTS
	args['friends_accepted'] = FriendList.objects.filter(sender_id=user, accepted=True).order_by('receiver_id')
	args['friends_pending'] = FriendList.objects.filter(sender_id=user, accepted=False)
	args['friends_request'] = FriendList.objects.filter(receiver_id=user, accepted=False)
	args['friends_form'] = FriendsForm()
	
	# GYMSTATUS ARGUMENTS
	args['gym_status'] = GymStatus.objects.all()
	
	args['curr_weekday'] = strftime("%A")
	args['curr_hour'] = strftime("%H")
	

	return render_to_response('home-index.html', args)


@swtLoginReq
def myProfile(request):
	user = request.user.username

	args = {}
	args['profile'] = Profile.objects.get(username=user)
	args['user_auth'] = User.objects.get(username=user)
	args['my_chest_workouts'] = Workout.objects.filter(username=user, weights_type='CHEST').count()
	args['my_legs_workouts'] = Workout.objects.filter(username=user, weights_type='LEGS').count()
	args['my_back_workouts'] = Workout.objects.filter(username=user, weights_type='BACK').count()
	args['my_treadmill_workouts'] = Workout.objects.filter(username=user, cardio_type='TREADMILL').count()
	args['my_stairs_workouts'] = Workout.objects.filter(username=user, cardio_type='STAIRS').count()
	args['my_rowing_workouts'] = Workout.objects.filter(username=user, cardio_type='ROWING').count()
	today = datetime.date.today()

	form = graphrequestform()
	args.update(csrf(request))
	args['chartform'] = form


	weightworkoutdata = \
		DataPool(
			series =
				[{'options': {
					'source': Workout.objects.filter(username=user, weights_type='CHEST', month=today.month )},
						'terms': [
						{'day_chest': 'day'},
						{'Chest Weight': 'weight'}]},

					{'options': {
						'source': Workout.objects.filter(username=user, weights_type='LEGS', month=today.month )},
						'terms': [
						{'day_legs': 'day'},
						{'Legs Weight': 'weight'}]},

					{'options': {
						'source': Workout.objects.filter(username=user, weights_type='BACK', month=today.month )},
						'terms': [
						{'day_back': 'day'},
						{'Back Weight': 'weight'}]},
					])

	weightworkoutchart = Chart(
		datasource = weightworkoutdata,
			series_options =
				[{'options':{
				'type': 'column',
				'stacking': False},
				'terms': {
					'day_chest': [
						'Chest Weight'],
					'day_legs': [
						'Legs Weight'],
					'day_back': [
						'Back Weight'],
					}}],
			chart_options =
				{'title': {
					'text': ' '},
				'xAxis': {
					'title': {
						'text': 'Weights by Day'}}})

	cardioworkoutdata = \
		DataPool(
			series =
				[{'options': {
					'source': Workout.objects.filter(username=user, cardio_type='TREADMILL', month = today.month )},
					'terms': [
					{'day_treadmill': 'day'},
					{'Treadmill Duration': 'time'}]},

				{'options': {
					'source': Workout.objects.filter(username=user, cardio_type='STAIRS', month = today.month )},
					'terms': [
					{'day_stairs': 'day'},
					{'Stairs Duration': 'time'}]},

				{'options': {
					'source': Workout.objects.filter(username=user, cardio_type='ROWING', month = today.month )},
					'terms': [
					{'day_rowing': 'day'},
					{'Rowing Duration': 'time'}]},
				])

	cardioworkoutchart = Chart(
		datasource = cardioworkoutdata,
			series_options =
				[{'options':{
					'type': 'column',
					'stacking':False},
						'terms': {
							'day_treadmill': [
								'Treadmill Duration'],
							'day_stairs': [
								'Stairs Duration'],
							'day_rowing': [
								'Rowing Duration'],
							}}],
			chart_options =
			{'title': {
				'text': ' '},
			'xAxis': {
				'title': {
					'text':  'Workout Duration by Day'}}})

	
	charts = [cardioworkoutchart, weightworkoutchart]
	args['charts'] = charts
	args['cur_month'] = today.strftime('%B')
	
	# Profile Image hash
	signer = Signer()
	img_hash = signer.sign('p-img-' + user)
	args['img_hash'] = img_hash

	return render_to_response('profiles-index.html', args)


@swtLoginReq
def newProfile(request):
	user = request.user.username
	user_profile = Profile.objects.filter(username=user, completed=True)

	# Check if logged in user already has a completed profile
	if user_profile.count() > 0:
		return HttpResponseRedirect('/swt/')

	profile = Profile.objects.get(username=user)

	if request.POST:
		form = ProfileForm(request.POST, instance=profile)
			
		if form.is_valid():
			form.save()
			
			# Create hash name for profile image
			signer = Signer()
			img_hash = signer.sign('p-img-' + user)
		
			data = form.cleaned_data
			
			if data['profile_pic'] == '':
				folder = '/home/phoenix470/swt/media/static/assets/uploaded_files'
				imgurl = 'http://terryshoemaker.files.wordpress.com/2013/03/placeholder1.jpg'
				urllib.urlretrieve(imgurl, folder + '/' + img_hash + '.jpg')
			else:
				folder = '/home/phoenix470/swt/media/static/assets/uploaded_files'
				imgurl = data['profile_pic']
				urllib.urlretrieve(imgurl, folder + '/' + img_hash + '.jpg')
				
			profile.completed = True
			profile.save()

			return HttpResponseRedirect('/swt/')
	else:
		form = ProfileForm()

	args = {}
	args.update(csrf(request))
	
	args['form'] = form

	return render_to_response('profile-new.html', args)


@swtLoginReq
def editProfile(request):
	user = request.user.username
	profile = Profile.objects.get(username=user)

	if request.POST:
		form = ProfileForm(request.POST, request.FILES, instance=profile)
		
		if form.is_valid():
			form.save()
			
			# create hash name for profile image
			signer = Signer()
			img_hash = signer.sign('p-img-' + user)
			
			data = form.cleaned_data
			
			if data['profile_pic'] == '':
				folder = '/home/phoenix470/swt/media/static/assets/uploaded_files'
				imgurl = 'http://terryshoemaker.files.wordpress.com/2013/03/placeholder1.jpg'
				urllib.urlretrieve(imgurl, folder + '/' + img_hash + '.jpg')
			else:
				folder = '/home/phoenix470/swt/media/static/assets/uploaded_files'
				imgurl = data['profile_pic']
				urllib.urlretrieve(imgurl, folder + '/' + img_hash + '.jpg')
			
			return HttpResponseRedirect('/swt/profiles/')

	else:
		form = ProfileForm(instance=profile)

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('profile-edit.html', args)


@swtLoginReq
def requestFriend(request):
	user = request.user.username

	if request.POST:
		friend_request = FriendList(sender_id=user)
		form = FriendsForm(request.POST, instance=friend_request)
		if form.is_valid():
			data = form.cleaned_data
			receiver_id = data['receiver_id']
			
			# Check if User exists
			requested_user = Profile.objects.filter(username=receiver_id)
			request_check = FriendList.objects.filter(sender_id=user, receiver_id=receiver_id)
			friend_check = FriendList.objects.filter(sender_id=receiver_id, receiver_id=user)
			
			if (requested_user.count() < 1 or request_check.count() >= 1 or friend_check.count() >= 1):
				# Send to User A;ready Requested
				return HttpResponseRedirect('/swt/')
			else:
				form.save()

	return HttpResponseRedirect('/swt/')


@swtLoginReq
def acceptFriend(request, friend_id):
	user = request.user.username
	friend_request = FriendList.objects.get(sender_id=friend_id, receiver_id=user, accepted=False)
    
	if friend_request != None:
		friend_request.accepted = True
		friend_request.save()
	
	friend_new = FriendList(sender_id=user, receiver_id=friend_id, accepted=True)
	friend_new.save()
	
	return HttpResponseRedirect('/swt/')


@swtLoginReq
def declineFriend(request, friend_id):
    user = request.user.username
    friend_request = FriendList.objects.get(sender_id=friend_id, receiver_id=user, accepted=False)
    if friend_request != None:
		friend_request.delete()

    return HttpResponseRedirect('/swt/')


@swtLoginReq
def deleteFriend(request, friend_id):
	user = request.user.username
	friend_del1 = FriendList.objects.get(sender_id=user, receiver_id=friend_id, accepted=True)
	friend_del2 = FriendList.objects.get(sender_id=friend_id, receiver_id=user, accepted=True)

	if friend_del1 != None:
		friend_del1.delete()
	if friend_del2 != None:
		friend_del2.delete()

	return HttpResponseRedirect('/swt/')


@swtLoginReq
def viewFriend(request, friend_id):
	user = request.user.username
	
	friend = FriendList.objects.get(sender_id=user, receiver_id=friend_id, accepted=True)

	if friend != None:
		friend_profile = Profile.objects.get(username=friend_id)
		
		
		args = {}
		args['profile'] = friend_profile
		args['user_auth'] = User.objects.get(username=friend_id)
		
		# Friend WORKOUT Arguments
		args['my_chest_workouts'] = Workout.objects.filter(username=friend_id, weights_type='CHEST').count()
		args['my_legs_workouts'] = Workout.objects.filter(username=friend_id, weights_type='LEGS').count()
		args['my_back_workouts'] = Workout.objects.filter(username=friend_id, weights_type='BACK').count()
		args['my_treadmill_workouts'] = Workout.objects.filter(username=friend_id, cardio_type='TREADMILL').count()
		args['my_stairs_workouts'] = Workout.objects.filter(username=friend_id, cardio_type='STAIRS').count()
		args['my_rowing_workouts'] = Workout.objects.filter(username=friend_id, cardio_type='ROWING').count()
		today = datetime.date.today()
		
		weightworkoutdata = \
			DataPool(
				series =
					[{'options': {
						'source': Workout.objects.filter(username=friend_id, weights_type='CHEST', month=today.month )},
							'terms': [
							{'day_chest': 'day'},
							{'Chest_Weight': 'weight'}]},

						{'options': {
							'source': Workout.objects.filter(username=friend_id, weights_type='LEGS', month=today.month )},
							'terms': [
							{'day_legs': 'day'},
							{'Legs_Weight': 'weight'}]},

						{'options': {
							'source': Workout.objects.filter(username=friend_id, weights_type='BACK', month=today.month )},
							'terms': [
							{'day_back': 'day'},
							{'Back_Weight': 'weight'}]},
						])

		weightworkoutchart = Chart(
			datasource = weightworkoutdata,
				series_options =
					[{'options':{
					'type': 'column',
					'stacking': False},
					'terms': {
						'day_chest': [
							'Chest_Weight'],
						'day_legs': [
							'Legs_Weight'],
						'day_back': [
							'Back_Weight'],
						}}],
				chart_options =
					{'title': {
						'text': ' '},
					'xAxis': {
						'title': {
							'text': 'Weights by Day'}}})

		cardioworkoutdata = \
			DataPool(
				series =
					[{'options': {
						'source': Workout.objects.filter(username=friend_id, cardio_type='TREADMILL', month = today.month )},
						'terms': [
						{'day_treadmill': 'day'},
						{'Treadmill_Duration': 'time'}]},

					{'options': {
						'source': Workout.objects.filter(username=friend_id, cardio_type='STAIRS', month = today.month )},
						'terms': [
						{'day_stairs': 'day'},
						{'Stairs_Duration': 'time'}]},

					{'options': {
						'source': Workout.objects.filter(username=friend_id, cardio_type='ROWING', month = today.month )},
						'terms': [
						{'day_rowing': 'day'},
						{'Rowing_Duration': 'time'}]},
					])

		cardioworkoutchart = Chart(
			datasource = cardioworkoutdata,
				series_options =
					[{'options':{
						'type': 'column',
						'stacking':False},
							'terms': {
								'day_treadmill': [
									'Treadmill_Duration'],
								'day_stairs': [
									'Stairs_Duration' ],
								'day_rowing': [
									'Rowing_Duration' ],
								}}],
				chart_options =
				{'title': {
					'text': 'Cardio Workouts'},
				'xAxis': {
					'title': {
						'text':  'Workout Duration by Day'}}})

		
		charts = [cardioworkoutchart, weightworkoutchart]
		args['charts'] = charts
		args['cur_month'] = today.strftime('%B')

		signer = Signer()
		img_hash = signer.sign('p-img-' + friend_id)
		args['img_hash'] = img_hash

		return render_to_response('profile-friend.html', args)
		
	# ADD ELSE THAT REDIRECTS TO ERROR
	else:
		return HttpResponseRedirect('/swt/')


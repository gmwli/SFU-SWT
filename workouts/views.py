import os
from django.shortcuts import render_to_response
from workouts.models import Workout, FilterPreference
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from chartit import DataPool, Chart, PivotDataPool, PivotChart
from django.http import HttpResponse
from workouts.forms import AddWorkoutForm, CommunityStatsForm, graphrequestform
from django.db.models import Count, Avg, Sum
from profiles.declarators import swtLoginReq
import calendar

# View for WORKOUT TRACKER
@swtLoginReq
def workoutsummary(request, page_id=1):
	user = request.user.username
	workouts = Workout.objects.filter(username=user).order_by('-date')
	
	per_page = 10
	total_pages = (workouts.count() / per_page) + 1
	total_pages = (total_pages - 1) if (workouts.count() % per_page == 0) else total_pages
	page_list = []

	for i in range(1,total_pages+1):
		page_list.append(i)

	index_low = per_page * (int(page_id)-1)
	index_high = per_page * int(page_id)
	workouts = Workout.objects.filter(username=user).order_by('-date')[index_low:index_high]
	
	#process form post - adds a new workout to user's workouts
	if request.POST:
		new_workout = Workout(username=user)
		form = AddWorkoutForm(request.POST, instance=new_workout)
		
		if form.is_valid():
			data = form.cleaned_data
			
			form.save()
			
			if (data['style'] == 'Cardio Workout'):
				new_workout.weights_type = ''
			elif (data['style'] == 'Weights Workout'):
				new_workout.cardio_type = ''

			day = data['date'].day
			month = data['date'].month
			new_workout.day = day
			new_workout.month = month
			new_workout.save()

			return HttpResponseRedirect('/swt/workouts/')
	
	#load the form if it isn't a post
	else:
		form = AddWorkoutForm()

	#set values for rendering
	args = {}
	args.update(csrf(request))
	args['form'] = form
	args['workouts'] = workouts
	args['page_list'] = page_list
	args['page_id'] = page_id
	
	return render_to_response('workouts-index.html', args)

	
# View for COMMUNITY STATS
@swtLoginReq
def communityStats(request):
	user = request.user.username
	user_prefs = FilterPreference.objects.get(username=user)
	
	#Request form for FILTERED statistics
	if request.POST:
		form = CommunityStatsForm(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect('/swt/workouts/community/')

	has_cardio_workouts = False;
	has_weights_workouts = False;
	args = {}
	charts = {}
	# Arguments for TOPLIST CARDIO & WEIGHTS
	toplist = {}
	
	#set arguements when there a user has workouts in their database
	if Workout.objects.filter().count() != 0:
		
		if Workout.objects.filter(style='Cardio Workout').count() != 0:
			has_cardio_workouts = True
			toplist['top_cardio_type'] = Workout.objects.filter(style='Cardio Workout').values('cardio_type').annotate(workout_count=Count('id')).order_by('-workout_count')[0]
			toplist['top_cardio_speed'] = Workout.objects.filter(style='Cardio Workout').order_by('-speed')[0]
			toplist['top_cardio_duration'] = Workout.objects.filter(style='Cardio Workout').order_by('-time')[0]
		
		if Workout.objects.filter(style='Weights Workout').count() != 0:
			has_weights_workouts = True
			toplist['top_weights_type'] = Workout.objects.filter(style='Weights Workout').values('weights_type').annotate(workout_count=Count('id')).order_by('-workout_count')[0]
			toplist['top_weights_weight'] = Workout.objects.filter(style='Weights Workout').order_by('-weight')[0]
			toplist['top_weights_sets'] = Workout.objects.filter(style='Weights Workout').order_by('-sets')[0]
			toplist['top_weights_reps'] = Workout.objects.filter(style='Weights Workout').order_by('-reps')[0]
	
		args['toplist'] = toplist

	
		# Arguments for GOOGLE CHARTS
		args['all_treadmill_workouts'] = Workout.objects.filter(cardio_type='TREADMILL').count()
		args['all_stairs_workouts'] = Workout.objects.filter(cardio_type='STAIRS').count()
		args['all_rowing_workouts'] = Workout.objects.filter(cardio_type='ROWING').count()
		args['all_chest_workouts'] = Workout.objects.filter(weights_type='CHEST').count()
		args['all_legs_workouts'] = Workout.objects.filter(weights_type='LEGS').count()
		args['all_back_workouts'] = Workout.objects.filter(weights_type='BACK').count()
	
		# Arguments for CHARTIT
		all_weightworkoutdata = \
			DataPool(
				series =
					[{'options': {
						'source': Workout.objects.filter(weights_type='CHEST')},
							'terms': [
							{'day_chest': 'day'},
							{'Chest Weight': 'weight'}]},

						{'options': {
							'source': Workout.objects.filter(weights_type='LEGS')},
							'terms': [
							{'day_legs': 'day'},
							{'Legs Weight': 'weight'}]},

						{'options': {
							'source': Workout.objects.filter(weights_type='BACK')},
							'terms': [
							{'day_back': 'day'},
							{'Back Weight': 'weight'}]},
						])

		all_weightworkoutchart = Chart(
			datasource = all_weightworkoutdata,
				series_options =
					[{'options':{
					'type': 'column',
					'stacking': False},
					'terms': {
						'day_chest': [
							'Chest Weight'],
						'day_legs':[
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
		
		all_cardioworkoutdata = \
			DataPool(
				series =
					[{'options': {
						'source': Workout.objects.filter(cardio_type='TREADMILL')},
						'terms': [
						{'day_treadmill': 'day'},
						{'Treadmill Duration': 'time'}]},
	
					{'options': {
						'source': Workout.objects.filter(cardio_type='STAIRS')},
						'terms': [
						{'day_stairs': 'day'},
						{'Stairs Duration': 'time'}]},
	
					{'options': {
						'source': Workout.objects.filter(cardio_type='ROWING')},
						'terms': [
						{'day_rowing': 'day'},
						{'Rowing Duration': 'time'}]},
					])

		all_cardioworkoutchart = Chart(
			datasource = all_cardioworkoutdata,
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

	charts = [all_cardioworkoutchart, all_weightworkoutchart]
	
	args['has_cardio_workouts'] = has_cardio_workouts
	args['has_weights_workouts'] = has_weights_workouts
	args['charts'] = charts
	
	return render_to_response('community_stats.html', args)

#view for request of personal workout chart base on month
@swtLoginReq
def personalworkoutchart(request):
	user = request.user.username
	
	#when there is a post - render the request chart for the user
	if request.POST:
		form = graphrequestform(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			monthint = int(data['month'])
			titlestring = 'Workouts for the Month of %s' % calendar.month_name[monthint]

			#set output based on workout chart style requested (weight style)
			if data['style'] == 'Weights Workout':
				
				#set chartit values
				workoutdata = \
					DataPool(
						series =
							[{'options': {
								'source': Workout.objects.filter(username=user, weights_type='CHEST', month=data['month'] )},
								'terms': [
								{'day_chest': 'day'},
								{'Chest Weight': 'weight'}]},

							{'options': {
								'source': Workout.objects.filter(username=user, weights_type='LEGS', month=data['month'] )},
								'terms': [
								{'day_legs': 'day'},
								{'Legs Weight': 'weight'}]},

							{'options': {
								'source': Workout.objects.filter(username=user, weights_type='BACK', month=data['month'] )},
								'terms': [
								{'day_back': 'day'},
								{'Back Weight': 'weight'}]},
							])
				#more chartit valued
				cht = Chart(
					datasource = workoutdata,
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
							'text': titlestring },
						'xAxis': {
							'title': {
								'text': 'Weights by Day'}}})

				return render_to_response('chart.html', {'workoutchart':cht})
			
			#set workout type based on cardio type
			else:

				#set chartit values
				workoutdata = \
					DataPool(
						series =
							[{'options': {
								'source': Workout.objects.filter(username=user, cardio_type='TREADMILL', month = data['month'] )},
								'terms': [
								{'day_treadmill': 'day'},
								{'Treadmill Duration': 'time'}]},

							{'options': {
								'source': Workout.objects.filter(username=user, cardio_type='STAIRS', month = data['month'] )},
								'terms': [
								{'day_stairs': 'day'},
								{'Stairs Duration': 'time'}]},

							{'options': {
								'source': Workout.objects.filter(username=user, cardio_type='ROWING', month = data['month'] )},
								'terms': [
								{'day_rowing': 'day'},
								{'Rowing Duration': 'time'}]},
							])

				cht = Chart(
					datasource = workoutdata,
						series_options =
							[{'options':{
								'type': 'column',
								'stacking':False},
								'terms': {
									'day_treadmill': [
										'Treadmill Duration'],
									'day_stairs': [
										'Stairs Duration' ],
									'day_rowing': [
										'Rowing Duration' ],
									}}],
						chart_options =
						{'title': {
							'text': titlestring},
						'xAxis': {
							'title': {
								'text':  'Workout Duration by Day'}}})
				return render_to_response('chart.html', {'workoutchart':cht})
	
	#if the user didn't post, set the form 
	else:
		form = graphrequestform()
		args = {}
		args.update(csrf(request))
		args['form'] = form
		return render_to_response('requestworkout.html', args)



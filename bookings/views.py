import os
from django.shortcuts import render, render_to_response
from bookings.models import Bookings
from django.core.context_processors import csrf
from bookings.forms import AddBookingForm ,DeleteBookingsForm , AddBookingFormTomorrow
import datetime
from django.http import HttpResponseRedirect , HttpResponse
from profiles.declarators import swtLoginReq
from time import strftime
from datetime import timedelta

# Create your views here.

@swtLoginReq
def BookMachine(request):
    #query everything that it is available to use today during the whole day until gym closes. assume it clos$
    #everything is done ine simple 24 hours format so 1 is 1 am 13 is 1 pm ...
    #select current date #year month day
    curr_date=datetime.datetime.now()
    today=curr_date.strftime("%Y-%m-%d")
    tmr_date=datetime.datetime.today()+timedelta(days=1)
    tomorrow=tmr_date.strftime("%Y-%m-%d")
    time=strftime("%H")
    sfu_id=request.user.username
    multi_book=""
    if request.POST:
	#'id_machine_name' is passed via the form
	new_booking = Bookings(machine_name='id_machine_name',booked_date=today, username=sfu_id)
	form = AddBookingForm(request.POST, instance=new_booking)#try to add the bookings for today
	booked_time=""
  	if form.is_valid():
	    data = form.cleaned_data
	    if(data['machine_name']=='rowing'):
	        booked_time=data['rowing_time']

	    elif(data['machine_name']=='treadmill'):
	        booked_time=data['treadmill_time']

	    elif(data['machine_name']=='stairs'):
		booked_time=data['stairs_time']
	   
	    new_booking.booked_time=booked_time  
	    #check that user hasnt previoulsy booked that machine
	    booked_check=Bookings.objects.filter(machine_name=data['machine_name'],booked_date=today,username=sfu_id,booked_time=booked_time)

	    if(booked_check.count()>0):
	        return HttpResponseRedirect('/swt/bookings/')
	    else:	

	        form.save()

	        return HttpResponseRedirect('/swt/bookings/')

    else:
        form_today= AddBookingForm()	
	form_tomorrow=AddBookingFormTomorrow()	
    args={}
    args.update(csrf(request))
 
    #query database see what the user has booked for today
    my_bookings= Bookings.objects.filter(booked_date=today,username=sfu_id).order_by('booked_time')
    #assume that there are 2  machines of each type at the gym and we have to calculate how many machines are booked for each time
    fully_booked_treadmill=Bookings.fully_booked_arr(today,'treadmill')
    fully_booked_rowing=Bookings.fully_booked_arr(today,'rowing')
    fully_booked_stairs=Bookings.fully_booked_arr(today,'stairs')

    #now do the same types of query's but for tomorrow's date
    my_bookings_tmr=Bookings.objects.filter(booked_date=tomorrow,username=sfu_id).order_by('booked_time')
    #assume there are 2 machines of each time, if wished change number in the model function
    fully_booked_treadmill_tmr=Bookings.fully_booked_arr(tomorrow,'treadmill')
    fully_booked_rowing_tmr=Bookings.fully_booked_arr(tomorrow,'rowing')
    fully_booked_stairs_tmr=Bookings.fully_booked_arr(tomorrow,'stairs')
    #we may not need THIS
    booked_times_treadmill = []
    booked_times_stairs = []
    booked_times_rowing = []
    # The Default Index to start with in Booking Time Dropdown
    default_t_index = 6
    default_s_index = 6
    default_r_index = 6
    #tomorrows indexes
    default_t_index_tmr=6
    default_s_index_tmr=6
    default_r_index_tmr=6
    
    #calculatin the indexes for today
    default_t_index=default_t_index + Bookings.get_delta_index(fully_booked_treadmill)
    default_s_index=default_s_index + Bookings.get_delta_index(fully_booked_stairs)
    default_r_index=default_r_index + Bookings.get_delta_index(fully_booked_rowing)      
    #calculatin the index for tomorrow
    default_t_index_tmr=default_t_index_tmr+ Bookings.get_delta_index(fully_booked_treadmill_tmr)
    default_s_index_tmr=default_s_index_tmr+ Bookings.get_delta_index(fully_booked_stairs_tmr)
    default_r_index_tmr=default_r_index_tmr+ Bookings.get_delta_index(fully_booked_rowing_tmr)

    args['form_today'] = form_today
    args['booked_times_treadmill'] = booked_times_treadmill
    args['booked_times_stairs'] = booked_times_stairs
    args['booked_times_rowing'] = booked_times_rowing
    args['default_t_index'] = default_t_index
    args['default_s_index'] = default_s_index
    args['default_r_index'] = default_r_index 
    args['fully_booked_treadmill']=fully_booked_treadmill
    args['fully_booked_stairs']=fully_booked_stairs
    args['fully_booked_rowing']=fully_booked_rowing
    args['my_bookings']=my_bookings
    args['time']=int(time)
    #tomorrow variables and related 
    args['tomorrow']=tomorrow
    args['form_tomorrow']=form_tomorrow
    args['my_bookings_tmr']=my_bookings_tmr
    return render_to_response('bookmachine.html',args)

@swtLoginReq
def UnbookMachine(request,machine_name,booked_date,booked_time):
    sfu_id=request.user.username
    #convert the yearmonthday to good formated date
    fmt_date=str(booked_date[:4])+'-'+str(booked_date[4:6])+'-'+str(booked_date[6:8])
    booked_machine= Bookings.objects.get(machine_name=machine_name,booked_date=fmt_date,booked_time=booked_time,username=sfu_id)    
    #return HttpResponse(machine_name +fmt_date+sfu_id+ booked_time)
    # if booked_machine!=None:
    booked_machine.delete()
    return HttpResponseRedirect('/swt/bookings')



@swtLoginReq
def BookMachineTmr(request):
    #this function will only be called when we book machines for tomorrow this is a POST
    tmr_date=datetime.datetime.today()+timedelta(days=1)
    tomorrow=tmr_date.strftime("%Y-%m-%d")
    sfu_id=request.user.username
    if request.POST:
        #'id_machine_name' is passed via the form
        new_booking_tmr = Bookings(machine_name='id_machine_name',booked_date=tomorrow, username=sfu_id)
        form = AddBookingFormTomorrow(request.POST, instance=new_booking_tmr)#try to add the bookings for today
        booked_time=""
        if form.is_valid():
            data = form.cleaned_data
            if(data['machine_name_tmr']=='rowing'):
                booked_time=data['rowing_time_tmr']

            elif(data['machine_name_tmr']=='treadmill'):
                booked_time=data['treadmill_time_tmr']

            elif(data['machine_name_tmr']=='stairs'):
                booked_time=data['stairs_time_tmr']

            new_booking_tmr.booked_time=booked_time
	    new_booking_tmr.machine_name=data['machine_name_tmr']
            #check that user hasnt previoulsy booked that machine
            booked_check=Bookings.objects.filter(machine_name=data['machine_name_tmr'],booked_date=tomorrow,username=sfu_id,booked_time=booked_time)

            if(booked_check.count()>0):
                return HttpResponseRedirect('/swt/bookings/')
            else:

                form.save()

                return HttpResponseRedirect('/swt/bookings/')
    else:
	return HttpResponseRedirect('/swt/bookings')














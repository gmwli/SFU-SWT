from django.db import models
from datetime import datetime


# Create your models here.
class Bookings(models.Model):
    machine_name=models.CharField(max_length=50)
    booked_date=models.DateField()
    booked_time=models.CharField(max_length=2)
    username=models.CharField(max_length=50)    
    
    @classmethod
    def create_range(self, avail_times):
	formated=[]
	for i in range(len(avail_times)):
            startrange_val=avail_times[i]
            formated.append(startrange_val)
            formated.append(startrange_val+1)
        return formated

    @classmethod
    def format_range(self, avail_times):
	formated=[]
	for i in range(0,len(avail_times),2):
            formated.append(str(avail_times[i])+":00"+ "-"+str(avail_times[i+1])+":00")
        return formated

    @classmethod
    def get_delta_index(self, booked_times):
	i=0
	while (booked_times[i]==1):
            i=i+1
        return i

    @classmethod
    #returns an array with possitins where pos 0 is 6am 
    #if value at pos is 1 that means that at that time everythingis fully booked
    def fully_booked_arr(self,booked_date,machine_name):
	result=[0]*15
	total_machines=0
	if(machine_name=='stairs'):
            temp= Machines.objects.get(machine_name='stairs')
	    total_machines=temp.available
	elif(machine_name=='treadmill'):
	    temp= Machines.objects.get(machine_name='treadmill')
	    total_machines=temp.available
	else:
	    temp= Machines.objects.get(machine_name='rowing')
	    total_machines=temp.available

        for time in range(6,21):
	    if(Bookings.objects.filter(booked_date=booked_date,machine_name=machine_name,booked_time=time).count()>=total_machines):
	        result[time-6]=1
        return result

class Machines(models.Model):
      machine_name=models.CharField(max_length=20)
      available=models.IntegerField()

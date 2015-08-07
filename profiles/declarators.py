from django.http import HttpResponseRedirect

def swtLoginReq(function):
	def wrapper(request, *args, **kw):
		user = request.user
		if not (user.id):
			return HttpResponseRedirect('/swt/login/')
		else:
			return function(request, *args, **kw)

	return wrapper

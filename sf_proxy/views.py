
import urllib
import httplib

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import  csrf_exempt

from models import AccessLog

def save_access(request_meta, response, ip):
	try:
		AccessLog(request_meta=request_meta, response=response, ip=ip).save()
	except:
		pass

@csrf_exempt
def proxy_tunnel(request, *args, **kwargs):
	path = request.get_full_path()
		
	if settings.TARGET_PORT == 443:
		connector = httplib.HTTPSConnection
	else:
		connector = httplib.HTTPConnection

	connection = connector(settings.TARGET_HOST, settings.TARGET_PORT)
	# TODO headers
	connection.request(request.method, path, body=request.body)

	target_resp = connection.getresponse()

	response = HttpResponse()	
	response.status_code = target_resp.status
	response.reason_phrase = target_resp.reason
		
	for header_name, value in target_resp.getheaders():
		response[header_name] = value
	
	resp_body = target_resp.read()
	response.write(resp_body)

	save_access(request_meta=str(request.META), response=resp_body, ip=request.get_host())
	
	return response


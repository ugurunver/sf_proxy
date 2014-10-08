
import os
import urllib
import httplib
from uuid import uuid4

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import  csrf_exempt

from models import AccessLog

def save_access(request_meta, response, ip):
	try:
		AccessLog(request_meta=request_meta, response=response, ip=ip).save()
	except:
		pass

def save_to_file(data):
	name = str(uuid4()).upper()

	# benzersiz uuid bulana kadar donecek
	while name in os.listdir(settings.LOG_DIR):
		name = str(uuid4()).upper()

	path = os.path.join(settings.LOG_DIR, name)
	try:
		with open(path,"wb") as _file:
			_file.write(data)
	except Exception as ex:
		pass


@csrf_exempt
def proxy_tunnel(request, *args, **kwargs):
	path = request.get_full_path()
	request_body = request.body

	if settings.TARGET_PORT == 443:
		connector = httplib.HTTPSConnection
	else:
		connector = httplib.HTTPConnection

	connection = connector(settings.TARGET_HOST, settings.TARGET_PORT)
	# TODO headers
	connection.request(request.method, path, body=request_body)

	target_resp = connection.getresponse()

	response = HttpResponse()	
	response.status_code = target_resp.status
	response.reason_phrase = target_resp.reason
		
	for header_name, value in target_resp.getheaders():
		response[header_name] = value
	
	resp_body = target_resp.read()
	response.write(resp_body)

	save_access(request_meta=str(request.META), response=resp_body, ip=request.get_host())
	save_to_file(request_body)
	
	return response


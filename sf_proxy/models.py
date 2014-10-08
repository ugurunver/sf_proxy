
from django.db import models 

class AccessLog(models.Model):
	ip = models.CharField(max_length=50)
	request_meta = models.TextField()
	response = models.TextField()
	req_time = models.DateTimeField(auto_now_add=True)
	
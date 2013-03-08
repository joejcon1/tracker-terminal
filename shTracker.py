#/usr/bin/python
import hashlib
import urllib
import urllib2
import json
import simplejson
from simplejson.compat import StringIO
import sys
import md5
#CLASSES
class User(object):
    def __init__(self, first_name, last_name, username, picture_url, email, id):
        self.firstName = first_name
        self.lastName = last_name
        self.username = username
        self.pictureUrl = picture_url
        self.email = email
        self.id = id

class Project(object):
    def __init__(self, code,description, id, name):
        self.code = code
        self.description = description
        self.id = id
        self.name = name
class Task(object):
    def __init__(self, code, id, status, task, estimate, project):
        self.code = code
        self.id = id
        self.status = status
        self.task = task
        self.estimate = estimate
        self.project = project

_BASEURL = 'http://dev.letolab.com:8000/api/'

#JSON
def project_decoder(obj):
    return Project(obj['code'], obj['description'], obj['id'], obj['name'])    
def user_decoder(obj):
    return User(obj['first_name'], obj['last_name'], obj['username'], obj['picture_url'], obj['email'], obj['id'])
def task_decoder(obj, project):
    return Task(obj['number'], obj['id'], obj['status'], obj['task'], obj['estimation'], project)
# METHODS

def getAuth():
	return 'api_id=' + urllib.quote(sys.argv[1]) +'&api_key=' + md5.new((sys.argv[2])).hexdigest()

def getProjects():
	url = _BASEURL + 'projects?' + getAuth() 
	response = makeAPICall(url)
	project_json_list = json.load(StringIO(response))
	project_list = []
	for p in project_json_list:
		# print p['code']
		project = project_decoder(p)
		project_list.append(project)
	return project_list

def makeAPICall(url):
	response = urllib2.urlopen(url).read()
	return response

def login():
	url = _BASEURL + 'login?' + getAuth() 
	print url
	response = makeAPICall(url)
	user = json.loads(response, object_hook=user_decoder)

	print 'logged in as '  + user.username
	return response
	
def getProject(code):
	project_list = getProjects()
	current_project = None
	for p in project_list:
		if p.code == code:
			current_project = p
	url = _BASEURL + 'tasks?' + getAuth() + '&project_id=' + current_project.id 
	response = makeAPICall(url)
	# print response
	task_json_list = json.load(StringIO(response))
	task_list = []
	for t in task_json_list:
		task = task_decoder(t, current_project)
		task_list.append(task)

	color_new = '1;34'
	color_ready = '00;31'
	color_active = '1;33'
	color_resolved = '00;32'
	color_restore = '\33[00m'
	#print new tasks
	print '#######NEW#######'
	for t in task_list:
		if t.status == 'new':
			print '\33['+color_new+'m' + t.project.code + ' ' + str(t.code) + ':\t ' +  t.task + color_restore
	#print ready tasks
	print '#######ready#######'
	for t in task_list:
		if t.status == 'ready':
			print '\33['+color_ready+'m' + t.project.code + '-' + str(t.code) + ':\t ' +  t.task + color_restore
	#print active tasks
	print '#######active#######'
	for t in task_list:
		if t.status == 'active':
			print '\33['+color_active+'m' + t.project.code + '-' + str(t.code) + ':\t ' +  t.task + color_restore
	#print resolved tasks
	print '#######resolved#######'
	for t in task_list:
		if t.status == 'resolved':
			print '\33['+color_resolved+'m' + t.project.code + '-' + str(t.code) + ':\t ' +  t.task + color_restore


def run():
	login()
	getProject(sys.argv[3])



if  __name__ =='__main__':
    run()
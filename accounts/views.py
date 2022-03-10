
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import cv2
from imutils.video import VideoStream
import pandas as pd
from dateutil import parser
import ntpath
from skvideo import io
import skvideo.io
from subprocess import Popen
from signal import SIGINT
import signal
import dataframe_image as dfi
import numpy as np
from datetime import datetime
import pandas as pd
from time import time
import urllib.request
from django.contrib.auth import authenticate, login, logout
import os
import shutil
from imutils.video import VideoStream
import tempfile
from django.contrib import messages
from .camera import VideoCamera,LiveWebCam
from time import sleep
from onvif import ONVIFCamera
import cv2
from converter import Converter
import glob
import threading
from django.contrib.auth.decorators import login_required
from django.http.response import StreamingHttpResponse
from django.http.response import HttpResponse
import asyncio, sys
import sys
import pandas as pd
import os
import threading
from sensecam_control import onvif_control
import json
import random

# Create your views here.
from .models import *
from .forms import CreateUserForm
from .filters import OrderFilter
IP="10.5.1.10"   # Camera IP address
PORT=554          # Port
USER="Admin"         # Username
PASS="sveltetech123"        # Password
ip2 = 'rtsp://Admin:sveltetech123@10.5.1.10:554/h264'

XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1
moverequest = None
ptz = None
active = False
#ffmpegPath = r"C:\Users\Shivam\Downloads\ffmpeg-N-101759-g7fc8ba9068-win64-gpl-shared-vulkan\bin\ffmpeg.exe"

#ffprobePath = r"C:\Users\Shivam\Downloads\ffmpeg-N-101759-g7fc8ba9068-win64-gpl-shared-vulkan\bin\ffprobe.exe"
#conv = Converter(ffmpegPath, ffprobePath)

def main(request):
	return render(request, 'accounts/home.html')

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	return render(request, 'accounts/dashboard.html')
def dashboard(request):
	return render(request, 'accounts/dashboard.html')
@login_required	
def video(request):
	for i in glob.glob('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\static\\video\\*.avi'):
		file_name=ntpath.basename(i)	
		os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = i, output = file_name))	
	path = "C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\static\\video"
	files = os.listdir(path)
	# defining the dest directory
	for index, file in enumerate(files):
		dest_file = path +"\\"+ str(file)
		if not os.path.exists(os.path.join(path, ''.join(["record"+str(index), '.mp4']))):
			os.rename(dest_file,os.path.join(path, ''.join(["record"+str(index), '.mp4'])))
		else:
			print("video is there")	
		
	return render(request, 'accounts/video.html')	
@login_required	
def csv_file(request):
	time_stamps=[]
	objects=[]
	df=pd.read_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\csv_file.csv')
	num_rows=df.shape[0]
	frame = df.iloc[0:num_rows,1:].values
	print(frame)
	for i in range(num_rows):
		date_and_time = frame[i][0]
		print(date_and_time)
		time_stamp=pd.to_datetime(date_and_time)
		print(time_stamp.hour)
		time_stamps.append(time_stamp)
	object_s = df.iloc[0:num_rows,0:].values
	for i in range(num_rows):
		print(object_s[i][0])
		objects.append(object_s[i][0])
	df = []
	for i in range(len(objects)):
		a=[]
		a.append(objects[i])
		a.append(time_stamps[i])
		df.append(a)    
	df = pd.DataFrame(df)
	df.rename(columns = {0:'objects'}, inplace = True)
	df.rename(columns = {1:'time_stamps'}, inplace = True)  

	df['time_hour'] = df.time_stamps.apply(lambda x: x.hour)

	df[['objects','time_hour']]


	# print(Time_stamps.dtype)
	fd = df[['objects','time_hour']]
	fd.drop_duplicates()
	fd.to_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\file_time_hour.csv', index=False)

	#for day_hour
	time_stamps=[]
	objects=[]
	df=pd.read_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\csv_file.csv')
	num_rows=df.shape[0]
	frame = df.iloc[0:num_rows,1:].values
	print(frame)
	for i in range(num_rows):
		date_and_time = frame[i][0]
		print(date_and_time)
		time_stamp=pd.to_datetime(date_and_time)
		print(time_stamp.day)
		time_stamps.append(time_stamp)
	object_s = df.iloc[0:num_rows,0:].values
	for i in range(num_rows):
		print(object_s[i][0])
		objects.append(object_s[i][0])
	df = []
	for i in range(len(objects)):
		a=[]
		a.append(objects[i])
		a.append(time_stamps[i])
		df.append(a)    
	df = pd.DataFrame(df)
	df.rename(columns = {0:'objects'}, inplace = True)
	df.rename(columns = {1:'time_stamps'}, inplace = True)  

	df['time_day'] = df.time_stamps.apply(lambda x: x.day)

	df[['objects','time_day']]


	# print(Time_stamps.dtype)
	fd = df[['objects','time_day']]
	fd.drop_duplicates()
	fd.to_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\file_time_day.csv', index=False)

	
	html = """<style>
	@import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";
	.rwd-table {
	margin: 1em 0;
	min-width: 300px;
	margin-left: auto;
	margin-right: auto;
	}
	.rwd-table tr {
	border-top: 1px solid #ddd;
	border-bottom: 1px solid #ddd;
	}
	.rwd-table th {
	display: none;
	}
	.rwd-table td {
	display: block;
	}
	.rwd-table td:first-child {
	padding-top: .5em;
	}
	.rwd-table td:last-child {
	padding-bottom: .5em;
	}
	.rwd-table td:before {
	content: attr(data-th) ": ";
	font-weight: bold;
	width: 6.5em;
	display: inline-block;
	}
	@media (min-width: 480px) {
	.rwd-table td:before {
		display: none;
	}
	}
	.rwd-table th, .rwd-table td {
	text-align: left;
	}
	@media (min-width: 480px) {
	.rwd-table th, .rwd-table td {
		display: table-cell;
		padding: .25em .5em;
	}
	.rwd-table th:first-child, .rwd-table td:first-child {
		padding-left: 0;
	}
	.rwd-table th:last-child, .rwd-table td:last-child {
		padding-right: 0;
	}
	}
	
	
	h1 {
	font-weight: normal;
	letter-spacing: -1px;
	color: #34495E;
	}
	
	.rwd-table {
	background: #34495E;
	color: #fff;
	border-radius: .4em;
	overflow: hidden;
	}
	.rwd-table tr {
	border-color: #46637f;
	}
	.rwd-table th, .rwd-table td {
	margin: .5em 1em;
	}
	@media (min-width: 480px) {
	.rwd-table th, .rwd-table td {
		padding: 1em !important;
	}
	}
	.rwd-table th, .rwd-table td:before {
	color: #dd5;
	}
		html
	{
	background-color: #48ca7c;
	}
	</style>
	<script>
	window.console = window.console || function(t) {};
	</script>
	<script>
	if (document.location.search.match(/type=embed/gi)) {
		window.parent.postMessage("resize", "*");
	}
	</script>"""
	
	df = pd.read_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\csv_file.csv')
	df.to_html("C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\templates\\accounts\\data.html")
	with open("C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\templates\\accounts\\data.html") as file:
		file = file.read()
	file = file.replace("<table ", "<table class='rwd-table'")
	with open("C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\templates\\accounts\\data.html", "w") as file_to_write:
		file_to_write.write(html + file)
	
	return render(request, 'accounts/data.html')		



def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def webcam_feed(request):
	return StreamingHttpResponse(gen(LiveWebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def camera_control(request):
	k=request.GET.get('request_data')
	#print(k)
	
	ip = '10.5.1.10'

	login = 'Admin'

	password = 'sveltetech123'


	exit_program = 0


	def event_keyboard(k):
		global exit_program
		print("this is ",k)

		if k == 27:  # esc
			exit_program = 1

		elif k == 1:
			X.relative_move(0, 0.1, 0)

		elif k == 2:
			X.relative_move(-0.1, 0, 0)

		elif k == 3:
			X.relative_move(0, -0.1, 0)

		elif k == 4:
			X.relative_move(0.1, 0, 0)

		elif k == 5:
			X.go_home_position()

		elif k == 6:
			X.relative_move(0, 0, 0.05)

		elif k == 7:
			X.relative_move(0, 0, -0.05)
		

		elif k == 8:
			X.relative_move(0, 0, -0.05)
		elif k == 9:
			X.relative_move(0, 0, 5)
		elif k == 10:
			X.relative_move(0, 0, -1)


	def capture(ip_camera):
		global exit_program

		ip2 = 'rtsp://' + login + ':' + password + '@' + ip_camera + '/h264'

		cap = cv2.VideoCapture(ip2)

		while True:
			ret, frame = cap.read()
			# print(frame)
			break
			if ret is not False:
				break

		while True:
			ret, frame = cap.read()
			'''
			if exit_program == 1:
				sys.exit()
			'''
			#cv2.imshow('Camera', frame)
			


	X = onvif_control.CameraControl(ip, login, password)
	X.camera_start()
	t = threading.Thread(target=capture, args=(ip,))
	t.start()
	
	event_keyboard(int(k))
	#return StreamingHttpResponse(gen(LiveWebCam()),
					#content_type='multipart/x-mixed-replace; boundary=frame')

def logging_info(request):
	k=request.GET.get('request_data')
	print(k)
	#k=int(k)
	
	def logging(df, class_name):
		details = {'Object': class_name, 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
		df = df.append(details, ignore_index=True)
		return df

	df = pd.DataFrame()
	# Initialise variables to store current time difference as well as previous time call value
	previous = time()
	delta = 0
	logged_ids = []
	# Load Yolo
	net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
	classes = []
	with open("dota.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	camera =VideoStream(0).start()
	
	fps = 1
	
	crf = 17
	

	# Loading video
	#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	#video_out = cv2.VideoWriter("C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\static\\video\\record.avi", fourcc, 10,  (640,480))
	video = io.FFmpegWriter('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\static\\video\\record'+str(random.randint(0,100000))+'.mp4', 
            inputdict={'-r': str(fps), '-s':'{}x{}'.format(640,480)},
            outputdict={'-r': str(fps), '-c:v': 'libx264', '-crf': str(crf), '-preset': 'ultrafast', '-pix_fmt': 'yuv444p'}
	)
	
	#time.sleep(2.0)
	# camera = cv2.VideoCapture(1)
	while True:
		img = camera.read()
		
		if True:
			height, width, channels = img.shape
			print(height,width)
			# Detecting objects
			blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
			net.setInput(blob)
			outs = net.forward(output_layers)
			
			
			# Showing informations on the screen
			class_ids = []
			confidences = []
			boxes = []
			for out in outs:
				for detection in out:
					scores = detection[5:]
					class_id = np.argmax(scores)
					confidence = scores[class_id]
					if confidence > 0.05:
						# Object detected
						center_x = int(detection[0] * width)
						center_y = int(detection[1] * height)
						w = int(detection[2] * width)
						h = int(detection[3] * height)
						# Rectangle coordinates
						x = int(center_x - w / 2)
						y = int(center_y - h / 2)
						boxes.append([x, y, w, h])
						confidences.append(float(confidence))
						class_ids.append(class_id)

						# Get the current time, increase delta and update the previous variable
						current = time()
						delta += current - previous
						previous = current

						if delta > 1:
							df = logging(df, classes[class_id])
							logged_ids = []
							logged_ids.append(classes[class_id])
							delta = 0

						if (delta < 1 and (classes[class_id] not in logged_ids)):
							df = logging(df, classes[class_id])
							logged_ids.append(classes[class_id])


			indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

			
			font = cv2.FONT_HERSHEY_PLAIN
			for i in range(len(boxes)):
				if i in indexes:
					x, y, w, h = boxes[i]
					label = str(classes[class_ids[i]])
					color = colors[i]

					cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
					cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
			
			img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)		
			#video_out.write(img)
			video.writeFrame(img)
			# key=cv2.waitKey(1) 
			# if key==int(k):
			# 	break
			
			#video_out.release()
			#cv2.imshow("Image", img)
			print("video write")
			
			df.to_csv('C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\csv_file.csv',index=False)
			dfi.export(df, 'C:\\Users\\Shivam\\Downloads\\olive\\crash-course-CRM-Part-14-User-Registration-Login-Authentication\\crm1_v14_registration_login\\accounts\\media_file\\log_of_detection.png')
	if int(k)==15:
		camera.stop()
		video.close()
	#video_out.release()
	#return StreamingHttpResponse()
					
	
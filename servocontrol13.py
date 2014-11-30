#!/usr/bin python
from subprocess import call
from time import gmtime,strftime,sleep
import os
import picamera
import io
import sys
from PIL import Image
import math,operator
import tweepy

#import numpy as np

width = 1280
heigth = 960
treshold = 20 # trigger for change detection
res1 = 100  # x resolution for compare
res2 = 75   # y resolution for compare	
trigger = 100
tweepy_codes_path="tweepy_codes.txt"
how_often_detection_test=6 #testing motion

def start():
        print("starting servo")
        os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")


        
def call_command(servo,pulsewidth):
	print("echo "+str(servo)+"="+pulsewidth+" > /dev/servoblaster")
        os.system("echo "+str(servo)+"="+pulsewidth+" > /dev/servoblaster")

def servo_adjust_plus(servo,adjust): #+10,+20
        os.system("echo "+servo+"=+"+adjust+" > /dev/servoblaster")
        print("executing:"+"echo "+servo+"=+"+adjust+" > /dev/servoblaster")

def servo_adjust_minus(servo,adjust):   
        os.system("echo "+servo+"=-"+adjust+" > /dev/servoblaster")
        print("executing:"+"echo "+servo+"=-"+adjust+" > /dev/servoblaster")
        
def kill_servos():
        os.system("sudo killall servod")
        

def servo_adjust_pct(servo,adjust):
        os.system("echo "+(servo)+"="+(adjust)+" > /dev/servoblaster")
       
def move_tilt_pct():    
        start()
        command=(raw_input("how much to move the servo 0 in pc "))
        servo_adjust_pct("0",command)
        command2=(raw_input("how much to move servo 1  in pct "))
        servo_adjust_pct("1",command2)
        kill_servos()

def move_tilt_value():
	start()
	command=(raw_input("how much to move the servo 0 in pts "))
	print(command)
	call_command(0,command)
	command=(raw_input("how much to move the servo 1 in pts "))
	call_command(1,command)
	kill_servos()

def take_a_photo(path):
        with picamera.PiCamera() as camera:
                camera.start_preview()
                sleep(5)
                camera.capture(path)
                camera.stop_preview()



#loads old picture takes a new one, compares with trshold and b/e and sends a signal
#should be the same resolution

def detect_if_move(old_path):

	p1 = Image.open(old_path) #loading pattern
	tmp = "test.jpg"
 	w,h = p1.size

	#picture.show()

	with picamera.PiCamera() as camera:  #taking new shot
		camera.resolution = (w,h)
		sleep(2)
		camera.capture(tmp)
	p2 = Image.open(tmp)	

	print("w,h %i %i" % (w,h))

	#diff = np.subtract(p1,p2)
	#total = np.sum(diff)

	h1=p1.histogram()
	h2=p2.histogram()

	rms = math.sqrt(reduce(operator.add,
		map(lambda a,b: (a-b)**2, h1,h2))/len(h1))

	return (rms,tmp)

def easy_shot(path,camera):
	camera.capture(path,resize=(1024,768))
	print"taking a picture %s \n" % path 

def shot_to_publish(path,w=1024,h=768):
	with picamera.PiCamera() as camera:  #taking new shot
		camera.resolution = (w,h)
		sleep(2)
		camera.capture(path)
		


def compare(camera):
	camera.resolution=(res1,res2)
	stream = io.BytesIO()
	camera.capture(stream,format='bmp') 
	stream.seek(0)
	im = Image.open(stream)
	buffer = im.load()
	stream.close()
	return buffer

def count_diff(buffer):
	diff = 0 
	for x in xrange(0,res1):
	   for y in xrange(0,res2):
		px_diff = abs(buffer[0][x,y][1]-buffer[1][x,y][1])
		if px_diff > treshold:
			diff += 1
	return diff

  
#detection of the move using stream                
def detect_and_save(how_many=10):

	camera = picamera.PiCamera()
	count = 0

	buffer=[]
	buff = compare(camera)
	buffer.append(buff)
	buffer.append(buff)

	sleep(10)
	while count < how_many:
		buffer[1] = compare(camera)	
		if count_diff(buffer) > trigger:
			buffer[0] = buffer[1]
			shottime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
		
			easy_shot(shottime+".jpg",camera)
			count += 1
			#break
		sleep(10)

def load_tweepy_codes(path):
	codes={}
	file = open(path)
	for i in range(0,4):
		line = file.readline()
		tmp=line.split(":")
		#print tmp
		codes[tmp[0]]=tmp[1]
	return codes

def update_twitter(photo_path,comment):
	api.update_with_media(photo_path,status=comment)
	
                         

codes = load_tweepy_codes(tweepy_codes_path)


api_key = codes['Consumer Key (API Key)'].strip()
api_secret = codes['Consumer Secret (API Secret)'].strip()
access_token = codes['Access Token'].strip()
token_secret = codes['Access Token Secret'].strip()


auth = tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,token_secret)
api = tweepy.API(auth)
my_twitter = api.me()

print my_twitter.name, "is connected"
tweet_text=['Test shot of birds station',
	    'Move detected with rPi']


#move_tilt_pct()
#move_tilt_value()

go=1

pattern = strftime("%Y-%m-%d %H:%M:%S",gmtime())+'.jpg'
shot_to_publish(pattern)

while go==1:
	diff, path = detect_if_move(pattern)	
        sleep(how_often_detection_test)
	print(diff)
	if diff > 3000:
		shot_name = strftime("%Y-%m-%d %H:%M:%S",gmtime())+'.jpg'
                shot_to_publish(shot_name)
		#adding publishing to tweeter
	

	


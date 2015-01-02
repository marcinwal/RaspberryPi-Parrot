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
import re
import RPi.GPIO as GPIO
import urllib
#import numpy as np

width = 1280
heigth = 960
treshold = 20 # trigger for change detection
res1 = 100  # x resolution for compare
res2 = 75   # y resolution for compare	
trigger = 100
tweepy_codes_path="tweepy_codes.txt"
how_often_detection_test=6 #testing motion
pir = 18 #pin 18th as IN for sensoe




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
       
def move_tilt_pct(command,command2):    
  start()
  sleep(5)
  #command=(raw_input("how much to move the servo 0 in pc "))
  servo_adjust_pct("0",command)
  #command2=(raw_input("how much to move servo 1  in pct "))
  servo_adjust_pct("1",command2)
  kill_servos()


def move_tilt_value():
  start()
  sleep(5)
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



#comapres two pictures and returns the number ofdifferent pixels
def compare_with_pattern(path1,path2):
  p1 = Image.open(path1)
  p2 = Image.open(path2)
  h1 = p1.histogram()
  h2 = p2.histogram()

  rms = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, h1,h2))/len(h1))

  return rms

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
  h1=p1.histogram()
  h2=p2.histogram()
  rms = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, h1,h2))/len(h1))

  return (rms,tmp)

def easy_shot(path,camera):
  camera.capture(path,resize=(1024,768))
	#print"taking a picture %s \n" % path 

def shot_to_publish(path,w=1024,h=768):
  print "shooting to publish"
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

#loading tweepy codes to feed to twitter
def load_tweepy_codes(path):
	codes={}
	file = open(path)
	for i in range(0,4):
		line = file.readline()
		tmp=line.split(":")
		#print tmp
		codes[tmp[0]]=tmp[1]
	return codes

#updating the twitter
def update_twitter(photo_path,comment = 'detection'):
	api.update_with_media(photo_path,status = comment)

#loading servos information form the page
def load_servos_info_from_page(page):
  sock = urllib.urlopen(page)
  html = sock.read()
  sock.close()

  serv1 = re.findall("Servo1:[-+%]?\d+",html)
  serv2 = re.findall("Servo2:[-+%]?\d+",html)

  s1 = serv1[-1].split(':')
  s2 = serv2[-1].split(':')

  return s1[1],s2[1]


def motion_detected(pir):
  time_event = strftime("%Y-%m-%d %H:%M:%S",gmtime())       
  shot_name = strftime("%Y-%m-%d %H:%M:%S",gmtime())+'.jpg'  
  shot_to_publish(shot_name)
  numberOfPictures += 1
  if to_twitter:
    update_twitter(shot_name,"picture taken in the garden by RasPi " + time_event[11:])



codes = load_tweepy_codes(tweepy_codes_path)

servo_page = "http://ratingpedia.eu/parrots/"
api_key = codes['Consumer Key (API Key)'].strip()
api_secret = codes['Consumer Secret (API Secret)'].strip()
access_token = codes['Access Token'].strip()
token_secret = codes['Access Token Secret'].strip()


auth = tweepy.OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,token_secret)
api = tweepy.API(auth)
my_twitter = api.me()

servo1,servo2 = load_servos_info_from_page(servo_page) #loading servos settings from the page

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir,GPIO.IN)

print my_twitter.name, "is connected"
#tweet_text=['Test shot of birds station',
#	    'Move detected with rPi']
#move_tilt_pct()
#move_tilt_value()
sleep(60)
numberOfPictures = 0 
pattern = strftime("%Y-%m-%d %H:%M:%S",gmtime())+'.jpg'
# to_twitter = False
# input_read = raw_input("Sending to twitter y/n?")
# if input_read == 'y':
#   to_twitter = True
# print "\n %r" %to_twitter
to_twitter = False
#sleep(how_often_detection_test)
# for i in xrange(1,5):  #takes 5 picstures if move is detected
#   print "motion detected"
      # time_event = strftime("%Y-%m-%d %H:%M:%S",gmtime())				
      # shot_name = strftime("%Y-%m-%d %H:%M:%S",gmtime())+'.jpg'
      # shot_to_publish(shot_name)
      # update_twitter(shot_name,"picture taken in the garden by RasPi")
      # sleep(10)
try:
  GPIO.add_event_detect(pir,GPIO.RISING,callback = motion_detected) 
  while True:
    time.sleep(60)
    s1,s2 = load_servos_info_from_page(servo_page)
    if (s1 != servo1) or (s2 != servo2):
      servo1, servo2 = s1, s2
      print "moving servos"
      print s1,s2
      move_tilt_pct(s1,s2)
except KeyboardInterrupt:
  print "Ending.."
finally:
  camera.close()
  GPIO.cleanup()
  kill_servos()

               
             	


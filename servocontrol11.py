#!/usr/bin python
from subprocess import call
from time import gmtime,strftime,sleep
import os
import picamera
import io
from PIL import Image


width = 1280
heigth = 960
treshold = 20 # trigger for change detection
res1 = 100  # x resolution for compare
res2 = 75   # y resolution for compare	
trigger = 100
tweepy_codes_path="tweepy_codes.txt"


def start():
        print("starting servo")
        os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")


        
def call_command(servo,pulsewidth):
        os.system("echo "+str(servo)+"="+str(pulsewidth)+"> /dev/servoblaster")

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
                        

def take_a_photo(path):
        with picamera.PiCamera() as camera:
                camera.start_preview()
                sleep(5)
                camera.capture(path)
                camera.stop_preview()


def easy_shot(path,camera):
	camera.capture(path,resize=(1024,768))
	print"taking a picture %s \n" % path 


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
		tmp=line.split(":") #format key ':' value
		#print tmp
		codes[i]=tmp[1]
	return codes

                         
#detect_and_save(5)
codes = load_tweepy_codes(tweepy_codes_path)
print codes

                

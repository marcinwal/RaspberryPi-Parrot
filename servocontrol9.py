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


#def easy_shot(path,camera):
#	camera.capture(path,resize=(640,480))


def compare(camera):
	camera.resolution(res1,res2)
	stream = io.BytesIO()
	camera.capture(stream,format='bmp') 
	stream.seek(0)
	im = Image.open(stream)
	buffer = im.load()
	stream.close()
	return im,buffer

def count_diff(buffer1,buffer2):
	diff = 0 
	for x in xrange(0,res1):
	   for y in xrange(0,res2):
		px_diff = abs(buffer1[x,y][1]-buffer2[x,y][1])
		if px_diff > treshold:
			diff += 1
	return diff

   
                
#shottime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
#move_tilt_pct()
#take_a_photo(shot_time+".jpg")

camera = picamera.PiCamera()
count = 0

im1,buffer1 = compare(camera)
sleep(10)

while count < 10:
	im2,buffer2 = compare(camera)	
	if count_diff(buffer1,buffer2) > trigger:
		buffer1 = buffer2
		im1 = im2
		shottime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
		
		#easy_shot(shottime,camera)
		camera.capture(shottime+".bmp")
		count += 1
		break;
	sleep(30)



                         
                

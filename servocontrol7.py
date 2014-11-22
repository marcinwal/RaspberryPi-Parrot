#!/dev/bin python
from subprocess import call
from time import gmtime,strftime,sleep
import os
import picamera


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
                
shottime = strftime("%Y-%m-%d %H:%M:%S",gmtime())
move_tilt_pct()
take_a_photo(shottime+".jpg")

                         
                

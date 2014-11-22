from subprocess import call
from time import sleep
import os


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
	os.system("echo "+str(servo)+"="+str(adjust)+"% > /dev/servoblaster")
       
	
start()
#command=0
while True:
		#command=eg.enterbox("How much move the the servo 0?")
		command=(raw_input("how much to move the servo 0"))
		
		if command != " ":
			servo_adjust_plus("0",command)
		else:
			kill_servos()
			break

                #pct = str(raw_input("how many % to move")
			
		#kill_servos()
		#start()

		command2=(raw_input("how much to move servo 1"))

		if command2 !=  " ":
			servo_adjust_plus("1",command2)
		else:
			kill_servos()
			break



		

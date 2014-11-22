from subprocess import call
from time import sleep
import os


def start():
	print("starting servo")
	os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")

def stop(time):
	print("stopleft")
	call (["echo 0=150 > /dev/servoblaster"],shell=True)
	print("stopright")
	call (["echo 1=150 > /dev/servoblaster"],shell=True)
	sleep(time)
	
def call_command(servo,pulsewidth):
	os.system("echo "+str(servo)+"="+str(pulsewidth)+"> /dev/servoblaster")
	

def forwards(time):
	call_command(0,200)
	call_command(1,100)
	sleep(time)
	stop(0.1)
	
def back(time):
	call_command(0,100)
	call_command(1,200)
	sleep(time)
	stop(0.1)
	
def servo_adjust_plus(servo,adjust): #+10,+20
	os.system("echo "+str(servo)+"=+"+str(adjust)+" > /dev/servoblaster")
	print("executing:"+"echo "+str(servo)+"=+"+str(adjust)+" > /dev/servoblaster")

def servo_adjust_minus(servo,adjust):	
	os.system("echo "+str(servo)+"=-"+str(adjust)+" > /dev/servoblaster")
	print("executing:"+"echo "+str(servo)+"=-"+str(adjust)+" > /dev/servoblaster")
	
def kill_servos():
	os.system("sudo killall servod")
	
	
start()
#command=0
while True:
		#command=eg.enterbox("How much move the the servo 0?")
		command=int(raw_input("how much to move the servo 0"))
		
		if command > 0:
			servo_adjust_plus(0,command)
		elif command < 0:	
			servo_adjust_minus(0,-command)
		else:
			kill_servos()
			break
			
		kill_servos()
		start()

		command2=int(raw_input("how much to move servo 1"))

		if command2 > 0:
			servo_adjust_plus(1,command)
		elif command2 < 0:	
			servo_adjust_minus(1,-command)
		else:
			kill_servos()
			break



		

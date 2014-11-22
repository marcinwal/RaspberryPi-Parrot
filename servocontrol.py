from subprocess import call
from time import sleep
import easygui as eg


def start():
	print("starting servo")
	call (["sudo ./servod"],shell=True)

def stop(time):
	print("stopleft")
	call (["echo 0=150 > /dev/servoblaster"],shell=True)
	print("stopright")
	call (["echo 1=150 > /dev/servoblaster"],shell=True)
	sleep(time)
	
def call_command(servo,pulsewidth):
	call(["echo "+str(servo)+"="+str(pulsewidth)+"> /dev/servoblaster"],shell=True)
	

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
	call(["echo "+str(servo)+"=+"+str(adjust)+"> /dev/servoblaster"],shell=True)

def servo_adjust_minus(servo,adjust):	
	call(["echo "+str(servo)+"=-"+str(adjust)+"> /dev/servoblaster"],shell=True)
	
def kill_servos():
	call(["sudo killall servod"],shell=True)	
	
	
start()
#command=0
while True:
		#command=eg.enterbox("How much move the the servo 0?")
		command=int(raw_input("how much to move the servo"))
		if command > 0:
			servo_adjust_plus(0,command)
		elif command < 0:	
			servo_adjust_minus(0,command)
		else:
			break

kill_servos()
		

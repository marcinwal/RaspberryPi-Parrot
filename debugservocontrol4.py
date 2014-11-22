from subprocess import call
from time import sleep
import os


def start():
	print("starting servo")
	os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")


	
def call_command(servo,pulsewidth):
	os.system("echo "+str(servo)+"="+str(pulsewidth)+"> /dev/servoblaster")
	

def servo_adjust_plus(servo,adjust): #+10,+20
        p="echo "+str(servo)+"=+"+str(adjust)+" > /dev/servoblaster"
        print p
	

def servo_adjust_minus(servo,adjust):	
	p="echo "+str(servo)+"=-"+str(adjust)+" > /dev/servoblaster"
	#print("executing:"+"echo "+str(servo)+"=-"+str(adjust)+" > /dev/servoblaster")
	print p
	
def kill_servos():
	os.system("sudo killall servod")
	
	
#start()
#command=0
while True:
		#command=eg.enterbox("How much move the the servo 0?")
		command=int(raw_input("how much to move the servo 0"))
		
		if command > 0:
			servo_adjust_plus(0,command)
		elif command < 0:	
			servo_adjust_minus(0,-command)
		else:
			#kill_servos()
			break
			
		#kill_servos()
		#start()

		command2=int(raw_input("how much to move servo 1"))

		if command2 > 0:
			servo_adjust_plus(1,command2)
		elif command2 < 0:	
			servo_adjust_minus(1,-command2)
		else:
			#kill_servos()
			break

import sys,tty,termios
import RPi.GPIO as GPIO

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        global atcenter
        global posicionactual
        global fullright
        global fullleft
        global pwm

        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print "up"
                posicionactual = atcenter
                pwm.ChangeDutyCycle(posicionactual)
                GPIO.output(11,GPIO.HIGH)

        elif k=='\x1b[B':
                print "down"
                posicionactual = atcenter
                pwm.ChangeDutyCycle(posicionactual)
                GPIO.output(11,GPIO.LOW)

        elif k=='\x1b[C':
                print "right"
                if posicionactual < fullleft:
                    posicionactual = posicionactual + .25
                    pwm.ChangeDutyCycle(posicionactual)
        elif k=='\x1b[D':
                print "left"
                if posicionactual > fullright:
                    posicionactual = posicionactual - .25
                    pwm.ChangeDutyCycle(posicionactual)
        else:
                print "not an arrow key!"

def main():
        global atcenter
        global posicionactual
        global fullright
        global fullleft
        global pwm

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(12,GPIO.OUT)
        pwm=GPIO.PWM(12,50)
        pwm.start(5)
        atcenter = 7
        posicionactual = atcenter
        fullright = 3
        fullleft = 11
        pwm.ChangeDutyCycle(atcenter)

        GPIO.setup(11,GPIO.OUT)
        GPIO.output(11,GPIO.HIGH)

        parasiempre = 1
        while(parasiempre):
            get()
        pwm.stop()
        GPIO.cleanup()

if __name__=='__main__':
        main()

from pyfirmata import Arduino, time
board = Arduino('COM5') # usb port
servo = board.get_pin('d:10:s') # pin PWM no 2

servo.write(0.0)
for i in range(180):
    print(i)
    servo.write(float(i))
    time.sleep(0.1)
 
print("goodbye")
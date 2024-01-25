"""! @file step_response.py
Creates and records the response of the given circuit for a step response input 
"""

import utime
import cqueue

# Timer Interrupt
def timer_float(tim):
    """!
        Interrupt callback function that measures voltages every 10ms
    """
    
    # Checks if queue is full and either stops the interrupt callbacks or adds value to queue
    if float_queue.full():
        tim.callback(None)
    else:
        float_queue.put(pinB0.read())
    
    
def step_response():
    """!
        Main function setting up interrupts, pins, queues, and prints output voltages
    """
    print('Start')
    
    # Initializing Timer Callback
    tim = pyb.Timer(1)
    tim.init(freq=100)
    tim.callback(timer_float)
    
    # Initializing Pin C0
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    pinC0.low()
    
    # Providing Step Input
    pinC0.high()
    
    # Waits for a Full Queue
    while not float_queue.full():
        pass
    
    # Deinitializes the Timer and Resets Pin C0
    tim.deinit()
    pinC0.low()
    
    # Reads each Value in the Queue and assigns it a corresponding time
    for i in range(float_queue.available()):
        times = i*10
        volts = float_queue.get()*(3.3/4095)
        print(f'{times:.0f},{volts:.5f}')    
    print('End')
    
if __name__ == "__main__":
    # Waits for an input to the Serial
#     while not Serial.available():
#         pass
#     
    # Initializing Readable Pin, Pin B0, and Queue, float_queue, as global
    pinB0 = pyb.ADC(pyb.Pin.board.PB0)
    float_queue = cqueue.FloatQueue(201)
    print('Start')

    step_response()
import utime
import cqueue

# Timer Interrupt
def timer_float(tim):
    # Checks if queue is full and either stops the interrupt callbacks or adds value to queue
    if float_queue.full():
        tim.callback(None)
    else:
        float_queue.put(pinB0.read())
    
    
def step_response():
    # Initializing Timer Callback
    tim = pyb.Timer(1)
    tim.init(freq=100)
    tim.callback(timer_float)
    
    # Initializing Pin C0 and Pin B0
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    
    # Providing Step Input
    pinC0.high()
    
    # Waits for a Full Queue
    while not float_queue.full():
        pass
    
    # Deinitializes the Timer and Resets Pin C0
    tim.deinit()
    pinC0.low()
    
    # Prints each Value in the Queue and assigns it a corresponding time
    for i in range(float_queue.available()):
        times = i*10
        volts = float_queue.get()*(3.3/4095)
        print(f'{times:.0f},{volts:.5f}')    
    print('End')
    
if __name__ == "__main__":
    # Initializing Readable Pin, Pin B0, and Queue, float_queue, as global
    pinB0 = pyb.ADC(pyb.Pin.board.PB0)
    float_queue = cqueue.FloatQueue(201)

    step_response()
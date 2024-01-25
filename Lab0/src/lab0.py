"""!
@file lab0.py
Runs a real and simulated dynamic response to a step response and plots the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Spluttflob (original)
@date   2023-12-24 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import tkinter
import serial
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_output(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Collects data from the test run when Run Test is clicked by reseting the step_response
    program on the microcontroller and reading the printed data to the connected COM Port. Then plots
    the collected data and produces a plot for theoretical data on the same canvas.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    
    # Real test data is read through the USB-serial
    # port and processed to make two lists, xlist and ylist
    
    # States COM device (May vary with different computers)
    com_port = 'COM5'
    
    # Tries to open the defined serial port and run data, and if it can not, will print error
    try:
        serial_port = serial.Serial(com_port, baudrate=115200, timeout=1)
    except serial.SerialException as error:
        print(f"could not open serial port '{com_port}': {error}")
    else:     
        # Uses readline() method to open file as read and run exceptions
        xlist = [] # List of x-values
        ylist = [] # List of y-values
        # Writes "b'\x04" (Ctrl-D) to reset the serial port and rerun main on microcontroller
        serial_port.write(b'\x04') 
        while True:
            # Catches any errors in converting Bytes to Strings
            try:
                # Reads each line printed by the serial port
                line = serial_port.readline()
                print(line)
                # Skips processing any blank lines
                if line == '':
                    pass
                # Converts the returned Byte format to String
                line = line.decode('utf-8')
                # Formats each line to be 0-2 values with no comments or \r\n
                line = line[:-2] # Removes \r\n
                # Checks if line says "End" and stops reading values
                if line == 'End':
                    break
                    print("broke out")
                #print(line)
                line = line.split(',') # Separates each comma separated value
                line = line[:2] # Limits the number of values per line to 2
                for i, value in enumerate(line):
                    value = value.split('#') # Separates out comments
                    line[i] = value[0] # Readds non-commented value to list
                    
                # Tests both values for string or float values
                try: # Tries to convert each pair of values into a float
                    for value in line:
                        value = float(value)
                except ValueError: # For non-float values
                    #print("Skipped line:", line)
                    pass
                else:
                    xlist.append(float(line[0])) # Adds passed float value to x-values
                    ylist.append(float(line[1])) # Adds passed float value to y-values
            except Exception as error:
                    print(error)
            
        # Draw the experimental plot.
        plot_axes.plot(xlist, ylist)
        plot_axes.set_xlabel(xlabel)
        plot_axes.set_ylabel(ylabel)
        plot_axes.grid(True)
        plot_canvas.draw()        
        
        # Closes the serial port
        serial_port.close()
        
    # Draw Theoretical Response on the plot based on the recorded time values
    R = 100*10**3 # Ohms
    C = 3.3*10**-6 # Farads
    xlist2 = xlist
    ylist2 = [3.3*(1-math.exp(-x/(1000*R*C))) for x in xlist2] # where x is in milliseconds
    plot_axes.plot(xlist2, ylist2)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_output,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Step Response")


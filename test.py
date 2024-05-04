import functions
import time

"""
I used this test script to test the calculated bounds from the button in the gui, if you would like to test yours as well just replace the region tuple with the bounds you calculated.
"""
time.sleep(3)
functions.take_screenshot('test_bounds', region=(580, 960, 905, 48))

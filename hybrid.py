import pyvisa
import numpy as np
import time
import sys

DM = 800
K = 4148.8
freq_hi = 600 # MHz
freq_lo = 400 # MHz
n_point = 800
t_total = K*DM*(1/freq_lo**2-1/freq_hi**2) # sec
t_sep = t_total/n_point # sec
print('duration:', t_total)
print('t_separation:', t_sep) 
t_points = np.arange(n_point)*t_sep # sec 

freqs = 1 / np.sqrt(t_points/(K*DM) + 1/freq_hi**2) # MHz
#print('freqs:', freqs)
#sys.exit()

rm = pyvisa.ResourceManager()
inst = rm.open_resource('TCPIP::192.168.40.212::5025::SOCKET')
inst.write("*RST")
time.sleep(2)
inst.write(":POW:MODE FIX")
inst.write(":FREQ:MODE CW")
inst.write(":INIT:CONT ON")
inst.write(":TRIG:SOUR IMM")
inst.write(":POW -10")
inst.write(":OUTP ON")
#inst.write(f":FREQ {freq_lo}MHz")
time.sleep(2)
print('start sending pulses now')


j = 0
while (True):
    print('loop:', j)

    t0 = time.time()
    i = -1
    for t, f in zip(t_points, freqs):
        i += 1
        if (i%50==0):
            print('...', i, t, f)
        tt = time.time()
        while (tt-t0 < t):
            time.sleep(0.001)
            tt = time.time()
        inst.write(f":FREQ {f}MHz")

    time.sleep(5)

import pyaudio
import wave
import sys, time
import numpy as np
import tkinter, time
import pylab
from scipy.io.wavfile import read
from scipy.fftpack import fft
import matplotlib.pyplot as plt


def ende():
    main.destroy()

main = tkinter.Tk()


CHUNK = 1024

wf = wave.open("C:/Users/Jonas/Desktop/Wav-Musik/MarshmelloAlone.wav", "rb")

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
sampwidth = wf.getsampwidth()
stream = p.open(format=p.get_format_from_width(sampwidth), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)


RATE = wf.getframerate()

data = bytearray(wf.readframes(CHUNK))


w = tkinter.Canvas(main,width=1000, height=800, bg="yellow", highlightthickness=0)
w.pack(fill="both", expand=True)

dataRect = []

d = 0
for i in range(200):
    dataRect.append(w.create_rectangle(d, 800, d+10, 800 , fill='red'))
    d+=10
main.update()



a = 3
et = w.create_oval( 400, 300, 500, 200, fill = "black")
et1 = w.create_oval( 500, 300, 600, 200, fill = "black")
et2 = w.create_oval( 600, 300, 700, 200, fill = "black")
et3 = w.create_oval( 700, 300, 800, 200, fill = "black")
z = 0
z1 = 0
z2 = 0
z3 = 0

while len(data) > 0:
    data = np.fromstring(wf.readframes(CHUNK), dtype=np.int16)
    
    # compute FFT and update line
    yf = fft(data)

    da = np.abs(yf[0:CHUNK])  / (128 * CHUNK)
  
    
    d = 20

    if da[2] > 76 or z > 1:
        w.itemconfig(et, fill='red')
        if da[2] > 76: 
            z = 4
    else:
        w.itemconfig(et, fill='black')
        #z = 0
    z -= 1  



    if da[2*2] > 30 or z1 > 1:
        w.itemconfig(et1, fill='white')
        if da[2*2] > 30:
            z1 = 4
    else:
        w.itemconfig(et1, fill='black')
        #z = 0
    z1 -= 1




    if da[2*4] > 30 or z2 > 1:
        w.itemconfig(et2, fill='cyan')
        if da[2*4] > 30: 
            z2 = 4
    else:
        w.itemconfig(et2, fill='black')
        #z = 0
    z2 -= 1


    if da[2*7] > 65 or z3 > 1:
        w.itemconfig(et3, fill='green')
        if da[2*7] > 50: 
            z3 = 4
    else:
        w.itemconfig(et3, fill='black')
        #z = 0
    z3 -= 1


    for i in range(200):
          
        if d < 200:
            w.coords(dataRect[i], d, 690-(da[i*2])*6, d+10, 700)
            
            d+=10
        else:
            w.coords(dataRect[i], d, 690-(da[i*2])*6, d+10, 700)
            d+=10

        main.update()    
    
    stream.write(bytes(data))
    
    
# stop stream (4)
main.mainloop()
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
p=Path(__file__).resolve().parent.parent  # song folder
sr,x=wavfile.read(p/'audio'/'opening20_float.wav'); m=x.mean(axis=1)
wavfile.write(p/'renders'/'opening_00-20.wav',sr,(x*.5*32767).clip(-32768,32767).astype(np.int16))
low=signal.sosfiltfilt(signal.butter(6,[25,250],fs=sr,btype='bandpass',output='sos'),m)
wavfile.write(p/'renders'/'bass_00-20.wav',sr,(low/abs(low).max()*.85*32767).astype(np.int16))
wavfile.write(p/'renders'/'slide_10-14.wav',sr,(x[10*sr:14*sr]*.5*32767).clip(-32768,32767).astype(np.int16))
# Zero-padding interpolates a windowed spectrum; actual temporal window is 240 ms.
ds=signal.resample_poly(m,1,24); fs=sr/24
f,t,z=signal.stft(ds,fs,nperseg=480,noverlap=460,nfft=16384)
amp=abs(z); ids=np.where((f>=28)&(f<=100))[0]
idx=ids[np.argmax(amp[ids],axis=0)]; hz=f[idx]
notes=69+12*np.log2(hz/440)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def note(v):
 n=int(round(v)); return names[n%12]+str(n//12-1)
with (p/'data'/'bass_pitch_track.csv').open('w') as out:
 w=csv.writer(out); w.writerow(['seconds','strongest_low_peak_hz','midi_float','nearest_note','peak_amplitude'])
 for tt,h,n,a in zip(t,hz,notes,amp[idx,np.arange(len(t))]): w.writerow([round(tt,3),round(h,3),round(n,3),note(n),round(float(a),6)])
fig,ax=plt.subplots(3,1,figsize=(16,12),layout='constrained')
for a,lim in [(ax[0],(0,20)),(ax[1],(10,14))]:
 a.pcolormesh(t,f,20*np.log10(amp+1e-8),vmin=-75,vmax=-15,cmap='magma',shading='auto')
 a.set(xlim=lim,ylim=(25,450),xlabel='Seconds',ylabel='Hz',yscale='log')
 a.set_yticks([30,40,50,60,80,100,120,160,200,300,400]); a.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax[0].set_title('Bass spectrum — 240 ms windows, 10 ms hops; harmonics corroborate pitch')
ax[2].plot(t,hz,lw=1); ax[2].set(xlim=(8.3,20),ylim=(28,100),xlabel='Seconds',ylabel='Strongest low spectral peak (Hz)')
for n in range(23,44):
 h=440*2**((n-69)/12)
 if 28<h<100: ax[2].axhline(h,c='gray',alpha=.3); ax[2].text(20,h,note(n),fontsize=8)
fig.savefig(p/'figures'/'bass_pitch20.png',dpi=150)
for tt in np.arange(8.5,20,.25):
 k=np.argmin(abs(t-tt)); print(f'{t[k]:.2f} {hz[k]:.2f} {note(notes[k])} {notes[k]:.2f}')

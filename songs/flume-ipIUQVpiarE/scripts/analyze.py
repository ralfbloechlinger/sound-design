from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

p=Path(__file__).resolve().parent.parent  # song folder
sr,raw=wavfile.read(p/'audio'/'opening_float.wav')
x=raw.astype(float)
m=x.mean(axis=1); side=(x[:,0]-x[:,1])/2
fig,ax=plt.subplots(3,1,figsize=(16,12),layout='constrained')
t=np.arange(len(m))/sr
ax[0].plot(t,x[:,0],lw=.3,label='Left'); ax[0].plot(t,x[:,1],lw=.3,alpha=.6,label='Right')
ax[0].set(xlabel='Seconds',ylabel='Amplitude',title='Opening 0–10 s — stereo waveform'); ax[0].legend()
for a,n,top in [(ax[1],8192,1500),(ax[2],2048,16000)]:
 f,tt,z=signal.stft(m,sr,nperseg=n,noverlap=n*7//8)
 a.pcolormesh(tt,f,20*np.log10(np.maximum(abs(z),1e-7)),vmin=-85,vmax=-20,shading='auto',cmap='magma')
 a.set(ylim=(30,top),yscale='log',xlabel='Seconds',ylabel='Hz')
 a.set_yticks([v for v in [30,50,100,200,400,800,1500,3000,6000,12000] if v<=top]); a.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
fig.savefig(p/'figures'/'spectrogram.png',dpi=150)
stats={'sample_rate':sr,'duration':len(m)/sr,'peak_dBFS':float(20*np.log10(abs(x).max())),'rms_dBFS':float(20*np.log10(np.sqrt(np.mean(x*x)))),'bands':{}}
for name,lo,hi in [('sub',25,120),('bass_body',120,500),('synth_detail',500,6000),('air',6000,18000)]:
 sos=signal.butter(6,[lo,hi],btype='bandpass',fs=sr,output='sos'); y=signal.sosfiltfilt(sos,x,axis=0)
 mid=y.mean(axis=1); s=(y[:,0]-y[:,1])/2
 stats['bands'][name]={'rms_dBFS':float(20*np.log10(np.sqrt(np.mean(y*y)))),'side_mid_dB':float(20*np.log10(np.sqrt(np.mean(s*s))/np.sqrt(np.mean(mid*mid)))),'LR_correlation':float(np.corrcoef(y.T)[0,1])}
 # Normalize each audition copy independently; these are frequency bands, not stems.
 wavfile.write(p/'renders'/(name+'_band.wav'),sr,(y/max(abs(y).max(),1e-9)*.85*32767).astype(np.int16))
f,ps=signal.welch(m,sr,nperseg=65536)
peaks,_=signal.find_peaks(ps)
stats['strongest_spectral_peaks_Hz']=[round(float(f[i]),2) for i in sorted(peaks,key=lambda i:ps[i],reverse=True)[:25]]
stats['sections']={}
for label,start,end in [('intro',.2,8.3),('bass_entry',8.5,10)]:
 xx=x[int(start*sr):int(end*sr)]
 entry={}
 for name,lo,hi in [('sub',25,120),('body',120,500),('detail',500,6000)]:
  y=signal.sosfiltfilt(signal.butter(6,[lo,hi],btype='bandpass',fs=sr,output='sos'),xx,axis=0)
  entry[name]={'rms_dBFS':float(20*np.log10(np.sqrt(np.mean(y*y)))),'LR_correlation':float(np.corrcoef(y.T)[0,1])}
 stats['sections'][label]=entry
(p/'data'/'measurements.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))

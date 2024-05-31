#%%
# comparing SWL, SIL, and SPL

import math
swl_dB = 10*(math.log10(800/1e-12))    # rate at which acoustic energy is radiated from the source - measures the ability of a source to produce sound
                                       # 10log10(W/Wref) https://engcourses-uofa.ca/books/vibrations-and-sound/12-sound-and-acoustics/sound-power-level/
                                       # if Wref ~= 120dB, then swl_dB = 10log10(W) + 120dB, and W = 10^((swl_dB-120)/10) gives the power delivered from the sound energy level.   
sil_dB= 10*(math.log10(1/1e-12))     # acoustic energy through a unit area.
                                       # 10log10(I/Iref) https://courses.lumenlearning.com/atd-austincc-physics1/chapter/17-3-sound-intensity-and-sound-level/
spl_dB = 20*(math.log10(800/2e-5))     # measure of sound relative to a reference level - threshold of human hearing - at 1kHz freq po = 2e-5 Pascal.
                                       # 20log10(p/po) https://en.wikipedia.org/wiki/Sound_pressure

print(f'SWL =  {swl_dB}dB \nSIL = {sil_dB}dB \nSPL = {spl_dB:1.1f}dB') # \nSWL_DB_2 = {swl_dB_2} \nPOWER_Watts from SWL_DB_2 = {power_W}')

# SIL == SPL with differences in the reference levels -> for SIL, the reference intensity level Io = 1e-12, while for SPL, the reference pressure level Po = 2e-5
# %%
# other relevant equations
# r = 1 # 1 sqm
# Q = 1 # for point source, free air, and could be 2, 4, 8 - for a closed space. 
# spl_dB = swl_dB + 10*math.log10(Q/(4*math.pi*r**2))
# swl_dB_2 = spl_dB - 10*math.log10(Q/(4*math.pi*r**2))
# power_W = 10**((swl_dB_2-120)/10)
# %%

import math
w = 800            	                 # power rating of speaker amplifier
w_eff = w * 0.05                         # 5% efficiency of power rating
swl_dB = 10*math.log10(w) + 120          # sound energy level calculated from  raw power rating
swl_dB_eff = 10*math.log10(w_eff) + 120  # sound energy level calculated from  power rating with 5 % efficiency
swl_dB, swl_dB_eff                       # (raw sound energy level, 5% * sound energy level)

# the above works for 1m2 Area - swl == swl
# actually, to calculate the sound intensity level from a speaker, we just need to:
# I = P (W) / A (m2)
# since we know that speakers are roughly 5% efficient => 
# I = P * 0.05 (W) / A (m2)
# %%

# comparing speaker amplifier rms Power (W) to speaker rms Power (W)
amp = (1300/2)**0.5
spk = (800/4)**0.5

(amp, spk)
# %%
# comparing speaker sensitivity v speaker power

spk_sens = 90
spk_pow = 1
while spk_sens < 155:
    print(spk_sens, spk_pow)
    spk_sens+=3
    spk_pow*=2

# %%

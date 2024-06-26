#%%
#  print values below 103, in steps of 6, but not below 60
i = 103
while i > 60:
    i-=6
    print(i)
# %%
#  print values above 103, in steps of 6, but not above 130
i = 103
while i < 130:
    i+=6
    print(i)
    
# %%
# can you combine the above in a while loop?
i = 103

while (i > 60) and (i < 130):
    print(f'above 103 {i+6}, below 103 {i-6}')

# %%
#  power (P) = v**2 / r, where r = 8 Ohms
v = [1.06, 1.44, 0.688, 0.364, 0.636, 0.332]
r = 14
for volt in v:
    p = volt**2 / r
    print(f'for r = 14 Ohms; \n voltage: {volt} V, power: {p} W')
# %%
1.44 / 2
# %%
5000/4
# %%
150-37
# %%
526.11-279.72
# %%
19+9
# %%
60*60*1
# %%
3**2 / 0.5
# %%
17.00-20.00
# %%

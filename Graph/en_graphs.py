#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

inpfilename=raw_input("Input Data (csv) Filename: ")

pip=np.loadtxt(inpfilename, dtype=str, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(0,6), unpack=False, ndmin=0)

AHBHAV = np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(4,5,6), unpack=False, ndmin=0)  #coefs AH,BH, AV

pipe_tag = []   #pip[count,0]
AH=[]			#AHBHAV[count,0]
BH=[]			#AHBHAV[count,1]
AV=[]			#AHBHAV[count,2]
H=[]
V=[]
nps = len(pip)

for count in range (0, nps):
	pipe_tag.append(pip[count, 0])
	AH.append(AHBHAV[count, 0])
	BH.append(AHBHAV[count, 1])
	AV.append(AHBHAV[count, 2])
	
	print pipe_tag
	print AH
	print BH
	print AV
	
	Q=np.linspace(0, 300)
	H = AH[count]*Q**2+BH[count]
	V = AV[count]*Q
	
	out_fn = pipe_tag[count]+"-Headl"+".png"
	plt.plot(Q, H, color = "blue")
	plt.title ("Headloss in "+pipe_tag[count])
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Headloss [m]")
	plt.grid(True)
	plt.savefig(out_fn)
	plt.close()
	
	out_fn_vel = pipe_tag[count]+"-Velo"+".png"
	plt.plot(Q, V, color="red")
	plt.title ("Fluid Velocity in "+pipe_tag[count])
	plt.xlabel("Flow [cum/hr]")
	plt.ylabel("Velocity [m/s]")
	plt.grid(True)
	plt.savefig(out_fn_vel)
	plt.close()
	
print ("Done")
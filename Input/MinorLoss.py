#!/usr/bin/env python


import numpy as np
import DWheadloss as dw

inpfilename = raw_input("Piping data file name: ")
outfilename = raw_input("Output file name: ")
	
fittings=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), unpack=False, ndmin=0)
chars=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(1,2,3,4,5), unpack=False, ndmin=0)
pipes_num=len(fittings)
ptag = np.loadtxt(inpfilename, dtype=str, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(0,1), unpack=False, ndmin=0)

#reading k-factors:

k=np.loadtxt("k_factors.csv", dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(None), unpack=False, ndmin=0)

pipes_num=len(fittings)

k_fact = []
pipe_id=[]
rough=[]
pipe_len=[]
pipe_tag = []

outfile = outfilename + '.csv'
fn = open(outfile, "a")
fn.write("Pipe tag"+","+"Minor Loss")
fn.write("\n")

for pipes in range(0, pipes_num):
# calculating local losses
	loss=fittings[pipes]
	dims=chars[pipes]
	
	# local losses due to elbows
	elbows=dw.elbow_loss(float(k[0]),float(loss[0]), float(k[1]),loss[1], float(k[2]),float(loss[2]), k[3],loss[3], float(k[4]),loss[4])
	
	# local losses in valves
	valves=dw.valve_loss(k[5],loss[5], k[6],loss[6], k[7],loss[7], k[8],loss[8], k[9],loss[9], k[10],loss[10], k[11],loss[11], k[12],loss[12])
	
	# local losses due to flow through tees - header and branch
	tee=dw.tee_loss(k[13],loss[13], k[14],loss[14])
	
	#local losses in reducer/contraction
	reducer=dw.red_loss(dims[0], dims[2], loss[18], loss[19])
	
	#miscellaneous local losses
	misc=dw.misc_loss(k[16],loss[16], k[15],loss[15], k[17],loss[17], k[20],loss[20])
	
	#total local losses
	total=dw.tot_loc_loss(elbows, valves, tee, misc, reducer)

	pipe_tag.append(ptag[pipes,0])
	pstr = pipe_tag[pipes]+","+str(total)
	fn.write(pstr)
	fn.write("\n")
	
fn.close()
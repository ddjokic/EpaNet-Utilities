#!/usr/bin/env python

''' prepare EpaNet Input file - only sections [JUNCTIONS], [PIPES] and [Coords] and calculates minor losses, prepared by user in "csv"-format as per template provided. Nothing cleaver, just script which "do the job".

requires: numpy
		  DWheadloss.py, which is in github repo
No warranties of any kind.

D. Djokic, 2014
'''

import numpy as np
import DWheadloss as dw

inpfilename = raw_input("Piping data file name: ")
coordfile = raw_input ("Nodal data file name: ")
	
fittings=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26), unpack=False, ndmin=0)
chars=np.loadtxt(inpfilename, dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(1,2,3,4,5), unpack=False, ndmin=0)
pipes_num=len(fittings)
ptag = np.loadtxt(inpfilename, dtype=str, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(0,1), unpack=False, ndmin=0)
p_nodes = np.loadtxt(inpfilename, dtype=str, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(27,28), unpack=False, ndmin=0)

junctions = np.loadtxt(coordfile, dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(1,2,3,4,5), unpack=False, ndmin=0)	
junction_tag=np.loadtxt(coordfile, dtype=str, comments="#", delimiter=',', converters=None, skiprows=1, usecols=(0,1), unpack=False, ndmin=0)

pipes_num=len(fittings)
junction_num = len(junctions)


inp_fname = raw_input("EpaNet INP file name: ")

#reading k-factors:

k=np.loadtxt("k_factors.csv", dtype=float, comments="#", delimiter=',', converters=None, skiprows=2, usecols=(None), unpack=False, ndmin=0)

junc_tag = []
junc_elevation=[]
junc_demand=[]
junc_pattern=[]
junc_x = []
junc_y=[]

#junctions part

for junction in range (0, junction_num):
	junc_tag.append(junction_tag[junction, 0])
	junc_elevation.append(junctions[junction, 0])
	junc_demand.append(junctions[junction, 1])
	junc_pattern.append(junctions[junction, 2])
	junc_x.append(junctions[junction, 3])
	junc_y.append(junctions[junction, 4])
	


k_fact = []
pipe_id=[]
rough=[]
pipe_len=[]
in_node=[]
out_node=[]

# calculate local losses 

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
	
	#pipe geometry
	k_fact.append(total)
	pipe_id.append(chars[pipes, 0])
	rough.append(chars[pipes,1])
	pipe_len.append(chars[pipes, 4])
	in_node.append(p_nodes[pipes,0])
	out_node.append(p_nodes[pipes,1])

inpfn = inp_fname+".inp"
fn=open(inpfn, "a")
fn.write("[JUNCTIONS]")
fn.write("\n")
fn.write(";ID \t Elev \t Demand")
fn.write("\n")
for junction in range (0, junction_num):
	fn.write(junc_tag[junction])
	fn.write("\t")
	fn.write(str(junc_elevation[junction]))
	fn.write("\t")
	fn.write(str(junc_demand[junction]))
	fn.write("\t")
	fn.write(str(junc_pattern[junction]))
	fn.write("\n")
fn.write("\n")

fn.write("[PIPES]")
fn.write("\n")
fn.write(";ID\tNode1\tNode2\tLength\tDiameter\tRoughness\tMinorLoss\tStatus")
fn.write("\n")
for pipe in range(0, pipes_num):
	pipe_str=ptag[pipe, 0]+"\t"+in_node[pipe]+"\t"+out_node[pipe]+"\t"+str(pipe_len[pipe])+"\t"+str(pipe_id[pipe])+"\t"+str(rough[pipe])+"\t"+str(k_fact[pipe])+"\t"+"Open"+"\n"
	fn.write(pipe_str)
fn.write("\n")

fn.write("[COORDINATES]")
fn.write("\n")
fn.write(";Node\tX-Coord\tY-Coord")
fn.write("\n")
for junction in range(0, junction_num):
	juncstr = junc_tag[junction]+"\t"+str(junc_x[junction])+"\t"+str(junc_y[junction])+"\n"
	fn.write(juncstr)
	
fn.close()	
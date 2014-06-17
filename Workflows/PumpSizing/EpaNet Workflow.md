#EPaNet Workflow

## Network file (*.inp)

Network file can be imported, having only following blocks:

1. [TITLE]
2. [JUNCTIONS]
3. [RESERVOIRS]
4. [TANKS]
5. [PIPES]
6. [PUMPS]
7. [COORDINATES]

EDIT 11-Jun-14: graphic minimum:

1. [TITLE]
2. [JUNCTIONS]
3. [PIPES]
4. [COORDINATES]


## Ex. 1: Pump Sizing

EpaNet File: EN_Workflow.inp
Excel/Result file: EN_Workflow2.xls
Python script (graph generating): en_graphs.py

1. Build EpaNet model, without pump but with tank/reservoar whose liquid level may be few millimetres above suction pipe entrance. All junction heights should be set to "0". 

2. Run Analysis. Depending on liquid level in tank/reservoar warning message saying that "Negative pressures at node XXX had been calculated" may appear. It is safe to ignore it, as we *will use pipe headloss solution*, only.

3. Open report menu, tables section, click on **Links** radio-button and on a  Columns tab check following items:
- Length
- Diameter
- Roughness
- Flow
- Velocity
- Unit Headloss
- Friction Factor
- Status   
  
Click OK.

4. Copy table to excel file EN_Workflow2.xls or similar template. Excel will perform further calculation, if file prepared properly, automatically.

5. Account end conditions as per excel file and export Headloss, height difference, Total Headloss, AH, BH, AV to csv file.    
**Note:** Use system curve with end conditions in this step!

6. Run en_graphs.py to get pipe and system headlosses diagrams (H-Q).

7. Perform <u>Sanity Check</u>. To do that, in EpaNet, set liquid level in reservoar/tank to be equal or **slightly** higher of calculated pump delivery. Run analysis - if everything OK system will be analysed without any warning messages and pressure at exit node will be close to end condition in that node.
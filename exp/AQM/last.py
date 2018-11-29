import csv    
import os
import math
import numpy as np
from tqdm import tqdm  

y_1=np.load("ymin_set.npy")
y_2=np.load("ymax_set.npy")
y_set=y_1+y_2
x_1=np.load("xmin_set.npy")
x_2=np.load("xmax_set.npy")
x_set=x_1+x_2

def improve(xmin,ymin,xmax,ymax,x_set,y_set):
    if ymax>1078.5:
        ymax=1080
    elif ymax>1077.5:
        ymax=1078
    else:
        ymax_ceil=math.ceil(ymax)
        ymax_floor=math.floor(ymax)
        if y_set[int(ymax_ceil)]>4.5:
            ymax=ymax_ceil
        elif y_set[int(ymax_floor)]>4.5:
            ymax=ymax_floor
    
    if ymin<2.0:
        ymin=0
    elif ymin<4:
        ymin=3
    elif ymin<6:
        ymin=5
    else:
        ymin_ceil=math.ceil(ymin)
        ymin_floor=math.floor(ymin)
        if y_set[int(ymin_ceil)]>4.5:
            ymin=ymin_ceil
        elif y_set[int(ymin_floor)]>4.5:
            ymin=ymin_floor
    if xmin<2:
        xmin=0
    elif xmin<4:
        xmin=3
    else:
        xmin_ceil=math.ceil(xmin)
        xmin_floor=math.floor(xmin)
        if x_set[int(xmin_ceil)]>4.5:
            xmin=xmin_ceil
        elif x_set[int(xmin_floor)]>4.5:
            xmin=xmin_floor
    if xmax>1918:
        xmax=1920
    elif xmax>1916:
        xmax=1917
    else:
        xmax_ceil=math.ceil(xmax)
        xmax_floor=math.floor(xmax)
        if x_set[int(xmax_ceil)]>4.5:
            xmax=xmax_ceil
        elif x_set[int(xmax_floor)]>4.5:
            xmax=xmax_floor
    return xmin,ymin,xmax,ymax
        
    

f=open("output.txt")
lines=f.readlines()
index_set={}
i=0
while i<len(lines):
    print i
    line=lines[i]
    if ".jpg" in line:
        index=[i]
        number=0
        frame_name=line.replace("\n","")
        for j in range(i+1,len(lines)):
            line_temp=lines[j]
            if ".jpg" in line_temp:
                i=j
                break
            else:
                number=number+1
            if j==(len(lines)-1):
                i=j
                number=number-1
                break
        index.append(number)
        index_set[frame_name]=index
    else:
        i=i+1
print "data collecting success!"
with open("last_try_3.csv","w+") as csvfile:
    writer=csv.writer(csvfile)
    for frame in tqdm(sorted(index_set.keys())):
        index_num=index_set[frame]
        start=index_num[0]
        length=index_num[1]
        if length==0:
            write_line=[]
            write_line.append(frame)
            tempstr=""
            write_line.append(tempstr)
            writer.writerow(write_line)
        else:
            for i in range(start+1,start+length+1):
                write_line=[]
                write_line.append(frame)
                tempstr=""
                line=lines[i]
                line=line.split(" ")
                xmin=float(line[0])
                ymin=float(line[1])
                xmax=float(line[2])
                ymax=float(line[3])
                w=xmax-xmin
                h=ymax-ymin
                center_x=(xmin+xmax)/2.0
                center_y=(ymin+ymax)/2.0
                xmin=center_x-w*1.01/2.0
                ymin=center_y-h*1.01/2.0
                xmax=center_x+w*1.01/2.0
                ymax=center_y+h*1.01/2.0
                score=float(line[4])
                xmin,ymin,xmax,ymax=improve(xmin,ymin,xmax,ymax,x_set,y_set)
                w=xmax-xmin
                h=ymax-ymin
                if w>0 and h>0 and score>=0.985:
                    tempstr=tempstr+str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)
                write_line.append(tempstr)
                writer.writerow(write_line)
            
    
        
        




        
    

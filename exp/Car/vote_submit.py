import csv    
f=open("output.txt")
lines=f.readlines()
index_set={}
i=0
while i<len(lines):
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
with open("submit.csv","w+") as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(["name","coordinate"])
    for frame in sorted(index_set.keys()):
        write_line=[]
        write_line.append(frame[-40:])
        thresh=0.84
        tempstr=""
        index_num=index_set[frame]
        start=index_num[0]
        length=index_num[1]
        for i in range(start+1,start+length+1):
            line=lines[i]
            line=line.split(" ")
            xmin=float(line[0])
            ymin=float(line[1])
            xmax=float(line[2])
            ymax=float(line[3])
            xmin=round(xmin,4)
            ymin=round(ymin,4)
            xmax=round(xmax,4)
            ymax=round(ymax,4)
            w=xmax-xmin
            h=ymax-ymin
            center_x=(xmin+xmax)/2.0
            center_y=(ymin+ymax)/2.0
            xmin=center_x-w*1.01/2.0
            ymin=center_y-h*1.01/2.0
            xmax=center_x+w*1.01/2.0
            ymax=center_y+h*1.01/2.0
            score=float(line[4])
            if xmin<3.1:
                xmin=0
            if ymin<3.1:
                ymin=0
            if xmax>1066.1:
                xmax=1069
            if ymax>497.1:
                ymax=500
            w=xmax-xmin
            h=ymax-ymin
            if w*h>100000:
                center_x=(xmin+xmax)/2.0
                center_y=(ymin+ymax)/2.0
                xmin=center_x-w*1.03/2.0
                ymin=center_y-h*1.03/2.0
                xmax=center_x+w*1.03/2.0
                ymax=center_y+h*1.03/2.0
                if xmin<20:
                    xmin=0.5
                if ymin<20:
                    ymin=0.5
                if xmax>=1050:
                    xmax=1068.5
                if ymax>=480:
                    ymax=499.5
            if w>0 and h>0 and score>=thresh:
                tempstr=tempstr+str(xmin)+"_"+str(ymin)+"_"+str(xmax-xmin)+"_"+str(ymax-ymin)+";"
        write_line.append(tempstr[:-1])
        writer.writerow(write_line)
            
    
        
        




        
    

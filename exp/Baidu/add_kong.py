import pandas as pd
import json
image_dicts=json.load(open("baidu_test.json"))
image_names=image_dicts["images"]
img_names=[]
out=open("sub_110.csv","a+")
csv=pd.read_csv("sub_110.csv")
group=csv.groupby("ImageId")
a=group.size()
b=a.keys()
for i in range(0,1917):
    img_name=image_names[i]["file_name"].replace(".jpg","")
    if img_name not in b:
        out.write(img_name+",")
        out.write("33,".decode("gb2312").encode("utf-8"))
        out.write("12,".decode("gb2312").encode("utf-8"))
        out.write("0.0001,".decode("gb2312").encode("utf-8"))
        out.write("0 4|0 4|0 4|\n".decode("gb2312").encode("utf-8"))
out.close()

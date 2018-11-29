import json
import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image
from collections import Counter
import cv2
from tqdm import tqdm
import os
import random

class baidu2coco(object):
    def __init__(self,rootDir,label_imgs=[],save_json_path="./baidu_train.json"):
        self.label_imgs=label_imgs
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[]
        self.annotations=[]
        self.label=[]
        self.annID=1
        self.height=1210
        self.width=3384
        
        self.label_set={33:"car",34:"motor",35:"bicycle",36:"person",38:"trunk",39:"gongjiao",40:"three"}
        self.label_list=[33,34,35,36,38,39,40]
        self.MAX_obj=200
        self.rootDir=rootDir
        self.save_json()
    def data_transfer(self):
        for num,label_file in tqdm(enumerate(self.label_imgs)):
            self.num=num
            self.label_png=label_file
            obj_flag=self.encode_png(self.label_png)
            if obj_flag==1:
                self.file_name=self.label_png.replace("_instanceIds.png",".jpg")
                self.images.append(self.image())
            
            
    
    def image(self):
        image={}
        image["height"]=self.height
        image["width"]=self.width
        image["id"]=self.num+1
        image["file_name"]=self.file_name
        return image
    
    def mask2box(self,mask):
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
    
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x
    
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)
    
        return [left_top_c, left_top_r, right_bottom_c,right_bottom_r] 
    
    def categorie(self):
        categorie = {}
        categorie['supercategory'] = self.supercategory
        categorie['id'] = len(self.label) + 1  
        categorie['name'] = self.supercategory
        return categorie
    
    def getcatid(self, label):
        for categorie in self.categories:
            if label == categorie['name']:
                return categorie['id']
        return -1
    
    def annotation(self):
        annotation = {}
        # annotation['segmentation'] = [self.getsegmentation()]
        annotation['segmentation'] = [list(map(float, self.getsegmentation()))]
        annotation['iscrowd'] = 0
        annotation['image_id'] = self.num + 1
        # annotation['bbox'] = list(map(float, self.bbox))
        annotation['bbox'] = self.bbox
        annotation["area"]=int(self.area)
        annotation['category_id'] = self.getcatid(self.supercategory)
        annotation['id'] = self.annID
        return annotation
    
    def mask2polygons(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
        bbox=[]
        for cont in contours[1]:
            [bbox.append(i) for i in list(cont.flatten())]
        return bbox 
    
    def getsegmentation(self):
        self.mask=self.instance
        return self.mask2polygons()

    def encode_png(self,label_png):
        im=Image.open(os.path.join(self.rootDir,label_png))
        img=np.array(im)
        img=img[1500:,:]
        label,obj=divmod(img,1000)
        flag=0
        for i in self.label_list:
            if np.sum(label==i)>100:
                vis = np.zeros_like(label,dtype=np.uint8)
                vis[label==i]=1
                for j in range(0,self.MAX_obj):
                    obj_vis=np.zeros_like(label,dtype=np.uint8)
                    obj_vis[obj==j]=1
                    self.instance=vis*obj_vis
                    if np.sum(self.instance)<1:
                        break
                    elif np.sum(self.instance)<100:
                        continue
                    else:
                        flag=1
                        self.area=np.sum(self.instance)
                        xmin,ymin,xmax,ymax=self.mask2box(self.instance)
                        self.supercategory=self.label_set[i]
                        if self.supercategory not in self.label:
                            self.categories.append(self.categorie())
                            self.label.append(self.supercategory)
                        self.rectangle=[xmin,ymin,xmax,ymax]
                        self.bbox=[xmin,ymin,xmax-xmin,ymax-ymin]
                        self.annotations.append(self.annotation())
                        self.annID+=1
        return flag
    def data2coco(self):
        data_coco = {}
        data_coco['images'] = self.images
        data_coco['categories'] = self.categories
        data_coco['annotations'] = self.annotations
        return data_coco
    
    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4) 
        
rootDir="/home/cvpr/dataset/FC2/train_label"
filenames=os.listdir(rootDir)
#filenames=random.sample(filenames,100)
print(filenames)
baidu2coco(rootDir,filenames, './baidu_train_2.json')
                        
                
                
            
        
            





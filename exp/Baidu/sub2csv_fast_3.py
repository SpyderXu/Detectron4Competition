from pycocotools import mask as mask_util
import numpy as np
from tqdm import tqdm
import json
from scipy import ndimage
from six.moves import cPickle as cPickle
image_dicts=json.load(open("baidu_test.json"))
image_names=image_dicts["images"]


csv=open("sub_110.csv","w")
csv.write("ImageId,")
csv.write("LabelId,")
csv.write("PixelCount,")
csv.write("Confidence,")
csv.write("EncodedPixels")
csv.write("\n")
TOL=0.000001
#mask_area_threshold=30
mask_area_threshold=15
accuracy_thresh=0.00
intersection_thresh=0.15
start=1500*3384


def load_results():
    RES_DIR="."
    res_file=RES_DIR+"/detections.pkl"
    D=cPickle.load(open(res_file,"rb"))
    return D,RES_DIR

D,RES_DIR=load_results()
version_conf='_'.join([str(i) for i in [mask_area_threshold, accuracy_thresh, intersection_thresh]])
save_dir=""

[{u'supercategory': u'gongjiao', u'id': 1, u'name': u'gongjiao'}, 
                      {u'supercategory': u'three', u'id': 2, u'name': u'three'},
                      {u'supercategory': u'car', u'id': 3, u'name': u'car'},
                      {u'supercategory': u'trunk', u'id': 4, u'name': u'trunk'}, 
                      {u'supercategory': u'bicycle', u'id': 5, u'name': u'bicycle'},
                      {u'supercategory': u'person', u'id': 6, u'name': u'person'},
                      {u'supercategory': u'motor', u'id': 7, u'name': u'motor'}]

category_list=[0,39,40,33,38,35,36,34]


for obj_class in range(1,8):
    class_name=category_list[obj_class]
    for index,(boxs, segs) in tqdm(enumerate(zip(D["all_boxes"][obj_class],D["all_segms"][obj_class]))):
        image_name=image_names[index]["file_name"]
        
        segs=np.array(segs)
        sort_idx=(-boxs[:,4]).argsort()
        
        boxs=boxs[sort_idx]
        segs=segs[sort_idx]
        
        all_mask=None
        res_segs=[]
        res_boxes=[]
        all_mask_no_refine=None
        
        for b,rle in zip(boxs,segs):
            if b[-1]<accuracy_thresh:
                continue
            mask_int_orig=mask_util.decode(rle)
            xmin=int(b[0])-3
            ymin=int(b[1])-3
            xmax=int(b[2])+3
            ymax=int(b[3])+3
            if xmin<0:
                xmin=0
            if ymin<0:
                ymin=0
            if xmax>=3384:
                xmax=3383
            if ymax>=1210:
                ymax=1219
            w=xmax-xmin
            h=ymax-ymin
            instance_int=mask_int_orig[ymin:ymax,xmin:xmax]
            instance_int=ndimage.morphology.binary_fill_holes(instance_int.copy()).astype(np.uint8)
            instance_rect=instance_int>0
            
            
            pixel_count=(instance_rect>0).sum()
            if pixel_count>15:
                csv.write("{},".format(image_name.replace(".jpg","")))
                csv.write("{},".format(str(class_name)))
                csv.write("{},".format(str(pixel_count)))
                csv.write("{},".format(str(b[-1])))
                
                begin = 0
                length = 0
                check = 0
                idmap1d = np.reshape(instance_rect>0,(-1))
                find = False
                Totalcount=pixel_count
                #print("fast:")
                for index in range(idmap1d.shape[0]):
                    if find:
                        if idmap1d[index]:
                            length = length+1
                        else:
                            begin_div=begin//w
                            begin_mod=begin%w
                            begin_true=(ymin+begin_div)*3384+xmin+begin_mod
                            csv.write("{} {}|".format(begin_true+start,length))
                            check = check + length
                            length = 0
                            find = False
                    else:
                        if idmap1d[index]:
                            begin = index
                            length = 1
                            find = True
                    if index == idmap1d.shape[0]-1 and find:
                        begin_div=begin//w
                        begin_mod=begin%w
                        begin_true=(ymin+begin_div)*3384+xmin+begin_mod
                        csv.write("{} {}|".format(begin_true+start,length))
                        check = check + length
                        length = 0
                        find = False
                csv.write("\n")
                if Totalcount !=check:
                    print("failed!{}vs{}.".format(Totalcount,check))
                check = 0

                

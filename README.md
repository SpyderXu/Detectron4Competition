# D4C
## Detectron for Competition
Detectron is Facebook AI Research's software system that implements state-of-the-art object detection algorithms, most common used algorithms platform for competition. It is easy to obtain good results for object detection and instance segmentation competition. This sources contrain the source code for belows ,and the purpose of this open source is to give some ideas for Novice.<br> 
>   [DC: Traffic jam car detection 3rd](http://www.dcjingsai.com/common/cmpt/%E4%BA%A4%E9%80%9A%E5%8D%A1%E5%8F%A3%E8%BD%A6%E8%BE%86%E4%BF%A1%E6%81%AF%E7%B2%BE%E5%87%86%E8%AF%86%E5%88%AB_%E6%8E%92%E8%A1%8C%E6%A6%9C.html)<br>
>   [DF: Safety hat detection 3rd](https://www.datafountain.cn/competitions/304/details)<br>
>   [DF: Video Segmentation Challenge 2nd](https://www.datafountain.cn/competitions/324/details)<br>
>   [Kaggle: Airbus Ship Detection Challenge (Part solution) 23/884](https://www.kaggle.com/c/airbus-ship-detection)<br>
## Detectors and detection tricks in Detectron
Detectron supplies [Fast RCNN](https://arxiv.org/abs/1504.08083), [Faster RCNN](https://arxiv.org/abs/1506.01497), [FPN](https://arxiv.org/abs/1612.03144), [RetinaNet](https://arxiv.org/abs/1708.02002), [MaskRCNN](https://arxiv.org/pdf/1703.06870v1.pdf). We could learn a lot from this series of work. Besides, Detectron also provides different kinds of base network which could be found under the configs folder.<br> 
Detectron also provides some detection tricks. Reading the config.py and the yaml file under test_time_aug folder carefully, you would find how to open them.<br> 
>   [Soft-nms](http://cn.arxiv.org/abs/1704.04503)<br>
>   Box voting <br>
>   TTA<br>
>   Multi_scale Training<br>
>   Multi_scale testing<br>
## The verison of Detectron
> [Official Verison](https://github.com/facebookresearch/Detectron): More reliable, faster to train and test and at the same time more GPU memory needed. The caffe2 is difficult to configure, has less documents, and is difficult to improve. It may be difficult to do some changes.<br>
> [Pytorch Verison](https://github.com/roytseng-tw/Detectron.pytorch): May have some bugs, slower to train and test compared with official verison, GPU memory optimization seems better. Easy to deploy and more documents, so it is easy to do some improvement.<br>
## Other Works based on detectron
> [PANet](https://github.com/ShuLiu1993/PANet): Does not see obvious improvement. <br>
> [Cascade-RCNN](https://github.com/zhaoweicai/Detectron-Cascade-RCNN): Performs better than the faster rcnn + FPN on kitti val dataset (splited as subCNN)
## Solutions and Ideas
In this section, I would intorduce the concrete methods adopted for competition.
### [DC: Traffic jam car detection](http://www.dcjingsai.com/common/cmpt/%E4%BA%A4%E9%80%9A%E5%8D%A1%E5%8F%A3%E8%BD%A6%E8%BE%86%E4%BF%A1%E6%81%AF%E7%B2%BE%E5%87%86%E8%AF%86%E5%88%AB_%E6%8E%92%E8%A1%8C%E6%A6%9C.html)
The purpose of this competition is to detect the cars from the pictures which are captured from the traffic jam. The detailed information about this competition could be found on their website. Overall, it is an easy competition.
#### Solution
> ##### Data Augmentation: 
> As this dataset contains the scenes in day and night, so do gamma transformation randomly for each picture.<br>
> H-flip<br>
> Multi-scale Training: five kinds of scales<br>
> ##### Network Structure:
> Faster RCNN + FPN , Base Network: X-101-64x4d <br>
> ##### Test Time Augmentation
> H-flip <br>
> Multi_scale testing: Larger scales could be adopted during inference compared with the training procedure.<br>
> ##### Test Time Common Tricks:
> Soft-nms: threshold 0.43.<br>
> Box-voting: threshold 0.8. <br>
> ##### Test Time Uncommom Trick:
> Float representation of the (x,y,w,h) is better than int representation if you do not have more trick to do approximate.<br>
> Enlarging the rectangle to 1.1 times of the predicted boxes could boost the score because of hand labeling<br>
> Approximating the x,y which is too small(large) to zero(width or hight of the picture) could boost score because of hand labeling.<br>
### [DF: Safety hat detection](https://www.datafountain.cn/competitions/304/details)
The purpose of this competition is to detect the safety hat from the pictures. The detailed information about this competition could be found on their website. Overall, it is also an easy competition.
#### Solution
> The solution of safety hat detection is similar to car detection. The differences are the adopted scales during multi-scale training and multi-scale testing.
> ##### Some ideas that we not try:
> 1) Save the results of different model before nms then ensemble the results and do final soft-nms<br>
### [DF: Video Segmentation Challenge](https://www.datafountain.cn/competitions/324/details)
This is an instance segmentation competition which is a bit complicate compared with purely detection challenge. The competition has appeared in [Kaggle:CVPR 2018 WAD Video Segmentation Challenge](https://www.kaggle.com/c/cvpr-2018-autonomous-driving) before the [DF: Video Segmentation Challenge](https://www.datafountain.cn/competitions/324/details) (interesting phenomenon). You may find some solution in kaggle.
#### Solution
> The solution is similar with above solution. The differences are the adopted scales during multi-scale training and multi
> scale testing. Here, I introduce some new ideas:
> ##### network paramter
> Crop the image from 3384 * 2710 to 2284 * 1210
> Change the ROI align resolution for object detection from 7 * 7 to 14 * 14
> Change the ROI align resolution for instance segmentation
> ##### Some ideas that we have no time to try
> 1) More training augmentation: It is easy to expand the detectron with H-flip,V-flip, change the brightness or other attributes of the images, but difficult to do random crop. You may do random crop before training. 
> 2) Change the softmax classification loss to focal loss to balance the classes.
> 3) Change the Cross Entropy Loss（instance segmentation loss）to Dice loss or other new semantic segemtation loss.
> 4) PANet may be better.
> 5) [Cascade-RCNN](https://github.com/zhaoweicai/Detectron-Cascade-RCNN) may be better. The Cascade-RCNN performs about 0.1 higher than Faster RCNN + FPN (metric: ap), so it may be a better solution for the other two object detection competition.
### [Kaggle: Airbus Ship Detection Challenge](https://www.kaggle.com/c/airbus-ship-detection)
The Airbus ship detection challenge 







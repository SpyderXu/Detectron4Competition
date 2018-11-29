This folder contains the code and config file for Baidu Instance Segmentation Challenge
#### Pipeline:
> 1): Change the dataset to COCO format and config dataset_catalog.py. You may get some ideas from convert4coco.py. The crop_img.py could crop the original image.<br>
> 2): Train the network with the config file, some parameters may need to edit.<br>
> 3): Do inference, the test_net.py support multi-gpu-testing, and would generate the detections.pkl<br>
> 4): Adopt the sub2csv_fast_3.py to do some post processing and generate the submit file.<br>

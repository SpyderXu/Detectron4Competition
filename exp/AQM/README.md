This folder contains the code and config file for safety hat detection
#### Pipeline:
> 1): Change the dataset to COCO format and config dataset_catalog.py.<br>
> 2): Train the network with the config file, some parameters may need to edit.<br>
> 3): Do inference, the test_net.py support multi-gpu-testing, you can read the original Detectron the find out the usage. In this place ,I adopt the infer_xcz.py to do inference which would generate the output.txt file.<br>
> 4): Adopt the last.py to do some post processing and generate the submit file.<br>

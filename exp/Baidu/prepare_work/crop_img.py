import os
import cv2
from tqdm import tqdm
rootDir="/data/XCZ/baidu/train"
save_dir="/data/XCZ/baidu/train_crop"
filenames=os.listdir(rootDir)
filenames.sort(key=str.lower)
filenames=filenames[:10000]
for filename in tqdm(filenames):
    img_path=os.path.join(rootDir,filename)
    im=cv2.imread(img_path)
    im=im[1500:,:,:]
    cv2.imwrite(os.path.join(save_dir,filename),im)

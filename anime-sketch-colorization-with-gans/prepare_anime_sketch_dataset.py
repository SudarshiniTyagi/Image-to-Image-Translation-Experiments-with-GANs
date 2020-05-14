import os
from pdb import set_trace
from PIL import Image
import numpy as np
from tqdm import tqdm
import sys

if sys.version_info >= (3, 7):
    import zipfile
else:
    import zipfile37 as zipfile

print("Extracting the ZipFile ...")

# with zipfile.ZipFile('anime-sketch-colorization-pair.zip', 'r') as zipObj:
#    # Extract all the contents of zip file in temp directory
#    zipObj.extractall('temp')


ugatit_dataset = "UGATIT-pytorch/dataset/sketch2anime"
cyclegan_and_pix2pix_dataset = "pytorch-CycleGAN-and-pix2pix/datasets/sketch2anime"
folders = {
	"train": ("train", "temp/data/train"),
	"test": ("val", "temp/data/val")
}

def pil_loader(path):
  # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
  with open(path, 'rb') as f:
      img = Image.open(f)
      return img.convert('RGB')

print("Preparing the dataset for the UGATIT-pytorch...")

if not os.path.exists(f"{ugatit_dataset}"):
	os.makedirs(f"{ugatit_dataset}")
	os.makedirs(f"{ugatit_dataset}/trainA")
	os.makedirs(f"{ugatit_dataset}/trainB")
	os.makedirs(f"{ugatit_dataset}/testA")
	os.makedirs(f"{ugatit_dataset}/testB")

if not os.path.exists(f"{cyclegan_and_pix2pix_dataset}"):
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/train")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/val")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/trainA")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/trainB")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/testA")
	os.makedirs(f"{cyclegan_and_pix2pix_dataset}/testB")

for _type, (_type2, folder) in folders.items():
	for filepath in tqdm(os.listdir(folder)):
		image = pil_loader(folder + "/" + filepath)
		image = np.asarray(image)

		color_part = image[:, :512, :]
		sketch_part = image[:, 512:, :]
		color = Image.fromarray(np.uint8(color_part))
		sketch = Image.fromarray(np.uint8(sketch_part))
		
		sketch.save(f"{ugatit_dataset}/{_type}A/{filepath}")
		color.save(f"{ugatit_dataset}/{_type}B/{filepath}")
		sketch.save(f"{cyclegan_and_pix2pix_dataset}/{_type}A/{filepath}")
		color.save(f"{cyclegan_and_pix2pix_dataset}/{_type}B/{filepath}")
		
		image_order_change = np.concatenate((sketch_part, color_part), axis=1)
		image_order_change = Image.fromarray(np.uint8(image_order_change))
		image_order_change.save(f"{cyclegan_and_pix2pix_dataset}/{_type2}/{filepath}")
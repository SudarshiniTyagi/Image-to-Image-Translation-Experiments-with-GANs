# anime-sketch-colorization-with-gans
Comparison of various GANS for anime sketch colorization task 

- download the anime-sketch-colorization-pair data from the 
write steps how to get the data from kaggle



### Installations

### Download the Dataset
* Manual
	* Download the anime-sketch-colorization-pair from the [Kaggle Link](https://www.kaggle.com/ktaebum/anime-sketch-colorization-pair) into root folder.
* Use Kaggle API
	* Sign up/Log In to [https://www.kaggle.com](https://www.kaggle.com)
	* Go to the 'Account' tab of your user profile and create API Token.
```bash
export KAGGLE_USERNAME=datadinosaur
export KAGGLE_KEY=xxxxxxxxxxxxxx
kaggle datasets download -d ktaebum/anime-sketch-colorization-pair
```

### How to run the repository
* UGATIT
```bash
cd UGATIT-pytorch/
python main.py --dataset sketch2anime --light=True
```
* Pix2Pix
```bash
cd pytorch-CycleGAN-and-pix2pix
python train.py --dataroot ./datasets/sketch2anime --name sketch2anime_pix2pix --model pix2pix --direction AtoB --display_id -1
```

* CycleGan
```bash
cd pytorch-CycleGAN-and-pix2pix
python train.py --dataroot ./datasets/sketch2anime --name sketch2anime_cyclegan --model cycle_gan --display_id -1
```

Changes:
Pix2Pix

### Other works on the anime-sketch-colorization




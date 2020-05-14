from flask import Flask, url_for, render_template, request, redirect
from markupsafe import escape
from pdb import set_trace
import os
from PIL import Image
import numpy as np
import subprocess
import time
from pdb import set_trace

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = (os.path.join(os.getcwd(), "GAN-Experiments/static"))
port = int(os.getenv("PORT"))
# Bootstrap(app)

@app.route('/')
def index():
	return render_template('compare_gan_uploader.html')

# landing page for the single dataset evaluation
@app.route('/evaluate/<dataset>')
def evaluate(dataset):
	if dataset == "nyu_depth":
		return render_template('nyu_depth_uploader.html')
	elif dataset == "c_c":
		return render_template('c_c_uploader.html')
	elif dataset == "old_young2":
		return render_template('old_young2_uploader.html')
	else:
		abort(500)

def pil_loader(path):
  # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
  with open(path, 'rb') as f:
      img = Image.open(f)
      return img.convert('RGB')

@app.route('/results/<dataset>')
def result(dataset):
	# combining image for pix2pix
	A = pil_loader(os.path.join(app.config['UPLOAD_FOLDER'], dataset, "testA", "A.png"))
	if A.size != (512, 512):
		A = A.resize((512, 512))
	A = np.asarray(A)
	B = pil_loader(os.path.join(app.config['UPLOAD_FOLDER'], dataset, "testB", "B.png"))
	if B.size != (512, 512):
		B = B.resize((512, 512))
	B = np.asarray(B)

	AB = np.concatenate((A, B), axis=1)
	AB = Image.fromarray(np.uint8(AB))
	AB.save(os.path.join(app.config['UPLOAD_FOLDER'], dataset, "test", "AB.png"))
	timing = {}
	start = time.time()
	subprocess.call("(cd anime-sketch-colorization-with-gans/pytorch-CycleGAN-and-pix2pix && python3 test.py --dataroot ./../../GAN-Experiments/static/sketch2anime --name sketch2anime_pix2pix --model pix2pix --direction AtoB --results_dir ./../../GAN-Experiments/static/sketch2anime/results)", shell=True)
	timing["pix2pix"] = round(time.time() - start, 2)
	
	start = time.time()
	subprocess.call("(cd anime-sketch-colorization-with-gans/pytorch-CycleGAN-and-pix2pix && python3 test.py --dataroot ./../../GAN-Experiments/static/sketch2anime --name sketch2anime_cyclegan --model cycle_gan --results_dir ./../../GAN-Experiments/static/sketch2anime/results)", shell=True)
	timing["cycle_gan"] = round(time.time() - start, 2)
	
	start = time.time()
	subprocess.call("(cd anime-sketch-colorization-with-gans/UGATIT-pytorch && python3 main.py --dataset sketch2anime --datapath ../../GAN-Experiments/static/sketch2anime --phase test --device cpu --light True --output_dir ../../GAN-Experiments/static/sketch2anime/results)", shell=True)
	timing["ugatit"] = round(time.time() - start, 2)
	return render_template('compare_gan_result.html', timing = timing)

@app.route('/single_results/<dataset>')
def single_result(dataset):
	timing = {}
	start = time.time()
	subprocess.call(f"(cd anime-sketch-colorization-with-gans/UGATIT-pytorch && python3 main.py --dataset {dataset} --datapath ../../GAN-Experiments/static/{dataset} --phase test --device cpu --light True --output_dir ../../GAN-Experiments/static/{dataset}/results)", shell=True)
	timing["ugatit"] = round(time.time() - start, 2)
	if dataset == "nyu_depth":
		return render_template('nyu_depth_result.html', timing = timing)
	elif dataset == "c_c":
		return render_template('c_c_result.html', timing = timing)
	elif dataset == "old_young2":
		return render_template('old_young2_result.html', timing = timing)
	else:
		abort(500)

@app.route('/clears')
def clear():
	# delete the input images	# reset the page
	# os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "sketch.jpeg"))
	# os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "color.jpeg"))
	return redirect(url_for('index'))

@app.route('/upload/<dataset>/<type>', methods=['POST'])
def upload_file(dataset, type):
	file = request.files['file']
	if type == "A":
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], dataset, "testA", "A.png"))
	elif type == "B":
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], dataset, "testB", "B.png"))
	if dataset == "nyu_depth":
		return render_template('nyu_depth_uploader.html')
	elif dataset == "c_c":
		return render_template('c_c_uploader.html')
	elif dataset == "old_young2":
		return render_template('old_young2_uploader.html')
	else:
		return render_template('compare_gan_uploader.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
    # app.run(host='localhost', port=8001)


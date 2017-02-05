import os
import sys
sys.path.insert(0, 'D:/WenyuLv/caffe-windows/caffe-master/Buildx/x64/Release/pycaffe/')
import caffe
import random
from skimage import io, transform
import numpy as np
import logging
import time
from multiprocessing import Pool #when batch_size is very large
import codecs

class data_layer(caffe.Layer):

	def _image_preprocess(self, img):

		#img = transform.rescale(img, 0.3)*255.0
		img = img - [123.0, 117.0, 104.0]

		if self.random_crop and self.phase:

			#try:
			#	hc, wc = int(img.shape[0]/2), int(img.shape[1]/2)
			#	
			#	shift = np.random.choice([-30, -15, 0, 15, 30], size=2, p=[0.1, 0.2, 0.4, 0.2, 0.1])
			#	hcn , wcn= hc+shift[0], wc+shift[1]

			#	if (hcn-112)>=0 and (wcn-112)>=0 and (hcn+112)<img.shape[0] and (wcn+112)<img.shape[1]:
			#		img = img[hcn-112: hcn+112, wcn-112: wcn+112, :] #self._crop_size
			#	else:
			#		img = img[hc-112: hc+112, wc-112: wc+112, :]

			#except:

			#	hc, wc = int(img.shape[0]/2), int(img.shape[1]/2)
			#	img = img[hc-112: hc+112, wc-112: wc+112, :]


			h_off = max(0, random.randint(0, img.shape[0] - self.random_crop))
			w_off = max(0, random.randint(0, img.shape[1] - self.random_crop))

			if h_off+self.random_crop< img.shape[0] and w_off+self.random_crop< img.shape[1]:
				img = img[h_off: h_off+self.random_crop, w_off: w_off+self.random_crop, :]
			else:
				hc, wc = int(img.shape[0]/2), int(img.shape[1]/2)
				img = img[hc-112: hc+112, wc-112: wc+112, :]


		if self.mirror and random.random()<0.5 and self.phase:
			img = img[:, ::-1, :]

		img = img[:,:,[2,1,0]]
		img = np.transpose(img, [2, 0, 1])
		
		#print img.shape
		return img

	def _load_next_batch(self):


		if self._cur+self.batch_size >= len(self._lines):
			self._cur = 0
			if self.shuffle: self._perm = np.random.permutation(np.arange(len(self._lines)))

		data = []
		label = []

		for i in self._perm[self._cur: self._cur+ self.batch_size]:
			
			path, lab = self._lines[i].strip().split('\t') # 

			try:

				img = io.imread(path)

				if self.phase==1 and img.shape[0]>750 and img.shape[1]>750 :

					img = transform.rescale(img, 0.3)*255.0
					img = self._image_preprocess(img)
					data.append(img)
					label.append(int(lab))

				if self.phase==0:

					img = transform.resize(img, [224,224])*255.0
					img = self._image_preprocess(img)
					data.append(img)
					label.append(int(lab))

			except:

				print 'load xxx',
				continue


		self._cur += self.batch_size
		
		return np.array(data), np.array(label)


	def setup(self, bottom, top):

		layer_params = eval(self.param_str)
		self.data_file = layer_params['data_file']
		self.batch_size = layer_params['batch_size']
		self.shuffle = 1 #layer_params['shuffle']
		self.mirror = 1 #layer_params['mirror']
		
		self.random_crop = 224 #layer_params['crop_size']
		self.phase = layer_params['phase']

		top[0].reshape(1, 3, 224, 224)
		print top[0].data.shape

		top[1].reshape(1, 1)

		with codecs.open(self.data_file, 'r', 'utf-8') as f:
			self._lines = f.readlines()

		print 'Total images: {}.'.format(len(self._lines))

		#random.shuffle(self._lines)
		#self.batchs_per_epoch = int(len(self.lines) / self.batch_size)
		self._cur = 0
		self._perm = np.random.permutation(np.arange(len(self._lines)))



	def forward(self, bottom, top):

		#start = time.time()
		#logging.warning('{}'.format('xxxxxxx'))

		data, label= self._load_next_batch()
		#print data.shape, label.shape

		
		top[0].reshape(*(data.shape))
		top[0].data[...] = data

		top[1].reshape(*(label.shape))
		top[1].data[...] = label


		#logging.warning('{}'.format(time.time()-start))

	def reshape(self, bottom, top):
		
		#print top[0].data.shape
		#print top[1].data.shape
		pass

	def backward(self, top, propagate_down, bottom):
		pass


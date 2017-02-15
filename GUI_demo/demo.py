# -*- coding: utf-8 -*-  


import os  
import re
import sys  
import time  
import chardet  
import datetime  
import tkFileDialog  
import tkMessageBox  
from   Tkinter import *  

import caffe
import numpy as np
import matplotlib.pyplot as plt
from skimage import transform, io



car_style_rear = [u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x',
u'x']


img_filename = u''
model_filename = u''
net_filename = u''

net = ''

def get_img_file():  
	global img_filename
	img_filename = tkFileDialog.askopenfilename(filetypes=[("text file", "*.jpg")])  
	var_img.set(img_filename)  


def get_net_file():  
	global net_filename
	net_filename = tkFileDialog.askopenfilename(filetypes=[("text file", "*.prototxt")])  
	var_net.set(net_filename) 

def get_model_file():  
	global model_filename  
	global net

	model_filename = tkFileDialog.askopenfilename(filetypes=[("binary file", "*.caffemodel")])  
	var_model.set(model_filename) 

	net = caffe.Net(str(net_filename), str(model_filename), caffe.TEST)

def show_result(info):  
	tkMessageBox.showinfo("result ", info)  


def net_init(net, model):

	net = caffe.Net(net, model, caffe.TEST)

	return net

def img_process(img, size=[224, 224]):

	img = transform.resize(img, size)*255.0
	img = img - [123.0, 117.0, 104.0]
	img = img[:,:,[2,1,0]]
	img = np.transpose(img, [2, 0, 1])
	return np.expand_dims(img, 0)


def run():

	global img_filename  
	global model_filename
	global net_filename
	global net
	#net = net_init(net_filename, model_filename)
	#net = caffe.Net(str(net_filename), str(model_filename), caffe.TEST)

	im = plt.imread(img_filename)
	im = img_process(im)


	net.blobs['data'].data[...] = im
	res = net.forward()['prob'][0].argmax()

	info = u'{}'.format(car_style_rear[res])

	var_label.set(info)
	#info = '{}\n {}\n'.format(net_filename , model_filename)

	show_result(info) 

if __name__ == '__main__':  
	#reload(sys)  
	#sys.setdefaultencoding('utf-8')  
	
	root = Tk()  
	root.title("car label recognition")  
	root.geometry("400x200+450+210") #width x height; start coor
	
	frame = Frame(root)
	frame.pack()
	
	frm_1 = Frame(frame)
	var_img = StringVar()  
	Label(frm_1,text="").pack()  
	Entry(frm_1,textvariable=var_img,bd=1, width=25).pack(expand=1, side=LEFT) 
	Button(frm_1,text="select image",command=get_img_file,height=1,width=10).pack(side=RIGHT)
	frm_1.pack()
	

	frm_2 = Frame(frame)
	var_net = StringVar()
	Entry(frm_2,textvariable=var_net,bd=1, width=25).pack(expand=1, side=LEFT) 
	Button(frm_2,text="select net",command=get_net_file,height=1,width=10).pack(side=RIGHT)
	frm_2.pack()


	frm_3 = Frame(frame)
	var_model = StringVar()  
	Entry(frm_3,textvariable=var_model,bd=1, width=25).pack(expand=1, side=LEFT) 
	Button(frm_3,text="select model",command=get_model_file,height=1,width=10).pack(side=RIGHT)
	frm_3.pack()


#	frm_4 = Frame(frame)
#	var_img = StringVar()  
#	Label(frm_1,text=var_img).pack() 
#	frm_1.pack()

	
	frm_res = Frame(root)  
	Label(frm_res,text="").pack() 
	Label(frm_res,text="Label : ").pack(side=LEFT) 
	#Label(frm_res,text="").pack() 
	#Label(frm_res,text="").pack() 
	var_label = StringVar()
	Label(frm_res,textvariable=var_label).pack()  
	frm_res.pack()  #side=BOTTOM


	frm_D = Frame(root)  
	Button(frm_D,text="run",command=run,height=2,width=10).pack(side=LEFT)
	Button(frm_D,text="exit",command=root.quit,height=2,width=10,bg="#B0D060").pack()  
	frm_D.pack(side=BOTTOM) 
	

	

	root.mainloop()  
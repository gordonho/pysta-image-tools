#conding : utf-8

'''
2018-01-29
author: gordon
把图片切分为九宫格，用于发布到社交网络：微信、微博
'''

import clipboard
from PIL import Image,ImageFilter
import console
import appex
from six.moves import input
import math
from enum import Enum
import photos

num = 9
col = 3
image_path = './album'
im = clipboard.get_image(idx=0)
is_debug = False

class info_type(Enum):
	error = 0
	info = 1
	debug = 2

def resize_auto_scale(im, ww, hh):
	"""按照宽度进行所需比例缩放"""
	(x, y) = im.size
	scale = x/y
	square_size = 0
	if x < y:
		x_s = math.ceil(hh*scale)
		y_s = hh
		square_size = x_s
	else:
		scale = y/x
		x_s = ww
		y_s = math.ceil(ww*scale)
		square_size = y_s
	printEx('resize: w %d,h %d,scale %f,size %d' %(x_s,y_s,scale,square_size),info_type.info)
	out = im.resize((x_s, y_s), Image.ANTIALIAS)
	is_square = ww == hh
	if is_square:
		_x = math.floor((x_s-square_size)/2)
		_y = math.floor((y_s-square_size)/2)
		_box = [_x,_y,x_s-_x,y_s-_y]
		out = out.crop(_box)
		printEx(_box)
	return out

def printEx(value,itype=info_type.info):
	if is_debug:
		print(value)
	elif itype != info_type.debug:
		print(value)

def getAlbum(album_name):
	albums = photos.get_albums()
	for ab in albums:
		if ab.title == album_name:
			return ab
	return photos.create_album(album_name)

def save2Album(image_files):
	album_name = 'pythonEx'
	printEx('Save to Album: %s' % album_name)
	asset_collections = getAlbum(album_name)
	assets = []
	for f in image_files:
		_asset = photos.create_image_asset(f)
		assets.append(_asset)
	asset_collections.add_assets(assets)
	#printEx(assets,info_type.debug)

def split():
	console.clear()
	printEx('Now spliting ...')
	if not im:
		printEx('Please select one picture.')
		return
	im1 = resize_auto_scale(im,1024,1024)
	(w,h) = im1.size
	ww = math.floor(w / col)
	hh = math.floor(h / (num /3))
	printEx(im1.size,info_type.info)
	imgs = []
	boxs = []
	for i in range(num):
		_x = (i % col)*ww
		_y = math.floor((i)/col) * hh
		
		printEx('[%d] x:%d,y:%d,w:%d,h:%d'%(i,_x,_y,ww,hh),info_type.info)
		boxs.append((_x,_y,ww+_x,hh+_y))
		
		_img = im1.crop([_x,_y,ww+_x,hh+_y])
		imgs.append(_img)
		printEx(_img.size,info_type.debug)
		printEx(_img.mode,info_type.debug)

	printEx(boxs, info_type.debug)
	image_files = []
	for _idx,ix in enumerate(imgs):
		_f_name = '%s/split_%d.jpg'%(image_path,_idx)
		ix.save(_f_name)
		image_files.append(_f_name)
	printEx('\nsucess!!save to %s'%image_path)

	save2Album(image_files)
	

if __name__ == '__main__':
	split()

#conding : utf-8

'''
2018-01-29
author: gordon
图片拼接，用于发布到社交网络：微信、微博
有两种运行模式：正常模式、扩展模式
'''

import clipboard
from PIL import Image,ImageFilter
import console
import appex
from six.moves import input
import math
from enum import Enum
import photos

#im1 = clipboard.get_image(idx=0)
#im2 = clipboard.get_image(idx=1)

background = Image.new('RGBA', (746, 792), (255, 255, 255, 255))
#background = Image.new('RGBA', (2436, 1125), (255, 255, 255, 255))

#iphone x
#setW = 366
#setH = 792
setW = 562
setH = 1218

#ext mode
mode_ext = False
is_debug = False

span = 2
max_imags = 20

#要处理的图片集
image_list = []

class info_type(Enum):
	error = 0
	info = 1
	debug = 2

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

def fixed_size(im, width, height):
	"""按照固定尺寸处理图片"""
	out = im.resize((width, height),Image.ANTIALIAS)
	return out
	
def resize_auto_scale(im, ww, hh):
	"""按照宽度进行所需比例缩放"""
	(x, y) = im.size
	scale = x/y
	if x < y:
		x_s = math.ceil(hh*scale)
		y_s = hh
	else:
		scale = y/x
		x_s = ww
		y_s = math.ceil(ww*scale)
	print('resize: w %d,h %d' %(x_s,y_s))
	
	background = im.crop([0,0,ww,hh])
	#background.filter(ImageFilter.BLUR)
	out = im.resize((x_s, y_s), Image.ANTIALIAS)
	_pos_y = math.floor((hh-y_s)/2)
	_pos_x = math.floor((ww-x_s)/2)
	background.paste(out,(_pos_x,_pos_y))
	return background
	'''
	if y_s < hh:
		background = im.crop([0,0,ww,hh])
		background.filter(ImageFilter.BLUR)
		out = im.resize((x_s, y_s), Image.ANTIALIAS)
		_pos_y = math.floor((hh-y_s)/2)
		background.paste(out,(0,_pos_y))
		return background
	else:
		out = im.resize((x_s, y_s), Image.ANTIALIAS)
		return out
	'''

def getClipboardImages():
	_sizs = []
	_scales = []
	for i in range(max_imags):
		_im = clipboard.get_image(idx=i)
		if not _im:
			break
		else:
			image_list.append(_im)
			_sizs.append(_im.size)
			(w,h) = _im.size
			_scales.append(round(w/h,2))
			
	print('clipboard images:{}{}'.format(_sizs,_scales))
	return image_list

def getSelectImages():
	_sizs = []
	_scales = []
	images = appex.get_images()
	if len(images)>1:
		for _im in images:
			#if i < max_imags:
			image_list.append(_im)
			_sizs.append(_im.size)
			(w,h) = _im.size
			_scales.append(round(w/h,2))
			
	print('select images:{}{}'.format(_sizs,_scales))
	return image_list

def joinImagesEx(imgs, num_per_line=0):
	if not imgs:
		print('Select one more picture')
		return
	num = len(imgs)
	if num < 2:
		print('at least 2 picture selected')

	if num_per_line == 0:
		background = Image.new('RGBA', ((setW+span)*num, setH), (255, 255, 255, 255))
		for i in range(num):
			_im = imgs[i].resize((setW, setH), Image.ANTIALIAS)
			pos = i * (setW+span)
			background.paste(_im, (pos, 0))	
	else:
		w = (setW+span)*num_per_line
		h = (span+setH)*(math.ceil(num/num_per_line))
		background = Image.new('RGBA', (w, h), (255, 255, 255, 255))
		print('h:%d,w:%d,count:%d,column:%d'%(h,w,num,num_per_line))
		_pre_y = 0
		for i in range(num):
			_im = resize_auto_scale(imgs[i],setW,setH)
			#_im = imgs[i].resize((setW, setH), Image.ANTIALIAS)
			print('resize images %d' % i)
			posX = i%num_per_line * (setW+span)
			posY = math.floor((i)/num_per_line) * (setH+span)
			
			background.paste(_im, (posX, posY))
			_pre_y = _im.size[1]
			print('paste images %d.x:%d,y:%d' % (i,posX,posY))
	
	_file = './album/ss_join.jpg'
	background.save(_file)
	save2Album([_file])
	#clipboard.set_image(background, format='jpeg', jpeg_quality=0.90)
	
	if num_per_line != 1 and not mode_ext:
		background.show()

	console.hide_activity()
	print("\nImage save to Ablum")

def main(col=2):
	print('\n')
	#console.clear()
	print("Generating image...")
	console.show_activity()
	'''
	if mode_ext:
		imgs = getSelectImages()
	else:
		imgs = getClipboardImages()
	'''
	
	joinImagesEx(image_list,col)
	

if __name__ == '__main__':
	console.clear()
	#print('\n')
	print("运行模式")
	print("[1] 插件")
	print("[2] 正常")
	mode = input("模式(默认为 2): ")
	if mode == '1':
		mode_ext = True
	if mode_ext:
		getSelectImages()
	else:
		getClipboardImages()
	
	print('\n')
	print("请选择图片分辨率")
	print("[1] iphon X")
	print("[2] 1024x768")
	print("[3] 600x800")
	print("[4] 320x568 iphone5")
	print("[5] 自定义")
	set_mode = input("请选择(默认为 1):")
	if set_mode == "x":
		print("Exited")
		exit(1)
	elif set_mode == "2":
		setW = 1024
		setH = 768
	elif set_mode == "3":
		setW = 600
		setH = 800
	elif set_mode == "4":
		setW = 320
		setH = 568
	elif set_mode == "5":
		fbl = input("请输入分辨率(如1024x768):")
		if 'x' in fbl:
			try:
				(w,h)=fbl.split('x')
				setW = int(w)
				setH = int(h)
			except Exception:
				print('输入的分辨率有误:%s'%fbl)
				exit(2)
			print('custom: %s,%d-%d'%(fbl,setW,setH))

	print('\n')
	print("每行几张图片: 0--9")
	print("0 所有照片模向排列")
	col = input("请输入列数(默认为 1): ")
	
	if col == "":
		col = 1
		
	#执行主程序
	main(int(col))


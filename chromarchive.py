import cv2
import numpy as np
from optparse import OptionParser
import re
import os


#TODO : Check if the filenames found during exploration match a real file
def exploreCamerasPath(cameras_path,cameras_pattern):
	#Check if the cameras path we guessed exists
	cameras_id = []
	if os.path.isdir(cameras_path):
		
		for dir in os.listdir(cameras_path):
			id = extractNumber(cameras_pattern,dir)
			if id != []:
				cameras_id.append(id)

		if len(cameras_id) > 0:
			print str(len(os.listdir(cameras_path))) + " cameras detected : " + str(getMinMax(cameras_id))
			return os.listdir(cameras_path)
		else : 
			print "Unable to match cameras folders witch pattern: " + cameras_pattern	

def exploreImagesPath(images_path,images_pattern,image_format):
	images_id = []
	if os.path.isdir(images_path):
		
		for image in os.listdir(images_path): 
			id =  extractNumber(images_pattern,image,image_format)
			if id != []:
				images_id.append(id)
		if len(images_id) > 0:
			print str(len(images_id)) + " images detected : " + str(getMinMax(images_id))
			return os.listdir(images_path)

# Assumes that an image file is ALWAYS ended by a file format (.png, .jpg ...)
def getImageFormat(image_path):
	return  "."+image_path.split('.')[-1]

def extractNumber(pattern,image_path,file_format=""):
	search_pattern = pattern.replace("#","")
	number_lenght = pattern.count("#")
	regex = r'\d{'+str(number_lenght)+'}'
	number =  re.findall(regex,image_path)
	if len(number) != 1 :
		print "No match found in " + image_path + " ,incorrect pattern : " + pattern
	else: 
		if (image_path == (search_pattern+number[0]+file_format)):
			number = int(number[0])
		else:
			print "No match found, incorrect pattern : " + pattern
	return number

def getMinMax(id_list):
	return (min(id_list),max(id_list))

def getImageDirectory(image_path):
	return options.image_path.split(getFrameNumber(image_path)+getImageFormat(image_path))[0]

def silhouetteMask(img,silhouette,dilate=2):
	if dilate > 0:
		kernel = np.ones((dilate,dilate),np.uint8)
		silhouette = cv2.erode(silhouette,kernel,iterations = 1)
	return cv2.bitwise_and(img,	silhouette)

class RunMode:
	def __init__(self):
		self.multiple_frames = False
		self.multiple_cameras = False

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i","--image",dest="image_path",help="Input Image Path")
	parser.add_option("-s","--silhouette",dest="silhouette_path",help="Input Silhouette Path")
	parser.add_option("-o","--output_directory",dest="output",help="Output Directory")
	
	(options,args) = parser.parse_args()
	image_path = options.image_path

	run_mode = RunMode()

	camera_dir_name = ""
	image_name = ""
	# Search for frame number pattern
	path_analysis = re.findall('([\w]*)([#]+)',image_path)
	print path_analysis
	if len(path_analysis) == 0:
		run_mode.multiple_frames = False
		run_mode.multiple_cameras = False
		print "Single Frame mode"

	elif len(path_analysis) == 1:
		if image_path.find(path_analysis[0][0]+path_analysis[0][1]+getImageFormat(image_path)) != -1:
			run_mode.multiple_frames = True
			run_mode.multiple_cameras = False
			image_name = path_analysis[0][0]+path_analysis[0][1]

			print "Multiple Frame Mode"
		else:
			run_mode.multiple_frames = False
			run_mode.multiple_cameras = True
			camera_dir_name = path_analysis[0][0]+path_analysis[0][1]
			print "Multiple Camera Mode"
	elif len(path_analysis) == 2:
		run_mode.multiple_frames = True
		run_mode.multiple_cameras = True
		image_name = path_analysis[1][0]+path_analysis[1][1]
		camera_dir_name = path_analysis[0][0]+path_analysis[0][1]
		print "Multiple Cameras & Frames mode"

	print camera_dir_name
	print image_name

	# exploreCamerasPath(image_path.split(camera_dir_name)[0],camera_dir_name)
	if run_mode.multiple_frames and run_mode.multiple_cameras:
		for cam in exploreCamerasPath(image_path.split(camera_dir_name)[0],camera_dir_name):
			exploreImagesPath(image_path.split(camera_dir_name)[0]+cam,image_name,getImageFormat(image_path))
	# sample_image_name = ''.join((['#']*frame_id_size)) + getImageFormat(options.image_path)
	# print getImageFormat(options.image_path)

	
	# print getFrameNumber(options.image_path)
	# print getImageDirectory(options.image_path)


	# img = cv2.imread(options.image_path,1)
	# silhouette = cv2.imread(options.silhouette_path,0)
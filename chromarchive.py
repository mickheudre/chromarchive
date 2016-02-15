import cv2
import numpy as np
from optparse import OptionParser
import re
import os
from collections import OrderedDict
import multiprocessing as mp

#TODO : Check if the filenames found during exploration match a real file
def exploreCamerasPath(cameras_path,cameras_pattern):
	#Check if the cameras path we guessed exists
	cameras_id = []
	cameras_to_explore = OrderedDict()
	if os.path.isdir(cameras_path):
		for dir in os.listdir(cameras_path):
			id = extractNumber(cameras_pattern,dir)
			if id != []:
				cameras_id.append(id)

		if len(cameras_id) > 0:
			cameras_id.sort()
			print str(len(os.listdir(cameras_path))) + " cameras detected : " + str(getMinMax(cameras_id))
			for cam in cameras_id:
				cameras_to_explore[re.sub(r'(#)+',cam,cameras_pattern)] = int(cam)
		else : 
			print "Unable to match cameras folders witch pattern: " + cameras_pattern	
	return cameras_to_explore

def exploreImagesPath(images_path,images_pattern,image_format):
	images_id = []
	images_to_load = OrderedDict()

	if os.path.isdir(images_path):
		file_list = os.listdir(images_path)
		files_to_analyse = []

		for file in file_list:
			if file.endswith(image_format):
				files_to_analyse.append(file.split(image_format)[0])
		files_to_analyse.sort()

		for image in files_to_analyse: 
				id =  extractNumber(images_pattern,image)
				if id != []:
					images_id.append(id)

		if len(images_id) > 0:
			print str(len(images_id)) + " images detected : " + str(getMinMax(images_id))
			for id in images_id:
				images_to_load[images_path +"/"+ images_pattern.replace("#","")+ id + image_format] = (id)
	return images_to_load

def exploreSilhouettesPath(silhouettes_path,silhouettes_pattern,silhouettes_format):
	images_id = []
	silhouettes_to_load = OrderedDict()
	if os.path.isdir(silhouettes_path):
		file_list = os.listdir(silhouettes_path)
		files_to_analyse = []

		for file in file_list:
			if file.endswith(silhouettes_format):
				files_to_analyse.append(file.split(silhouettes_format)[0])
		files_to_analyse.sort()

		for image in files_to_analyse: 
				id =  extractNumber(silhouettes_pattern,image)
				if id != []:
					images_id.append(id)

		if len(images_id) > 0:
			print str(len(images_id)) + " silhouettes detected : " + str(getMinMax(images_id))
			for id in images_id:
				silhouettes_to_load[silhouettes_path +"/"+ silhouettes_pattern.replace("#","")+ id + silhouettes_format] = (id)
	return silhouettes_to_load

# Assumes that an image file is ALWAYS ended by a file format (.png, .jpg ...)
def getImageFormat(image_path):
	return  os.path.splitext(image_path)[1]

def extractNumber(pattern,path,file_format=""):
	search_pattern = pattern.replace("#","")
	number_lenght = pattern.count("#")
	regex = r'\d{'+str(number_lenght)+'}'
	number =  re.findall(regex,path)
	
	if len(number) != 1 :
		print "No match found in " + path + " ,incorrect pattern : " + pattern
	else: 
		if (path == (search_pattern+number[0]+file_format)):
			return number[0]
		else:
			print "No match found, incorrect pattern : " + pattern
	

def getMinMax(id_list):
	return (min(id_list),max(id_list))

# def getImageDirectory(image_path):
# 	return options.image_path.split(getFrameNumber(image_path)+getImageFormat(image_path))[0]

def silhouetteMask(img,silhouette,dilate=2):
	if dilate > 0:
		kernel = np.ones((dilate,dilate),np.uint8)
	return cv2.bitwise_and(img,	cv2.dilate(silhouette,kernel,iterations = 1))

def processFrame(paths):
	"""
		Multiply the input image and the input silhouette and save the result
		:param paths : a list containing the input image, the input silhouette and the output path 
	"""
	cv2.imwrite(paths[2],silhouetteMask( cv2.imread(paths[0]),cv2.imread(paths[1])))


class ChromArchive:
	def __init__(self):
		self.multiple_frames = False
		self.multiple_cameras = False
		self.image_path = ""
		self.silhouette_path = ""
		self.output_path = ""
		self.image_pattern = ""
		self.image_format = ""
		self.silhouette_patter = ""
		self.camera_pattern = ""

	def parseInputArguments(self,options):
		if options.image_path == None:
			raise IOError("Input image path is not set.")
		if options.silhouette_path == None:
			raise IOError("Input image path is not set.")
		if options.output == None:
			raise IOError("Output directory is not set.")
		self.image_path = options.image_path
		self.silhouette_path = options.silhouette_path
		self.output_path = options.output

	def analysePaths(self):
		if self.image_path != "" and self.silhouette_path != "" and self.output_path != "":
			self.image_format = getImageFormat(self.image_path)
			#Analyse the image path to find patterns defined with #
			path_analysis = re.findall('([\w]*)([#]+)',self.image_path)
			#case 1 : no pattern found, a single frame will be processed
			if len(path_analysis) == 0:
				self.multiple_frames = False
				self.multiple_cameras = False
				print "[Single frame mode]"
			#case 2 : one pattern is found, we need to figure out if it is a camera or an image pattern
			if len(path_analysis) == 1:
				#The patter is associated to the file format, it is an image.
				if (image_path.find(path_analysis[0][0]+path_analysis[0][1]+self.image_format)) != -1:
					self.multiple_frames = True
					self.multiple_cameras = False
					self.image_pattern = path_analysis[0][0] + path_analysis[0][1]
					print "[Multiple frames mode]"
				#We assume that the other possibility is a camera pattern
				else:
					self.multiple_cameras = True
					self.multiple_frames = False
					self.camera_pattern = path_analysis[0][0] + path_analysis[0][1]
					print "[Multiple cameras mode]"
			#case 3 : 
			if len(path_analysis) == 2:
				self.multiple_cameras = True
				self.multiple_frames = True
				if (image_path.find(path_analysis[1][0]+path_analysis[1][1]+self.image_format)) != -1:
					self.image_pattern = path_analysis[1][0]+path_analysis[1][1]
					self.camera_pattern = path_analysis[0][0]+path_analysis[0][1]
				else:
					self.image_pattern = path_analysis[0][0]+path_analysis[0][1]
					self.camera_pattern = path_analysis[1][0]+path_analysis[1][1]
				print "[Multiple frames & cameras mode]"
				print "Image pattern : " + self.image_pattern
				print "Cameras pattern : " + self.camera_pattern
				self.cameras_directory = self.image_path.split(self.camera_pattern)[0]
				
	def archiveSingleFrame(self):
		"""
			Archive a single frame
		"""

	def archiveMultipleFrames(self):
		"""
			Archive multiple frames
		"""


	
if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i","--image",dest="image_path",help="Input Image Path")
	parser.add_option("-s","--silhouette",dest="silhouette_path",help="Input Silhouette Path")
	parser.add_option("-o","--output_directory",dest="output",help="Output Directory")
	
	(options,args) = parser.parse_args()

	if (options.image_path == None) or (options.silhouette_path == None) or (options.output == None):
		raise IOError("Invalid input arguments")
	image_path = options.image_path
	silhouettes_path = options.silhouette_path
	output_path = options.output

	if not(os.path.isdir(output_path)):
		os.mkdir(output_path)

	run_mode = ChromArchive()
	run_mode.parseInputArguments(options)
	run_mode.analysePaths()

	camera_dir_name = ""
	image_name = ""
	# Search for frame number pattern
	path_analysis = re.findall('([\w]*)([#]+)',image_path)

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

	# exploreCamerasPath(image_path.split(camera_dir_name)[0],camera_dir_name)
	if run_mode.multiple_frames and run_mode.multiple_cameras:
		process_queue = []
		for cam in exploreCamerasPath(image_path.split(camera_dir_name)[0],camera_dir_name):
			print "Processing camera " + cam + " :" 
			if not(os.path.isdir(output_path+"/"+cam)):
				os.mkdir(output_path+"/"+cam)
			images_to_load = exploreImagesPath(image_path.split(camera_dir_name)[0]+cam,image_name,getImageFormat(image_path))
			silhouettes_to_load = exploreSilhouettesPath(silhouettes_path.split(camera_dir_name)[0]+cam,image_name,getImageFormat(silhouettes_path))

			output_paths = []
			
			for files in zip(images_to_load.keys(), silhouettes_to_load.keys()):
				#Check if the frame number is the same
				im_id = images_to_load[files[0]]
				sil_id = silhouettes_to_load[files[1]]

				if im_id == sil_id:
					output_paths.append(output_path+"/"+cam+"/"+re.sub(r'(#)+',im_id,image_name)+getImageFormat(image_path))
				else:
					images_to_load.pop(files[0])
					silhouettes_to_load.pop(files[1])
			if len(images_to_load) == len(silhouettes_to_load):

				process_queue = process_queue + zip(images_to_load.keys(), silhouettes_to_load.keys(),output_paths)
				


		pool = mp.Pool()
		pool.map(processFrame,process_queue)
	
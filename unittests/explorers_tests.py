import unittest
import sys
sys.path.append("..")
import chromarchive

class TestPathExplorer(unittest.TestCase):
	def test_image_explorer_single_mode(self):
		image_to_load = chromarchive.exploreImagesPath("/disc/heudre/DATA/Test_Compression_Images/cam_01/frame01287904.png","",".png")
		self.assertIn("/disc/heudre/DATA/Test_Compression_Images/cam_01/frame01287904.png",image_to_load)
	def test_image_explorer_multiple_mode(self):
		images_to_load = chromarchive.exploreImagesPath("/disc/heudre/DATA/Test_Compression_Images/cam_01/","frame########",".png")
		self.assertIn("/disc/heudre/DATA/Test_Compression_Images/cam_01/frame01287904.png",images_to_load)
	def test_camera_explorer_multiple_mode(self):
		cameras_to_load = chromarchive.exploreCamerasPath("/disc/heudre/DATA/Test_Compression_Images/","cam_##")
		self.assertIn("cam_01",cameras_to_load)
	def test_extract_number(self):
		number = chromarchive.extractNumber("##", "01")
		self.assertEqual(number,"01")
	def test_extract_number_pattern(self):
		number = chromarchive.extractNumber("cam_##", "cam_01")
		self.assertEqual(number,"01")
	def test_extract_number_file(self):
		number = chromarchive.extractNumber("frame########","frame01287904.png",".png")
		self.assertEqual(number,"01287904")
	def test_get_minmax_strings(self):
		list = ("01","02","03","04","05")
		minmax = chromarchive.getMinMax(list)
		self.assertEqual(("01","05"),minmax)
	def test_get_minmax_int(self):
		list = (1,2,3,4,5)
		minmax = chromarchive.getMinMax(list)
		self.assertEqual((1,5),minmax)

if __name__ == '__main__':
	unittest.main()
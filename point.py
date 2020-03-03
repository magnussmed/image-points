from PIL import Image
import multiprocessing as mp
import cv2
import numpy as np
import collections
import os

# Point Class
class Point( object ) :
	def __init__( self ) :
		# Set image
		self.image_id = '7'
		self.path = 'assets/img/' + self.image_id + '.jpg'
		self.photo = Image.open( self.path )
		self.width, self.height = self.photo.size

		# Read image with CV2
		self.pointed_image = cv2.imread( self.path, 1 )

		# Photo average color
		self.average = self.average()

		self.points = []

		# Set sentiment percentage
		self.senti = 0.25

		# Start middle to top and bottom to middle simultaneously
		p1Q = mp.Queue()
		self.p1 = mp.Process( target = self.middle_top, args=(p1Q,))

		p2Q = mp.Queue()
		self.p2 = mp.Process( target = self.bottom_middle, args=(p2Q,))

		self.p1.start()
		self.p2.start()

		# Add both queries points (x, y)
		self.points = p1Q.get() + p2Q.get()
		self.draw_points( self.points )


	# Get average color from image
	# For each pixel get the RGB colorset and get average value afterwards
	#
	# Return int color
	def average( self ) :
		colors = []
		average = 0
		for c in self.photo.getdata() :
			average = int(sum( list(c) ) / 3)
			colors.append(average)

		print("Got color-average now! {}".format( average ))

		return round(sum(colors) / len(colors))

	# Draw points
	# Loop through each coordinate set and create a dot on image
	#
	# Return save image and open it
	def draw_points( self, points ) :
		for x, y in points :
			cv2.drawMarker( self.pointed_image, (x, y), (132,255,0), markerType = cv2.MARKER_SQUARE, markerSize = 1, thickness=2, line_type = cv2.LINE_AA )
		cv2.imwrite( 'assets/draw/' + self.image_id + '-point.jpg', self.pointed_image )

		cv2.imshow( 'image', self.pointed_image )
		cv2.waitKey( 0 )

	# From the bottom to the middle
	# For each pixel from the bottom of the image to the middle
	# searching for an interesting change in color from average
	#
	# Return string
	def bottom_middle( self, q ) :
		width = int( self.width )
		height = int( self.height / 2 )

		# For each x from 0 to total width
		for x in range( 0, width ) :
			# For each y from 0 to half height
			for y in range( 0, height ) :
				r, g, b = self.photo.getpixel(( x, y ))
				average = int( sum([r, g, b]) / 3 )

				# Break if the current average color is above image average * sentiment percentage
				# or if it is under image average * sentiment percentage
				if int( self.average + (self.senti * self.average) ) > average < int( self.average - (self.senti * self.average) ) :
					# print( "Point found: x: {}, y: {} {}".format( x,y,(r,g,b)) )
					self.points.append( ( x, y ) )
			else :
				continue
			break

		q.put( self.points )

	# From the middle to the top
	# For each pixel from the bottom of the image to the middle
	# searching for an interesting change in color from average
	#
	# Return string
	def middle_top( self, q ) :
		width = int( self.width )
		height = int( self.height / 2 )

		# For each x from 0 to total width
		for x in range( 0, width ) :
			# For each y from half height to full height
			for y in range( height, self.height ) :
				r, g, b = self.photo.getpixel(( x, y ))
				average = int( sum([r, g, b]) / 3 )

				# Break if the current average color is above image average * sentiment percentage
				# or if it is under image average * sentiment percentage
				if int( self.average + (self.senti * self.average) ) > average < int( self.average - (self.senti * self.average) ) :
					# print( "Point found: x: {}, y: {} {}".format( x,y,(r,g,b)) )
					self.points.append( ( x, y ) )
			else :
				continue
			break

		q.put( self.points )

if __name__ == '__main__' :
	point = Point()

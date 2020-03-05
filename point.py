from PIL import Image
import multiprocessing as mp
import cv2
import numpy as np
import os
import time

# Point Class
class Point( object ) :
	def __init__( self ) :
		# Set image id
		self.image_id = '19'
		self.path = 'assets/img/' + self.image_id + '.jpg'
		self.photo = Image.open( self.path )
		self.width, self.height = self.photo.size

		# Read image with CV2
		self.pointed_image = cv2.imread( self.path, 1 )

		# Photo average color
		self.average = self.average()
		print( "--- Find average time: %s seconds ---" % ( time.time() - start_time ) )

		self.points = []

		# Set sentiment percentage and averages
		self.senti = 0.3
		self.high_average = int( self.average + ( self.senti * self.average ) )
		self.low_average = int( self.average - ( self.senti * self.average ) )

		# Start middle to top and bottom to middle simultaneously
		self.points = self.start()

		# Draw points
		self.draw_points( self.points )

		print( "--- %s seconds ---" % ( time.time() - start_time ) )

	# Start processes simultaneously
	# Using the multiprocessing libary we're able to execute multiple functions at once.
	#
	# Return self.points
	def start( self ) :
		p1Q = mp.Queue()
		self.p1 = mp.Process( target = self.find_points, args=(p1Q,'mt'))

		p2Q = mp.Queue()
		self.p2 = mp.Process( target = self.find_points, args=(p2Q,'bm'))

		self.p1.start()
		self.p2.start()
		self.points = p1Q.get() + p2Q.get()

		return self.points

	# Get average color from image
	# For each pixel get the RGB colorset and get average value afterwards
	#
	# Return int color
	def average( self ) :
		count = 0
		for c in self.photo.getdata() :
			count += int( sum( list(c) ) )

		average = round( ( count / 3 ) / ( self.width * self.height ) )
		print("Got color-average now! {}".format( average ))

		return average

	# Draw points
	# Loop through each coordinate set and create a dot on image
	#
	# Return save image and open it
	def draw_points( self, points ) :
		for x, y in points :
			cv2.drawMarker( self.pointed_image, ( x, y ), ( 132, 255,0 ), markerType = cv2.MARKER_CROSS, markerSize = 2, thickness=1 )
		cv2.imwrite( 'assets/draw/' + self.image_id + '-point.jpg', self.pointed_image )

		cv2.imshow( 'image', self.pointed_image )
		cv2.waitKey( 0 )

	# Find points
	# Loop through everything and find relevant points
	#
	# Return self.points
	def find_points( self, q, type ) :
		width = int( self.width )
		height = int( self.height / 2 )

		# Determine whether it's middle-top or bottom-top
		if type == 'mt' :
			f = height
			to = self.height
		if type == 'bm' :
			f = 0
			to = height

		# For each x from 0 --> width
		for x in range( 0, width ) :
			# For each y from f --> height or self.height
			for y in range( f, to ) :
				r, g, b = self.photo.getpixel(( x, y ))
				average = int( sum([r, g, b]) / 3 )

				# Exclude pixels with the same average color as the image-average
				if average != self.average :
					if self.average > 127.5 :
						# Dark average
						if self.low_average > average :
							# print( "Point found: x: {}, y: {} {}".format( x,y,(r,g,b)) )
							self.points.append( ( x, y ) )
					else :
						# Light average
						if self.high_average < average :
							# print( "Point found: x: {}, y: {} {}".format( x,y,(r,g,b)) )
							self.points.append( ( x, y ) )
			else :
				continue
			break

		q.put( self.points )

if __name__ == '__main__' :
	start_time = time.time()
	point = Point()

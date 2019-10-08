"""
This file is the main API to use Interferometry without the UI.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt 

sys.path.append('..')

from core.evaluate import min_max_method, cff_method, fft_method, cut_gaussian, gaussian_window , ifft_method, spp_method, args_comp
from core.edit_features import savgol, find_peak, convolution, cut_data, find_closest
from core.generator import generatorFreq, generatorWave


class DatasetError(Exception):
	pass


class Generator(object):
	def __init__(self, start, stop, center, delay=0, GD=0, GDD=0, TOD=0, FOD=0, QOD=0, resolution=0.1, delimiter=',',
		         pulseWidth=10, includeArms=False):
		self.start = start
		self.stop = stop
		self.center = center
		self.delay = delay
		self.GD = GD
		self.GDD = GDD
		self.TOD = TOD
		self.FOD = FOD
		self.QOD = QOD
		self.resolution = resolution
		self.delimiter = delimiter
		self.pulseWidth = pulseWidth
		self.includeArms = includeArms
		self.x = np.array([])
		self.y = np.array([])
		self.ref = np.array([])
		self.sam = np.array([])
		self.plotwidget = plt

	def __str__(self):
		return '''Generator({}, {}, {}, delay = {},GD={}, GDD={}, TOD={}, FOD={}, QOD={}, resolution={}, 
				  delimiter={},pulseWidth={}, includeArms={}'''.format(self.start, self.stop, self.center,
				  self.delay, self.GD, self.GDD, self.TOD, self.FOD, self.QOD, self.resolution, 
				  self.delimiter, self.pulseWidth, self.includeArms)

	def generate_freq(self):
		self.x, self.y, self.ref, self.sam = generatorFreq(self.start, self.stop, self.center, self.delay, self.GD,
			self.GDD, self.TOD, self.FOD, self.QOD,
			self.resolution, self.delimiter, self.pulseWidth, self.includeArms)

	def generate_wave(self):
		self.x, self.y, self.ref, self.sam = generatorWave(self.start, self.stop, self.center, self.delay, self.GD,
			self.GDD, self.TOD, self.FOD, self.QOD,
			self.resolution, self.delimiter, self.pulseWidth, self.includeArms)
		
	def show(self):
		if len(self.ref) != 0:
			self._y =  (self.y - self.ref - self.sam)/(2*np.sqrt(self.sam*self.ref))
		try:
			self.plotwidget.plot(self.x, self._y, 'r')
		except:
			self.plotwidget.plot(self.x, self.y, 'r')
		self.plotwidget.grid()
		self.plotwidget.show()

	def save(self, name, path=None):
		if path == None:
			np.savetxt('{}.txt'.format(name), np.transpose([self.x, self.y, self.ref, self.sam]))
		else:
			np.savetxt('{}/{}.txt'.format(path, name), np.transpose([self.x, self.y, self.ref, self.sam]))


class Dataset(object):
	def __init__(self, x, y, ref=None, sam=None):
		self.x = x
		self.y = y
		if ref is None:
			self.ref = []
		else:
			self.ref = ref 
		if sam is None:
			self.sam = []
		else:
			self.sam = sam
		self._is_normalized = False
		if not isinstance(self.x, np.ndarray):
			try:
				self.x = np.array(self.x)
				self.x.astype(float)
			except:
				raise DatasetError('Invalid type of data')
		if not isinstance(self.y, np.ndarray):
			try:
				self.y = np.array(self.y)
				self.y.astype(float)
			except:
				raise DatasetError('Invalid type of data')
		if not isinstance(self.ref, np.ndarray):
			try:
				self.ref = np.array(self.ref)
				self.ref.astype(float)
			except:
				pass
		if not isinstance(self.sam, np.ndarray):
			try:
				self.sam = np.array(self.sam)
				self.sam.astype(float)
			except:
				pass
		if len(self.ref) == 0:
			self.y_norm = self.y
		else:
			self.y_norm = (self.y - self.ref - self.sam)/(2*np.sqrt(self.sam*self.ref))
			self._is_normalized = True
		self.plotwidget = plt

	
	def __str__(self):
		try:
			string = "{}, {}, {}, {}\n{}, {}, {}, {}".format(self.x[0], self.y[0], self.ref[0], self.sam[0],
			                                                 self.x[1], self.y[1], self.ref[1], self.sam[1])
		except:
			string = "{}, {}\n{}, {}".format(self.x[0], self.y[0], self.x[1], self.y[1])
		return string

	def __repr__(self):
		 return 'Dataset(x = %s, y = %s, ref = %s, sam = %s)' % (self.x, self.y, self.ref, self.sam)

	@property
	def is_normalized(self):
		return self._is_normalized
	
	def savgol_fil(self, window=101, order=3):
		self.x, self.y_norm = savgol(self.x, self.y, self.ref, self.sam, window = window, order = order)
		self.ref = []
		self.sam = []
		

	def cut(self, start=-9999, stop=9999):
		self.x, self.y_norm = cut_data(self.x, self.y, self.ref, self.sam, startValue = start, stopValue = stop)
		self.ref = []
		self.sam = []

	def convolution(self, std=20):
		self.x, self.y_norm = convolution(self.x, self.y, self.ref, self.sam, standev = std)
		self.ref = []
		self.sam = []

	def detect_peak(self, pmax=1, pmin=1, threshold=0.1):
		xmax, ymax, xmin, ymin = find_peak(self.x, self.y, self.ref, self.sam, proMax = pmax, proMin = pmin, threshold=threshold)
		return xmax, ymax, xmin, ymin
		
	def show(self):
		self.plotwidget.plot(self.x, self.y_norm)
		self.plotwidget.grid()
		self.plotwidget.show()


class MinMaxMethod(Dataset):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.xmin = []
		self.xmax = []

	def __str__(self):
		return '''MinMaxMethod({},{},{},{})'''.format(self.x, self.y, self.ref, self.sam)

	def calculate(self, reference_point, fit_order, show_graph = False):
		dispersion, dispersion_std, fit_report = min_max_method(
			self.x, self.y, self.ref, self.sam, ref_point = reference_point,
			maxx = self.xmax, minx = self.xmin, fitOrder = fit_order, showGraph = show_graph
			)
		return dispersion, dispersion_std, fit_report


class CosFitMethod(Dataset):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.params = [1, 1, 1, 1, 1, 1, 1, 1]
		self.fit = None

	def __str__(self):
		return '''CosFitMethod({},{},{},{})'''.format(self.x, self.y, self.ref, self.sam)

	def calculate(self, reference_point):
		dispersion, self.fit = cff_method(self.x, self.y, self.ref, self.sam, 
			ref_point = reference_point, p0 = self.params)
		return dispersion

	def plot_result(self):
		if self.fit is not None:
			self.plotwidget.plot(self.x, self.fit, 'ko', label = 'fit')
			self.plotwidget.legend()
			self.show()
		else:
			self.show()


class SPPMethod(Dataset):

	raw = False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.om = None
		self.de = None
		self.bf = None
		print('With SPP-Method x and y values have a different meaning compared to other methods.')
		print('\t\tMake sure you put delays to y and frequencies to x:')
		print('\t\t\t\tSPPMethod(frequencies, delays)')

	def __str__(self):
		return '''SPPMethod({},{})'''.format(self.x, self.y)

	@classmethod
	def from_raw(cls, omegas, delays):
		cls.raw = True
		return cls(omegas, delays)

	def calculate(self, fit_order):
		if self.raw:
			_, _, dispersion, dispersion_std, self.bf = spp_method(self.y, self.x, fitOrder = fit_order, from_raw = True)
			self.om = self.x
			self.de = self.y
		else:
			self.om, self.de, dispersion, dispersion_std, self.bf = spp_method(self.y, self.x, fitOrder = fit_order, from_raw = False)
		return dispersion, dispersion_std, self.bf

	def plot_result(self):
		self.plotwidget.plot(self.om, self.de, 'o')
		try:
			self.plotwidget.plot(self.om, self.bf, 'r--')
		except:
			pass
		self.plotwidget.show()


class FFTMethod(Dataset):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#making sure it's not normalized
		if self._is_normalized:
			self.y_norm = self.y
			self._is_normalized = False

	def __str__(self):
		return '''FFTMethod({},{})'''.format(self.x, self.y)

	def ifft(self, interpolate = True):
		self.x, self.y = ifft_method(self.x, self.y, interpolate = interpolate)
	
	def fft(self):
		self.y = fft_method(self.y)

	def cut(self, at, std, window_order = 6):
		self.y = cut_gaussian(self.x, self.y, spike = at, sigma = std, win_order = window_order)
		
	def calculate(self, fit_order, showGraph):
		dispersion, dispersion_std, fit_report = args_comp(self.x, self.y, fitOrder = fit_order, showGraph = show_graph)
		return dispersion, dispersion_std, fit_report


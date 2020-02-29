"""
This file implements the basic Dataset class.
"""

import json # for pretty printing dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pysprint.api.dataset_base import  DatasetBase, C_LIGHT
from pysprint.core.dataedits import savgol, find_peak, convolution, cut_data, cwt
from pysprint.core.normalize import DraggableEnvelope
from pysprint.api.exceptions import *
from pysprint.api.spp_editor import SPPEditor
from pysprint.utils import MetaData


__all__ = ['Dataset']

class Dataset(DatasetBase):
	"""
	Base class for the evaluating methods.
	"""
	meta = MetaData("""Additional info about the dataset""", copy=False)

	def __init__(self, x, y, ref=None, sam=None, meta=None):
		
		super().__init__()

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
			except ValueError:
				raise DatasetError('Invalid type of data')
		if not isinstance(self.y, np.ndarray):
			try:
				self.y = np.array(self.y)
				self.y.astype(float)
			except ValueError:
				raise DatasetError('Invalid type of data')
		if not isinstance(self.ref, np.ndarray):
			try:
				self.ref = np.array(self.ref)
				self.ref.astype(float)
			except ValueError:
				pass # just ignore invalid arms
		if not isinstance(self.sam, np.ndarray):
			try:
				self.sam = np.array(self.sam)
				self.sam.astype(float)
			except ValueError:
				pass # just ignore invalid arms
		if len(self.ref) == 0:
			self.y_norm = self.y
		else:
			self.y_norm = (self.y - self.ref - self.sam) / (2 * np.sqrt(self.sam * self.ref))
			self._is_normalized = True
		self.plotwidget = plt
		self.xmin = None
		self.xmax = None
		self.probably_wavelength = None
		self._check_domain()
		
		if meta is not None:
			self.meta = meta

		self._delay = None
		self._positions = None


	@property
	def delay(self):
		return self._delay

	@delay.setter
	def delay(self, value):
		self._delay = value

	@property
	def positions(self):
		return self._positions

	@positions.setter
	def positions(self, value):
		self._positions = value


	def _safe_cast(self):
		'''
		Return a copy of key attributes in order to prevent inplace modification.
		'''
		x, y, ref, sam = np.copy(self.x), np.copy(self.y), np.copy(self.ref), np.copy(self.sam)
		return x, y, ref, sam


	def _check_domain(self):
		"""
		Checks the domain of data just by looking at x axis' minimal value.
		Units are obviously not added yet, we work in nm and PHz...
		"""
		if min(self.x) > 100:
			self.probably_wavelength = True
		else:
			self.probably_wavelength = False

	@classmethod
	def parse_raw(cls, basefile, ref=None, sam=None, skiprows=8,
		decimal=',', sep=';', meta_len=5):
		'''
		Dataset object alternative constructor. Helps to load in data just by giving the filenames
		in the target directory.

		Parameters:
		----------
		basefile: `str`
			base interferogram
			file generated by the spectrometer

		ref: `str`, optional
			reference arm's spectra
			file generated by the spectrometer

		sam: `str`, optional
			sample arm's spectra
			file generated by the spectrometer

		skiprows: `int`, optional
			Skip rows at the top of the file. Default is `8`.

		sep: `str`, optional
			The delimiter in the original interferogram file.
			Default is `;`.

		decimal: `str`, optional
			Character recognized as decimal separator in the original dataset. 
			Often `,` for European data.
			Default is `,`.

		meta_len: `int`, optional
			The first `n` lines in the original file containing the meta information
			about the dataset. It is parsed to be dict-like. If the parsing fails,
			a new entry will be created in the dictionary with key `unparsed`.
			Default is `4`.
		'''
		with open(basefile) as file:
			comm = next(file).strip('\n').split('-')[-1]
			additional = (next(file).strip('\n').strip('\x00').split(':') for _ in range(1, meta_len))
			cls.meta = {'comment': comm}
			try:
				for info in additional:
					cls.meta[info[0]] = info[1]
			except IndexError:
				cls.meta['unparsed'] = str(list(additional))
		df = pd.read_csv(basefile, skiprows=skiprows, sep=sep, decimal=decimal, names=['x', 'y'])
		if (ref is not None and sam is not None):
			r = pd.read_csv(ref, skiprows=skiprows, sep=sep, decimal=decimal, names=['x', 'y'])
			s = pd.read_csv(sam, skiprows=skiprows, sep=sep, decimal=decimal, names=['x', 'y'])
			return cls(df['x'].values, df['y'].values, r['y'].values, s['y'].values)
		return cls(df['x'].values, df['y'].values)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		string = f'''
{type(self).__name__} object

Parameters
----------
Datapoints = {len(self.x)}
Normalized: {self._is_normalized}
Arms are separated: {True if len(self.ref) > 0 else False}
Predicted domain: {'wavelength' if self.probably_wavelength else 'frequency'}

Metadata extracted from file
----------------------------
{json.dumps(self.meta, indent=4)}
		'''
		return string

	@property
	def data(self):
		"""
		Returns the *current* dataset as `pandas.DataFrame`.
		"""
		if self._is_normalized:
			try:
				self._data = pd.DataFrame({
				'x': self.x,
				'y': self.y,
				'sample': self.sam,
				'reference': self.ref,
				'y_normalized': self.y_norm
					})
			except ValueError:
				self._data = pd.DataFrame({
					'x': self.x,
					'y': self.y,
					})
		else:
			self._data = pd.DataFrame({
				'x': self.x,
				'y': self.y,
				})
		return self._data

	@property
	def is_normalized(self):
		"""
		Retuns whether the dataset is normalized.
		"""
		return self._is_normalized
	
	def chdomain(self):
		""" Changes from wavelength [nm] to ang. freq. [PHz] domain and vica versa."""
		self.x = (2*np.pi*C_LIGHT)/self.x
		self._check_domain()
		if type(self).__name__ == 'FFTMethod':
			self.original_x = self.x


	def detect_peak_cwt(self, width, floor_thres=0.05):
		x, y, ref, sam = self._safe_cast()
		xmax, ymax, xmin, ymin = cwt(x, y, ref, sam, width=width, floor_thres=floor_thres)
		return xmax, ymax, xmin, ymin

	def savgol_fil(self, window=10, order=3):
		"""
		Applies Savitzky-Golay filter on the dataset.

		Parameters:
		----------
		window: `int`
			Length of the convolutional window for the filter.
			Default is `10`.

		order: `int`
			Degree of polynomial to fit after the convolution.
			If not odd, it's incremented by 1. Must be lower than window.
			Usually it's a good idea to stay with a low degree, e.g 3 or 5.
			Default is 3.

		Notes:
		------
		If arms were given, it will merge them into the `self.y` and `self.y_norm` variables.
		Also applies a linear interpolation on dataset (and raises warning).
		"""
		self.x, self.y_norm = savgol(self.x, self.y, self.ref, self.sam, window=window, order=order)
		self.y = self.y_norm
		self.ref = []
		self.sam = []
		warnings.warn('Linear interpolation have been applied to data.', InterpolationWarning)
		
	# TODO: implement a better way
	def slice(self, start=-9999, stop=9999):
		"""
		Cuts the dataset on x axis in this form: [start, stop]

		Parameters:
		----------
		start: `float`
			start value of cutting interval
			Not giving a value will keep the dataset's original minimum value.
			Note that giving `-9999` will leave original minimum untouched too.
			Default is `-9999`.

		stop: `float`
			stop value of cutting interval
			Not giving a value will keep the dataset's original maximum value.
			Note that giving `9999` will leave original maximum untouched too.
			Default is `9999`.

		Notes:
		------

		If arms were given, it will merge them into the `self.y` and `self.y_norm` variables.
		"""
		self.x, self.y_norm = cut_data(self.x, self.y, self.ref, self.sam, startValue=start, endValue=stop)
		self.ref = []
		self.sam = []
		self.y = self.y_norm
		# Just to make sure it's correctly shaped. Later on we might delete this.
		if type(self).__name__ == 'FFTMethod':
			self.original_x = self.x

	def convolution(self, window_length, std=20):
		"""
		Applies a convolution with a gaussian on the dataset

		Parameters:
		----------
		window_length: `int`
			Length of the gaussian window.

		std: `float`
			Standard deviation of the gaussian
			Default is `20`.

		Notes:
		------
		If arms were given, it will merge them into the `self.y` and `self.y_norm` variables.
		Also applies a linear interpolation on dataset (and raises warning).
		"""
		self.x, self.y_norm = convolution(self.x, self.y, self.ref, self.sam, window_length, standev=std)
		self.ref = []
		self.sam = []
		self.y = self.y_norm
		warnings.warn('Linear interpolation have been applied to data.', InterpolationWarning)


	def detect_peak(self, pmax=0.1, pmin=0.1, threshold=0.1, except_around=None):
		"""
		Basic algorithm to find extremal points in data using ``scipy.signal.find_peaks``.

		Parameters:
		----------

		pmax: `float`
			Prominence of maximum points.
			The lower it is, the more peaks will be found.
			Default is `0.1`.

		pmin: float
			Prominence of minimum points.
			The lower it is, the more peaks will be found.
			Default is `0.1`.

		threshold: `float`
			Sets the minimum distance (measured on y axis) required for a point to be
			accepted as extremal.
			Default is 0.

		except_around: interval (array or tuple), 
			Overwrites the threshold to be 0 at the given interval.
			format is `(lower, higher)` or `[lower, higher]`.
			Default is None.

		Returns:
		-------
		xmax: `array-like`
			x coordinates of the maximums

		ymax: `array-like`
			y coordinates of the maximums

		xmin: `array-like`
			x coordinates of the minimums

		ymin: `array-like`
			y coordinates of the minimums
		"""
		x, y, ref, sam = self._safe_cast()
		xmax, ymax, xmin, ymin = find_peak(x, y, ref, sam, proMax=pmax, proMin=pmin, threshold=threshold, except_around=except_around)
		return xmax, ymax, xmin, ymin
		
	def show(self):
		"""
		Draws a graph of the current dataset using matplotlib.
		"""
		if np.iscomplexobj(self.y):
			self.plotwidget.plot(self.x, np.abs(self.y))
		else:   
			try:
				self.plotwidget.plot(self.x, self.y_norm, 'r')
			except Exception:
				self.plotwidget.plot(self.x, self.y, 'r')
		self.plotwidget.grid()
		self.plotwidget.show()


	def normalize(self, filename=None):
		'''
		Normalize the interferogram by finding upper and lower envelope
		on an interactive matplotlib editor.

		Parameters
		----------

		filename: `str`
			Save the normalized interferogram named by filename in the 
			working directory. If not given it will not be saved.
			Default None.

		Returns
		-------
		None
		'''
		if run_from_ipython():
			return '''It seems you run this code in IPython. Interactive plotting is not yet supported. Consider running it in the regular console.'''
		_l_env = DraggableEnvelope(self.x, self.y, 'l')
		y_transform = _l_env.get_data()
		_u_env = DraggableEnvelope(self.x, y_transform, 'u')
		y_final = _u_env.get_data()
		self.y = y_final
		self.y_norm = y_final
		self._is_normalized = True
		self.plotwidget.title('Final')
		self.show()
		if filename:
			if not filename.endswith('.txt'):
				filename += '.txt'
			np.savetxt(filename, np.transpose([self.x, self.y]), delimiter=',')
			print(f'Successfully saved as {filename}')


	def open_SPP_panel(self):
		_spp = SPPEditor(self.x, self.y_norm)
		self.delay, self.positions = _spp.get_data()

	def emit(self):
		# validate if it's typed by hand..
		if not isinstance(self._positions, np.ndarray):
			np.asarray(self.positions)
		if not isinstance(self.delay, np.ndarray):
			self.delay = np.ones_like(self.positions) * self.delay
		return self.delay, self.positions

	def set_SPP_data(self, delay, positions):
		if not isinstance(positions, np.ndarray):
			positions = np.asarray(positions)
		if not isinstance(delay, float):
			delay = float(delay)
		delay = np.ones_like(positions) * delay
		self._delay = delay
		self._positions = positions

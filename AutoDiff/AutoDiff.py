import numpy as np

class DualNumber:
	""" This class defines dual number and the way of a series of arithmetic functions implemented on it."""
	def __init__(self, val = None, der = None):
		"""The constructor for DualNumber Class.

		Args:
			val (real number): The value of the function at a certain stage.
			der (real number): The value of the derivate at a ceratin stage. If no value given for der in dual number, the default is 1.
		"""
		# This only applies for the case of scalar
		if der is None:
			self.val = val
			self.der = 1
		else:
			self.val = val
			self.der = der

	def __add__(self, other):
		"""Return the result of self + other as a dual number.

		INPUTS
			self (DualNumber object): The value of the function at a certain stage.
			other (DualNumber object or real number):
				If it is dual number, then add its val and del respectively to the value and del of our recent dual number.
				If it is a real number, add it to the val of our recent dual number.

		RETURNS
			The result of self + other (DualNumber)

		EXAMPLES
		>>> ad = ad()
		>>> x = 1
		>>> user_def = lambda x: x+2
		>>> t = ad.auto_diff(function = user_def, eval_point = x)
		>>> print(t.val, t.der)
		3 1
 		"""
		try:
			return DualNumber(self.val + other.val, self.der + other.der)
		except AttributeError:
			return DualNumber(self.val + other, self.der)

	def __radd__(self, other):
		"""Return the result of other + self as a dual number use the __add__ above.

		INPUTS
			self (DualNumber object): The value of the function at a certain stage.
			other (DualNumber object or real number):
				If it is dual number, then add its val and del respectively to the value and del of our recent dual number.
				If it is a real number, add it to the val of our recent dual number.

		RETURNS
			The result of self + other (DualNumber)

		EXAMPLES
		>>> ad = ad()
		>>> x = 1
		>>> user_def = lambda x: x+2
		>>> t = ad.auto_diff(function = user_def, eval_point = x)
		>>> print(t.val, t.der)
		3 1
 		"""
		# use __add__ defined above
		return self + other

	def __mul__(self, other):
		try:
			return DualNumber(self.val * other.val, self.der * other.val + self.val * other.der)
		except AttributeError:
			return DualNumber(self.val * other, self.der * other)

	def __rmul__(self, other):
		return self * other

	def __sub__(self, other):
		# Take advantage of the addition defined above
		return self + (-1) * other

	def __rsub__(self, other):
		return (-1) * self + other

	def __truediv__(self, other):
		return self * (other ** (-1))

	def __rtruediv__(self, other):
		return other*(self ** (-1))

	def __pow__(self, other):
		try:
			return DualNumber(self.val ** other.val, \
							 other.val * self.val ** (other.val - 1) * self.der + \
							 (self.val ** other.val) * np.log(self.val) * other.der)
		except AttributeError:
			return DualNumber(self.val ** other, other * self.val ** (other - 1) * self.der)

	def __rpow__(self, other):
		return DualNumber(other ** self.val, other ** self.val * np.log(other) * self.der)

	def __neg__(self):
		return DualNumber(-self.val, -self.der)

	def __pos__(self):
		return DualNumber(self.val, self.der)

class ad:
	"""
    >>> 1+1
    2
    """
	def __init__(self):
		pass

	def auto_diff(self, function, eval_point, order = 1):
		dual = DualNumber(eval_point)
		return function(dual)

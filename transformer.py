import datetime
from functools import partial


class Transformer:
	def __init__(self, mappings):
		self.mappings = mappings

	@staticmethod
	def lookup(map):
		return lambda src: map[src]

	@staticmethod
	def strpdate(src):
		datetime.datetime.strptime(src, '%Y-%m-%d').date()

	@staticmethod
	def strptime(src):
		datetime.datetime.strptime(src, '%Y-%m-%d').time()

	@staticmethod
	def strpweekday(src):
		datetime.datetime.strptime(src, '%Y-%m-%d').date().weekday() + 1

	@staticmethod
	def identity(src):
		return src

	def transform(self, src):
		return {mapping[1]: mapping[2](src[mapping[0]]) for mapping in self.mappings}


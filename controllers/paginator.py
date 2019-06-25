# File: paginator.py
# pagination

class Paginator:
	def __init__(self, max_page_size):
		self.delta = max_page_size
		self.offset = -1 # indicates start

	def getPagination(self, results_len, getting_next=True):
		limit = self.delta
        
		# case: at the beginning
		if self.offset == -1 and getting_next:
			self.offset = 0
			return limit, self.offset

		# case: continue paging forward only if there may be more results
		if results_len == self.delta and getting_next:
			#offset = self.left_offset
			if results_len == self.delta:
				self.offset += self.delta
			return limit, self.offset
		elif results_len < self.delta and getting_next:
			return limit, self.offset

		# case: continue paging backward to min offset of 0
		if not getting_next:
			self.offset = max(self.offset - self.delta, 0)
			return limit, self.offset

		raise Exception("Situation not anticipated!") # TODO: find more specific exception class
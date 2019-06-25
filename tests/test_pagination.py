# File: test_pagination.py
# Run with: python -m unittest app.tests.test_pagination

import unittest

from ..controllers.paginator import Paginator

class TestPagination(unittest.TestCase):
	def test_first_page(self):
		'''Should be able to get the first page.'''
		c = Paginator(5)
		limit, offset = c.getPagination(5)
		self.assertEqual((limit, offset), (5,0))

	def test_attempt_backwards_from_first_page(self):
		'''Should not be able to page backward beyond the beginning of results.'''
		c = Paginator(5)
		limit, offset = c.getPagination(5)
		assert((limit,offset)==(5,0))
		limit, offset = c.getPagination(5, False)
		limit, offset = c.getPagination(5, False)
		limit, offset = c.getPagination(5, False)
		limit, offset = c.getPagination(5, False)
		self.assertEqual((limit, offset), (5, 0))

	def test_second_page(self):
		'''Should be able to load subsequent pages in a forward direction.'''
		c = Paginator(5)
		c.getPagination(5)
		limit, offset = c.getPagination(5)
		self.assertEqual((limit, offset), (5, 5))

	def test_back_one_from_second_page(self):
		'''Should be able to move backwards to previous pages after moving forwards.'''
		c = Paginator(5)
		limit, offset = c.getPagination(5)
		assert((limit,offset)==(5,0))
		limit, offset = c.getPagination(5)
		assert((limit,offset)==(5,5))

		limit, offset = c.getPagination(5, False)
		self.assertEqual((limit, offset), (5, 0))

	def test_last_page_fewer_results(self):
		'''With 4 items and max page size of 5, there should be only 1 page: 
		offset should stay at 0.'''
		c = Paginator(5)
		c.getPagination(5) # get limit and offset for first page
		limit, offset = c.getPagination(4)
		self.assertEqual((limit, offset), (5, 0))
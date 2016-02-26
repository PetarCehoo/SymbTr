# -*- coding: utf-8 -*-
from symbtrdataextractor import symbtrreader
from fileoperations.fileoperations import getFileNamesInDir

import os

def test_mu2_header():
	col_names = {2:u'Pay', 3:u'Payda', 4:u'Legato%', 5:u'Bas', 
		6:u'Çek', 7:u'Söz-1', 8:u'Söz-2'}	
	
	num_columns = 10
	all_headers_valid = True
	all_header_rows_valid = True
	all_num_columns_correct = True

	[mu2filepaths, mu2folders, mu2names] = get_mu2_filenames()

	for mf, mn in zip(mu2filepaths, mu2names):
		mu2_header, header_row, is_header_valid = symbtrreader.readMu2Header(mf, mn)

		if not is_header_valid:
			all_headers_valid = False

		if not len(header_row) == num_columns:
			all_num_columns_correct = False
			print mn + ': Number of columns is different than 10!'

		for ii in range(0, len(col_names) + 3):
			if ii in [0, 1]:
				try: 
					dummyint = int(header_row[ii])
				except ValueError:  # not int
					all_header_rows_valid = False
					print mn + ': ' + str(ii) + 'th column in the header row should have been an integer!'
			elif ii == len(col_names) + 2:
				try: 
					dummyfloat = float(header_row[ii])
				except ValueError:  # not float
					all_header_rows_valid = False
					print mn + ': ' + str(ii) + 'th column in the header row should have been a float!'
			else:
				if not header_row[ii] == col_names[ii]:
					all_header_rows_valid = False
					print u'%s: %dth column in the header row should have been named "%s" instead of "%s"' % (
						mn, ii, col_names[ii], header_row[ii])

	assert all_header_rows_valid and all_num_columns_correct and all_headers_valid

def get_mu2_filenames():
	symbTrMu2folder = './mu2/'
	return getFileNamesInDir(symbTrMu2folder, keyword = '*.mu2')
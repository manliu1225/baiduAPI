#! /usr/bin/env python3
from . tokenization_pos import Baiduapi
import argparse
import codecs
import logging
import pickle
import random
import os
import chardet as chardet
from itertools import chain
logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process(argws):
	''' input: raw_data, and output dir
	output: output/filename/1~50.txt
	'''
	filename, output = argws
	output_dir = os.path.join(output,os.path.basename(filename))
	if not os.path.exists(output_dir): os.mkdir(output_dir)
	data_li = readf(filename)
	data_li = list(set(data_li))
	random.shuffle(data_li)
	word_sentence_li, pos_sentence_li = get_pos(data_li, filename)
	data = []
	for (w_li, p_li) in zip(word_sentence_li, pos_sentence_li):
		data.extend(zip(w_li, p_li))
		data.append('')
	data_li, data_lili = [], []
	for e in data:
		data_li.append(e)
		if e == '': 
			data_lili.append(data_li)
			data_li = []
	### split sentences to 50
	n = 50		
	data_50_li = [data_lili[i:i + n] for i in range(0, len(data_lili), n)]
	for i, file_data in enumerate(data_50_li):
		with open(os.path.join(output_dir, '{}.txt'.format(i)), 'w') as output_f:
			for e in chain(*file_data):
					if e == '': output_f.write(e+'\n')
					else:
						for i, ee in enumerate(e[0]):
							# print(chardet.detect(ee))
							if i == 0: output_f.write('{}\tB-{}\tO\n'.format(ee, e[1]))
							elif i == len(e[0])-1: output_f.write('{}\tE-{}\tO\n'.format(ee, e[1]))
							else: output_f.write('{}\tI-{}\tO\n'.format(ee, e[1]))
	return 0

def readf(f):
	ff = open(f, 'rb')
	data = ff.readlines()
	n = 0
	data_li = []
	for i, e in enumerate(data):
		try:
			data_li.append(e.decode('utf-8'))
		except:
			try: data_li.append(e.decode('gb2312'))
			except:
				try: line.strip().decode('KOI8-R')
				except:
					n += 1
					logger.error('error line number is {}'.format(i))
	logger.info('the number of lines without processed because of decoding error is {}'.format(n))
	return data_li

def get_pos(data_li, dumpf):
	baiduapi = Baiduapi()
	filedump = './wordf_dir0806/wordf_{}'.format(os.path.basename(dumpf))
	new_data_json, error = baiduapi.tokpos_data(data_li, filedump)
	word_sentence_li, pos_sentence_li = baiduapi.get_word_pos(new_data_json)
	return word_sentence_li, pos_sentence_li


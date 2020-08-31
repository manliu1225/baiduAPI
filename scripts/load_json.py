from multiprocessing import Pool
import argparse
from . tokenization_pos import Baiduapi
import pickle
import glob 
import sys
import os
from itertools import chain
import logging

logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
	''' input: dump_f, and output dir
	output: output/filename/1~50.txt
	'''
	parser = argparse.ArgumentParser(description='Load data from the previously dumped json file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('input', help='input json file dir')
	parser.add_argument('output', help='output dir')
	parser.add_argument('process', type = int, help='process number.')
	args = parser.parse_args()
	filename_s = glob.glob(os.path.join(args.input, '*'))
	print(filename_s)
	pool = Pool(args.process)
	print(list(zip(filename_s, [args.output]*len(filename_s)))) 
	pool.map(process, list(zip(filename_s, [args.output]*len(filename_s)))) 
	pool.close()
	pool.join()
	return 0

def process(argws):
	'''
	load data from single json file
	'''
	filename, output = argws
	logger.info('processing file {}...'.format(filename))
	output_dir = os.path.join(output,os.path.basename(filename))
	if not os.path.exists(output_dir): os.mkdir(output_dir)
	new_data_json = pickle.load(open(filename, "rb"))
	baiduapi = Baiduapi()
	word_sentence_li, pos_sentence_li = baiduapi.get_word_pos(new_data_json)
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

if __name__ == '__main__':
	main()
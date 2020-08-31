#! /usr/bin/env python3
import argparse
import codecs
import logging
import sys
import os
import glob
logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.ERROR)
logger = logging.getLogger(__name__)

def main():
	parser = argparse.ArgumentParser(description='Convert plain files to two-column format.',
	        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('input_dir' , help='input dir')
	parser.add_argument('left_f', type=lambda x : open(x, 'r'), help='input file')
	parser.add_argument('right_f', type=lambda x : open(x, 'r'), help='input file')
	args = parser.parse_args()
	bracket_li = [x.strip() for x in args.left_f.readlines()] + [x.strip() for x in args.right_f.readlines()]

	filename_s = glob.glob(os.path.join(args.input_dir, '*.txt'))
	output = args.input_dir+'_processed'

	if os.path.exists(output) == False: os.makedirs(output)
	for filename in filename_s:
		with open(filename, 'r') as inputf:
			li = [x.strip() for x in inputf.readlines()]
			new_li = []
			for line in li:
				if line == '':
					new_li.append(line)
					continue
				if line.split()[0] in bracket_li: continue
				new_li.append(line)
		with open(os.path.join(output, os.path.basename(filename)), 'w') as output_f:
			for line in new_li: output_f.write(line + '\n')
	return 0

if __name__ == '__main__':
	main()
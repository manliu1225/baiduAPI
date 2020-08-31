import glob 
import sys
import os
import argparse
import codecs
import logging

logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.ERROR)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Convert plain files to two-column format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input',  help='input file')
parser.add_argument('output',  help='output file')
args = parser.parse_args()

filename_s = glob.glob(os.path.join(args.input, '*.txt'))
if os.path.exists(args.output) == False: os.makedirs(args.output)
data_li = []
for filename in filename_s:
	file_li = []
	with open(filename, 'r') as inputf:
		new_li = []
		li = inputf.readlines()
		line_li = []
		for line in li:
			line = line.strip()
			if line == '':
				file_li.append(line_li)
				line_li = []
				continue
			line_li.append(line+'\tO')
	data_li.extend(file_li)
print(len(data_li))
data_li_50 = [data_li[i:i+50] for i in range(0,len(data_li),50)]
for i, file_li in enumerate(data_li_50):
	output_filename = os.path.join(args.output, '{}.txt'.format(i))
	with open(output_filename, 'w') as outputf:
		for line_li in file_li:
			for e in line_li:
				outputf.write(e + '\n')
			outputf.write('\n')

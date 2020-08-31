import argparse
import codecs
import logging
import re

logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.ERROR)
logger = logging.getLogger(__name__)
global TAG
TAG = {'SINGER':'ART', 'ALBUM':'ALB', 'SONG':'SNG'}

def main():
	parser = argparse.ArgumentParser(description='Convert plain files to two-column format.',
	        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('input_f', type=lambda x : open(x, 'r'), help='input file')
	parser.add_argument('pos_f', type=lambda x : open(x, 'r'), help='input file')
	parser.add_argument('output_f', type=lambda x : open(x, 'w'), help='output file')
	args = parser.parse_args()

	data_li = [x.strip() for x in args.input_f.readlines()]
	pos_data_li = [x.strip() for x in args.pos_f.readlines()]
	li_li, li = [], []
	for e in pos_data_li: 
		if len(e.split()) == 1: continue
		if e!= '': li.append(e.split())
		else: 
			li_li.append(li)
			li = []

	print(li_li)
	for i, line in enumerate(data_li):
		if len(line.split('	')) > 1:
			nes = line.split('	')[1:]
			for ne in nes:
				for j in range(len(li_li[i])):
					print(li_li[i][j])
					pretag = li_li[i][j][1].split()[0]
					if (j == 0 and li_li[i][j][0] in ne.split('')[0]) or (j > 0 and li_li[i][j][0] in ne.split('')[0] and li_li[i][j-1][0] not in ne.split('')[0]): li_li[i][j][1]='{}\tB-{}'.format(pretag, TAG[ne.split('')[1]])
					elif li_li[i][j][0] in ne.split('')[0] and li_li[i][j-1][0] in ne.split('')[0] and j!=0:
						li_li[i][j][1]='{}\tI-{}'.format(pretag, TAG[ne.split('')[1]])
					elif li_li[i][j][0] not in ne.split('')[0] and len(li_li[i][j][1].split()) == 1 : li_li[i][j][1]='{}\tO'.format(pretag)
			for j in range(len(li_li[i])-1):
				if re.search(r'B-SNG|B-ALB|B-ART',li_li[i][j][1].split('\t')[-1]) and not re.search(r'I-SNG|I-ALB|I-ART',li_li[i][j+1][1].split('\t')[-1]) and not li_li[i][j][0].split('\t')[0] in [ne.split('')[0] for ne in nes]: li_li[i][j][1]='{}\tO'.format(pretag)
		else: 
			for j in range(len(li_li[i])): li_li[i][j][1]='{}\tO'.format(li_li[i][j][1])
	for sentence in li_li:
		for e in sentence: args.output_f.write('{}\t{}\n'.format(*e))
		args.output_f.write('\n')
	return 0


if __name__ == '__main__':
	main()

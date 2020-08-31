import glob 
import sys
import os
from multiprocessing import Pool
from . process_token2 import process
import argparse

parser = argparse.ArgumentParser(description='tokenize data by Baidu API.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input', help='input file')
# parser.add_argument('input_f', type=lambda x : open(x, encoding="gb2312"), help='input file')
parser.add_argument('output', help='output dir')
parser.add_argument('process', type = int, help='process number.')
args = parser.parse_args()
filename_s = glob.glob(os.path.join(args.input, '*'))
print(filename_s)
if os.path.exists(args.output) == False: os.makedirs(args.output)
pool = Pool(args.process)
print(list(zip(filename_s, [args.output]*len(filename_s)))) 
pool.map(process, list(zip(filename_s, [args.output]*len(filename_s)))) 
pool.close()
pool.join()

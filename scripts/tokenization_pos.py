#! /usr/bin/env python3

'''this script is used for tokenization and pos tagging
baidu NLP api is used
pip install baidu-aip
'''
# import chardet
from aip import AipNlp
import json
import time
import logging
import pickle
logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Baiduapi():
	def tokpos_data(self, data_li, dumpfile):
		APP_ID = '10767475'
		API_KEY = 'LsxYY5WawstbGwu56DV4i8q1'
		SECRET_KEY = 'WoKhSGCfyDN8UbL22tpk2y0tseF9HKVz'
		client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
		new_data_json = []
		error = []
		print(len(data_li))
		for line in data_li:
			line = line.strip()
			time.sleep(1)
			try:
				result_json = client.lexer(line)
				result_json_str = json.dumps(result_json)
				logger.info('Baiduapi process line {} successfully!'.format(line))
				new_data_json.append(result_json_str)
				# print(result_json_str)
			except:
				logger.error('Baiduapi process line {} error!'.format(line))
				error.append(line)
				continue
		wordf = open(dumpfile, 'wb')
		pickle.dump(new_data_json, wordf, 0)
		return new_data_json, error

	def get_word_pos(self,new_data_json_li):
		word_sentence_li, pos_sentence_li = [], []
		for x in new_data_json_li:
			try:
				sentence_json = json.loads(x)
				word_sentence_li.append([e['basic_words'] for e in sentence_json['items']])
				pos_sentence_li.append([e['pos'] if e['pos']!='' else e['ne'] for e in sentence_json['items']])
			except: continue
		return word_sentence_li, pos_sentence_li
	

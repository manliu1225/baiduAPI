f = open('./test', 'r', encoding='gb2312')
ff = open('./test_w', 'w')
for e in f.readlines():
	ff.write(e)

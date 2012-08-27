#!/usr/bin/python

import os
import sys
import math
import re

from matplotlib import pyplot as plt
import sys

COLUMN = 11
SUM    = False
FILTER = False

FilterText = ''


class File:
	
	def __init__(self):
		self.others = []
		self.path = '' 
		self.scale = 1

	def __repr__(self): 
		return '[P:'+self.path+'|S:'+str(self.scale)+'|O:'+str(len(self.others))+']';

	def getDaily(self):
		text = open(self.path).readlines()
		pnls = map(lambda l: int(l.split()[COLUMN]),text)
		return pnls

	def scaleDaily(self):
		text = []

		if(self.path == '<STDIN>'):
			text = sys.stdin.readlines()
		else:
			text = open(self.path).readlines()

		
		if(FILTER):
			tmp = []
			for l in text:
				if(l.find(FilterText) != -1):
					tmp.append(l)
			text = tmp


		text = map(lambda s: s.strip(), text)		
		pnls = map(lambda l: self.scale*float(l.split(',')[COLUMN]),text)
		return pnls

	def sumDaily(self,pnls):
		total = reduce(lambda l,v: (l.append(l[-1]+v) or l), pnls, [0])
		return total



if(len(sys.argv) < 2):
	print('Needs Path[:Scale,Path2:Scale,...] Path3\n')
	print('Options')
	print('-c <Num>\tColumn in data to plot')
	print('-g <Text>\tFilters file by <Text> much like grep')
	print('-a\tAggregate the data, default is off')
	print('-s\tRead in from stdin. Useful for piping')
	print
	print('Examples:')
	print('---------')
	print('plotOutput.py Output <--- standard plot');
	print('plotOutput.py Output:2 AlsoOutput:3 <-- plots 2 series scaled 2x and 3x');
	print('plotOutput.py Output:2,AlsoOutput <-- plots 1 series, two outputs scaled then aggregated together');
	sys.exit(1)


myfiles = []

def fileCriteria(path,arr):
	file = File()
	if(path.find('.err') == -1):
		if(path.find(',') != -1):
			fileCriteria(path[path.find(',')+1:],file.others);
			path = path[:path.find(',')]
			
		if(path.find(':') != -1):
			offset = 1
			for c in path[path.find(':')+1:]:
				if not c.isdigit() and c != "." and c != '-':
					break
				offset = offset + 1
			
			file.scale = float(path[path.find(':')+1:path.find(':')+offset])
			path = path[:path.find(':')] + path[path.find(':')+offset:]
		file.path = path; 
		
		arr.append(file);


args = sys.argv[1:]

for idx,path in enumerate(args):
	if path == "-c":
		if (1+idx) == len(args):
			print("Need Column")
			break;
		
		COLUMN = int(args[idx+1])
		del(args[idx+1])
	
	elif path == '-g':
		FILTER = True
		FilterText = args[idx+1]
		del(args[idx+1])
	elif path == '-a':
		SUM = True
	elif path == '-s':
		fileCriteria('<STDIN>',myfiles)

	elif not os.path.isdir(path):
		if(path.find('.err') == -1):
			fileCriteria(path,myfiles)
	
	else:
		for root, dirs, files in os.walk(path):
			for file in files:
				if(file.find('.err') == -1):
					fileCriteria(path,myfiles)
			# First level only
			break


#myfiles.sort()



for file in myfiles:
	
	pnls = [file.scaleDaily()]
	
	node = file.others
	while node:
		pnls.append(node[0].scaleDaily())
		node = node[0].others
	
	agg = map(sum,zip(*pnls))
	total = agg
	if(SUM):
		total = file.sumDaily(agg);
	
	plt.plot(range(0,len(total)),total)

plt.show()

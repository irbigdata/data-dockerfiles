#!/usr/bin/env python

#Average visit length for each page
from mrjob.job import MRJob
class MRmyjob(MRJob):

	def mapper(self, _, line):
		#Split the line with tab separated fields
		data=line.split(' ')
		#Parse line
		date = data[0].strip()
		time = data[1].strip()
		url = data[2].strip()
		ip = data[3].strip()
		try :
			visit_len = int(data[4].strip())
		except : 
			visit_len = 1	
		year=date[0:4]
		month=date[5:7]
		yield url, visit_len
	def reducer(self, key, list_of_values):
		count = 0
		total = 0.0
		for x in list_of_values:
			total = total+x
			count=count+1
		
		avgLen = ("%.2f" % (total/count))
		yield key, avgLen

if __name__ == '__main__':
	MRmyjob.run()
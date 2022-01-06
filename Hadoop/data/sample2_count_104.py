#!/usr/bin/env python

#Total number of times each page is visited in the year 2014
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
		#Extract year from date
		year=date[0:4]
		#Emit URL and 1 if year is 2014
		if year=='2014':
			yield url, 1

	def reducer(self, key, list_of_values):
		yield key,sum(list_of_values)

if __name__ == '__main__':
	MRmyjob.run()
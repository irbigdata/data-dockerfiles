#!/usr/bin/env python

# Most visited page in each month of year 2014
from mrjob.job import MRJob
from mrjob.step import MRStep

class FindMaxPerMonthJob(MRJob):
	def mapper1(self, _, line):
		#Split the line with tab separated fields
		data=line.split(' ') 
		#Parse line
		date = data[0].strip()
		time = data[1].strip()
		url = data[2].strip()
		ip = data[3].strip()
		#Extract year from date
		year=date[0:4]
		month=date[5:7]
		#Emit (month,url) pair and 1 if year is 2014
		if year=='2014':
			yield (month,url), 1
			
	def reducer1(self, key, list_of_values):
		yield key[0], (sum(list_of_values), key[1])

	def reducer2(self, key, list_of_values):
		yield key, max(list_of_values)
	
	def steps(self):
		return [
			MRStep(mapper=self.mapper1,
            		reducer=self.reducer1),
			MRStep(reducer=self.reducer2)
		]

if __name__ == '__main__':
	FindMaxPerMonthJob.run()
#!/usr/bin/env python


# Top 3 visited page in year 2014
from mrjob.job import MRJob
from mrjob.step import MRStep

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
		month=date[5:7]
		#Emit url and 1 if year is 2014
		if year=='2014':
			yield url, 1
	def reducer(self, key, list_of_values):
		total_count = sum(list_of_values)
		yield None, (total_count, key)
	
	def reducer2(self, _, list_of_values):
		N = 3
		list_of_values = sorted(list(list_of_values), reverse=True)
		return list_of_values[:N]
	
	def steps(self):
		return [
			MRStep(mapper=self.mapper, reducer=self.reducer),
			MRStep(reducer=self.reducer2)
		]

if __name__ == '__main__':
	MRmyjob.run()
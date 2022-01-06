#!/usr/bin/env python

# Parition records by Quarter

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
		#visit_len=int(data[4].strip())
		#Extract year from date
		year=date[0:4]
		month=int(date[5:7])
		#Emit url and 1 if year is 2014
		if year=='2014':
			if month<=3:
				yield "Q1", (date, time, url, ip, visit_len)
			elif month<=6:
				yield "Q2", (date, time, url, ip, visit_len)
			elif month<=9:
				yield "Q3", (date, time, url, ip, visit_len)
			else:
				yield "Q4", (date, time, url, ip, visit_len)
if __name__ == '__main__':
	MRmyjob.run()
#!/usr/bin/python3

import string

file1 = open("/home/jk52891/Desktop/product_trace_hsm.txt", "r")
print("Output of Read function is ")

while True:
	file_line = file1.readline()

	if not file_line:
		break

	#print(file_line)
	LineContent = file_line.rsplit(",")
	Event = LineContent[0].replace("Event:",'').strip()
	CurrentState = LineContent[1].replace("CurrentState:",'').strip()
	NextState = LineContent[2].replace("NextState:",'').strip()

	# print('Event:',Event)
	# print('CurrentState:',CurrentState)
	# print('NextState:',NextState)

	if NextState != "NA":
		print("State change here .........")
		print("Current State is: ", CurrentState, " Next State is: ", NextState)
	else:
		print("Else...........")



file1.close()
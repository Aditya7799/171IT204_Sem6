import numpy as np 


f=open("test_dataset_1.csv","r")


l=f.read()
l=l.split("\n")

a=[]

for i in l:
	temp=i.split(",")
	a.append(temp)
	# print(temp)


data_array=np.array(a)

np.save("test_dataset_1.npy",data_array)

#
#               Jiwan Ninglekhu
#               MPI with Python
#               Use case of point to point communication in MPI
#               Nov 2015
#
#
##################################################################


import numpy as np
from numpy import *
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank=comm.Get_rank()

if rank == 0:
	A = np.arange(0,10000,0.01).reshape((1000,1000))
	print "Matrix A: "
	print A
	print A.shape

	B = A.T
	print "Matrix B: "
	print B

	dotAB = np.dot(A, B)
	A1 = vsplit(A, 10)		
	
	#reshaping the sub-matrices into correct dimension as the 
	#vsplit arranged the elemets into a single array 
	a0=A1[0].reshape(100,1000)	
	a1=A1[1].reshape(100,1000)
	a2=A1[2].reshape(100,1000)
	a3=A1[3].reshape(100,1000)
	a4=A1[4].reshape(100,1000)
	a5=A1[5].reshape(100,1000)
	a6=A1[6].reshape(100,1000)
	a7=A1[7].reshape(100,1000)
	a8=A1[8].reshape(100,1000)
	a9=A1[9].reshape(100,1000)
	
	#sending each sub-matrix and the Matrix B to the nodes
	comm.send([a0,B], dest=1, tag=11)
	comm.send([a1,B], dest=2, tag=11)
	comm.send([a2,B], dest=3, tag=11)
	comm.send([a3,B], dest=4, tag=11)
	comm.send([a4,B], dest=5, tag=11)
	comm.send([a5,B], dest=6, tag=11)
    comm.send([a6,B], dest=7, tag=11)
    comm.send([a7,B], dest=8, tag=11)
    comm.send([a8,B], dest=9, tag=11)


	d1= comm.recv(source=1, tag=15)
	d2= comm.recv(source=2, tag=15)
	d3= comm.recv(source=3, tag=15)
	d4= comm.recv(source=4, tag=15)	
	d5= comm.recv(source=5, tag=15)	
	d6= comm.recv(source=6, tag=15)
	d7= comm.recv(source=7, tag=15)
	d8= comm.recv(source=8, tag=15)
	d9= comm.recv(source=9, tag=15)
	d10 = np.dot(a9, B)#one sub-matrix's dot product being calculated
	#in the master node 

	#reconstructing the received submatrices with vstack()
	Z = np.vstack((d1,d2,d3,d4,d5,d6,d7,d8,d9,d10))
	print "The constructed matrix with point-to-point mechanism of 
	MPI with 10 nodes is:\n", Z
	print 'Shape of the constructed Matrix is:\n', Z.shape 
	print 'Matrix with Direct A.B is: \n', dotAB
	print "Determinant of the constructed matrix is:\n"
	, np.linalg.det(Z)
	print "Determinant of the A.B is :\n", np.linalg.det(dotAB)
	
	assert dotAB.all() == Z.all()

elif rank == 1:
	data1 = comm.recv(source=0, tag=11)
	a_0 = np.dot(data1[0],data1[1])
	comm.send(a_0, dest=0, tag=15)

elif rank == 2:
    data2 = comm.recv(source=0, tag=11)
    a_1 = np.dot(data2[0],data2[1])
	comm.send(a_1, dest=0, tag=15)
elif rank == 3:
    data3= comm.recv(source=0, tag=11)
    a_2 = np.dot(data3[0],data3[1])       
	comm.send(a_2, dest=0, tag=15)
elif rank == 4:
    data4 = comm.recv(source=0, tag=11)
    a_3 = np.dot(data4[0],data4[1])
	comm.send(a_3, dest=0, tag=15)
elif rank == 5:
    data5 = comm.recv(source=0, tag=11)
    a_4 = np.dot(data5[0],data5[1])
	comm.send(a_4, dest=0, tag=15)
elif rank == 6:
    data6 = comm.recv(source=0, tag=11)
    a_5 = np.dot(data6[0],data6[1])
	comm.send(a_5, dest=0, tag=15)
elif rank == 7:
    data7 = comm.recv(source=0, tag=11)
    a_6 = np.dot(data7[0],data7[1])
	comm.send(a_6, dest=0, tag=15)
elif rank == 8:
   data8 = comm.recv(source=0, tag=11)
   a_7 = np.dot(data8[0],data8[1])
   comm.send(a_7, dest=0, tag=15)
elif rank == 9:
    data9 = comm.recv(source=0, tag=11)
    a_8 = np.dot(data9[0],data9[1])
	comm.send(a_8, dest=0, tag=15)

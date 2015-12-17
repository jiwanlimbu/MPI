#
#		Jiwan Ninglekhu
#		MPI with Python
#		Use case of bcast(), scatter(), gather() in MPI
#		Nov 2015
#
#
##################################################################
import numpy as np
from numpy import *
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank=comm.Get_rank()

A = np.arange(0,10000,0.01).reshape((1000, 1000))

print "Matrix A: "
print A
print A.shape
B = A.T
dotAB = np.dot(A, B)
DET = np.linalg.det(dotAB)
print "Matrix B: "
print B
print B.shape
A1 = vsplit(A, 10)
## Since vsplit made the submatrix(subarray) as single array thus 
##needed to reshape  
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


if rank == 0:
	data = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
	data1 = B ##B matrx sent as broadcast and sub-matrices of Matrix A 
	##sent as Scatter function
else: 
	data = None 
	data1 = None
	
data = comm.scatter(data, root = 0)
data1 = comm.bcast(data1, root =0)
##commented part to debug the data and rank
#print 'rank',rank,'has data:', data 
#print '\n rank has data: %d and data1: %d', data, data1
dotp =  np.dot(data, data1)
##check the shape of the dot product of sub-matrix of A and B
#print 'shape of dotp is :', dotp.shape 
#gather all the got products at master 
ndata = comm.gather(dotp,root=0)

if rank == 0:

	print 'master collected from rank :',rank,'is :', ndata
	print '\n\n'
	##check the sub-matrix
	#print 'ndata[0] is :', ndata[0]
	##check the shape of submatrix
	#print 'shape of n[0] is: ', ndata[0].shape

	##name each of the sub-matrix.Fortunately, the data gathered from 
	##all the nodes are ordered
	##by rank starting with rank 0
	n0=ndata[0]
	n1=ndata[1]
	n2=ndata[2]
	n3=ndata[3]
	n4=ndata[4]
	n5=ndata[5]
	n6=ndata[6]
	n7=ndata[7]
	n8=ndata[8]
	n9=ndata[9]
	##vstack them together starting with n0
	final = np.vstack((n0, n1, n2, n3, n4, n5, n6, n7, n8, n9))
	print 'The constructed Matrix with MPI in 10 nodes using broadcast,
	scatter &  gather is: \n', final
	print'\n'
	print 'Shape of constructed matrix is :\n', final.shape
	##print to check A dot B	
	print 'The matrix with direct A.B is :\n',dotAB 
	det = np.linalg.det(final)
	#print determinant of direct calculation and distributed MPI computing
	print '\nDeterminant of finally constructed matrix :', det
	print '\nDeterminant of (A.B) calculated directly in a node :', DET
	##check determinant of direct dot product and distributed dot product 
	##with MPI
	assert det == DET

	



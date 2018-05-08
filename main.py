#####################################
#CS 6385.001 | PROJECT-1            #
#Author: Konchady Gaurav Shenoy     #
#NETID: kxs168430                   #
#####################################

from numpy import matrix
from numpy import linalg
import sys
import random
import matplotlib.pyplot as plt
plt.rcdefaults()
import networkx as nx


N=21

k=8


class node(object)	:
	'''label='';
	neighbors=[];
	distance=[];
	cost=0;
	via=[];'''
	def __init__(self,label):
		self.label=label;
		self.bandwidth=0; #bij
		self.cost=250; #aij
		self.via=250; #aij=250
	def identify(self):
		print self.label



print ("Enter value of N");
N=input();

k=input("Enter value for k (3-15)")
k=int(k);
if k<3 or k>15:
	print "invalid k\nExiting"
	sys.exit();
	
'''
if len(sys.argv) < 2:
	print 'Need value for k\n Usage: $ python main.py <k>'
	sys.exit();
if 3 <= int(sys.argv[1]) <= 15:	
	k = int(sys.argv[1]);
	print k
else:
	print "Invalid input for k.\n[3~15] Preferred.\n Exiting...."
	sys.exit();
'''

node_table=""

print ("Provided N value: %r"%(N));
print "Value used for k: %r"%(k);

#n1=node('AXXX');
#print n1
#n1.identify()

##########
#Functions
##########

#Generate aij values
def generate_aij(k,z):
	foo=range(0,N)
	foo.remove(z) #other than i
	#print k
	#print "Foo: ",	
	#print foo
	#k=8
	chosen_k=[];
	for i in range(0,k):
		pick = random.choice(foo)
		#print "Pick: ",
		#print pick;
		foo.remove(pick)
		#print foo
		chosen_k.append(pick)
	#print "Chosen K: "
	#print chosen_k	
	return chosen_k
##

#Path functions
def path(i,j):
	print '%2r'%i,
	if i!=j:
		n=node_table[i][j]
		print "--->",
		y=n.via
		#print y 
		path(y,j)

	#print""
	return
##

#Path Cost
def path_cost(i,j):
	sum = 0
	if i==j:
		return 0
	else:
		n=node_table[i][j]
		y=n.via
		b=n.bandwidth
		a=n.cost
		sum = (a*b)
		return (sum + path_cost(y,j))

'''
def path_cost(i,j,val):
	if i!=j:
		n=node_table[i][j]
		val=val+(n.cost*n.bandwidth);
		y=n.via
		path_cost(y,j,val)
	print "(%2r,"%i+"%2r)"%j+"= "+str(val)
'''

########################
#Main Code Starts here:#
########################

#Create Node Table
node_table = [[node('') for x in range(N)] for y in range(N)] 
#node_table[1][1]=n1;

#Initialize the node array and put bij values.
for i in range(0,N):
	for j in range(0,N):
		val=str(i)+","+str(j) #i,j
		bij=random.randint(0,3) #Generate bij value
		n=node(str(val))
		n.bandwidth=bij;
		if i==j:
			n.cost=0
			n.via=j
		node_table[i][j]=n
		#print node_table[i][j]

#Now about those aij values
for i in range(0,N):
	alist=generate_aij(k,i)
	print i,
	print alist
	llen=len(alist)
	#w=0
	for j in range(0,llen):
		j_index = alist[j]
		if i!=j_index:
			n=node_table[i][j_index]	
			n.cost=1
			n.via=j_index
			node_table[i][j_index]=n

'''		
for i in range(0,N):
	for j in range(0,N):
		n=node_table[i][j]
		print "("+ n.label +") has bandwidth(bij) = "+ str(n.bandwidth) +" and cost(aij) = "+ str(n.cost)
'''
#print node_table costwise

print "\t",
for i in range(0,N):
	print '('+str(i)+')\t',
print""
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
for i in range(0,N):
	print "%2r"%i+": "+"| \t",
	for j in range(0,N):
		n=node_table[i][j]
		print "%3r"%n.cost+",%r"%n.via+"\t",
	print ""
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
##

#Routing Algorithm


for x in range(0,N):
	for i in range(0,N):
		if x!=i:
			for j in range(0,N):
				if i!=j:
					n  = node_table[i][j]
					n1 = node_table[i][x]
					n2 = node_table[x][j]
					newcost = n1.cost + n2.cost;
					if newcost < n.cost:
						n.cost = newcost
						n.via = n1.via



#print node_table costwise

print "\t",
for i in range(0,N):
	print '('+str(i)+')\t',
print""
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
for i in range(0,N):
	print "%2r"%i+": "+"| \t",
	for j in range(0,N):
		n=node_table[i][j]
		print "%3r"%n.cost+",%r"%n.via+"\t",
	print ""
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
##



#Print shortest routes

FULLSUM=0
for ii in range(0,N):
	for jj in range(0,N):
		if ii!=jj:
			print "Path from %r"%ii+" to %r"%jj+" :",
			path(ii,jj)
			print "\nPath Cost Sigma-Sum(a*b):",
			z= path_cost(ii,jj)
			print z
			FULLSUM+= z
	print"\n"
	print ''

noondirectededges=0
for ii in range(0,N):
	for jj in range(0,N):
		n=node_table[ii][jj]
		x=n.via
		if x==jj:
			noondirectededges+=1

print "Value for k ="+str(k)		
print "noondirectededges ="+str(noondirectededges)
print "TOTAL NET COST = "+str(FULLSUM)
print "DENSITY = %5.3f"%(float(noondirectededges)/float(N*(N-1)))

################
#Plot The Graph#
################
G=nx.Graph()
#pos = nx.circular_layout(G)

for i in range(0,N):
	G.add_node(i)
	
for i in range(0,N):
	for j in range(0,N):
		n=node_table[i][j]
		x=n.via
		if x==j:
			G.add_edge(i,j)
      
nx.draw(G,with_labels = True)

plt.show()


#End
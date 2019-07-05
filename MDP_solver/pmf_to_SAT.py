import binarytree as bt

# depth == coins
STATE_CODE	= 0
COIN_CODE	= 1
TEMP_CODE	= 2

def pmf_to_SAT1(pmf,depth):

	clauses=[]
	def add_equi_clause(p,q,r,clauses):
		clauses.append([[not(p[0]),p[1]],q])
		clauses.append([[not(p[0]),p[1]],r])
		clauses.append([p,[not(q[0]),q[1]],[not(r[0]),r[1]]])

	# def add_rev_impl_clause(p,q,r,clauses):
	# 	clauses.append([p,[not(q[0]),q[1]],[not(r[0]),r[1]]])

	root=False
	free_leaves=[]
	transitions = pmf
	dirac=False

	# node_desc={}
	glob_ind=0 #ind_start
	root_var=[]
	S = len(transitions)
	s_temps = [[] for x in range(S)]

	root_var=[True,[TEMP_CODE,glob_ind]]
	glob_ind += 1
	for s_i in range(len(transitions)):
		if transitions[s_i][0]==1:
			# root=bt.Node(-s_i)
			# node_desc[-s_i]=([0,True,s_i])
			s_temps[s_i].append(root_var)
			dirac=True
			break
	if(dirac == False):
		# root=bt.Node(glob_ind)
		# node_desc[glob_ind]=([0,False,0])
		free_leaves=[root_var]
	
	for d in range(1,depth+1):
		next_leaf=0
		child_free = False

		for s_i in range(S):
			if transitions[s_i][d] == 1:
				s=[True,[TEMP_CODE,glob_ind]]
				glob_ind += 1	
				s_temps[s_i].append(s)
				t=[True,[TEMP_CODE,free_leaves[next_leaf][1][1] ]]
				if(child_free == 0):
					# s <==> ( t ^ ~c )
					c=[False,[COIN_CODE,d-1]]
				else:
					# s <==> ( t ^ c )
					c=[True,[COIN_CODE,d-1]]
					next_leaf += 1
				add_equi_clause(s,t,c,clauses)
				child_free = not(child_free)
						
		if (next_leaf==len(free_leaves)) and (child_free==0):
			break

		next_free_leaves=[]
		# coin_clones=0
		if child_free==1:
			# t_2 <==> ( t_1 ^ c )
			t_2=[True,[TEMP_CODE,glob_ind]]
			glob_ind += 1
			c=[True,[1,d-1]]
			t_1=[True,[TEMP_CODE,free_leaves[next_leaf][1][1] ]]
			add_equi_clause(t_2,t_1,c,clauses)	
			# coin_clones += 1
			
			next_free_leaves.append(t_2)
			next_leaf += 1
			child_free = not(child_free)
			
		for nl in range(next_leaf,len(free_leaves)):
			t_1=[True,[2,free_leaves[next_leaf][1][1] ]]
			
			# t_2 <==> ( t_1 ^ ~c )
			t_2=[True,[TEMP_CODE,glob_ind]]
			glob_ind += 1
			c=[False,[COIN_CODE,d-1]]
			add_equi_clause(t_2,t_1,c,clauses)
			
			# t_3 <==> ( t_1 ^ c )
			t_3=[True,[TEMP_CODE,glob_ind]]
			glob_ind += 1
			c=[True,[COIN_CODE,d-1]]
			add_equi_clause(t_3,t_1,c,clauses)
			
			next_free_leaves.append(t_2)
			next_free_leaves.append(t_3)
			
		free_leaves=next_free_leaves	
		
	return clauses,glob_ind,root_var,s_temps

# pmf=[[0,0,0,1,0,1],[0,0,1,0,1,1],[0,1,0,0,0,0]]
# depth = 5
# pmf_to_SAT(pmf,depth)

# print(node_desc)
	# print(dirac)
	# print(glob_ind)
	# print(pmf)
	# print(root)
	# print(clauses)
	# for c in clauses:
	# 	for lit in c:
	# 		if not lit[0]:
	# 				print("~",end="")
	# 		else:
	# 				print(" ",end="")
	# 		if lit[1][0] == 0:
	# 			print("s",end="")
	# 		if lit[1][0] == 1:
	# 			print("c",end="")
	# 		if lit[1][0] == 2:
	# 			print("t",end="")
	# 		print(str(lit[1][1]),end="\t")
	# 	print("")

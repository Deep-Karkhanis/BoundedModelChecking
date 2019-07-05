import binarytree as bt

# depth == coins
def pmf_to_SAT1(pmf,depth,ind_start,k,curr_s):

	clauses=[]
	def add_equi_clause(p,q,r,clauses):
		clauses.append([[not(p[0]),p[1]],q])
		clauses.append([[not(p[0]),p[1]],r])
		clauses.append([p,[not(q[0]),q[1]],[not(r[0]),r[1]]])

	def add_rev_impl_clause(p,q,r,clauses):
		clauses.append([p,[not(q[0]),q[1]],[not(r[0]),r[1]]])

	root=False
	free_leaves=[]
	transitions = pmf
	dirac=False

	node_desc={}
	glob_ind=ind_start
	root_var=[]
	# state_leaves = 0 

	S = len(transitions)
	s_temps = [[] for x in range(S)]

	for s_i in range(len(transitions)):
		if transitions[s_i][0]==1:
			root=bt.Node(-s_i)
			node_desc[-s_i]=([0,True,s_i])
			
			root_var=[True,[2,glob_ind]]
			s_temps[s_i].append(root_var)
			# root_var=[True,[3,[s_i + S*k,curr_s]]]
			glob_ind += 1
			dirac=True
			break
	# print(dirac)
	if(dirac == False):
		root=bt.Node(glob_ind)
		node_desc[glob_ind]=([0,False,0])
		root_var=[True,[2,glob_ind]]
		glob_ind += 1
		free_leaves=[root]
	
	for d in range(1,depth+1):
		next_leaf=0
		child_free = False

		for s_i in range(len(transitions)):
			if transitions[s_i][d] == 1:
				if(child_free == 0):
					free_leaves[next_leaf].left = bt.Node(-1*s_i)
					node_desc[-1*s_i]=([d,True,s_i])
					free_leaves[next_leaf].value
					
					# s <==> ( c_1 ^ ~c )
					# s=[True,[3,[s_i + S*k,curr_s]]]
					s=[True,[2,glob_ind]]
					s_temps[s_i].append(s)
					glob_ind += 1
					c=[False,[1,d-1 + depth*(k-1)]]
					c_1=[True,[2,free_leaves[next_leaf].value]]
					add_equi_clause(s,c_1,c,clauses)
					# s_leaves[s_i].append([c,c_1])

				else:
					free_leaves[next_leaf].right = bt.Node(-1*s_i)
					node_desc[-1*s_i]=([d,True,s_i])
					
					# s <==> ( c_1 ^ c )
					# s=[True,[3,[s_i + S*k,curr_s]]]
					s=[True,[2,glob_ind]]
					s_temps[s_i].append(s)
					glob_ind += 1
					c=[True,[1,d-1 + depth*(k-1)]]
					c_1=[True,[2,free_leaves[next_leaf].value]]
					add_equi_clause(s,c_1,c,clauses)
					# s_leaves[s_i].append([c,c_1])
					
					next_leaf += 1
				child_free = not(child_free)
						
		if (next_leaf==len(free_leaves)) and (child_free==0):
			break

		next_free_leaves=[]
		coin_clones=0
		if child_free==1:
			free_leaves[next_leaf].right=bt.Node(glob_ind)
			
			node_desc[glob_ind]=([d,False,coin_clones])
			
			# c_2 <==> ( c_1 ^ c )
			c_2=[True,[2,glob_ind]]
			c=[True,[1,d-1 + depth*(k-1)]]
			c_1=[True,[2,free_leaves[next_leaf].value]]
			add_equi_clause(c_2,c_1,c,clauses)
			
			glob_ind += 1
				
			coin_clones += 1
			next_free_leaves.append(free_leaves[next_leaf].right)
			next_leaf += 1
			child_free = not(child_free)
			
		for nl in range(next_leaf,len(free_leaves)):
			free_leaves[nl].left=bt.Node(glob_ind)
			
			node_desc[glob_ind]=([d,False,coin_clones])
			
			# c_2 <==> ( c_1 ^ ~c )
			c_2=[True,[2,glob_ind]]
			c=[False,[1,d-1 + depth*(k-1)]]
			c_1=[True,[2,free_leaves[next_leaf].value]]
			add_equi_clause(c_2,c_1,c,clauses)
			
			glob_ind += 1
			
			coin_clones += 1
			free_leaves[nl].right=bt.Node(glob_ind)
			
			node_desc[glob_ind]=([d,False,coin_clones])
			
			# c_2 <==> ( c_1 ^ c )
			c_2=[True,[2,glob_ind]]
			c=[True,[1,d-1 + depth*(k-1)]]
			c_1=[True,[2,free_leaves[next_leaf].value]]
			add_equi_clause(c_2,c_1,c,clauses)
			
			glob_ind += 1
			
			coin_clones += 1
			next_free_leaves.append(free_leaves[next_leaf].left)
			next_free_leaves.append(free_leaves[next_leaf].right)
			
		free_leaves=next_free_leaves	
		
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
	var_added = glob_ind - ind_start
	return clauses,var_added,root_var,s_temps

# pmf=[[0,0,0,1,0,1],[0,0,1,0,1,1],[0,1,0,0,0,0]]
# depth = 5
# pmf_to_SAT(pmf,depth)
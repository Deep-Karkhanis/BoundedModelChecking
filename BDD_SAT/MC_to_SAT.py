import pmf_to_SAT as pmf_SAT
import sys
import os
import math
from pyeda.inter import *

# MODES
ST_BITS	= 0 
BDD_N0 	= 1 
BDD_LE 	= 2 
TR_LV 	= 3 
TR_NO 	= 4 
TR_LE 	= 5 
	
vars_Step = []
litCorr = dict()

def MC_to_SAT1(S_inp, ini_S_inp, tgt_S_inp, bdd_inp, coins_inp, ,K_inp, out_file,trace_file):
	# func_argv = ["",inp_file,out_file,trace_file]
	# value is scaled to coins
	
	def equi_clause(p,q):
			clses = []
			clses.append([[not(p[0]),p[1]],q])
			clses.append([p,[not(q[0]),q[1]]])
			return clses

	def equi_clause_and_list(p,lst):
			clses = []
			clses.append([p] + [[not(l[0]),l[1]] for l in lst])
			for l in lst:
				clses.append([[not(p[0]),p[1]],l])
			return clses

	def equi_clause_list(p,lst):
			clses = []
			clses.append([[not(p[0]),p[1]]]+lst)
			for lit in lst:	
				clses.append([p,[not(lit[0]),lit[1]]])
			return clses

	def get_sbit(lvl):
		lvltree = lvl - 10
		return lvltree

	def litCorrGen(inps):
		global litCorr
		global vars_Step
		
		diff = set(inps) - set(vars_Step)
		s1 = len(inps)
		s2 = len(vars_Step)
		d = len(diff)
		diff2 = list(diff)

		for aux_i in range(len(diff2)):
			aux = diff2[aux_i]
			litCorr[inps.index(aux)] = s2 + aux_i + 1
		
		for v_i in range(len(vars_Step)):
			v = vars_Step[v_i]
			litCorr[inps.index(v)] = v_i + 1
		


	def parse_Ast(expr_ast)
		# lits = set()
		lits = 0
		clauses = []
		if expr_ast[0] == 'and':
			for exp in expr_ast[1:]:
				cl1,lits1 = parse_Ast(exp)
				lits = max(lits1,lits)
				clauses += cl1

		if expr_ast[0] == 'or':
			clause = []
			for exp in expr_ast[1:]:
				cl1,lits1 = parse_Ast(exp)
				lits = max(lits1,lits)
				clause += cl1[0]
			clauses = [clause]

		if expr_ast[0] == 'lit':
			lit = expr_ast[1]
			if lit < 0:
				lits = -1*lit
				clauses = [[ [litCorr[lits] False] ]]
			else:
				lits = lit
				clauses = [[ [litCorr[lits] True] ]]
			
		if expr_ast[0] == 'const':
			lits = 1
			if expr_ast[1] == 1:
				clauses = [[ [1 True] [1 False] ]]
			if expr_ast[1] == 0:
				clauses = [[ [1 True] ] [ [1 False] ]]
			


	S = S_inp
	clauses=[]
	K = K_inp
	tgt_S = tgt_S_inp
	ini_S = ini_S_inp
	coins = coins_inp
	# List of nodes and list of leaves
	# bdds[0] ==> [id,var,low,high] node
	# bdds[1] ==> [id,type,"value"] leaves
	# value is scaled
	bdd = bdd_inp
	
	# MODES
	# 0 S(k,i)
	# 1 bdd nodes
	# 2 bdd leaves
	# 3 tree levels
	# 4 tree nodes
	# 5 tree leaves
	I = []
	for i1 in range(len(ini_S)):
		x = ini_S[i1]
		if x==0:
			I.append([False,[ST_BITS,0,i1]])
		else:
			I.append([True,[ST_BITS,0,i1]])

	clauses = clauses + I

	par_cond = [[] for x in range(len(bdd[0]) + len(bdd[1])+1)] 
	par_expr = [[] for x in range(len(bdd[0]) + len(bdd[1])+1)] 
	
	# vars_Step = dict()
	
	bdd_vars = [exprvar(("bdd_"+str(x))) for x in range(len(bdd[0]) + len(bdd[1])+1)]
	
	vars_Set += bdd_vars
	# for var_i in range(1,len(bdd_vars)):
	# 	vars_Step[bdd_vars[var_i]] = var_i + (len(ini_S)*2)
		
	for node in bdds[0]:
		lcd = node[2]
		rcd = node[3]
		par_cond[lcd].append([get_sbit(node[1]),node[0],False])
		par_cond[rcd].append([get_sbit(node[1]),node[0],True])
	
	s_vars = [0 for x in range(len(ini_S) *2)] 
	for sb_i in range(len(s_vars)):
		str_i = "s_" + str(sb_i)
		s_vars[sb_i] = exprvar(str_i)

	vars_Step += s_vars
	# for var_i in range(len(s_vars)):
	# 	vars_Step[s_vars[var_i]] = var_i + 1

	for pc_i in range(1,len(par_cond)):
		pc = par_cond[pc_i]
		node_expr = expr(0)
		for cond_i in pc:
			if pc[2] == 0:	
				node_expr = Or(node_expr,And(bdd_vars[pc[1]],Not(s_vars[pc[0]])))
			else:	
				node_expr = Or(node_expr,And(bdd_vars[pc[1]],s_vars[pc[0]]))

			# node_expr = node_expr.to_cnf()
		par_expr[pc_i] = node_expr.tseitin()
	# Root of BDD true
	par_expr[len(bdd[0]) + len(bdd[1])] = bdd_vars[len(bdd[0]) + len(bdd[1])]
	
	bdd_expr = expr(1)
	for p_expr in par_expr[1:]:
		bdd_expr = And(bdd_expr,p_expr)
	bdd_expr = bdd_expr.tseitin()

	treeN_vars = [exprvar(("treeN_"+str(x))) for x in range(coins*2 + 1)]
	treeL_vars = [exprvar(("treeL_"+str(x))) for x in range(coins)]
	tree_expr_ske = treeN_vars[0]
	
	vars_Step += (treeN_vars + treeL_vars)

	# for var_i in range(len(treeN_vars)):
	# 	vars_Step[treeN_vars[var_i]] = var_i + 1 + (len(ini_S)*2) + \
	# 									len(bdd[0]) + len(bdd[1])
	# for var_i in range(len(treeL_vars)):
	# 	vars_Step[treeL_vars[var_i]] = var_i + 1 + (len(ini_S)*2) + \
	# 									len(bdd[0]) + len(bdd[1]) + \
	# 									len(treeN_vars)
	
	for coin_i in range(coins):
		lvl = coin_i+1
		tree_expr_ske = And(tree_expr_ske,
						Equal(treeN_vars[lvl*2], And(treeN_vars[(lvl-1)*2], treeL_vars[coin_i])) ,
						Equal(treeN_vars[lvl*2 - 1], And(treeN_vars[(lvl-1)*2], Not(treeL_vars[coin_i]))) ) 
	
	# tree_expr = tree_expr_ske.tseitin()		
	tree_expr = tree_expr_ske		
	
	
	bcnt_exprs = [expr(0) for x in range(len(bdd[1]))]
	for leaf_i in range(len(bdd[1])):
		leaf = bdd[1][leaf_i]
		val = leaf[2]
		val = bin(int(val))[2:] 
		if val[0] == '1':
			bcnt_exprs[leaf_i] = expr(1)
		else:	
			for bit_i in range(len(val[1:])) :
				bit = val[bit_i + 1]
				lvl = bit_i + 1
				if bit == '1':
					bcnt_exprs[leaf_i] = Or(bcnt_exprs[leaf_i],
											treeN_vars[lvl*2 - 1])
				else:
					continue

		tree_expr = And(tree_expr,
						Implies(bdd_vars[leaf[0]], bcnt_exprs[leaf_i]))

	tree_expr = tree_expr.tseitin()

	sstep_expr = And(bdd_expr,tree_expr)
	sstep_expr = sstep_expr.tseitin()

	lits=[]	
	clauses=[]	

	expr_ast = sstep_expr.to_ast()
	litCorrGen(expr_ast.inputs)
	clauses,lits = parse_Ast(expr_ast)
	# list of lits
	# lit :: [no, t/f]

	# 1 to 2*log(S)  
	# +1 to + len bdd_vars  
	# +1 to + tree nodes
	# +1 to + tree levels

	sst_Vars = len(ini_S) * 2
	sbdd_Vars = len(bdd[0]) + len(bdd[1])
	streeN_Vars = 2*coins + 1 
	streeL_Vars = coins 
	saux_Vars = lits - (sst_Vars + sbdd_Vars + streeN_Vars + streeL_Vars)

	sLst_Vars = len(ini_S) * 2
	sLbdd_Vars = len(bdd[0]) + len(bdd[1]) + sLst_Vars
	sLtreeN_Vars = 2*coins + 1 + sLbdd_Vars
	sLtreeL_Vars = coins + sLtreeN_Vars
	sLaux_Vars = lits  
	
	Fclauses = clauses
	currLits = lits
	newLits = currLits - len(ini_S)

	clauses2 = []
	for k_i in range(2,min(K+1,3)):
		for clause in clauses:
			temp = []
			for lit in clause:
				if lit[0] <= sLst_Vars and lit[0]%2 == 1:
					temp.append([lit[0]+1, lit[1]])
				else
					temp.append([lit[0]+newLits, lit[1]])
			clauses2.append(temp)
	Fclauses += clauses2

	for k_i in range(3,K+1):
		for clause in clauses2:
			temp = []
			for lit in clause:
				temp.append([lit[0]+newLits, lit[1]])
			Fclauses.append(temp)

	totLits = newLits*K + currLits

	return Fclauses,totLits





# 	step_vars = sstep_expr.inputs
# 	tot_step_vars = len(step_vars)
# 	aux_step_vars = tot_step_vars - 





# 	temp_vars=0
# 	s_temps = [[] for x in range(S)]
# 	s_pre_temps = [[] for x in range(S)]
# 	# print(coins)

# 	for k in range(1,K+1):
# 		s_temps = [[] for x in range(S)]
# 		for s_no in range(S):
# 			for a_i in range(A):	
# 				# act_k_s = int_Acts[k][s_no]
# 				# pmf=pmfs[s_no][act_k_s]
# 				pmf=pmfs[s_no][a_i]
# 				pmf_clauses,var_added,root_var,s_ts = pmf_SAT.pmf_to_SAT1(pmf,coins,temp_vars,k,s_no)

# 				# t <==> s
# 				t=root_var
# 				s_lst = [[True,[0,s_no + (k-1)*S]]]
# 				curr_Act = a_i
# 				for a_x in range(num_act_bits):
# 					next_bit = curr_Act%2
# 					curr_Act = curr_Act/2
# 					# print(num_act_bits - 1 - a_x)
# 					if(next_bit == 1):	
# 						s_lst.append([True,[3,[k-1,s_no,num_act_bits - 1 - a_x]]])
# 					else:
# 						s_lst.append([False,[3,[k-1,s_no,num_act_bits - 1 - a_x]]])

# 				# clauses = clauses + equi_clause(s,t) + pmf_clauses
# 				clauses = clauses + equi_clause_and_list(t,s_lst) + pmf_clauses
# 				temp_vars += var_added

# 				for s_j in range(S):
# 					s_temps[s_j] = s_temps[s_j] + s_ts[s_j]

# 			# print(s_ts)
# 		# clauses += equi_clause_list([True,[0,s_no+ S*k]],[[True,[3,[s_no+ S*k,x]]] for x in range(S)])
# 		for s_no in range(S):
# 			clauses += equi_clause_list([True,[0,s_no+ S*k]],s_temps[s_no])
			
# 			# print(var_added)

# 	F = [[True,[0,tgt_S + x*S]] for x in range(K+1)]
# 	clauses.append(F)

	# f=open(out_file,"w")
# 	# total_Vars = loc_temp_vars - 1
# 	tot_StateVars = (K+1)*S
# 	tot_act_Vars = num_act_bits*K*S
# 	total_Vars = tot_StateVars + coins*K + temp_vars + tot_act_Vars
# 	tot_s_temp_vars = (S*K*S)
	# f.write("c ind")
	# for x in range(K+1):
		# for y in range(coins):	
			# f.write(" "+str(y + x*coins + tot_StateVars + 1))
# 	# f.write(" 0\n")
# 	# f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")
# 	# f.write("c\n")

# 	# print(tot_StateVars)
# 	# print(coins*K)
# 	# print(temp_vars)
# 	# print(tot_act_Vars)

# 	for i in range(len(clauses)):
# 		c = clauses[i]
# 		# f.write(str(i))
# 		for lit in c:
# 			if lit[0]==False:
# 				f.write("-")
# 			if lit[1][0] == 0:
# 				f.write(str(lit[1][1] + 1))		
# 			if lit[1][0] == 1:
# 				f.write(str(lit[1][1] + tot_StateVars + 1))		
# 			if lit[1][0] == 2:
# 				f.write(str(lit[1][1] + tot_StateVars + coins*K + 1))	
# 			if lit[1][0] == 3:
# 				f.write(str(lit[1][1][0]*S*num_act_bits + lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
# 				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
# 			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
# 			f.write(" ")
# 		f.write("0\n")

# 	f.close()

# 	f=open(trace_file,"w")

# 	f.write(str(tot_StateVars) + "\n")
# 	f.write(str(coins*K) + "\n")
# 	f.write(str(temp_vars) + "\n")
# 	f.write(str(tot_act_Vars) + "\n")


# 	f.write("c ind")
# 	for x in range(K):
# 		for y in range(coins):	
# 			f.write(" "+str(y + x*coins + tot_StateVars + 1))
# 	f.write("\n")
# 	f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")

# 	for i in range(len(clauses)):
# 		c = clauses[i]
# 		# f.write(str(i))
# 		for lit in c:
# 			if lit[0]==False:
# 				f.write("-")
# 			if lit[1][0] == 0:
# 				f.write("s"+str(lit[1][1]))	
# 			if lit[1][0] == 1:
# 				f.write("c"+str(lit[1][1]))	
# 			if lit[1][0] == 2:
# 				f.write("t"+str(lit[1][1]))	
# 			if lit[1][0] == 3:
# 				f.write("a"+str(lit[1][1][0])+"."+str(lit[1][1][1])+"."+str(lit[1][1][2]))	
# 				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
# 			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
# 			f.write("\t\t")
# 		f.write("0\n")
# 	f.close()

# 	return act_bits_list

# # os.system("approxmc --seed 42 "+func_argv[2])

# # for c in clauses:
# # 		for lit in c:
# # 			if not lit[0]:
# # 					print("~",end="")
# # 			else:
# # 					print(" ",end="")
# # 			if lit[1][0] == 0:
# # 				print("s",end="")
# # 			if lit[1][0] == 1:
# # 				print("c",end="")
# # 			if lit[1][0] == 2:
# # 				print("t",end="")
# # 			print(str(lit[1][1]),end="\t")
# # 		print("")
	

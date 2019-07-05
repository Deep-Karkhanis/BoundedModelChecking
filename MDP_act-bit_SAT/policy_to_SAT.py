import pmf_to_SAT as pmf_SAT
import sys
import os
import math


class pmf_encoding:
	def __init__(self,S):
		self.no_of_temps = -1
		self.root_temp = -1
		self.state_temp_list = [[] for x in range(S)]
	
	def gen_encod(self,probs,depth):
		pmf_SAT.pmf_to_SAT1(probs,depth,0,)


[s,k,a]

def MC_to_SAT1(S_inp, A_inp, ini_S_inp, tgt_S_inp, pmfs_inp, K_inp, out_file,trace_file):
	# func_argv = ["",inp_file,out_file,trace_file]

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

	"""
		S A k ini_S tgt_S lambda iters
		pmf for each s0 a0
		pmf for each s0 a1

		pmf for each s1 a0
		pmf for each s1 a1

		policy for k0
		policy for k1
		policy for k2
		
	"""

	S = S_inp
	clauses=[]
	K = K_inp
	tgt_S = tgt_S_inp
	ini_S = ini_S_inp
	pmfs = pmfs_inp
	coins = 0
	A = A_inp

	relevant_params = 5
	lambda_index = 5

	# f=open(func_argv[1],"r")
	# lines=f.readlines()
	# lines=[line.strip() for line in lines]

	# line_1 = lines[0].split()
	# S,A,K,ini_S,tgt_S,max_iters= [int(x) for x in \
	# 								line_1[:relevant_params] + line_1[relevant_params+1:]]
	# lambda_thres = float(line_1[lambda_index])
	# num_act_bits = 0
	# next_line = 1

	# for s_i in range(S):
	# 	pmfs.append([])
	# 	for a_i in range(A):
	# 		toks_i_j = lines[next_line].split()
	# 		next_line += 1
	# 		pmf=[]
	# 		for s_j in range(S):
	# 			p_ij=[int(x) for x in toks_i_j[s_j]]
	# 			pmf.append(p_ij)	
	# 		pmfs[s_i].append(pmf)
	# 	next_line += 1	
	num_act_bits = int(math.ceil(math.log(A,2)))

	policy = []
	act_bits_list = []
	# for k in range(K):
	# 	toks = lines[next_line].split()
	# 	policy.append([])
	# 	for s_i in range(S):
	# 		act_encod = [int(x) for x in toks[s_i]]
	# 		num_act_bits = len(act_encod)
	# 		policy[k].append(act_encod)
	# 		act_bits_list += act_encod
	# 	next_line += 1
	avlbl_Acts = [list(range(0,A)) for x in range(S)]
	for k in range(K):
		policy.append([])
		for s_i in range(S):

			act_chosen = avlbl_Acts[s_i][0]
			
			act_encod = [int(x) for x in (bin(act_chosen)[2:])]
			# num_act_bits = len(act_encod)
			policy[k].append(act_encod)
			act_bits_list += act_encod
		# next_line += 1
	
	# for l_no in range(1,len(lines)):
	# 	# print(line)
	# 	lexemes = lines[l_no].split()
	# 	i=l_no-1
	# 	pmf=[]
	# 	for j in range(len(lexemes)):
	# 		p_ij=[int(x) for x in lexemes[j]]
	# 		pmf.append(p_ij)	
	# 	pmfs.append(pmf)

	coins = len(pmfs[0][0][0]) - 1
	# f.close()

	# print(S,K,ini_S,tgt_S)
	# for pmf in pmfs:
	# 	for p_ij in pmf:
	# 		for bit in p_ij:
	# 			print(bit,end="")
	# 		print(" ",end="")
	# 	print()

	I = [[[False,[0,x]]] if x!=ini_S else [[True,[0,x]]] for x in range(S)]
	clauses = clauses + I

	P = []

	int_Acts = []

	# for k in range(K):
	# 	int_Acts.append([])
	# 	for s_i in range(S):
	# 		int_Val = 0
	# 		for a_x in range(num_act_bits):
	# 			int_Val = int_Val*2 +  int(policy[k][s_i][a_x])
	# 			if policy[k][s_i][a_x] == 0:
	# 				P.append([[False,[3,[k,s_i,a_x]]]])
	# 			else:
	# 				P.append([[True,[3,[k,s_i,a_x]]]])
	# 		int_Acts[k].append(int_Val)

	# clauses = clauses + P

	temp_vars=0
	s_temps = [[] for x in range(S)]
	s_pre_temps = [[] for x in range(S)]
	# print(coins)

	# print(num_act_bits)

	for k in range(1,K+1):
		s_temps = [[] for x in range(S)]
		for s_no in range(S):
			for a_i in range(A):	
				# act_k_s = int_Acts[k][s_no]
				# pmf=pmfs[s_no][act_k_s]
				pmf=pmfs[s_no][a_i]
				pmf_clauses,var_added,root_var,s_ts = pmf_SAT.pmf_to_SAT1(pmf,coins,temp_vars,k,s_no)

				# t <==> s
				t=root_var
				s_lst = [[True,[0,s_no + (k-1)*S]]]
				curr_Act = a_i
				for a_x in range(num_act_bits):
					next_bit = curr_Act%2
					curr_Act = curr_Act/2
					# print(num_act_bits - 1 - a_x)
					if(next_bit == 1):	
						s_lst.append([True,[3,[k-1,s_no,num_act_bits - 1 - a_x]]])
					else:
						s_lst.append([False,[3,[k-1,s_no,num_act_bits - 1 - a_x]]])

				# clauses = clauses + equi_clause(s,t) + pmf_clauses
				clauses = clauses + equi_clause_and_list(t,s_lst) + pmf_clauses
				temp_vars += var_added

				for s_j in range(S):
					s_temps[s_j] = s_temps[s_j] + s_ts[s_j]

			# print(s_ts)
		# clauses += equi_clause_list([True,[0,s_no+ S*k]],[[True,[3,[s_no+ S*k,x]]] for x in range(S)])
		for s_no in range(S):
			clauses += equi_clause_list([True,[0,s_no+ S*k]],s_temps[s_no])
			
			# print(var_added)

	F = [[True,[0,tgt_S + x*S]] for x in range(K+1)]
	clauses.append(F)

	f=open(out_file,"w")
	# total_Vars = loc_temp_vars - 1
	tot_StateVars = (K+1)*S
	tot_act_Vars = num_act_bits*K*S
	total_Vars = tot_StateVars + coins*K + temp_vars + tot_act_Vars
	tot_s_temp_vars = (S*K*S)
	# f.write("c ind")
	# for x in range(K):
	# 	for y in range(coins):	
	# 		f.write(" "+str(y + x*coins + tot_StateVars + 1))
	# f.write(" 0\n")
	# f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")
	# f.write("c\n")

	# print(tot_StateVars)
	# print(coins*K)
	# print(temp_vars)
	# print(tot_act_Vars)

	for i in range(len(clauses)):
		c = clauses[i]
		# f.write(str(i))
		for lit in c:
			if lit[0]==False:
				f.write("-")
			if lit[1][0] == 0:
				f.write(str(lit[1][1] + 1))		
			if lit[1][0] == 1:
				f.write(str(lit[1][1] + tot_StateVars + 1))		
			if lit[1][0] == 2:
				f.write(str(lit[1][1] + tot_StateVars + coins*K + 1))	
			if lit[1][0] == 3:
				f.write(str(lit[1][1][0]*S*num_act_bits + lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
			f.write(" ")
		f.write("0\n")

	f.close()

	f=open(trace_file,"w")

	f.write(str(tot_StateVars) + "\n")
	f.write(str(coins*K) + "\n")
	f.write(str(temp_vars) + "\n")
	f.write(str(tot_act_Vars) + "\n")


	f.write("c ind")
	for x in range(K):
		for y in range(coins):	
			f.write(" "+str(y + x*coins + tot_StateVars + 1))
	f.write("\n")
	f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")

	for i in range(len(clauses)):
		c = clauses[i]
		# f.write(str(i))
		for lit in c:
			if lit[0]==False:
				f.write("-")
			if lit[1][0] == 0:
				f.write("s"+str(lit[1][1]))	
			if lit[1][0] == 1:
				f.write("c"+str(lit[1][1]))	
			if lit[1][0] == 2:
				f.write("t"+str(lit[1][1]))	
			if lit[1][0] == 3:
				f.write("a"+str(lit[1][1][0])+"."+str(lit[1][1][1])+"."+str(lit[1][1][2]))	
				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
			f.write("\t\t")
		f.write("0\n")
	f.close()

	return act_bits_list

# os.system("approxmc --seed 42 "+func_argv[2])

# for c in clauses:
# 		for lit in c:
# 			if not lit[0]:
# 					print("~",end="")
# 			else:
# 					print(" ",end="")
# 			if lit[1][0] == 0:
# 				print("s",end="")
# 			if lit[1][0] == 1:
# 				print("c",end="")
# 			if lit[1][0] == 2:
# 				print("t",end="")
# 			print(str(lit[1][1]),end="\t")
# 		print("")
	


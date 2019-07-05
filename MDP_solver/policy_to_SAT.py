import pmf_to_SAT as pmf_SAT
import sys
import os
import math
import copy

STATE_CODE	= pmf_SAT.STATE_CODE
COIN_CODE	= pmf_SAT.COIN_CODE
TEMP_CODE	= pmf_SAT.TEMP_CODE

pmf_encod = []
S = -1
K = -1 
final_states = [] 
ini_S = -1 
# pmfs = [] pmfs_inp
coins = -1
A = -1

def deep_copy(obj):
    '''Return a deep (i.e., non-aliased at all) copy of obj, a nested list of 
    integers'''
    #Base case:
    if type(obj) != list:
        return obj
    copy = []
    for elem in obj:
        #The leap of faith: assume that deep_copy works!
        copy.append(deep_copy(elem))
    return copy


class pmf_encoding:
	def __init__(self,S):
		self.no_of_temps = -1
		self.root_temp = -1
		self.state_temp_list = [] #[[] for x in range(S)]
		self.clauses = []

	def gen_encod(self,pmf,depth):
		self.clauses,self.no_of_temps,self.root_temp,self.state_temp_list = pmf_SAT.pmf_to_SAT1(pmf,depth)
		return True

	def new_offset_pmf(self,offset,k):
		ret_root = deep_copy(self.root_temp)
		# print(offset)
		ret_root[1][1] += offset
		ret_temps = self.no_of_temps

		ret_s_tlst = deep_copy(self.state_temp_list)
		for s_i in range(len(self.state_temp_list)):
			for x_j in range(len(self.state_temp_list[s_i])):
				ret_s_tlst[s_i][x_j][1][1] += offset

		ret_clauses = deep_copy(self.clauses)
		# if(offset == 4):	
		# 	print(self.clauses)
		# 	print(ret_clauses)
		for c_i in range(len(self.clauses)):
			for lit_j in range(len((self.clauses)[c_i])):
				# if (ret_clauses[c_i][lit_j][1][1] > 4) and (offset == 4):
				# 		print(ret_clauses)
				# 		print(self.clauses)
				if ret_clauses[c_i][lit_j][1][0] == TEMP_CODE:
					ret_clauses[c_i][lit_j][1][1] += offset	
				if ret_clauses[c_i][lit_j][1][0] == COIN_CODE:
					ret_clauses[c_i][lit_j][1][1] += coins*(k-1)
		return ret_clauses,ret_temps,ret_root,ret_s_tlst

def create_pmf_encodings(pmfs_inp,S_inp, A_inp, ini_S_inp, tgt_Sts_inp, K_inp):
	global pmf_encod,S,K,final_states,ini_S,coins,A,S

	K = K_inp
	final_states = tgt_Sts_inp
	ini_S = ini_S_inp
	coins = len(pmfs_inp[0][0][0]) - 1
	S = S_inp
	A = A_inp
	# [s,k,a]
	pmf_encod = [[pmf_encoding(S) for a_k in range(A)] for s_i in range(S)]
	
	for s_i in range(S):
		for a_j in range(A):
			pmf_encod[s_i][a_j].gen_encod(pmfs_inp[s_i][a_j],coins)

	return True

def Policy_to_SAT1(act_list_inp,out_file,trace_file):
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

	
	# relevant_params = 5
	# lambda_index = 5
	# num_act_bits = int(math.ceil(math.log(A,2)))

	# policy = []
	# act_bits_list = []
	# avlbl_Acts = [list(range(0,A)) for x in range(S)]

	# for k in range(K):
	# 	policy.append([])
	# 	for s_i in range(S):

	# 		act_chosen = avlbl_Acts[s_i][0]
			
	# 		act_encod = [int(x) for x in (bin(act_chosen)[2:])]
	# 		policy[k].append(act_encod)
	# 		act_bits_list += act_encod
	act_list = act_list_inp
	clauses = []
	I = [[[False,[STATE_CODE,x]]] if x!=ini_S else [[True,[STATE_CODE,x]]] for x in range(S)]
	clauses = clauses + I

	P = []
	# int_Acts = []

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

	for k in range(1,K+1):
		s_temps = [[] for x in range(S)]
		for s_no in range(S):

				act_todo = act_list[k-1][s_no]
				# curr_pmf = pmf_encod[s_no][act_todo]

				# pmf_clauses,var_added,root_var,s_ts = pmf_SAT.pmf_to_SAT1(pmf,coins,temp_vars,k,s_no)

				# if act_list[0][0] == 1 and act_list[1][0] == 1:
				# 	if k==2:		
				# 		print(pmf_encod[s_no][act_todo].clauses)
				
				pmf_clauses,var_added,pmf_off_root,s_ts = \
							pmf_encod[s_no][act_todo].new_offset_pmf(temp_vars,k)
				# t <==> s
				t = pmf_off_root
				s = [True,[STATE_CODE,s_no + (k-1)*S]]
				
				clauses = clauses + equi_clause(t,s) + pmf_clauses
				temp_vars += var_added
				for s_j in range(S):
					s_temps[s_j] = s_temps[s_j] + s_ts[s_j]

		# clauses += equi_clause_list([True,[0,s_no+ S*k]],[[True,[3,[s_no+ S*k,x]]] for x in range(S)])	
		for s_no in range(S):
			clauses += equi_clause_list([True,[STATE_CODE,s_no+ S*k]],s_temps[s_no])
			
	F = []
	for x_i in range(K+1):
		for s_f in final_states:
			F.append([True,[STATE_CODE,s_f + x_i*S]])
	# F = [[True,[STATE_CODE,tgt_S + x*S]] for x in range(K+1)]
	clauses.append(F)

	f=open(out_file,"w")
	# total_Vars = loc_temp_vars - 1
	tot_StateVars = (K+1)*S
	tot_coin_vars = coins*K
	# tot_act_Vars = num_act_bits*K*S
	total_Vars = tot_StateVars + coins*K + temp_vars# tot_act_Vars
	f.write("c ind")
	for x in range(K):
		for y in range(coins):	
			f.write(" "+str(y + x*coins + tot_StateVars + 1))
	f.write(" 0\n")
	f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")
	
	for i in range(len(clauses)):
		c = clauses[i]
		# f.write(str(i))
		for lit in c:
			if lit[0]==False:
				f.write("-")
			if lit[1][0] == STATE_CODE:
				f.write(str(lit[1][1] + 1))		
			if lit[1][0] == COIN_CODE:
				f.write(str(lit[1][1] + tot_StateVars + 1))		
			if lit[1][0] == TEMP_CODE:
				f.write(str(lit[1][1] + tot_StateVars + coins*K + 1))	
			# if lit[1][0] == 3:
			# 	f.write(str(lit[1][1][0]*S*num_act_bits + lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
			f.write(" ")
		f.write("0\n")

	f.close()

	f=open(trace_file,"w")

	f.write(str(tot_StateVars) + "\n")
	f.write(str(coins*K) + "\n")
	f.write(str(temp_vars) + "\n")
	# f.write(str(tot_act_Vars) + "\n")


	f.write("c ind")
	for x in range(K):
		for y in range(coins):	
			f.write(" "+str(y + x*coins + tot_StateVars + 1))
	f.write(" 0\n")
	f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")

	for i in range(len(clauses)):
		c = clauses[i]
		# f.write(str(i))
		for lit in c:
			if lit[0]==False:
				f.write("-")
			if lit[1][0] == STATE_CODE:
				f.write(str(lit[1][1] + 1))		
				# f.write("s"+str(lit[1][1]))	
			if lit[1][0] == COIN_CODE:
				f.write(str(lit[1][1] + tot_StateVars + 1))		
				# f.write("c"+str(lit[1][1]))	
			if lit[1][0] == TEMP_CODE:
				f.write(str(lit[1][1] + tot_StateVars + coins*K + 1))	
				# f.write("t"+str(lit[1][1]))	
			# if lit[1][0] == 3:
			# 	f.write("a"+str(lit[1][1][0])+"."+str(lit[1][1][1])+"."+str(lit[1][1][2]))	
				# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
			# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
			f.write(" ")
		f.write("0\n")
	f.close()

	cmd = "approxmc "+out_file	+" | " + \
	  "egrep \"Number of solutions is: \""
	line = os.popen(cmd).read()
	line=line.strip()
	toks = line.split()
	sig = int(toks[-3])
	base,exp = [int(x) for x in (toks[-1].split('^'))]

	cnt = sig*(base**exp)
	prob = (1.0*cnt)/(2**(tot_coin_vars))


	# f=open(trace_file,"w")

	# f.write(str(tot_StateVars) + "\n")
	# f.write(str(coins*K) + "\n")
	# f.write(str(temp_vars) + "\n")
	# # f.write(str(tot_act_Vars) + "\n")


	# f.write("c ind")
	# for x in range(K):
	# 	for y in range(coins):	
	# 		f.write(" "+str(y + x*coins + tot_StateVars + 1))
	# f.write("\n")
	# f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")

	# for i in range(len(clauses)):
	# 	c = clauses[i]
	# 	# f.write(str(i))
	# 	for lit in c:
	# 		if lit[0]==False:
	# 			f.write("-")
	# 		if lit[1][0] == 0:
	# 			f.write("s"+str(lit[1][1]))	
	# 		if lit[1][0] == 1:
	# 			f.write("c"+str(lit[1][1]))	
	# 		if lit[1][0] == 2:
	# 			f.write("t"+str(lit[1][1]))	
	# 		if lit[1][0] == 3:
	# 			f.write("a"+str(lit[1][1][0])+"."+str(lit[1][1][1])+"."+str(lit[1][1][2]))	
	# 			# f.write(str(lit[1][1][0]) lit[1][1][1]*num_act_bits + lit[1][1][2] + tot_StateVars + coins*K + temp_vars + 1))	
	# 		# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
	# 		f.write("\t\t")
	# 	f.write("0\n")
	# f.close()


	return prob,cnt

import sys
import os
import random
import policy_to_SAT as Policy_SAT
import DRN_to_BMC_SAT as DRN_conv
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

trace_file = "trace/tr"
os.system("mkdir -p trace")
# os.system("python3 MC_to_SAT.py "+sys.argv[1]+" "+sys.argv[2]+" "+trace_file)

K = int(sys.argv[3])
lambda_thresh = float(sys.argv[4])
max_iters = int(sys.argv[5])

S,A,ini_S,final_states,pmfs = DRN_conv.DRN_to_BMC_SAT1(sys.argv[1])
print("------> Input Parsed")

Policy_SAT.create_pmf_encodings(pmfs,S,A,ini_S,final_states,K)


# policy = []
act_list = []
act_index_list = []
# act_bits_list = []
avlbl_Acts = [list(range(0,A)) for x in range(S)]

for k in range(K):
	act_list.append([])
	act_index_list.append([])
	# policy.append([])
	for s_i in range(S):
		index_chosen = random.randint(0,len(avlbl_Acts[s_i])-1)
		act_chosen = avlbl_Acts[s_i][index_chosen]
		
		#============== NOTE DIFFERENCE BETWEEN INDEX AND VALUE ==============
		# act_encod = [int(x) for x in (bin(act_chosen)[2:])]
		# policy[k].append(act_encod)
		# act_bits_list += act_encod
		#=====================================================================
		act_list[k].append(act_chosen)
		act_index_list[k].append(index_chosen)

# points_of_choice = S*K
achieved = 0
prev_prob,prev_cnt = Policy_SAT.Policy_to_SAT1(act_list,sys.argv[2],trace_file)

print("")
print("Iter 0")
print("No. of SATisfying Assignments\t: "+str(prev_cnt))
print("Reachability Probability\t: "+str(prev_prob))
print("")

if(prev_prob >= lambda_thresh):
	achieved = 1
	print("------> Reachability Threshold Achievable")
	
print("------> Policy: ")
for k_i in range(K):
	for s_j in range(S):
		print(act_list[k_i][s_j],end=" ")
	print("\n",end="")	
print("")

# for k_i in range(K):
# 	for s_j in range(S):
# 		print(act_list[k_i][s_j],end=" ")
# 	print("\n",end="")	
# print(prev_prob)
# print("")

for iter_ in range(1,max_iters+1):
	if achieved == 1:
		break

	converged = 1
	
	choice_at_S = list(range(S))
	choice_at_K = list(range(K))
	random.shuffle(choice_at_S)
	random.shuffle(choice_at_K)

	for ch_S in choice_at_S:
		for ch_K in choice_at_K:
			curr_Act_ind = act_index_list[ch_K][ch_S]
			
			act_rem = 	list(range(0,curr_Act_ind)) + \
						list(range(curr_Act_ind+1,len(avlbl_Acts[ch_S])))
			random.shuffle(act_rem)
			# print(len(act_rem))
			for act_new_ind in act_rem:
				act_list[ch_K][ch_S] = avlbl_Acts[ch_S][act_new_ind]
				act_index_list[ch_K][ch_S] = act_new_ind
				next_prob,next_cnt = Policy_SAT.Policy_to_SAT1(act_list,sys.argv[2],trace_file)
				
				# for k_i in range(K):
				# 	for s_j in range(S):
				# 		print(act_list[k_i][s_j],end=" ")
				# 	print("\n",end="")	
				# print(next_prob)
				# print("")
		
				if(next_prob > prev_prob):
					prev_prob = next_prob
					prev_cnt = next_cnt
					if(prev_prob >= lambda_thresh):
						achieved = 1
					converged = 0
					break

			if converged == 0:
				break
			else:
				act_list[ch_K][ch_S] = avlbl_Acts[ch_S][curr_Act_ind]
				act_index_list[ch_K][ch_S] = curr_Act_ind
		if converged == 0:
				break

	print("")
	print("Iter "+str(iter_))
	print("No. of SATisfying Assignments\t: "+str(prev_cnt))
	print("Reachability Probability\t: "+str(prev_prob))
	print("")
	
	if(converged==1 or achieved==1):
		if(converged==1):
			print("------> Optimal Policy Reached")
		if(achieved==1):
			print("------> Reachability Threshold Achievable")
		else:
			print("------> Reachability Threshold NOT Achievable")
		
		print("------> Policy: ")
		for k_i in range(K):
			for s_j in range(S):
				print(act_list[k_i][s_j],end=" ")
			print("\n",end="")	
		print("")
		break

	if(iter_ == max_iters and achieved==0):	
		print("")
		print("------> Iteration Limit reached")
		print("------> Reachability Threshold NOT YET Achieved")
			
		print("------> Policy: ")
		for k_i in range(K):
			for s_j in range(S):
				print(act_list[k_i][s_j],end=" ")
			print("\n",end="")	
		print("")
		

# print("")
# print("------>Formula Generated")

# f=open(trace_file,"r")
# lines_tr=f.readlines()
# lines_tr=[line.strip() for line in lines_tr]
# tot_state_vars = int(lines_tr[0])
# tot_coin_vars = int(lines_tr[1])
# tot_temp_vars = int(lines_tr[2])
# tot_action_vars = int(lines_tr[3])
# str_iVars_base = lines_tr[4]
# str_cnf_data = lines_tr[5]
# f.close()

# act_Vars_indices = list(range(	(tot_temp_vars+tot_state_vars+tot_coin_vars+1), \
# 						(tot_temp_vars+tot_state_vars+tot_coin_vars+tot_action_vars+2)))
# act_Vars = [act_Vars_indices[x]	if act_bits[x]==1 else -1*act_Vars_indices[x] \
#								for x in range(tot_action_vars)]

# f=open(sys.argv[2],"r")
# data_out=f.read()
# f.close()

# temp_file = sys.argv[2]+".tmp"

# f=open(temp_file,"w")
# f.write(str_iVars_base + " 0\n")
# f.write(str_cnf_data + "\n")

# clauses = []
# P = []
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
# str_action_clauses = ""
# for a_j in act_Vars:
# 	str_action_clauses = str_action_clauses + str(a_j) + " 0\n"
# f.write(str_action_clauses)
# f.write(data_out)
# f.close()

# f=open(trace_file,"r")
# lines_tr=f.readlines()
# lines_tr=[line.strip() for line in lines_tr]
# tot_state_vars = int(lines_tr[0])
# tot_coin_vars = int(lines_tr[1])
# tot_temp_vars = int(lines_tr[2])
# tot_action_vars = int(lines_tr[3])
# str_iVars_base = lines_tr[4]
# str_cnf_data = lines_tr[5]
# f.close()

# act_Vars_indices = list(range(	(tot_temp_vars+tot_state_vars+tot_coin_vars+1), \
# 						(tot_temp_vars+tot_state_vars+tot_coin_vars+tot_action_vars+2)))
# act_Vars = [act_Vars_indices[x]	if act_bits[x]==1 else -1*act_Vars_indices[x] \
# 								for x in range(tot_action_vars)]

# f=open(sys.argv[2],"r")
# data_out=f.read()
# f.close()

# temp_file = sys.argv[2]+".tmp"

# f=open(temp_file,"w")
# f.write(str_iVars_base + " 0\n")
# f.write(str_cnf_data + "\n")

# # clauses = []
# # P = []
# # for k in range(K):
# # 	int_Acts.append([])
# # 	for s_i in range(S):
# # 		int_Val = 0
# # 		for a_x in range(num_act_bits):
# # 			int_Val = int_Val*2 +  int(policy[k][s_i][a_x])
# # 			if policy[k][s_i][a_x] == 0:
# # 				P.append([[False,[3,[k,s_i,a_x]]]])
# # 			else:
# # 				P.append([[True,[3,[k,s_i,a_x]]]])
# # 		int_Acts[k].append(int_Val)
# # clauses = clauses + P
# str_action_clauses = ""
# for a_j in act_Vars:
# 	str_action_clauses = str_action_clauses + str(a_j) + " 0\n"
# f.write(str_action_clauses)
# f.write(data_out)
# f.close()

# cmd = "approxmc --seed 42 "+temp_file	+" | " + \
# 	  "egrep \"Number of solutions is: \""
# line = os.popen(cmd).read()
# line=line.strip()
# toks = line.split()
# sig = int(toks[-3])
# base,exp = [int(x) for x in (toks[-1].split('^'))]

# prev_cnt = sig*(base**exp)
# prev_prob = (1.0*prev_cnt)/(2**(tot_coin_vars))

# print("")
# print("Iter 0")
# print("No. of SATisfying Assignments\t: "+str(prev_cnt))
# print("Reachability Probability\t: "+str(prev_prob))
# print("")

# # max_prob = prev_prob	
# # max_cnt = prev_cnt
# next_prob = prev_prob	
# next_cnt = prev_cnt
# converged = 1
# # rev_bit_loc = -1

# for iter_ in range(1,max_iters+1):
# 	converged = 1
# 	a_next = random.randint(0,tot_action_vars-1)
# 	for a_x in (list(range(a_next,tot_action_vars)) + list(range(0,a_next))):
		
# 		iVars = str(abs(act_Vars[a_x]))
# 		f=open(temp_file,"w")
# 		f.write(str_iVars_base + " " + iVars + " 0\n")
# 		f.write(str_cnf_data + "\n")

# 		str_action_clauses = ""
# 		for a_j in range(tot_action_vars):
# 			if (a_j != a_x):
# 				str_action_clauses = str_action_clauses + str(act_Vars[a_j]) + " 0\n"
# 		f.write(str_action_clauses)

# 		f.write(data_out)
# 		f.close()

# 		cmd = "approxmc --seed 42 "+temp_file	+" | " + \
# 			  "egrep \"Number of solutions is: \""
# 		line = os.popen(cmd).read()
# 		line=line.strip()
# 		toks = line.split()
# 		sig = int(toks[-3])
# 		base,exp = [int(x) for x in (toks[-1].split('^'))]

# 		cnt = sig*(base**exp)
# 		prob = (1.0*cnt)/(2**(tot_coin_vars))
# 		next_cnt = cnt - prev_cnt
# 		next_prob = prob - prev_prob

# 		if(next_prob > prev_prob):
# 			prev_cnt = next_cnt
# 			prev_prob = next_prob
# 			converged = 0
# 			act_Vars[a_x] *= -1
# 			break
# 			# rev_bit_loc = a_x

# 	print("")
# 	print("Iter "+str(iter_))
# 	print("No. of SATisfying Assignments\t: "+str(prev_cnt))
# 	print("Reachability Probability\t: "+str(prev_prob))
# 	print("")
	
# 	if(converged==1 or prev_prob >= lambda_thresh):
# 		if(converged==1):
# 			print("------> Optimal Policy Reached")
# 		if(prev_prob >= lambda_thresh):
# 			print("------> Reachability Threshold Achievable")
# 		else:
# 			print("------> Reachability Threshold NOT Achievable")
		
# 		policy_bitStr = ""
# 		for x in range(tot_action_vars):
# 			if act_Vars[x] > 0:
# 				policy_bitStr += "1"
# 			else:
# 				policy_bitStr += "0"
# 		print("------> Policy: "+policy_bitStr)
# 		print("")
# 		break

	
# 	# prev_prob = max_prob
# 	# prev_cnt = max_cnt
# 	# rev_bit_loc = -1
	
# 	if(iter_ == max_iters and prev_prob < lambda_thresh):	
# 		print("")
# 		print("------> Iteration Limit reached")
# 		print("------> Reachability Threshold NOT YET Achieved")
# 		policy_bitStr = ""
# 		for x in range(tot_action_vars):
# 			if act_Vars[x] > 0:
# 				policy_bitStr += "1"
# 			else:
# 				policy_bitStr += "0"
# 		print("------> Policy: "+policy_bitStr)
# 		print("")


import sys
import os
import random
import MC_to_SAT as MC_SAT
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

S,A,ini_S,tgt_S,pmfs = DRN_conv.DRN_to_BMC_SAT1(sys.argv[1])
act_bits = MC_SAT.MC_to_SAT1(S,A,ini_S,tgt_S,pmfs, K,sys.argv[2],trace_file)
print()
print("------>Formula Generated")

f=open(trace_file,"r")
lines_tr=f.readlines()
lines_tr=[line.strip() for line in lines_tr]
tot_state_vars = int(lines_tr[0])
tot_coin_vars = int(lines_tr[1])
tot_temp_vars = int(lines_tr[2])
tot_action_vars = int(lines_tr[3])
str_iVars_base = lines_tr[4]
str_cnf_data = lines_tr[5]
f.close()

act_Vars_indices = list(range(	(tot_temp_vars+tot_state_vars+tot_coin_vars+1), \
						(tot_temp_vars+tot_state_vars+tot_coin_vars+tot_action_vars+2)))
act_Vars = [act_Vars_indices[x]	if act_bits[x]==1 else -1*act_Vars_indices[x] \
								for x in range(tot_action_vars)]

f=open(sys.argv[2],"r")
data_out=f.read()
f.close()

temp_file = sys.argv[2]+".tmp"

f=open(temp_file,"w")
f.write(str_iVars_base + " 0\n")
f.write(str_cnf_data + "\n")

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
str_action_clauses = ""
for a_j in act_Vars:
	str_action_clauses = str_action_clauses + str(a_j) + " 0\n"
f.write(str_action_clauses)
f.write(data_out)
f.close()

cmd = "approxmc --seed 42 "+temp_file	+" | " + \
	  "egrep \"Number of solutions is: \""
line = os.popen(cmd).read()
line=line.strip()
toks = line.split()
sig = int(toks[-3])
base,exp = [int(x) for x in (toks[-1].split('^'))]

prev_cnt = sig*(base**exp)
prev_prob = (1.0*prev_cnt)/(2**(tot_coin_vars))

print()
print("Iter 0")
print("No. of SATisfying Assignments\t: "+str(prev_cnt))
print("Reachability Probability\t: "+str(prev_prob))
print()

max_prob = prev_prob	
max_cnt = prev_cnt
next_prob = prev_prob	
next_cnt = prev_cnt
rev_bit_loc = -1

for iter_ in range(1,max_iters+1):
	for a_x in range(tot_action_vars):
		
		iVars = str(abs(act_Vars[a_x]))
		f=open(temp_file,"w")
		f.write(str_iVars_base + " " + iVars + " 0\n")
		f.write(str_cnf_data + "\n")

		str_action_clauses = ""
		for a_j in range(tot_action_vars):
			if (a_j != a_x):
				str_action_clauses = str_action_clauses + str(act_Vars[a_j]) + " 0\n"
		f.write(str_action_clauses)

		f.write(data_out)
		f.close()

		cmd = "approxmc --seed 42 "+temp_file	+" | " + \
			  "egrep \"Number of solutions is: \""
		line = os.popen(cmd).read()
		line=line.strip()
		toks = line.split()
		sig = int(toks[-3])
		base,exp = [int(x) for x in (toks[-1].split('^'))]

		cnt = sig*(base**exp)
		prob = (1.0*cnt)/(2**(tot_coin_vars))
		next_cnt = cnt - prev_cnt
		next_prob = prob - prev_prob

		if(next_prob > max_prob):
			max_cnt = next_cnt
			max_prob = next_prob
			rev_bit_loc = a_x


	print()
	print("Iter "+str(iter_))
	print("No. of SATisfying Assignments\t: "+str(max_cnt))
	print("Reachability Probability\t: "+str(max_prob))
	print()
	
	if(rev_bit_loc == -1 or max_prob >= lambda_thresh):
		if(rev_bit_loc == -1):
			print("------> Optimal Policy Reached")
		if(max_prob >= lambda_thresh):
			print("------> Reachability Threshold Achievable")
		else:
			print("------> Reachability Threshold NOT Achievable")
		
		policy_bitStr = ""
		for x in range(tot_action_vars):
			if act_Vars[x] > 0:
				policy_bitStr += "1"
			else:
				policy_bitStr += "0"
		print("------> Policy: "+policy_bitStr)
		print()
		break

	
	act_Vars[rev_bit_loc] *= -1
	prev_prob = max_prob
	prev_cnt = max_cnt
	rev_bit_loc = -1
	
	if(iter_ == max_iters and max_prob < lambda_thresh):	
		print()
		print("------> Iteration Limit reached")
		print("------> Reachability Threshold NOT YET Achieved")
		policy_bitStr = ""
		for x in range(tot_action_vars):
			if act_Vars[x] > 0:
				policy_bitStr += "1"
			else:
				policy_bitStr += "0"
		print("------> Policy: "+policy_bitStr)
		print()


import sys
import os


f1=open("./mdp_1","w")
f2=open("./mdp_k","w")
edge = int(sys.argv[1])
K = int(sys.argv[2])
S = edge*edge
tot_S = S*(K+1)
tgt_x = int(sys.argv[3])
tgt_y = int(sys.argv[4])

f1.write("@type: MDP\n")
f1.write("@parameters\n")
f1.write("\n")
f1.write("@reward_models\n")
f1.write("\n")
f1.write("@nr_states\n")
f1.write(str(S)+"\n")
f1.write("@model\n")

f2.write("@type: MDP\n")
f2.write("@parameters\n")
f2.write("\n")
f2.write("@reward_models\n")
f2.write("\n")
f2.write("@nr_states\n")
f2.write(str(tot_S)+"\n")
f2.write("@model\n")

strs_misc = ["" for s in range(3)]
strs_misc[0] = "state "
strs_misc[1] = "init "
strs_misc[2] = "target "

for s_i in range(edge):
	for s_j in range(edge):
		curr_S = s_i*edge + s_j
		succ_L = s_i*edge + min(edge-1,s_j+1)
		succ_R = min(edge-1,s_i+1)*edge + s_j
		#s0
		buf = strs_misc[0]+str(curr_S)+" "
		if((s_i+s_j) == 0):
			buf += strs_misc[1]
		if(s_i == tgt_x and s_j == tgt_y):
			buf += strs_misc[2]
		buf += "\n"

		buf += "	action 0\n"
		buf += "		"+str(succ_L)+" : 0.5\n"
		buf += "		"+str(succ_R)+" : 0.5\n"
		
		f1.write(buf)
		buf = ""

for k_i in range(K+1):
	for s_i in range(edge):
		for s_j in range(edge):
			curr_S = k_i*edge*edge + s_i*edge + s_j
			succ_L = -1 
			succ_R = -1
			if k_i == K:
				succ_L = curr_S
				succ_R = curr_S
			else: 
				succ_L = (k_i+1)*edge*edge + s_i*edge + min(edge-1,s_j+1)
				succ_R = (k_i+1)*edge*edge + min(edge-1,s_i+1)*edge + s_j
			
			buf = strs_misc[0]+str(curr_S)+" "
			if((s_i+s_j+k_i) == 0):
				buf += strs_misc[1]
			if(s_i == tgt_x and s_j == tgt_y):
				buf += strs_misc[2]
			buf += "\n"

			buf += "	action 0\n"
			buf += "		"+str(succ_L)+" : 0.5\n"
			buf += "		"+str(succ_R)+" : 0.5\n"
			
			f2.write(buf)
			buf = ""
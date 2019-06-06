import pmf_to_SAT as pmf_SAT
import sys
import os

def equi_clause(p,q):
		clses = []
		clses.append([[not(p[0]),p[1]],q])
		clses.append([p,[not(q[0]),q[1]]])
		return clses

def equi_clause_list(p,lst):
		clses = []
		clses.append([[not(p[0]),p[1]]]+lst)
		for lit in lst:	
			clses.append([p,[not(lit[0]),lit[1]]])
		return clses

"""
	S k ini_S tgt_S
	pmf for each s
	
"""

S = 0
clauses=[]
K = 0
tgt_S = -1
ini_S = -1
pmfs = []
coins = 0

f=open(sys.argv[1],"r")
lines=f.readlines()
lines=[line.strip() for line in lines]

line_1 = [int(x) for x in lines[0].split()]
S,K,ini_S,tgt_S= line_1

for l_no in range(1,len(lines)):
	# print(line)
	lexemes = lines[l_no].split()
	i=l_no-1
	pmf=[]
	for j in range(len(lexemes)):
		p_ij=[int(x) for x in lexemes[j]]
		pmf.append(p_ij)	
	pmfs.append(pmf)

coins = len(pmfs[0][0]) - 1
f.close()

# print(S,K,ini_S,tgt_S)
# for pmf in pmfs:
# 	for p_ij in pmf:
# 		for bit in p_ij:
# 			print(bit,end="")
# 		print(" ",end="")
# 	print()

I = [[[False,[0,x]]] if x!=ini_S else [[True,[0,x]]] for x in range(S)]
clauses = clauses + I

temp_vars=0
s_temps = [[] for x in range(S)]
# print(coins)

for k in range(1,K+1):
	for s_no in range(S):
		pmf=pmfs[s_no]
		pmf_clauses,var_added,root_var,s_ts = pmf_SAT.pmf_to_SAT1(pmf,coins,temp_vars,k,s_no)

		# t <==> s
		t=root_var
		s=[True,[0,s_no + (k-1)*S]]

		clauses = clauses + equi_clause(s,t) + pmf_clauses
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

f=open(sys.argv[2],"w")
# total_Vars = loc_temp_vars - 1
tot_StateVars = (K+1)*S
total_Vars = tot_StateVars + coins*K + temp_vars
tot_s_temp_vars = (S*K*S)
f.write("c ind")
for x in range(K):
	for y in range(coins):	
		f.write(" "+str(y + x*coins + tot_StateVars + 1))
f.write(" 0\n")
f.write("p cnf "+str(total_Vars)+" "+str(len(clauses))+"\n")
# f.write("c\n")

for i in range(len(clauses)):
	c = clauses[i]
	# f.write(str(i))
	for lit in c:
		if lit[0]==False:
			f.write("-")
		if lit[1][0] == 0:
			f.write(str(lit[1][1] + 1))		
			# f.write("s"+str(lit[1][1]))	
		if lit[1][0] == 1:
			f.write(str(lit[1][1] + tot_StateVars + 1))		
			# f.write("c"+str(lit[1][1]))	
		if lit[1][0] == 2:
			f.write(str(lit[1][1] + tot_StateVars + coins*K + 1))	
			# f.write("t"+str(lit[1][1]))	
		# if lit[1][0] == 3:
		# 	f.write(str(lit[1][1][1] + S*(lit[1][1][0]-S) + tot_StateVars + coins*K + 1))		
		f.write(" ")
	f.write("0\n")

f.close()

cmd = "approxmc --seed 42 "+sys.argv[2]		+" | " + \
	  "egrep \"Number of solutions is: \""
line = os.popen(cmd).read()
line=line.strip()
toks = line.split()
sig = int(toks[-3])
base,exp = [int(x) for x in (toks[-1].split('^'))]

cnt = sig*(base**exp)
prob = (1.0*cnt)/(2**(coins*K))
print()
print("No. of SATisfying Assignments\t: "+str(cnt))
print("Rechability Probability\t\t: "+str(prob))
print()
# os.system("approxmc --seed 42 "+sys.argv[2])



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
	


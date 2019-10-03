import sys
import os
import random
import MC_to_SAT as MC_SAT
import DD_to_SAT as DD_conv
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

ini_S = int(sys.argv[2])
tgt_S = int(sys.argv[3])
K = int(sys.argv[4])
# lambda_thresh = float(sys.argv[4])
# max_iters = int(sys.argv[5])

ini_S, tgt_S, bdd, coins = DD_conv.DD_to_SAT1(sys.argv[1],ini_S,tgt_S)
print("------> Input Parsed")

Fclauses,totLits,indVars = MC_SAT.MC_to_SAT1(ini_S, tgt_S, bdd, coins ,K,trace_file)

f=open(trace_file,"w")

f.write("c ind")
for x in indVars:
    f.write(" "+str(x))
f.write(" 0\n")
f.write("p cnf "+str(totalLits)+" "+str(len(Fclauses))+"\n")

for i in range(len(Fclauses)):
    c = Fclauses[i]
    for lit in c:
        if lit[1]==False:
            f.write("-")
        f.write(str(lit[0]))
        f.write(" ")
    f.write("0\n")
f.close()

cmd = "approxmc "+trace_file+" | " + \
    "egrep \"Number of solutions is: \""
line = os.popen(cmd).read()
line=line.strip()
toks = line.split()
sig = int(toks[-3])
base,exp = [int(x) for x in (toks[-1].split('^'))]

cnt = sig*(base**exp)
prob = (1.0*cnt)/(2**(tot_coin_vars))

print("")
print("No. of SATisfying Assignments\t: "+str(cnt))
print("Reachability Probability\t: "+str(prob))
print("")
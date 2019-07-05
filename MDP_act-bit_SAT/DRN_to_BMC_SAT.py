import sys

def float_to_bitStr(x,prec=7):
	bitStr=[0]
	num=x
	if num==1.0:
		return [1],0
	num = num - int(num)
	for i in range(prec):
		if num == 0.0:
			break
		num = num*2.0
		bitStr.append(int(num))
		num = num - int(num)
	if(num != 0.0):
		print("ERROR: "+str(x)+" cannot be represented with 7 binary places")

	return bitStr,(i+1)

def DRN_to_BMC_SAT1(inp_file,out_file=""):

	S = 0
	tgt_S = -1
	ini_S = -1
	T = [] #a,s,s
	A = 0

	clauses=[]
	K = 0
	coins = 0

	f = open(inp_file,"r")
	lines = f.readlines()
	lines=[line.strip() for line in lines]
	statements = []
	for line in lines:
		if len(line) == 0:
			continue
		if line[:2] == "//":
			continue
		else:
			statements.append(line.split())
	
	model_tag_start = -1
	# model_tag_end = -1
	for line_i in range(len(statements)):
		line = statements[line_i]
		if line[0] == "@type":
			if line[1].lower() != "mdp":
				print("ERROR: Not a MDP File")
				sys.exit()
		if line[0] == "@nr_states":
			S = int(statements[line_i + 1][0])
			T = [[[[0] for s_i in range(S)] for s_j in range(S)]]
		if line[0] == "@model":
			model_tag_start = line_i

	curr_prec = 0
	curr_S = -1
	curr_A = -1
	max_A = 0
	for line_i in range(model_tag_start+1,len(statements),1):
		line=statements[line_i]
		# print(line[0])
		if line[0][0] == "@":
			break
		elif line[0] == "state":
			curr_S = int(line[1])
			curr_A = -1
			for tok in line:
				if tok.lower() == "init":
					ini_S = curr_S
				if tok.lower() == "target":
					tgt_S = curr_S
		elif line[0] == "action":
			curr_A = int(line[1])
			if (A-1) < curr_A:
				for a_x in range(curr_A - (A-1)):
					T.append([[[0] for s_i in range(S)] for s_j in range(S)])
				A = curr_A+1
			# print(A)
		else:
			# print(line[0])
			T[curr_A][curr_S][int(line[0])],prec_ret = float_to_bitStr(float(line[2]))
			if prec_ret>curr_prec :
				curr_prec = prec_ret

	pmfs=[[[[] for s_j in range(S)] for a_x in range(A)] for s_i in range(S)]

	for a_x in range(A):
		for s_i in range(S):
			for s_j in range(S):
				pmfs[s_i][a_x][s_j] = T[a_x][s_i][s_j]
				if len(pmfs[s_i][a_x][s_j]) < (curr_prec + 1):
					pmfs[s_i][a_x][s_j] += [0 for add_0 in \
											range((curr_prec+1)-len(pmfs[s_i][a_x][s_j]))]

	return S,A,ini_S,tgt_S,pmfs
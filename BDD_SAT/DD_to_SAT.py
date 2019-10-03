import sys
import os
import math

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

def DD_to_SAT1(inp_file,ini_S,tgt_S,out_file=""):

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
	
	trans_tag_start = -1
	trans_tag_end = -1
	for line_i in range(len(statements)):
		line = statements[line_i]
		if line[0] == "%transitions":
			trans_tag_start = line_i + 1
		if trans_tag_end == -1 and trans_tag_start != -1:
			toks = line[0].split(',') 
			if toks[0] == "]":
				trans_tag_end = line_i

	bdd = [[],[]]
	max_prec = 0
	max_level = 0
	print(trans_tag_start,trans_tag_end)
	for line_i in range(trans_tag_start+1,trans_tag_end):
		line=statements[line_i]
		# print(line[0])
		word=line[0]
		word = word.replace(')','(')
		toks = word.split('(')
		if toks[0] == "leaf":
			toks1 = toks[1].split(',')
			leaf = []
			leaf.append(int(toks1[0]))
			leaf.append(int(toks1[1]))
			leaf_2,prec = float_to_bitStr(float(toks1[2][1:-1]))
			leaf.append(leaf_2)
			max_prec = max(prec,max_prec)
			bdd[1].append(leaf)    
		else:
			toks1 = toks[1].split(',')
			node = [0 for x in range(0,4)]
			node[0] = int(toks1[0])
			node[1] = int(toks1[1])
			node[2] = int(toks1[2])
			node[3] = int(toks1[3])
			bdd[0].append(node)
			# max_node = max(node[0],max_node)
			max_level = max(node[1],max_level)

	for leaf in bdd[1]:
		if len(leaf[2]) < (max_prec+1):
		   leaf[2] =    leaf[2] + \
						[0 for x in range(0,(max_prec+1 - len(leaf[2])))] 
	
	coins = max_prec
	max_level = int((max_level - 10 + 1)/2)
	
	ini_S_b = bin(ini_S)[2:]
	if len(ini_S_b) < max_level:
		ini_S_b =   [0 for x in range(0,(max_level - len(ini_S_b)))] \
					+ [int(x) for x in ini_S_b]
	
	tgt_S_b = bin(tgt_S)[2:]
	if len(tgt_S_b) < max_level:
		tgt_S_b =   [0 for x in range(0,(max_level - len(tgt_S_b)))] \
					+ [int(x) for x in tgt_S_b]
	
	return ini_S_b, tgt_S_b, bdd, coins
# BoundedModelChecking
Bounded Model Checking using #SAT


This tool uses approxMC to calculate bounded reachability probability of a given target state from a given initial state in a Markov Chain

__Usage:__

```
$ python3 BMC_SAT.py inp_file out_file
```

__Dependencies:__

1)ApproxMC 			:	https://github.com/meelgroup/ApproxMC

2)Python binarytree	:	https://pypi.org/project/binarytree/

===============================================================

__Input file format:__

	--No.of States-- --k-- --ini_S-- --tgt_S--
	--probability mass function for state 1--
	--probability mass function for state 2--
	--probability mass function for state 3--
			..
			..
			..
	

Note:		

1)  The prob mass function is a floating point number in binary
	eg: 
		If 	S = 2 k=2 
			T(s0,s0) = 1/4	= 0.01 
			T(s0,s1) = 3/4	= 0.11
			T(s1,s0) = 0	= 0.00 
			T(s1,s1) = 1	= 1.00

		File will be :
		(the point is omitted when giving input)
		
		$ cat inp_file
		2 2 0 1
		001 011
		000 100


2)  All the |S|^2 transition probabilities thus written must be of same length.	Thus in the above example , 1.0 is written as 100 and not 10

===============================================================

__Examples:__

```
$ python3 BMC_SAT.py inputs/inp1 outputs/out1 

No. of SATisfying Assignments	: 15
Rechability Probability		: 0.9375

$ python3 BMC_SAT.py inputs/inp2 outputs/out2 

No. of SATisfying Assignments	: 6
Rechability Probability		: 0.75

```

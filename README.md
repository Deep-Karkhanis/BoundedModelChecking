# BoundedModelChecking
Bounded Model Checking using #SAT

This tool uses approxMC to calculate optimal bounded reachability probability of a given target state from a given initial state for MDPs and Markov Chains

__Usage:__

For Markov Chains 
```
$ cd MC_solver
$ python3 BMC_SAT.py inp_file out_file
```
Input file details provided later

===============================================================\
For MDPs: 
```
$ cd MDP_solver
$ python3 BMC_SAT.py inp_file out_file _k_ _lambda_ _maxiters_
```
    Here:
	1) Input file should be in DRN format
	2) _k_ is the step limit 
	3) _lambda_ is the lower bound on reachability probability to be checked
	4) _maxiters_ is the maximum number of iterations for policy_iteration algorithm
  
For MDPs (actions encoded into the SAT formula itself): 
```
$ cd MDP_act-bit_SAT
$ python3 BMC_SAT.py inp_file out_file _k_ _lambda_ _maxiters_
```
     Here:
	1) Input file should be in DRN format
	2) _k_ is the step limit 
	3) _lambda_ is the lower bound on reachability probability to be checked
	4) _maxiters_ is the maximum number of iterations for policy_iteration algorithm



__Dependencies:__

1) ApproxMC 		:	https://github.com/meelgroup/ApproxMC

2) Python binarytree	:	https://pypi.org/project/binarytree/



===============================================================

__Input for Markov Chains__

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

================================================================

__BDD Based Model Counting:__

```
cd BDD_SAT
python3 BMC_SAT.py dd_file ini_S tgt_S K

```

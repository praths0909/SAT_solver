# ----------------------Necessary Libraries--------------#
import random
from pysat.solvers import Solver
import numpy as np
import time
from pysat.card import *
#---------------------Function for printing Sudokus-----------#

def prints_sudoku(data,k):
    print("Sudoku A is:-")
    for i in range(k*k):
        print(data[i])
    print("Sudoku B is:-")
    for i in range(k*k):
        print(data[i+k*k])

# -----------------input the value of k-------------------# 
k=int(input("Enter the value of k :-"))
k2=k*k
#--------------------Initaialization-----------------------#

sol = Solver(name='m22',use_timer=True)
begin=time.time()
a =[]
b=[]
#-----------------making  empty sudoku pair----------------#
data=[]
for i in range(k2):
    data.append([])
    for j in range(k2):
        data[i].append(0)


for i in range(k2):
    data.append([])
    for j in range(k2):
        data[i+k2].append(0)

#-------------------creating mapping of variables with natural numbers--------------#
## a is first sudoku maping
## b is second sudoku mapping
q=0
#### for a
for i in range(k*k):
    a.append([])
    for j in range(k*k):
        a[i].append([])
        for l in range(k*k):
            q=q+1
            a[i][j].append(q)

#### for b
for i in range(k*k):
    b.append([])
    for j in range(k*k):
        b[i].append([])
        for l in range(k*k):
            q=q+1
            b[i][j].append(q)
        
# --------------------filling one of the random diagonal block-----------------------#
temp=[]
for i in range(k2):
    temp.append(i)
random.shuffle(temp)
temp2=[]
for i in range(k):
    temp2.append(i)
random.shuffle(temp2)

block=temp2[0]
q=0
random.shuffle(temp)
for i in range(k):
    for j in range(k):
        data[(block%k)*k+i][(int(block/k)*k)+j]=temp[q]
        q=q+1


#--------------------- one place will hold only one value------------#
#### for a
for i in range(k*k):
    for j in range(0,k*k):
        s=[]
        for l in range(0,k*k):
            s.append(a[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)

#### for b
for i in range(k*k):
    for j in range(0,k*k):
        s=[]
        for l in range(0,k*k):
            s.append(b[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)

# ------------------one row will have all number from 1->k*k-----------#
#### for a
for i in range(k*k):
    for l in range(k*k):
        s=[]
        for j in range(k*k):
            s.append(a[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)
#### for b
for i in range(k*k):
    for l in range(k*k):
        s=[]
        for j in range(k*k):
            s.append(b[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)

# -----------------one column will have all number from 1->k*k----------#
#### for a
for j in range(k*k):
    for l in range(k*k):
        s=[]
        for i in range(k*k):
            s.append(a[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)
#### for b
for j in range(k*k):
    for l in range(k*k):
        s=[]
        for i in range(k*k):
            s.append(b[i][j][l])
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)
        
# -------------------one block will have all the values 1->k*k---------#
#### for a
for block in range(k*k):
    for l in range(k*k):
        s=[]
        for i in range(k):
            for j in range(k):
                s.append(a[(block%k)*k+i][(int(block/k)*k)+j][l])    
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)
#### for b
for block in range(k*k):
    for l in range(k*k):
        s=[]
        for i in range(k):
            for j in range(k):
                s.append(b[(block%k)*k+i][(int(block/k)*k)+j][l])    
        cnf1=CardEnc.equals(s, encoding=EncType.pairwise)
        sol.append_formula(cnf1.clauses)
        
# ------------------two positions in both sudoku should not have same value-------#

for i in range(k*k):
    for j in range(k*k):
        for l in range(k*k):
            sol.add_clause([-a[i][j][l],-b[i][j][l]])

# ------------------------value assumptions of the block we filled randomly --------------------------#
assume=[]
for i in range(k*k):
    for j in range(k*k):
        if data[i][j]>0:
            assume.append(a[i][j][data[i][j]])
                
for i in range(k*k):
    for j in range(k*k):
        if data[i+k*k][j]>0:
            assume.append(a[i][j][data[i+k*k][j]-1])

# ----------------------------Getting the answer Sudoku -------------------------------------#
ok=sol.solve(assumptions=assume)
answer=sol.get_model()
#--------------------Converting answer in 2Darray form-----------------------------#
sol_a =[]
sol_b=[]
q=-1
#### for a
for i in range(k*k):
    sol_a.append([])
    for j in range(k*k):
        sol_a[i].append([])
        for l in range(1,k*k+1):
            q=q+1
            if(answer[q]>0):
                sol_a[i][j]=l
#### for b
for i in range(k*k):
    sol_b.append([])
    for j in range(k*k):
        sol_b[i].append([])
        for l in range(1,k*k+1):
            q=q+1
            if(answer[q]>0):
                sol_b[i][j]=l
data=sol_a+sol_b
prints_sudoku(data,k)   #prints the sudoku pair
arr=np.array(data)
# saving in csv the solution sudoku
np.savetxt('generator_solution.csv', arr, delimiter=',', fmt='%d')
# -----------------making a clause which will not give the previous solution again-----------#
s1=[]
for i in range(k2):
    for j in range(k2):
        s1.append(-a[i][j][data[i][j]-1])
for i in range(k2):
    for j in range(k2):
        s1.append(-b[i][j][data[i+k2][j]-1])
sol.add_clause(s1)

# --------------------Making an array of all positions ----------------------------------------# 
temp=[]
for i in range(2*k2):
    for j in range(k2):
        temp.append([i,j])
#--------------------------------Assumptions of all values in answer-----------------------#
assume=[]
for i in range(k2):
    for j in range(k2):
        assume.append(a[i][j][data[i][j]-1])
for i in range(k2):
    for j in range(k2):
        assume.append(b[i][j][data[i+k2][j]-1])
# -----------------------------Iterating over list of positions-----------------------------------------#

for pos in temp:
    i=pos[0]
    j=pos[1]
    w=data[i][j]
    data[i][j]=0    
    # removing the current position from assumptions
    if(i<k*k):
        assume.remove(a[i][j][w-1])
    else:
        assume.remove(b[i-k2][j][w-1])
    
    ans=sol.solve(assumptions=assume)

    # if there exist an answer after removing this position ,then we have to include it back for getting unique solution
    if(ans==True):  
        data[i][j]=w
        if(i<k*k):
            assume.append(a[i][j][data[i][j]-1])
        else:
            assume.append(b[i-k2][j][data[i][j]-1])
    


# ------------------------------------printing and saving the final solution in csv--------------------------------------------# 
prints_sudoku(data,k)
arr=np.array(data)
np.savetxt('generator.csv', arr, delimiter=',', fmt='%d')
#------------------------------total time taken--------------------------------------#
end =time.time()
print("Total Time Taken is",end-begin)



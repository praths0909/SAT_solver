# ----------------------Necessary Libraries--------------#
from pandas import read_csv
from math import sqrt
from pysat.solvers import Solver
from pysat.card import *
import numpy as np
import time

begin=time.time() ### beginning time of program ###
#---------------------Function for printing Sudokus-----------#
def prints_sudoku(data,k):
    print("Sudoku A is:-")
    for i in range(k*k):
        print(data[i])
    print("Sudoku B is:-")
    for i in range(k*k):
        print(data[i+k*k])

#-------------------------Taking input-----------------------------#

file=read_csv("ques.csv",header=None)
data=file.values
k= int(sqrt(sqrt(data.size/2)))  #finding value of k

#------------------------Showing input in terminal-----------------#
print("k =",k)

prints_sudoku(data,k)
#---------------------------initialization-----------------------------#
sol = Solver(name='m22')
a =[]     # a contains first sudoku
b=[]      # b contains second sudoku


#------------------------creating mapping with natural number-------------------------------------#
q=0
##### for a
for i in range(k*k):
    a.append([])
    for j in range(k*k):
        a[i].append([])
        for l in range(k*k):
            q=q+1
            a[i][j].append(q)

##### for b
for i in range(k*k):
    b.append([])
    for j in range(k*k):
        b[i].append([])
        for l in range(k*k):
            q=q+1
            b[i][j].append(q)

#--------------------- one place will hold only one value-----------------#
##### for a
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
        
# ------------------two positions in both sudoku should not have same value----------#

for i in range(k*k):
    for j in range(k*k):
        for l in range(k*k):
            sol.add_clause([-a[i][j][l],-b[i][j][l]])
            
# ---------------------Already filled values are taken in assumptions----------------------------#

assume=[]
#### for a
for i in range(k*k):
    for j in range(k*k):
        if data[i][j]>0:
            assume.append(a[i][j][data[i][j]-1])
               
#### for b
for i in range(k*k):
    for j in range(k*k):
        if data[i+k*k][j]>0:
            assume.append(b[i][j][data[i+k*k][j]-1])
               
#--------------------------------solve using Pysat----------------------------#

ok= sol.solve(assumptions=assume)
if ok==True:   # if solution Exist
    print("Yeah ! We found the answer")
    answer=sol.get_model()
    sol_a =[]
    sol_b=[]
    q=-1
    for i in range(k*k):
        sol_a.append([])
        for j in range(k*k):
            sol_a[i].append([])
            for l in range(1,k*k+1):
                q=q+1
                if(answer[q]>0):
                    sol_a[i][j]=l
    for i in range(k*k):
        sol_b.append([])
        for j in range(k*k):
            sol_b[i].append([])
            for l in range(1,k*k+1):
                q=q+1
                if(answer[q]>0):
                    sol_b[i][j]=l
    data=sol_a+sol_b
    prints_sudoku(data,k)    

else:    # if solution not exist
    print("Sorry ! Answer is not possible")

#-------------------converting solution in csv---------------#

arr=np.array(data)
np.savetxt('sol.csv', arr, delimiter=',', fmt='%d')
#----------------------total time taken in running whole program--------#
end =time.time()
print("Total Time Taken is",end-begin)

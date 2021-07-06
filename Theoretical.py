import numpy as np

#there are 40 squares on the board (plus 2 on side for jail wiaiting)
#first is GO, position 0
#on positions 2,17,33 we have community chest DECK1
DECK1_Pos = [2,17,13]
#on positoins 7,22,36 for chance DECK2
DECK2_Pos = [7,22,36]

#The deck consists of positions that you could move to and their
#respective probability, -1 would be not moving (at end of list).
DECK1 = np.array([[0,0.5],[-1,0.5]])
DECK2 = np.array([[0,0.5],[-1,0.5]])

#Ways to roll an their probs
DRolls = np.array([2,3,4,5,6,7,8,9,10,11,12])
DProbs = np.array([1,2,3,4,5,6,5,4,3,2,1])/36
print(DProbs[0]*36)
print(len(DProbs))



#TRANSITION MATRIX

P = np.zeros((42,42))

#start by considering everything apart from what happens when you
#are in jail
for i in range(40):
    if i != 30: #position of go to jail
        #first get probs for just rolling 2-12
        for k in range(11):
            j=i+k+2
            #print(j)
            #print(DProbs[k]*36)
            P[i,j%40] = DProbs[k]
        #now consider landing on chance/chest
        for pos in DECK1_Pos:
            if P[i,pos]>0:
                for pair in DECK1:
                    if pair[0] != -1:
                        P[i,int(pair[0])] += pair[1]*P[i,pos]
                    elif pair[0] == -1:
                        P[i,pos] = pair[1]*P[i,pos]
        for pos in DECK2_Pos:
            if P[i,pos]>0:
                for pair in DECK2:
                    if pair[0] != -1:
                        P[i,int(pair[0])] += pair[1]*P[i,pos]
                    elif pair[0] == -1:
                        P[i,pos] = pair[1]*P[i,pos]
                        

                
print(P[0])
            
#Probability of rolling a double
Pdouble = 1/6
PNdouble = 5/6

#Now lets consider JAIL

#Possible landing spots out of jail(position 10 on real board)
JailSpots = [12,14,16,18,20,22]
for spot in JailSpots:
    P[30,spot] = 1/36
    P[40,spot] = 1/36 #after not rolling a double once
    P[41,spot] = 1/36
P[30,40] = 5/6
P[40,41] = 5/6
P[41,10] = 5/6 #back to visiting

print(P[40])


#NOW lets look for the STATIONARY DISTN

print(np.linalg.eig(P)[0][0]) #END UP WITH 1 BEING AN EVAL XD

v1 = np.linalg.eig(P.T)[1][:,0]
print(v1)
print(sum(v1.real))


#FINAL normalised stationary distn.
v1r = v1.real
norm_const = sum(v1r)
print(v1r/norm_const)

FinalProbs = v1r/norm_const


    
import numpy as np
import matplotlib.pyplot as plt

#there are 40 squares on the board (plus 2 on side for jail wiaiting)
#first is GO, position 0
#on positions 2,17,33 we have community chest DECK1
DECK1_Pos = [2,17,13]
#on positoins 7,22,36 for chance DECK2
DECK2_Pos = [7,22,36]

#The deck consists of positions that you could move to and their
#respective probability, -1 would be not moving (at end of list).
#going back 3 steps is -3 XD
DECK1 = np.array([[0,1/16],[30,1/16],[-1,14/16]])#CHEST
DECK2 = np.array([[0,1/16],[11,1/16],[30,1/16],[15,1/16],[39,1/16],[24,1/16],[-3,1/16],[-1,9/16]])
#Ways to roll an their probs
DRolls = np.array([2,3,4,5,6,7,8,9,10,11,12])
DProbs = np.array([1,2,3,4,5,6,5,4,3,2,1])/36



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
        #now consider landing on chest/chance
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
                    if pair[0] != -1 and pair[0] != -3:
                        P[i,int(pair[0])] += pair[1]*P[i,pos]
                    elif pair[0] == -3: #go back 3 steps
                        P[i,pos-3] += pair[1]*P[i,pos]
                    elif pair[0] == -1:
                        P[i,pos] = pair[1]*P[i,pos]
                        

                
#print(P[0])
            
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
#print(P[40])


#NOW lets look for the STATIONARY DISTN

print(np.linalg.eig(P)[0][0]) #END UP WITH 1 BEING AN EVAL XD

v1 = np.linalg.eig(P.T)[1][:,0]
#print(v1)
#print(sum(v1.real))


#FINAL normalised stationary distn.
v1r = v1.real
norm_const = sum(v1r)
print(v1r/norm_const)

Probs = v1r/norm_const

#print(Probs[30]+Probs[40]+Probs[41])
#print(Probs[10])



#Now lets revert back to the actual board
#namely combining the jail states
ProbsFinal= Probs[:40]
ProbsFinal[30]+= Probs[40]+Probs[41]

#Lets rank our probabilities for the tiles
Names = ['Go','Old Kent Road','Chest 1','Whitechapel Road','Income Tax','Station 1',
         'The Angel Islington','Chance 1','Euston Road','Pentonville Road','Just Visiting',
         'Pall Mall','Utility 1','Whitehall','Northumberland Avenue','Station 2',
         'Bow Street','Chest 2','Marlborough Street','Vine Street','Free Parking',
         'Strand','Chance 2','Fleet Street','Trafalgar Square','Station 3','Leicester Squre',
         'Coventry Street','Utility 2','Picadilly','Jail','Regent Street','Oxford Street',
         'Chest 3','Bond Street','Station4','Chance 3','Park Lane','Super Tax','Mayfair']

Colours = ['lavender','tab:brown','lavender','tab:brown','lavender','k','c','lavender','c','c','lavender','m','lavender','m','m',
           'k','tab:orange','lavender','tab:orange','tab:orange','lavender','r','lavender','r','r','k','yellow',
           'yellow','lavender','yellow','lavender','g','g','lavender','g','k','lavender','b','lavender','b']

RankedPositions = np.argsort(ProbsFinal)

RankedProbs = np.zeros(40)
RankedNames = []
RankedColours = []
for i in range(40):
    RankedProbs[i] = ProbsFinal[RankedPositions[i]]
    RankedNames.append(Names[RankedPositions[i]])
    RankedColours.append(Colours[RankedPositions[i]])


#Now lets plot our ranked results
#UNORDERED
plt.bar(range(len(ProbsFinal)),ProbsFinal,color=Colours)
plt.xticks(range(len(ProbsFinal)),Names,rotation=90)
plt.show()

#ORDERED
plt.bar(range(len(ProbsFinal)),RankedProbs,color=RankedColours)
plt.xticks(range(len(ProbsFinal)),RankedNames,rotation=90)
plt.show()

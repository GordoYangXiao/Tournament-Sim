from logging import exception, raiseExceptions
import random

# To do:
# drawn out bracket (Art)
# animation for brackets (Art)
# Specified stats (doable, implementable without anything else) 
# betting points ? (EASY after Specified Stats)
# file of team (Last)
# data of real teams (Last Last)
# First to x vs Points 

def versus(t1, t2, rounds, overtime, min, max):
    print(t1, "vs", t2)
    while True:
        final1 = final2 = 0
        for i in rounds:
            t1score = t2score = 0
            while t1score == t2score:
                t1score += random.randint(min, max)
                t2score += random.randint(min,max)
                if t1score > t2score:
                    final1 += 1
                    print(i + ":", str(t1score) + ":" + str(t2score))
                    break
                elif t1score < t2score:
                    final2 += 1
                    print(i + ":", str(t1score) + ":" + str(t2score))
                    break
                if overtime:
                    print(i + ":", str(t1score) + ":" + str(t2score))
                    print("Overtime ", end = '')
                else:
                    t1score = t2score = 0
            if final2 > len(rounds) // 2 or final1 > len(rounds) // 2:
                        break
        print("Final:", str(final1) + ":" + str(final2))
        if final1 > final2:
            print(t1, "Wins \n")            
            return t1,t2
        elif final1 < final2:
            print(t2, "Wins \n" )
            return t2,t1
        else:
            print("Tie, Rematch")

def round(group, round, L, rounds, overtime, min, max):
    y = []
    winner = set()
    loser = set()
    if L:
        print("Loser", end = ' ') 
    print("Round", round)
    for x in group:
        y.append(x)
        if len(y) == 2:
            win, lose = versus(y[0], y[1], rounds, overtime, min, max)
            winner.add(win)
            loser.add(lose)
            y.clear()
    return winner, loser

def tournament(group, L = False, rounds = ["Score"], overtime = False, min = 0, max = 3):
    if len(group) % 4 != 0 and len(group) != 2:
        raise Exception("Please make a compatable set of teams")
    i = j = 1
    losers = set()
    while len(group) != 1:
        if L:
            win, lose = round(group, i, False, rounds, overtime, min, max)
            losers.update(lose)
            group = win
            l = round(losers, j, True, rounds, overtime, min, max)
            for x in l[1]:
                losers.remove(x)
            i += 1
            j += 1
            # If for Loser finals
            if len(losers) == 2 and len(group) == 1:
                l = round(losers, j, True, rounds, overtime, min, max)
                for x in l[1]:
                    losers.remove(x)
            # If for finals
            if len(win) == 1 and len(losers) == 1:                     
                group.update(losers)
                round(group, 'Final', False, rounds, overtime, min, max)
                break
        else:
            group, lose = round(group, i, False, rounds, overtime, min, max)
            i += 1
            if len(group) == 2:
                round(group, 'Final', False, rounds, overtime, min, max)
                break

lst = {"1", "2", "3", "4", "5", "6", "7", "8"}
Loser = True
rounds = ["Map 1", "Map 2", "Map 3"]
types = "First to"
min = 0
max = 3
overtime = True

tournament(lst, Loser, rounds, overtime, min, max)

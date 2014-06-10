#!/usr/bin/env python

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2014
# Glenn P. Downing
# ---------------------------

# ------------
# collatz_read
# ------------

cache = [0]* 1000000
cache[1] = 1

def collatz_read (r, a) :
    """
    reads two ints into a[0] and a[1]
    r is a  reader
    a is an array of int
    return true if that succeeds, false otherwise
    """
    s = r.readline()
    if s == "" :
        return False
    l = s.split()
    a[0] = int(l[0])
    a[1] = int(l[1])
    assert a[0] > 0
    assert a[1] > 0
    return True

# ------------
# collatz_eval
# ------------

def collatz_eval (i, j) :
    """
    i is the beginning of the range, inclusive
    j is the end of the range, inclusive
    return the max cycle length in the range [i, j]
    """
    assert i > 0
    assert j > 0
    maxCycle = 1

    if(i > j):
        i,j = j,i
        
    if (j >> 1 ) > i:
        i = j >> 1

    for n in range(i,j+1):
        if(cache[n] > 0):
            currentCycle = cache[n]
        else:
            currentCycle = collatz_cycle(n)
            cache[n] = currentCycle
        if(currentCycle > maxCycle):
            maxCycle = currentCycle
    
    assert maxCycle > 0
    return maxCycle
    
# -------------
# collatz_cycle
# -------------
def collatz_cycle(n):
    """
    n is the number which we want to find the cycle length
    return the cycle length of n
    """
    assert n > 0
    
    cycle = 1
    while n != 1:
        if (n % 2 == 0):
            n = n >> 1
        else:
            n = n + (n >> 1) + 1
            cycle = cycle + 1
        cycle = cycle + 1
    
    assert cycle > 0

    return cycle

# -------------
# collatz_print
# -------------

def collatz_print (w, i, j, v) :
    """
    prints the values of i, j, and v
    w is a writer
    i is the beginning of the range, inclusive
    j is the end       of the range, inclusive
    v is the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# collatz_solve
# -------------

def collatz_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    a = [0, 0]
    while collatz_read(r, a) :
        v = collatz_eval(a[0], a[1])
        collatz_print(w, a[0], a[1], v)

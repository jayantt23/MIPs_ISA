### Only modify my_nsl and my_ol functions
### Only use bitwise and, or and not operations
### Bitwise not operation of x is (~x)&0xb1
### Bitwise or operaiton is |
### Bitwise and operation is &

def n(a):
    return (~a&0b1)

def a_lt_b(a, b): # returns if a_lt_b
    a0, a1, a2 = a & 0b1, (a >> 1) & 0b1, (a >> 2) & 0b1
    b0, b1, b2 = b & 0b1, (b >> 1) & 0b1, (b >> 2) & 0b1
    x1, x2 = n(a1 ^ b1), n(a2 ^ b2)
    
    a_lt_b = (n(a2) & b2) | (x2 & n(a1) & b1) | (x2 & x1 & n(a0) & b0)
    if (a_lt_b == 0b1):
        return True
    else:
        return False

def a_eq_b(a, b): #returns if a_eq_b
    a0, a1, a2 = a & 0b1, (a >> 1) & 0b1, (a >> 2) & 0b1
    b0, b1, b2 = b & 0b1, (b >> 1) & 0b1, (b >> 2) & 0b1
    x0, x1, x2 = n(a0 ^ b0), n(a1 ^ b1), n(a2 ^ b2)
    
    a_eq_b = x2 & x1& x0
    
    if (a_eq_b == 0b1):
        return True
    else:
        return False

def my_nsl(ps,sr):
    
    q0, q1, q2 = ps & 0b1, (ps >> 1) & 0b1, (ps >> 2) & 0b1
            
    d0 = n(sr) & n(q0)
    d1 = n(sr) & (q1 ^ q0)
    d2 = n(sr) & ((q2 & n(q1)) | (n(q2) & q1 & q0) | (q2 & q1 & n(q0)))
    
    ns = (d2 << 2) | (d1 << 1) | d0
    return (ns)

def my_ol(ps, period, compare, sr, ar):
    
    sr = 0b0
    if (ar==0b1):
        outputs = 0b0
        sr = 0b0
        return outputs, sr
    
    if a_eq_b(period, ps):
        sr = 0b1
    
    if a_lt_b(ps, compare):
        outputs = 0b1
    else:
        outputs = 0b0
    
    return (outputs, sr)
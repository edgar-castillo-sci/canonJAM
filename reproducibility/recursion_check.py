def closed_PL(n):
    if n % 2 == 0:
        return (3**(n//2) + 1) * (3**(n//2) + 3) // 12
    m = (n-1)//2
    return (3**m + 1)**2 // 4

def closed_BPLBU(n):
    if n % 2 == 0:
        return (6**n + 4*6**(n//2)) // 12
    return (6**n + 6**((n+1)//2)) // 12

def closed_BBU(n):
    if n % 2 == 0:
        return (12**n + 4*12**(n//2)) // 12
    return 12**(n-1)

def rec_PL(N):
    if N == 2: return 2
    # n empieza en 0 para N par, en 1 para N impar (Tabla S1 de [1])
    n = (N-1)//2 if N % 2 == 1 else (N-2)//2
    return 3*rec_PL(N-1) - (3**n + 1)//2

def rec_BPLBU(N):
    if N == 2: return 5
    n = (N-2)//2
    m = 1 if N % 2 == 1 else 0
    return 6*rec_BPLBU(N-1) - 6**n * 3**(2*m)

def rec_BBU(N):
    if N == 2: return 16
    n = (N-1)//2 if N % 2 == 1 else N//2 - 1
    m = 1 if N % 2 == 1 else -1
    return 12*rec_BBU(N-1) - 4*m*(12**n)

ok = True
for N in range(2, 31):
    for name, rec, clo in [("PL", rec_PL, closed_PL),
                            ("BPL/BU", rec_BPLBU, closed_BPLBU),
                            ("BBU", rec_BBU, closed_BBU)]:
        r, c = rec(N), clo(N)
        if r != c:
            print(f"MISMATCH {name} N={N}: rec={r} closed={c}")
            ok = False
if ok:
    print("All match for N=2..30 (PL, BPL/BU, BBU)")

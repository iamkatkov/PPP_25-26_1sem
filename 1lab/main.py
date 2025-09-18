def f(seats, K):
    N = len(seats)
    if N == 0:
        return (-1, -1)
    M = len(seats[0])
    
    for i in range(N):
        k = 0
        for j in range(M):  
            if seats[i][j] == 0:  
                k += 1
                if k == K:  
                    start = j - K + 1  
                    for pos in range(start, j + 1):  
                        seats[i][pos] = 1
                    return (i, start)
            else:
                k = 0  
    return (-1, -1) 

seats = [[1, 0, 1, 0, 1],[1, 0, 0, 1, 0],[0, 0, 0, 0, 0]]
K = 2

print(f(seats, K))

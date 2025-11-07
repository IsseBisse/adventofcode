t = [[2, 0, -2, 0, 3],[0, 5, -3, 0, 3],[0, 0, 5, -1, 8],[0, -1, 0, 5, 8]]

score = 0 
max_score = 0
combination = None
for i in range(0,100):
    for j in range(0,100-i):
        for k in range(0,100-i-j):
            h = 100-i-j-k
            a = t[0][0]*i+t[1][0]*j+t[2][0]*k+t[3][0]*h
            b = t[0][1]*i+t[1][1]*j+t[2][1]*k+t[3][1]*h
            c = t[0][2]*i+t[1][2]*j+t[2][2]*k+t[3][2]*h
            d = t[0][3]*i+t[1][3]*j+t[2][3]*k+t[3][3]*h
            e = t[0][4]*i+t[1][4]*j+t[2][4]*k+t[3][4]*h
           
            #extra condition for part b
            if(not(e == 500)):
                continue
            if (a <= 0 or b <= 0 or c <= 0 or d <= 0):
                score = 0
                continue
            score = a*b*c*d
            if (score > max_score):
                max_score = score
                combination = (i, j, k, h)

print(max_score)
print(combination)
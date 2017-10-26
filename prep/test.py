def testIf(x):
    if(x==0):
        return 5
    print("after if")
    return 10

print(testIf(0))

score=0
for i in range(0,10):
    score=score+i

print(score)
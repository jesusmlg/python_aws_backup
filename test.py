# 0 1 1 2 3 5 8 13 21 34


def fib(n):
    total = 0
    ant = 1
    for i in range(n):        

        total = total + ant
        ant = total
        
        print("- "+str(i) + " Total: "+ str(total) + " Ant:"+ str(ant))
    print("Res: " + str(total))

fib(3)

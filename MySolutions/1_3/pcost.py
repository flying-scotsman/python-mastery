with open('Data/portfolio.dat', 'r') as f:
    total_cost = 0
    for l in f:
        items = l.split(' ')
        total_cost += int(items[1]) * float(items[2])
    print(total_cost)
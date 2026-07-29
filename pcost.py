def portfolio_cost(filename) -> float:
    with open(filename, 'r') as f:
        total_cost = 0
        for l in f:
            items = l.split(' ')
            try:
                number_of_stocks = int(items[1])
                stock_price = float(items[2])
                total_cost += number_of_stocks * stock_price
            except ValueError as e:
                print(f"Couldn't parse {l.strip()}")
                print(f"Reason: {e}\n")
                continue
        return total_cost

if __name__ == '__main__':
    print(portfolio_cost('Data/portfolio3.dat'))
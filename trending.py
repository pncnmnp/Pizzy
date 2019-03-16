import pandas as pd
import operator

#convert the data from my SQL to csv file
def read_csv_file(filename):        #file in csv format
    df = pd.read_csv(filename)
    length = len(df)
    pizzas,sides,beverages = {},{},{}
    print(length)
    for i in range(length):
        pizzas[df['pizzas'][i]] = df['pizza_count'][i]
        sides[df['sides'][i]] = df['side_count'][i]
        beverages[df['beverages'][i]] = df['beverage_count'][i]
    
    pizzas = sorted(pizzas.items(), key=operator.itemgetter(1),reverse=True)
    sides = sorted(sides.items(), key=operator.itemgetter(1),reverse=True)
    beverages = sorted(beverages.items(), key=operator.itemgetter(1),reverse=True)

    sort_pizza = [i[0] for i in pizzas]
    sort_sides = [i[0] for i in sides]
    sort_beverages = [i[0] for i in beverages]

    
    
    return(sort_pizza,sort_sides,sort_beverages)

read_csv_file("menu.csv")
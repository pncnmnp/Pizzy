import ispositive
def modify(orders:list,toRemove:str):
    orders=orders.copy()
    orders.remove(toRemove)
    print("Would you like to try out these?")
    for i,o in enumerate(orders):
        print("%d) %s"%(i+1,o))
    user_input = input(">>").lower()
    if ispositive.is_positive(user_input):
        # Modify order listing
        print("Modify order")
        pass
    else:
        # User wants to delete
        # Greet
        print("Okay deleting")
        pass

def change(orders:list):
    ordinals=['first','second','third','fourth','fifth']
    print("What do you want to change?")
    for i,o in enumerate(orders):
        print("%d) %s"%(i+1,o))
    print("You can say the first one or item name")
    user_input = input(">>").lower()
    try:
        i=int(user_input)
        modify(orders,orders[i-1])
    except ValueError:
        for index,ordinal in enumerate( ordinals ):
            if ordinal in user_input:
                modify(orders,orders[index])
        for i,o in enumerate(orders):
            if user_input == o.lower():
                modify(orders,o) 
                break

change(['Pizza A','Beverage B','Item 3'])
# ========== Imports ==========
from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:
    '''
    Class Shoe consists of 1 initialization and 3 methods.

    Attributes for Shoe:
    1. Country (Type: String)
    2. Code (Type: String)
    3. (Name of) Product (Type: String)
    4. Cost (Type: int)
    5. Quantity (Type: int)

    Methods:
    1. get_cost() returns item cost
    2. get_quantity() returns item quantity
    3. __str__ returns all object attributes in a user friendly format
    '''

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        print(f"\nItem cost: {self.cost}")

    def get_quantity(self):
        print(f"Item quantity: {self.quantity}")

    def __str__(self):
        print(f'''\n============ {self.code} ============
Country:        {self.country}
Code:           {self.code}
Name:           {self.product}
Cost:           {self.cost}
Quantity:       {self.quantity}''')


# =============== Shoe List ===============
shoe_sku_list = []
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    try:
        with open('stock_info.txt', 'r', encoding='utf-8') as f:
            f.readline()  # Skip over first line

            for line in f:

                info_format = line.strip().split(',', 4)

                shoe_sku_list.append(info_format[1])

                # Create new shoe object with shoe name as object name
                info_format[1] = Shoe(info_format[0], info_format[1],
                                      info_format[2], info_format[3],
                                      info_format[4])

                # Save object name to list
                shoe_list.append(info_format[1])

    except FileNotFoundError:
        print("File not found.")


def capture_shoes():
    print("============ Capture New Shoe ============")

    try:

        # Get user inputs
        country = input("Enter Country: ")
        code = input("Enter ID code: ")
        product = input("Enter product name: ")
        cost = int(input("Enter cost: R"))
        quantity = int(input("Enter quantity: "))

        # Write to file
        with open('stock_info.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{country},{code},{product},{cost},{quantity}")

        # Create object and append list
        read_shoes_data()

    except ValueError:
        print("\nPlease enter a valid number.")


def view_all():
    print("\n========== Stock ==========\n")

    read_shoes_data()

    # Website used to understand tabulate:
    # https://www.datacamp.com/tutorial/python-tabulate

    try:
        data_lists = []  # Initialize list for all data lists

        with open('stock_info.txt', 'r', encoding='utf-8') as f:
            f.readline()  # Skip over first line

            for line in f:

                # Create a list of all items in a line
                info_format = line.strip().split(',')

                # Add list to big list of items
                data_lists.append(info_format)

        # Tabulate and print data
        table = tabulate(data_lists,
                         headers=["Country", "Code", "Product Name", "Cost",
                                  "Quantity"],
                         tablefmt='grid')

        print(table)

    except FileNotFoundError:
        print("File not found.")


def re_stock():
    print("\n========== Re-stock Page ==========")

    read_shoes_data()

    # Find lowest quantity
    reference = int(shoe_list[0].quantity)
    min_shoe = shoe_list[0]

    # Find min quantity
    for i in shoe_list:
        if int(i.quantity) < reference:
            reference = int(i.quantity)
            min_shoe = i
        else:
            continue

    # Print out result
    print(f"\n{min_shoe.code}: {min_shoe.product} has {min_shoe.quantity} "
          "units")

    # Get new quantity
    new_quantity = int(input("\nHow many would units would you like to add: "))

    # Add stock amount
    new_total = new_quantity + int(min_shoe.quantity)

    # Shoe index + 1 since first line of .txt isn't in shoe_list
    shoe_index = (shoe_list.index(min_shoe) + 1)

    with open('stock_info.txt', 'r', encoding='utf-8') as f:

        # Initialize writing lists
        country = []
        code = []
        product = []
        cost = []
        quantity = []

        # Build lists from file
        for lines in f:
            info_format = lines.strip().split(',')
            country.append(info_format[0])
            code.append(info_format[1])
            product.append(info_format[2])
            cost.append(info_format[3])
            quantity.append(info_format[4])

        # Test print

        # Append quantity list
        quantity.pop(shoe_index)
        quantity.insert(shoe_index, new_total)

    with open('stock_info.txt', 'w', encoding='utf-8') as f:

        # Re-write first line of file
        f.write(f"{country[0]},{code[0]},{product[0]},{cost[0]},{quantity[0]}")

        # Re-write rest of file
        for i in range(len(code)):
            if i == 0:
                next
            else:
                f.write(f"\n{country[i]},{code[i]},{product[i]},{cost[i]},"
                        f"{quantity[i]}")

    # Print out new table
    print("\n========== Updated stock ==========")
    view_all()


def search_shoe():

    print("\n========== Shoe Search ==========\n")
    shoe_search = input("\nEnter shoe code: ")

    # Search for shoe SKU
    if shoe_search in shoe_sku_list:

        # Get index for referencing
        object_index = int(shoe_sku_list.index(shoe_search))

        return shoe_list[object_index].__str__()

    else:
        print("Not found")


def value_per_item():

    read_shoes_data()

    data_list = []  # Initialise capture list

    # Compile item lists from shoe_list

    for i in shoe_list:
        item_data = [i.code, (int(i.cost)*int(i.quantity))]
        data_list.append(item_data)

    # Tabulate results
    value_table = tabulate(data_list,
                           headers=['Item Code', 'Total Value'],
                           tablefmt='grid')

    print("\n========== Stock Value ==========\n")
    print(value_table)

    # Clean up list
    data_list.clear()


def highest_qty():

    read_shoes_data()

    # Initialize references
    reference = int(shoe_list[0].quantity)
    max_shoe = shoe_list[0]

    # Find Max quantity
    for i in shoe_list:
        if int(i.quantity) > reference:
            reference = int(i.quantity)
            max_shoe = i
        else:
            continue

    print("\n========== Highest stock item ==========\n")
    print(f"{max_shoe.product} is currently on sale")


# ==========Main Menu=============
running = True

while running:
    try:
        menu = int(input('''\n========== Inventory Management ==========\n
[1] -   Capture new shoe data
[2] -   View all current stock
[3] -   Restock lowest item
[4] -   Search for inventory
[5] -   Show current stock value
[6] -   Show item with highest stock
[7] -   Application admin contact information
[8] -   Exit
\nEnter an option: '''))

        if menu == 1:
            capture_shoes()

        elif menu == 2:
            view_all()

        elif menu == 3:
            re_stock()

        elif menu == 4:
            search_shoe()

        elif menu == 5:
            value_per_item()

        elif menu == 6:
            highest_qty()

        elif menu == 8:
            print("\nPlease contact us if you encounter any issues:"
                  "Email: support@inventory.com\nCall us: 022 234 1234")

        elif menu == 8:
            print("\nGoodbye!!!\n")
            break

        else:
            print("\nInvalid option")

    except ValueError:
        print("\nInvalid input")

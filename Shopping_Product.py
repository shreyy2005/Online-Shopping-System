import mysql.connector
from datetime import datetime

class ProductCategory:
    ELECTRONICS = "Electronics"
    GROCERIES = "Groceries"
    MEDICINES = "Medicines"
    CLOTHING = "Clothing"
    WATCHES = "Watches"

class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

electronics_products = [
    Product("Laptop", 80000, ProductCategory.ELECTRONICS),
    Product("TV", 100000, ProductCategory.ELECTRONICS),
    Product("Smartphone", 60000, ProductCategory.ELECTRONICS),
    Product("Headphones", 5000, ProductCategory.ELECTRONICS),
]

groceries_products = [
    Product("Apples", 100, ProductCategory.GROCERIES),
    Product("Milk", 75, ProductCategory.GROCERIES),
    Product("Bread", 30, ProductCategory.GROCERIES),
    Product("Eggs", 60, ProductCategory.GROCERIES),
]

medicines_products = [
    Product("Painkiller", 100, ProductCategory.MEDICINES),
    Product("Vitamin C", 150, ProductCategory.MEDICINES),
    Product("Antibiotics", 200, ProductCategory.MEDICINES),
    Product("Allergy Medicine", 120, ProductCategory.MEDICINES),
]

clothing_products = [
    Product("T-shirt", 2000, ProductCategory.CLOTHING),
    Product("Jeans", 2500, ProductCategory.CLOTHING),
    Product("Dress", 3500, ProductCategory.CLOTHING),
    Product("Sweater", 3000, ProductCategory.CLOTHING),
]

watches_products = [
    Product("Digital Watch", 5150, ProductCategory.WATCHES),
    Product("Analog Watch", 4130, ProductCategory.WATCHES),
    Product("Smartwatch", 8000, ProductCategory.WATCHES),
    Product("Fitness Tracker", 4000, ProductCategory.WATCHES),
]


category_products_map = {
    1: electronics_products,
    2: groceries_products,
    3: medicines_products,
    4: clothing_products,
    5: watches_products,
}

def get_category_name(category_num):
    categories = {1: ProductCategory.ELECTRONICS, 2: ProductCategory.GROCERIES,
                  3: ProductCategory.MEDICINES, 4: ProductCategory.CLOTHING,
                  5: ProductCategory.WATCHES}
    return categories.get(category_num)

def browse_categories():
    print("Available categories:")
    for i, category in ProductCategory.__dict__.items():
        if not i.startswith("__"):
            print(f"{i}: {category}")

def get_category_choice():
    while True:
        choice = input("Enter the category number to browse products or 'exit' to quit: ")
        if choice.lower() == "exit":
            return None
        try:
            choice = int(choice)
            if choice in category_products_map:
                return choice
            else:
                print("Invalid category number. Please try again or type 'back' to go back.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def browse_products(category):
    products = category_products_map.get(category)
    if products:
        category_name = get_category_name(category)
        print(f"Available {category_name} products:")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.name} - Rs. {product.price}")
    else:
        print("No products found for this category")

class User:
    def __init__(self, name):
        self.name = name
        self.phone_number = None  # Initialize phone number
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)

# Your database connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shreyas@2005',
    'database': 'Shopping_Database'
}

def save_to_billing_table(customer_name, phone_number, total_price, payment_method):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert into billing table
        cursor.execute("INSERT INTO billing (customer_name, phone_number, total_price, payment_method) VALUES (%s, %s, %s, %s)",
                       (customer_name, phone_number, total_price, payment_method))
        conn.commit()

    except mysql.connector.Error as err:
        print("Error while saving to billing table:", err)

    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def save_to_purchase_history_table(customer_name, phone_number, product_name, price, purchase_date):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert into purchase_history table
        cursor.execute("INSERT INTO purchase_history (customer_name, phone_number, product_name, price, purchase_date) VALUES (%s, %s, %s, %s, %s)",
                       (customer_name, phone_number, product_name, price, purchase_date))
        conn.commit()

    except mysql.connector.Error as err:
        print("Error while saving to purchase history table:", err)

    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def shop(user):
    while True:
        browse_categories()
        category_choice = get_category_choice()
        if category_choice is None:
            break
        products = category_products_map.get(category_choice)
        if not products:
            print("No products found for this category")
            continue
        browse_products(category_choice)

        cart = []
        while True:
            product_choice = input("Enter the product number to add to cart, 'checkout' to proceed to payment, or 'back' to choose a different category: ")
            if product_choice.lower() == "checkout":
                if not cart:
                    print("Your cart is empty.")
                    continue
                else:
                    print("Your cart:")
                    total_price = sum(product.price for product in cart)
                    for i, product in enumerate(cart, 1):
                        print(f"{i}. {product.name}: Rs. {product.price}")
                    print(f"Total Price: Rs. {total_price}")

                    # Ask for phone number before payment method
                    user.phone_number = input("Enter your phone number: ")
                    print("Select Payment Method (1: Credit Card, 2: PayPal, 3: Cash)")
                    payment_method = input("Enter payment method: ")
                    print("Payment processing...")

                    # Save to billing table
                    save_to_billing_table(user.name, user.phone_number, total_price, payment_method)

                    # Save each item in the cart to purchase history table
                    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for product in cart:
                        save_to_purchase_history_table(user.name, user.phone_number, product.name, product.price,
                                                       purchase_date)

                    print("Thank you for your purchase!")
                    user.cart = []
                    return  # Exit the function
            elif product_choice.lower() == "back":
                break  # Break out of the inner loop to go back to category selection
            try:
                product_choice = int(product_choice)
                selected_product = products[product_choice - 1]
                cart.append(selected_product)
                print(f"{selected_product.name} added to cart.")
            except (ValueError, IndexError):
                print("Invalid product choice")


def main():
    user_name = input("Enter your name: ")
    user = User(user_name)
    shop(user)

if __name__ == "__main__":
    main()

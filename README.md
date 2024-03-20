# Online-Shopping-System

## Description
The Online Shopping System is a Python-based application that simulates an online shopping platform. Users can browse through various product categories, add products to their cart, and proceed to checkout. The system supports multiple payment methods and maintains a record of purchase history.

## File Structure
```
Online-Shopping-System/
│
├── python_code/
│   ├── online_shopping.py
│   └── README.md
│
├── sql_code/
│   ├── shopping_database.sql
│   └── README.md
│
└── README.md
```

## Getting Started
### Prerequisites
- Python 3.x
- MySQL (or any compatible relational database)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/online-shopping-system.git
   ```
2. Navigate to the `python_code` folder:
   ```
   cd Online-Shopping-System/python_code
   ```
3. Run the Python script to start the online shopping system:
   ```
   python online_shopping.py
   ```
4. For database setup, navigate to the `sql_code` folder and execute the `shopping_database.sql` script in your MySQL database management tool.

## Usage
1. Upon running the Python script, you will be prompted to enter your name to start shopping.
2. Browse through available categories and select a category by entering the corresponding number.
3. Add products to your cart by entering the product number.
4. Proceed to checkout by entering 'checkout' and follow the prompts to complete the payment process.
5. Your purchase history will be recorded in the database.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

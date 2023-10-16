# test_data.py
import pytest
from models import User, Product, Tag, ProductTag, Transaction, db, initialize_database, close_db


# Fixture to initialize the database before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    close_db()
    initialize_database()
    yield
    close_db()


# Sample data definitions
users_data = [
    {
        'first_name': 'Lotte',
        'surname': 'Mulders',
        'gender': 'female',
        'address': 'Keizersgracht 12',
        'city': 'Amsterdam',
        'payment_info': '123456',
    },
    {
        'first_name': 'Violet',
        'surname': 'Peters',
        'gender': 'female',
        'address': 'Valkenboskade 10',
        'city': 'Den Haag',
        'payment_info': '654321',
    },
    {
        'first_name': 'Michael',
        'surname': 'Meijer',
        'gender': 'male',
        'address': 'Vierambachstraat 2',
        'city': 'Rotterdam',
        'payment_info': '987654',
    },
    {
        'first_name': 'Marinus',
        'surname': 'Visser',
        'gender': 'male',
        'address': 'Piazza 21',
        'city': 'Eindhoven',
        'payment_info': '321654',
    },
    {
        'first_name': 'Sophie',
        'surname': 'Bakker',
        'gender': 'female',
        'address': 'Zomervaart 6',
        'city': 'Haarlem',
        'payment_info': '135246',
    },
    {
        'first_name': 'Mark',
        'surname': 'Halsema',
        'gender': 'male',
        'address': 'Hogedijk 37',
        'city': 'Aalsmeer',
        'payment_info': '864213',
    }
]

# Sample data for products
products_data = [
    {
        'name': 'Black Jeans',
        'description': 'Classic black jeans for everyday wear',
        'price': 29.99,
        'quantity': 30,
        'owner': 2,
        'tags': [1],  # ID 1 is associated with 'clothes', see tags_data
    },
    {
        'name': 'Wireless Headphones',
        'description': 'High-quality wireless headphones for an immersive audio experience',
        'price': 79.99,
        'quantity': 20,
        'owner': 3,
        'tags': [2],  # ID 2 is associated with 'electronics', see tags_data
    }
]

# Sample data for tags
tags_data = [
    {'name': 'clothes'},
    {'name': 'electronics'},
    {'name': 'accessories'},
    {'name': 'home decor'},
    {'name': 'toys'},
    {'name': 'books'},
    {'name': 'beauty'},
    {'name': 'sports'},
    {'name': 'food'},
    {'name': 'art'},
    {'name': 'music'},
    {'name': 'crafts'},
    {'name': 'stationery'},
    {'name': 'pets'},
]

# Sample data for product-tags relationships
product_tags_data = [
    {'product': 1, 'tags': [1]},  # Product ID 1 is associated with Tag ID 1
    # Product ID 2 is associated with Tag IDs 1 and 3
    {'product': 2, 'tags': [1, 3]},
]

# Sample data for transactions
transactions_data = [
    {'buyer': 2, 'seller': 1, 'product': 1, 'quantity': 3},
    {'buyer': 3, 'seller': 2, 'product': 2, 'quantity': 2},
    {'buyer': 1, 'seller': 3, 'product': 3, 'quantity': 1},
]
# i.e.  read as followed -> 'buyer'ID 2 buys 3 units of Product ID 1 from 'seller'ID 1.


# POPULATE TEST DATA FUNCTION
def populate_test_data():
    if not db.is_closed():
        db.close()
    db.drop_tables([User, Product, Tag, ProductTag, Transaction])
    initialize_database()

    with db.atomic():
        # Create users
        users = [User.create(**user_data) for user_data in users_data]

        # Create tags
        tags = [Tag.create(**tag_data) for tag_data in tags_data]

        # Create products and associate them with tags using the ProductTag junction table
        for product_data, product_tags in zip(products_data, product_tags_data):
            product_tags_list = product_tags['tags']
            product = Product.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                owner=users[product_data['owner'] - 1]
            )
            for tag_id in product_tags_list:
                tag = tags[tag_id - 1]
                ProductTag.create(product=product, tag=tag)

    # Close the database connection after data population
    close_db()


# Call the populate_test_data() function to populate the database
populate_test_data()

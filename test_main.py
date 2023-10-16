# test_main.py
import pytest
from models import ProductTag, Tag, Transaction, Product, db, initialize_database
from main import search, list_user_products, list_products_per_tag, purchase_product, update_stock, remove_product, close_db, add_product_to_catalog


# Fixture to initialize the database before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    if not db.is_closed():
        yield
    else:
        yield
        close_db()


# PYTEST FUNCTIONS
def test_search_existing_term():
    term = "T-shirt"
    results = search(term)
    assert isinstance(results, list)
    for item in results:
        assert term.lower() in item.lower()


def test_search_nonexistent_term():
    term = "nonexistent"
    results = search(term)
    assert results == []


def test_user_products_existing_user():
    user_id = 1
    results = list_user_products(user_id)
    assert isinstance(results, list)


def test_user_products_nonexistent_user():
    user_id = 999
    results = list_user_products(user_id)
    assert results == []


def test_products_per_tag_existing_tag():
    tag_id = 1
    results = list_products_per_tag(tag_id)
    assert isinstance(results, list)


def test_products_per_tag_nonexistent_tag():
    tag_id = 999
    results = list_products_per_tag(tag_id)
    assert results == []


def test_add_product():
    user_id = 1
    name = "Test Product"
    desc = "Test description"
    price = 10.99
    qty = 100
    tag_ids = [1, 2]

    # Create Product and associate it with tags using ProductTag
    product = Product.create(name=name, description=desc,
                             price=price, quantity=qty, owner=user_id)
    for tag_id in tag_ids:
        tag = Tag.get(Tag.id == tag_id)
        ProductTag.create(product=product, tag=tag)

    # Assertions
    assert product.name == name
    assert product.description == desc
    assert product.price == price
    assert product.quantity == qty
    assert product.owner.id == user_id

    # Check associations via ProductTag
    associated_tags = ProductTag.select().where(ProductTag.product == product)
    tag_ids_in_product_tag = [tag.tag.id for tag in associated_tags]
    assert set(tag_ids) == set(tag_ids_in_product_tag)


def test_update_stock():
    prod_id = 1
    qty = 50
    update_stock(prod_id, qty)
    product = Product.get(Product.id == prod_id)
    assert product.quantity == qty


def test_purchase_product():
    prod_id = 1
    buyer_id = 2
    qty = 5
    purchase_product(prod_id, buyer_id, qty)
    product = Product.get(Product.id == prod_id)
    assert product.quantity == 45
    transaction = Transaction.get(Transaction.product == prod_id)
    assert transaction.buyer.id == buyer_id
    assert transaction.seller.id == product.owner.id
    assert transaction.product.id == prod_id
    assert transaction.quantity == qty
    # Ensure product is associated with the buyer
    assert transaction.buyer.id == buyer_id


def test_remove_product():
    prod_id = 1
    remove_product(prod_id)
    with pytest.raises(Product.DoesNotExist):
        Product.get(Product.id == prod_id)


# Call close_db() after all the tests have been executed
close_db()

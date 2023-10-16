# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

# IMPORTS
from models import User, Tag, Product, Transaction, ProductTag, db, initialize_database, close_db
from peewee import fn


# INITIALIZE DATABASE FUNCTION
initialize_database()


# SEARCH FUNCTION
def search(term):
    term = term.lower()
    products = Product.select().where(
        (fn.lower(Product.name).contains(term)) | (
            fn.lower(Product.description).contains(term))
    )
    return [product.name for product in products]


# LIST USER PRODUCTS FUNCTION
def list_user_products(user_id):
    user_products = Product.select().where(Product.owner == user_id)
    return [product.name for product in user_products]


# LIST PRODUCTS PER TAG FUNCTION
def list_products_per_tag(tag_id):
    try:
        tag = Tag.get(Tag.id == tag_id)
        products = Product.select().join(ProductTag).where(ProductTag.tag == tag)
        return [f'Product: {product.name}, Quantity: {product.quantity}' for product in products]
    except Tag.DoesNotExist:
        return []


# ADD PRODUCT TO CATALOG FUNCTION
def add_product_to_catalog(user_id, product_name, product_description, price_pu, new_quantity, tag_ids):
    try:
        user = User.get(User.id == user_id)
        with User._meta.database.atomic():
            # Check if tags with the given tag_ids already exist in the database
            tags = [Tag.get_or_create(id=tag_id)[0] for tag_id in tag_ids]

            # Check if a product with the same name and owner already exists
            existing_product = Product.get_or_none(
                name=product_name, owner=user)
            if existing_product:
                existing_product.quantity += new_quantity
                existing_product.save()
            else:
                # Create a new product if it doesn't exist
                product = Product.create(name=product_name, description=product_description,
                                         price_pu=price_pu, quantity=new_quantity, owner=user)
                for tag in tags:
                    ProductTag.create(product=product, tag=tag)
    except User.DoesNotExist:
        raise Exception("Error: User not found.")
    except Tag.DoesNotExist:
        raise Exception("Error: Tag not found.")


# UPDATE STOCK FUNCTION
def update_stock(product_id, new_quantity):
    try:
        with Product._meta.database.atomic():
            Product.update(quantity=new_quantity).where(
                Product.id == product_id).execute()
    except Product.DoesNotExist:
        print("Error: Product not found.")


# PURCHASE PRODUCT FUNCTION
def purchase_product(product_id, buyer_id, quantity):
    try:
        product = Product.get(Product.id == product_id)
        seller_id = product.owner
        # Get associated tags using ProductTag model
        product_tags = ProductTag.select().where(ProductTag.product == product)
        tag_ids = [product_tag.tag.id for product_tag in product_tags]
        add_product_to_catalog(
            buyer_id, product.name, product.description, product.price, quantity, tag_ids)
        new_quantity = product.quantity - quantity
        update_stock(product_id, new_quantity)
        Transaction.create(buyer=buyer_id, seller=seller_id,
                           product=product_id, quantity=quantity)
    except Product.DoesNotExist:
        print("Error: Product not found.")


# REMOVE PRODUCT FUNCTION
def remove_product(product_id):
    try:
        with Product._meta.database.atomic():
            product = Product.get(Product.id == product_id)
            product.delete_instance()
    except Product.DoesNotExist:
        print("Error: Product not found.")


close_db()


# MAIN FUNCTION
def main():
    pass


if __name__ == '__main__':
    initialize_database()
    main()

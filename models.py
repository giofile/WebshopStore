# models.py
import peewee as pw

# Database initialization
db = pw.SqliteDatabase('betsy.db')


# INITIALIZE DATABASE FUNCTION
def initialize_database():
    if db.is_closed():
        db.connect()
    db.create_tables([User, Tag, Product, ProductTag, Transaction], safe=True)


# Function to close the database connection
def close_db():
    if not db.is_closed():
        db.close()


class BaseModel(pw.Model):
    class Meta:
        database = db


# User model
class User(BaseModel):
    first_name = pw.CharField(max_length=255)
    surname = pw.CharField(max_length=255)
    gender = pw.CharField(max_length=10)
    address = pw.CharField(max_length=255)
    city = pw.CharField(max_length=100)
    payment_info = pw.CharField(max_length=6)


# Tag model
class Tag(BaseModel):
    name = pw.CharField(unique=True)


# Product model
class Product(BaseModel):
    name = pw.CharField()
    description = pw.TextField()
    price = pw.DecimalField()
    quantity = pw.IntegerField()
    owner = pw.ForeignKeyField(User, backref='products')
    tags_id = pw.ForeignKeyField(Tag, backref='products', null=True)
    tag_id = pw.ForeignKeyField(Tag, backref='products', null=True)


# Product-Tag relationship model
class ProductTag(BaseModel):
    product = pw.ForeignKeyField(Product, backref='product_tags')
    tag = pw.ForeignKeyField(Tag, backref='product_tags')


# Transaction model
class Transaction(BaseModel):
    buyer = pw.ForeignKeyField(User, backref='purchases')
    seller = pw.ForeignKeyField(User, backref='sales')
    product = pw.ForeignKeyField(Product, backref='transactions')
    quantity = pw.IntegerField()


# Create tables if they don't exist
db.connect()
db.create_tables([User, Tag, Product, ProductTag, Transaction])

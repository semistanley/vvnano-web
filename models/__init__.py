from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


from .product import Product, ProductCategory
from .article import Article
from .inquiry import Inquiry

__all__ = ['db', 'utcnow', 'Product', 'ProductCategory', 'Article', 'Inquiry']

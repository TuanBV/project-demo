from models.model import Product, ProductKind, ProductImage, Image, Sale, Kind, Category
from core import CommonRepository
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
from utils.kbn import FlgDelete

class ProductRepository(CommonRepository):
    """
    Repository of product
    """

    def _filtered_query(self, session, category_id=None, kind_id=None, name=None):
        """
            # Build the Product query shared by get_all() and count(), filtered by
            # category/kind (joined through ProductKind, the real FK path) and name.
        """
        query = session.query(Product)
        if category_id or kind_id:
            query = query.join(ProductKind, ProductKind.id == Product.product_kind_id)
        if category_id:
            query = query.filter(ProductKind.category_id == int(category_id))
        if kind_id:
            query = query.filter(ProductKind.kind_id == int(kind_id))
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        return query

    def count_products(self, category_id=None, kind_id=None, name=None):
        """
            # Count product matching the given filters
            # Note: named distinctly from count() below, which counts Image rows
            # for upload validation — same class, unrelated purpose.
            # Output:
            #   return: int
        """
        with self.session_factory_read() as session:
            return self._filtered_query(session, category_id, kind_id, name).count()

    def get_all(self, page=1, page_size=12, category_id=None, kind_id=None, name=None):
        """
            # Get a page of product, optionally filtered by category/kind/name
            # Params:
            #   @page, @page_size: pagination
            #   @category_id, @kind_id, @name: optional filters
            # Output:
            #   return: List of product
        """
        with self.session_factory_read() as session:
            results = self._filtered_query(
                    session, category_id, kind_id, name
                ).options(
                    joinedload(Product.product_image).joinedload(ProductImage.images),
                    joinedload(Product.product_kinds).joinedload(ProductKind.kinds),
                    joinedload(Product.product_kinds).joinedload(ProductKind.categories)
                ).order_by(
                    asc(Product.flg_del), desc(Product.created_date)
                ).offset(
                    (page - 1) * page_size
                ).limit(
                    page_size
                ).all()
            return [
                {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'price': item.price,
                    'height': item.height,
                    'weight': item.weight,
                    'sale_id': item.sale_id,
                    'name': item.name,
                    'product_kind_id': item.product_kind_id,
                    'info': item.info,
                    'images': [
                        jsonable_encoder(item_image.images)
                        for item_image in item.product_image
                        if item.product_image
                    ],
                    'kind_name': item.product_kinds.kinds.name if item.product_kinds.kinds else None,
                    'category_name': item.product_kinds.categories.name if item.product_kinds.categories else None
                } for item in results
            ]

    # Get user by user_id
    def get_by_product_id(self, product_id):
        """
            # Get product by product_id
            # Params:
            #   @product_id: Product id
            # Output:
            #   return: Data product
        """
        with self.session_factory_read() as session:
            return session.query(Product).filter(Product.id == product_id).first()

    # Count record
    def count(self, list_img_id):
        """
            # Count record
            # Params:
            #   @list_img_id: list id of image
            # Output: record number
        """
        with self.session_factory_read() as session:
            return session.query(Image).filter(
                Image.id.in_(list_img_id),
                Image.flg_del == FlgDelete.OFF.value
            ).count()

    # Add record
    def add_product_img(self, list_img_id, product_id, created_user, session):
        """
            # Add record
            # Params:
            #   @list_img_id: list id of image
            #   @created_user: name of the created user
            # Output: None
        """
        lst_record = list()
        for img_id in list_img_id:
            lst_record.append(ProductImage(
                image_id=img_id,
                product_id=product_id,
                created_user=created_user
            ))
        session.add_all(lst_record)

    # Add product
    def add(self, data_request, created_user):
        """
            # Add product
            # Params:
            #   @data: name
            # Output:
            #   return: data product
        """
        with self.session_factory() as session:
            # Add product
            new_product = Product(
                name=data_request["name"],
                quantity=int(data_request["quantity"]),
                price=float(data_request["price"]),
                info=data_request["info"],
                weight=float(data_request["weight"]) if data_request["weight"] else 0,
                height=float(data_request["height"]) if data_request["height"] else 0,
                product_kind_id=int(data_request["product_kind_id"]),
                sale_id=int(data_request["sale_id"]) if data_request["sale_id"] else None,
                created_user=created_user
            )
            session.add(new_product)
            session.flush()
            # Add image to ProductImage table
            self.add_product_img(data_request["images"],
                new_product.product_id, created_user, session
            )
            # Commit to database
            session.commit()

    # Get the product by name
    def get_by_name(self, name):
        """
            # Get the product by name
            # Params:
            #   @name: name of product
            # Output:
            #   return: Boolean
        """
        with self.session_factory_read() as session:
            return session.query(Product).filter(
                Product.name == name,
                Product.flg_del == FlgDelete.OFF.value
            ).first()

    # Get product kind by category_id and kind_id
    def get_product_kind(self, category_id, kind_id):
        """
            # Get product kind by category_id and kind_id
            # Params:
            #   @category_id: category_id
            #   @kind_id: kind_id
            # Output:
            #   return: object|null
        """
        with self.session_factory_read() as session:
            return session.query(ProductKind).filter(
                ProductKind.category_id == int(category_id),
                ProductKind.kind_id == int(kind_id),
                
            ).first()

    # Add product kind by category_id and kind_id
    def add_product_kind(self, category_id, kind_id, created_user):
        """
            # Get product kind by category_id and kind_id
            # Params:
            #   @category_id: category_id
            #   @kind_id: kind_id
            # Output:
            #   return: object|null
        """
        with self.session_factory() as session:
            product_kind = ProductKind(
                category_id = int(category_id),
                kind_id = int(kind_id),
                created_user = created_user
            )
            session.add(product_kind)
            session.commit()
            session.refresh(product_kind)
            return product_kind.id

    # Update product
    def update(self, product_id, name, updated_user):
        """
            # Update product
            # Params:
            #   @product_id: id of the product
            #   @name: name of product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id,
                Product.flg_del == FlgDelete.OFF.value
            ).update({
                "name": name,
                "updated_user": updated_user
            })
            session.commit()

    # Delete product
    def delete(self, product_id, updated_user):
        """
            # Delete product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id,
                Product.flg_del == FlgDelete.OFF.value
            ).update({
                "flg_del": FlgDelete.ON.value,
                "updated_user": updated_user
            })
            session.commit()

    # Active product
    def active(self, product_id, updated_user):
        """
            # Active product
            # Params:
            #   @product_id: id of the product
            #   @updated_user: name of user update
            # Output:
            #   return:
        """
        with self.session_factory() as session:
            session.query(Product).filter(
                Product.id == product_id
            ).update({
                "flg_del": FlgDelete.OFF.value,
                "updated_user": updated_user
            })
            session.commit()

class dims:
    @staticmethod
    def customer(customer_id=1, name='Bob', country=None):
        return locals()

    @staticmethod
    def product(product_id=1, product_name='cauldron', category='Magic'):
        return locals()


class facts:
    @staticmethod
    def transactions(product_id=1, customer_id=1, purchase_date='2022-09-01'):
        return locals()

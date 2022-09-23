
def values(context):
    context = dict(context)
    context.pop('self', None)
    return context


class fixture:
    @classmethod
    def tables(cls):
        return [f for f in dir(cls) if callable(getattr(cls, f)) and not f.startswith("__") and f != 'tables']


class dims(fixture):
    def customer(self, customer_id=1, name='Bob', country=None):
        return values(locals())

    def products(self, product_id=1, product_name='cauldron', category='Magic'):
        return values(locals())


class facts(fixture):
    def transactions(self, product_id=1, customer_id=1, purchase_date='2022-09-01'):
        return values(locals())

    def another_table(self, f1=1, f2=2):
        return values(locals())
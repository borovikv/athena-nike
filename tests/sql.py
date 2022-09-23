import re

import pandas as pd
from sqlalchemy import create_engine


class TrinoBaseExecutor:
    def __init__(self, port=8880):
        engine = create_engine(f'trino://user@localhost:{port}/memory')
        self.connection = engine.connect()

    def execute(self, sql, output_format='dict'):
        response = self.connection.execute(sql)
        results = response.fetchall()
        if output_format == 'dict':
            return [r._asdict() for r in results]
        else:
            return results

    def __call__(self, sql, order_by=None, cte=None):
        sql = self.prepare_sql(sql)
        if cte:
            sql = re.sub(r'select \* from result', f'select * from {cte}', sql, flags=re.I)
        if order_by:
            if isinstance(order_by, list):
                order_by = ', '.join(order_by)
            sql = sql.strip().strip(';') + f'\norder by {order_by}'
        return self.execute(sql)

    @staticmethod
    def prepare_sql(sql):
        return sql.strip()


class SpecExecutor(TrinoBaseExecutor):
    def __init__(self, spec, port=8880):
        super().__init__(port=port)
        self.clean_database(spec)
        self.prepare_tables(spec)

    def clean_database(self, spec):
        schemas = [table.__qualname__.split('.')[0] for table in spec.get('tables', [])]
        existing_schemas = self.execute(f"show schemas", output_format='list')
        for schema, in existing_schemas:
            if schema not in schemas:
                continue
            tables = self.execute(f"show tables from {schema}", output_format='list')
            for table, in tables:
                sql = f"drop table {schema}.{table}"
                self.execute(sql, output_format='list')
            self.execute(f"drop schema {schema}", output_format='list')

        for schema in schemas:
            self.execute(f"create schema if not exists {schema}")

    def prepare_tables(self, spec):
        for table in spec['tables']:
            table_name = table.__qualname__
            table_rows_spec = spec['given'].get(table_name, [])
            table_rows = [table(**row) for row in table_rows_spec]
            if not table_rows:
                table_rows.append(table())
            self.create_table(table_name, table_rows)

    def create_table(self, name, rows, drop=False):
        schema, table_name = name.split('.')
        pd.DataFrame(rows).to_sql(
            name=table_name,
            schema=schema,
            con=self.connection,
            index=False,
            if_exists='replace' if drop else 'append'
        )

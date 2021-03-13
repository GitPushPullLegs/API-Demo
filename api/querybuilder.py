class QueryBuilder:
    _QUERY = {
        'SELECT': [],
        'FROM': [],
        'WHERE': [],
        'GROUP BY': [],
        'ORDER BY': [],
        'LIMIT': -1
    }

    args = []

    ## SELECT
    def distinct(self):
        if "DISTINCT" not in self._QUERY['SELECT']:
            self._QUERY['SELECT'].insert(0, "DISTINCT")

    def select(self, column):
        [self._QUERY['SELECT'].append(col) for col in column] if isinstance(column, list) else self._QUERY[
            'SELECT'].append(column)

    ## FROM
    def join(self, join_type: str, table: str, ON=None):
        if not ON and " ON " not in table.upper(): raise ValueError(
            'You have to merge on something, please add an ON statement or add the ON statement to the table value.')
        self._QUERY['FROM'].append(join_type + table + "" if not ON else (" ON " + ON))

    ### CONVENIENCE
    def inner_join(self, table: str, ON=None):
        self.join(join_type="INNER JOIN ", table=table, ON=ON)

    def left_join(self, table: str, ON=None):
        self.join(join_type="LEFT JOIN ", table=table, ON=ON)

    def right_join(self, table: str, ON=None):
        self.join(join_type="RIGHT JOIN ", table=table, ON=ON)

    def from_table(self, table: str):
        self._QUERY['FROM'].append(table)

    ## WHERE
    def where(self, where_clause):
        if len(self._QUERY['WHERE']) > 0:
            self._QUERY['WHERE'].append("AND " + where_clause)
        else:
            self._QUERY['WHERE'].append(where_clause)

    ## GROUP BY
    def add_group_by(self, column):
        [self._QUERY['GROUP BY'].append(col) for col in column] if isinstance(column, list) else self._QUERY[
            'GROUP BY'].append(column)

    ## SORT BY
    def add_order_by(self, column):
        [self._QUERY['ORDER BY'].append(col) for col in columns] if isinstance(column, list) else self._QUERY[
            'ORDER BY'].append(column)

    def limit(self, count: int):
        self._QUERY['LIMIT'] = count

    ## RETURN
    @property
    def query(self):
        parts = ["SELECT " + (", ".join(self._QUERY['SELECT'])).replace("DISTINCT,", "DISTINCT"),
                 "FROM " + ("\n".join(self._QUERY['FROM'])),
                 ("WHERE " + ("\n".join(self._QUERY['WHERE']))) if self._QUERY['WHERE'] else "",
                 ("GROUP BY " + (", ".join(self._QUERY['GROUP BY']))) if self._QUERY['GROUP BY'] else "",
                 ("ORDER BY " + (", ".join(self._QUERY['ORDER BY']))) if self._QUERY['ORDER BY'] else "",
                 ("LIMIT " + str(self._QUERY['LIMIT'])) if self._QUERY['LIMIT'] != -1 else ""]
        return "\n".join([x for x in parts if x != ""])

    ## INIT / DE-INIT
    def __del__(self):
        [value.clear() if isinstance(value, list) else -1 for _, value in
         self._QUERY.items()]  # Because the context does not disappear when the request is complete...
        self.args.clear()

import itertools
from collections import namedtuple

class TruthTable(object):
    STATES = [0, 1]

    def __init__(self, name, conditions):
        self._name = name
        self._conditions = self._validate_conditions(conditions)
        self._num_conditions = len(self._conditions) - 1
        self._n2 = self._n2_truth_table()
        self._row = namedtuple(self._name, self._conditions)
        self._table = self._create_table()

    def __iter__(self):
        for row in self._table:
            yield row
    
    def _validate_conditions(self, conditions):
        if len(conditions) == len(set(conditions)):
            return conditions
        else:
            raise ValueError('Condition labels are not unique')

    def _create_row(self, table_row):
        return self._row(*table_row)

    def _create_table(self):
        table = []
        for row in self._n2:
            table.append(self._create_row(row))
        
        return table

    def _n2_truth_table(self):
        truth_table = itertools.product(self.STATES, 
                                             repeat=self._num_conditions)
        n2_truth_table = self._n2_filter(truth_table)

        return self._results(n2_truth_table)


    def _results(self, truth_table):
        for i, row in enumerate(truth_table):
            result = all(row)  # TODO: add custom rule handling
            row_with_results = list(row) + [result]
            truth_table[i] = tuple(row_with_results)
        
        return truth_table

    def _convert_to_bools(self, row):
        return tuple([bool(x) for x in row])

    def _n2_filter(self, truth_table):
        n2_conditions = [0, self._num_conditions-1, self._num_conditions]
        return [self._convert_to_bools(row) for row in truth_table if sum(row) in n2_conditions]

if __name__ == '__main__':
    conditions = ['c0', 'c1', 'c2', 'c3', 'result']

    test1 = TruthTable("Test1", conditions)

    rule = '@c3 = @c1 or @c3'

    for row in test1:
        print(row)
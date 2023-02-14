import itertools
import re
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


    def apply_rules(self, rules):
        for rule in rules:
            for i, row in enumerate(self._table):
                lhs, rhs = self._parse(rule)
                new_value_expr = self._rule_string(rhs)
                value = eval(new_value_expr)

                # make the update
                update_expr = self._replace_string(lhs, value)
                self._table[i] = eval(update_expr)


    @classmethod
    def _replace_string(cls, condition, value):
        expr = 'row._replace({}={})'

        return expr.format(condition, value)

    @classmethod
    def _rule_string(cls, expr):
        get_attr = "getattr(row, '{}')"
        
        condition_names = re.findall(r'@(\w+)', expr)
        condition_variable_names = re.findall(r'@\w+', expr)
        condition_dict = {key: get_attr.format(value) for key, value in zip(condition_variable_names, condition_names)}
    
        expr = re.sub(r'@\w+', lambda match: condition_dict[match.group()], expr)

        return expr

    def _parse(self, rule):
        lhs, rhs = rule.split('=')
        rhs = rhs.lstrip().rstrip()
        lhs = lhs.replace('@', '').lstrip().rstrip()

        return lhs, rhs
        

def print_table(table):        
    print('*'*65)
    for row in table:
        print(row)
    print('*'*65, '\n')

if __name__ == '__main__':
    conditions = ['c0', 'c1', 'c2', 'c3', 'result']

    test1 = TruthTable("Test1", conditions)
    print_table(test1)
    
    
    rules = ['@c3 = @c1 and @c2',]
    test1.apply_rules(rules)
    print_table(test1)

    # TODO: apply the update BEFORE creating the table of Rows
    #       otherwise the result might not be correct

    # TODO: add functionality for excluding rows matching certain conditions

    # TODO: doc strings!
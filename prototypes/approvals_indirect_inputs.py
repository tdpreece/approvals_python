import mock
import pickle
import unittest


# When recording inputs for the first time you need to comment
# out verify.  If you don't you will get an iteration error
# as the mock is called too many times.

# 1) Example stubbing at module level.

def calculate_total(item_id):
    price = get_price(item_id)
    if price > 100:
        return price * 0.9
    return price


def get_price(item_id):
    return 1


class TestCalculateTotal(unittest.TestCase):
    @mock.patch('__main__.get_price')
    def test(self, get_price_stub):
        direct_inputs = [1, 2, 3, 4]
        indirect_inputs = [1, 1, 1, 1]
        get_price_stub.side_effect = indirect_inputs
        approval_test = ApprovalTest(calculate_total, lambda x, y: x == y)
        # approval_test.record(direct_inputs)
        approval_test.verify()


# 2) Example stubbing when dependency is passed in.

class Till(object):
    def __init__(self, get_price):
        self.get_price = get_price

    def calculate_total(self, item_id):
        price = self.get_price(item_id)
        if price > 100:
            return price * 0.9
        return price


class TestTillCalculateTotal(unittest.TestCase):
    def test(self):
        direct_inputs = [1, 2, 3, 4]
        indirect_inputs = [1, 1, 1, 1]
        get_price_stub = mock.MagicMock()
        get_price_stub.side_effect = indirect_inputs
        calculate_total_method = Till(get_price_stub).calculate_total
        approval_test = ApprovalTest(
            calculate_total_method,
            lambda x, y: x == y
        )
        # approval_test.record(direct_inputs)
        approval_test.verify()


# Approval Test code

class ApprovalTest(object):
    def __init__(self, func, outputs_equal, file_prefix='an_approval_test'):
        self.func = func
        self.file_prefix = file_prefix
        self.outputs_equal = outputs_equal

    def record(self, inputs):
        inputs_filename = '{}_inputs.pickle'.format(self.file_prefix)
        with open(inputs_filename, 'w') as inputs_file:
            pickle.dump(inputs, inputs_file)

        outputs = [self.func(i) for i in inputs]

        expected_outputs_filename = '{}_expected_outputs.pickle'.format(
            self.file_prefix
        )
        with open(expected_outputs_filename, 'w') as expected_outputs_file:
            pickle.dump(outputs, expected_outputs_file)

    def verify(self):
        inputs_filename = '{}_inputs.pickle'.format(self.file_prefix)
        with open(inputs_filename, 'r') as inputs_file:
            inputs = pickle.load(inputs_file)

        outputs = [self.func(i) for i in inputs]

        expected_outputs_filename = '{}_expected_outputs.pickle'.format(
            self.file_prefix
        )
        with open(expected_outputs_filename, 'r') as expected_outputs_file:
            expected_outputs = pickle.load(expected_outputs_file)
        print("expected: {}".format(expected_outputs))
        print("received: {}".format(outputs))
        assert all(
            self.outputs_equal(x[0], x[1])
            for x in zip(expected_outputs, outputs)
        )


if __name__ == '__main__':
    unittest.main()

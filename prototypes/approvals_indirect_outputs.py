import mock
import pickle
import unittest

# TODO
# How to verify mock calls when objects are user defined and may not
# have an appropriate __eq__?
#
# args = a_mock.call_args_list[0][0]
# kwargs = a_mock.call_args_list[0][0]

# When recording inputs for the first time you need to comment
# out verify.  If you don't you will get an iteration error
# as the mock is called too many times.


def calculate_total(request_id):
    if request_id in (1, 2, 3):
        log_request(request_id)


def log_request(item_id):
    pass


class TestCalculateTotal(unittest.TestCase):
    @mock.patch('__main__.log_request')
    def test(self, log_request_mock):
        direct_inputs = [1, 2, 3, 4]
        approval_test = ApprovalTest(
            calculate_total, lambda x, y: x == y, mock=log_request_mock
        )
        # approval_test.record(direct_inputs)
        approval_test.verify()


# Approval Test code

class ApprovalTest(object):
    def __init__(
        self, func, outputs_equal,
        file_prefix='an_approval_test', mock=None
    ):
        self.func = func
        self.file_prefix = file_prefix
        self.outputs_equal = outputs_equal
        self.mock = mock

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

        if self.mock:
            a_mock = self.mock
            mock_filename = 'mock.pickle'
            # Get a recursion error if try to write the mock object.
            call_args_list = [repr(call) for call in a_mock.call_args_list]
            with open(mock_filename, 'w') as mock_file:
                pickle.dump(call_args_list, mock_file)

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

        if self.mock:
            mock_filename = 'mock.pickle'
            with open(mock_filename, 'r') as mock_file:
                expected_calls = pickle.load(mock_file)
            print("expected mock calls: {}".format(expected_calls))
            a_mock = self.mock
            call_args_list = [repr(call) for call in a_mock.call_args_list]
            import pdb
            pdb.set_trace()
            print("mock calls: {}".format(call_args_list))


if __name__ == '__main__':
    unittest.main()

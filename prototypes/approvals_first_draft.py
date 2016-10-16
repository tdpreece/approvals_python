import pickle

# TODO:
# How to see which item in outputs didnt't match?
# Display associated input with output failures.
# Will probably want to extract list comparison tool so can use it to write the
#   custom assertion that goes in.
# Efficiently handle very long lists of inputs


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
        all(self.outputs_equal(x[0], x[1]) for x in zip(expected_outputs, outputs))
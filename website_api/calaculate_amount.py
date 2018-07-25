def calculate_amount_address(inputs, outputs):
	sum_inputs = 0
	sum_outputs = 0

	for _input in inputs:
		sum_inputs+=int(_input.input_value)
	for _output in outputs:
		sum_outputs+=int(_output.output_value)


	net_value = sum_outputs - sum_inputs
	net_value = net_value / 100000000

	return net_value


def calculate_amount_tx(inputs):
	sum_inputs = 0

	for _input in inputs:
		sum_inputs+=int(_input.input_value)

	net_value = sum_inputs / 100000000

	return net_value


def calculate_amount_received(outputs):
	sum_outputs = 0

	for _output in outputs:
		sum_outputs+=int(_output.output_value)

	net_value = sum_outputs / 100000000

	return net_value


def calculate_amount_received_tuple(outputs):
	sum_outputs = 0

	for _output in outputs:
		sum_outputs+=int(_output['output_value'])

	net_value = sum_outputs / 100000000

	return net_value


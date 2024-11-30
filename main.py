import math
from decimal import Decimal


def calculate_frequency(message: str):
    total_length = len(message)
    char_count = {}

    for character in message:
        char_count[character] = char_count.get(character, 0) + 1

    cumulative_probability = Decimal(0)
    probability_table = {}

    print("\nProbability Table\n")
    for character, count in sorted(char_count.items()):
        prob = Decimal(count) / Decimal(total_length)
        probability_table[character] = (prob, (cumulative_probability, cumulative_probability + prob))
        print(f"{character} - {prob:.8f}")
        cumulative_probability += prob
    print("\n")

    return probability_table


def encode_arithmetic(input_string: str):
    prob_table = calculate_frequency(input_string)

    lower_bound = Decimal(0)
    upper_bound = Decimal(1)

    for character in input_string:
        probability, (low, high) = prob_table[character]
        range_width = upper_bound - lower_bound
        upper_bound = lower_bound + range_width * high
        lower_bound = lower_bound + range_width * low
        print(f"{character}: {lower_bound:.30f} - {upper_bound:.30f}")

    if upper_bound - lower_bound == 0:
        raise ValueError("The range is zero, indicating an encoding error.")

    bit_size = round(math.log2(1 / (upper_bound - lower_bound)))
    encoded_value = bin(int(upper_bound * Decimal(2) ** bit_size))[2:]
    encoded_value = (bit_size - len(encoded_value)) * "0" + encoded_value

    return encoded_value


def encode_hamming(input_bits: str) -> str:
    bits = list(map(int, input_bits))
    num_data_bits = len(bits)

    num_parity_bits = 0
    while (2 ** num_parity_bits < num_data_bits + num_parity_bits + 1):
        num_parity_bits += 1

    total_length = num_data_bits + num_parity_bits
    encoded = [0] * total_length

    data_index = 0
    for position in range(1, total_length + 1):
        if (position & (position - 1)) != 0:
            encoded[position - 1] = bits[data_index]
            data_index += 1

    for parity in range(num_parity_bits):
        parity_pos = (2 ** parity) - 1
        parity_sum = 0
        for start in range(parity_pos, total_length, 2 ** (parity + 1)):
            parity_sum ^= sum(encoded[start:start + 2 ** parity])

        encoded[parity_pos] = parity_sum % 2

    return ''.join(map(str, encoded))


input_message: str = "сивицкийстепанолегович"

arithmetic_encode_result: str = encode_arithmetic(input_message)
hamming_encode_result: str = encode_hamming(arithmetic_encode_result)

if arithmetic_encode_result is None:
    raise BaseException("Encoded result cannot be None.")

print(f"Arithmetic encode result: {arithmetic_encode_result}")
print("A(s) = ", len(arithmetic_encode_result) / len(input_message))
print(f"Hamming's encode result: {hamming_encode_result}")
print(f"Rate: ", len(arithmetic_encode_result) / len(hamming_encode_result))

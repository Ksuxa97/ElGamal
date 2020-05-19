import random
import sympy
from termcolor import colored


def text_to_int(text, encoding='utf-8', errors='surrogatepass'):
    b = int.from_bytes(text.encode(encoding, errors), 'big')
    return b


def text_from_int(n, encoding='utf-8', errors='surrogatepass'):
    return n.to_bytes(
        (n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def gcd(a,b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def rapid_exp(number, power):
    bin_power = [int(i) for i in bin(power)[2:]]
    bin_power.reverse()
    result = 1

    for i in range(len(bin_power)):
        result *= pow(number, (2**i) * bin_power[i])

    return result


def primitive_root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g

def generate_key():
    max_key_value = int('0x' + 'f' * 1024, 16)

    # max_key_value = 1024
    prime = random.randint(1, max_key_value)
    while not sympy.isprime(prime):
        prime = random.randint(1, max_key_value)

    g = primitive_root(modulo=prime)
    x = random.randint(2, prime)
    y = rapid_exp(g, x) % prime

    return [prime, g, y], x

def alternative_key(prime):
    z = random.randint(2, prime)
    g = primitive_root(modulo=prime)
    y = rapid_exp(g, z) % prime

    return [prime, g, y], z


def encrypt(message, public_key):
    k = random.randint(2, public_key[0] - 1)
    a = rapid_exp(public_key[1], k) % public_key[0]
    encrypted_msg = [a]
    for letter in message:
        num_msg = text_to_int(letter)
        encrypted_msg += [(rapid_exp(public_key[2], k) * num_msg) % public_key[0]]
    return encrypted_msg


def decrypt(encrypted_message, key_pair):
    decrypted_message = ''
    a_pow_x = rapid_exp(encrypted_message[0], key_pair[1])
    mult_inverse = euclid(key_pair[0][0], a_pow_x)

    for b in encrypted_message[1::]:
        num_msg = (b * mult_inverse) % key_pair[0][0]
        decrypted_message += text_from_int(num_msg)

    return decrypted_message


def corrupt_msg(ecrypted_msg):

    for i in range(1, len(ecrypted_msg)):
        if random.randint(0, 2):
            ecrypted_msg[i] -= 1

    return


def euclid(dividend, divisor):

    quotient = 0
    reminder = 0

    quotient_list = []

    while True:
        quotient, reminder = divmod(dividend, divisor)
        quotient_list.append(quotient)
        if reminder == 1:
            break
        dividend = divisor
        divisor = reminder

    a = 1
    b = 0
    for i in range(len(quotient_list)):
        temp = b - quotient_list[i] * a
        b = a
        a = temp

    return a


def simple_run():
    print("Bob side -> Generate keys")
    public_key, private_key = generate_key()
    print("Public key: {}. Private key: {}.".format(public_key, private_key))
    print()

    print("Alice side -> Get public keys (p, g, y)")
    print("Public keys: {}".format(public_key))
    message = input("Input your message: ")
    # message = "Secret message"

    print("Encrypting message.....")
    encrypted_message = encrypt(message, public_key)
    print("Message encrypted: {}".format(encrypted_message))
    print()

    print("Bob side -> Got message. Decrypting...")
    decrypted_message = decrypt(encrypted_message, [public_key, private_key])
    print("Message Decrypted: {}".format(decrypted_message))
    return


def man_in_the_middle_attack():
    print("Bob side -> Generate keys")
    public_key, private_key = generate_key()
    print("Public key: {}. Private key: {}.".format(public_key, private_key))
    print()

    print(colored("Eve side -> Intersepts public key....", "red"))
    alternative_public, z = alternative_key(public_key[0])
    print(colored("Public key: {}. Private key: {}.".format(alternative_public, z), "red"))
    print()

    print("Alice side -> Get public keys (p, g, y)")
    print("Public keys: {}".format(alternative_public))
    message = input("Input your message: ")

    print("Encrypting message.....")
    encrypted_message = encrypt(message, alternative_public)
    print("Message encrypted: {}".format(encrypted_message))
    print()

    print(colored("Eve side -> Got message. Decrypting...", "red"))
    decrypted_message = decrypt(encrypted_message, [alternative_public, z])
    print(colored("Message Decrypted: {}".format(decrypted_message), "red"))
    print(colored("Corrupting message.....", "red"))
    corrupted_msg = encrypt("Good pancakes", public_key)
    print()

    print("Bob side -> Got message. Decrypting...")
    decrypted_message = decrypt(corrupted_msg, [public_key, private_key])
    print("Message Decrypted: {}".format(decrypted_message))
    return


def main():
    man_in_the_middle_attack()

    return

if __name__ == "__main__":
    main()


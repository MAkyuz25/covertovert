import string
import time
import random
from scapy.all import send, sendp, ARP, LLC

# You are not allowed to change CovertChannelBase class, please make your implementation in the MyCovertChannel class.
class CovertChannelBase:
    """
    - You must inherit the CovertChannelBase class in your implementation.
    """
    def __init__(self):
        """
        - Empty init
        """
        pass
    def send(self, packet, interface="eth0"):
        """
        - You must send each packet by using this function.
        - Call this function with the packet and sender's interface (Default interface is "eth0" and you do not have to set unless there is a specific purpose.)
        """
        if packet.haslayer(ARP) or packet.haslayer(LLC):
            sendp(packet, iface=interface, verbose=False)
        else:
            send(packet, iface=interface, verbose=False)
    def log_message(self, message, log_file_name):
        """
        - You can use this function to log the received message and it is not a must, you can write your own.
        """
        with open(log_file_name, "w") as my_file:
            my_file.write(message)
    def convert_string_message_to_binary(self, message):
        """
        - Converts the incoming string value to binary format.
        - You do not have to use it directly; instead, you can use generate_random_binary_message or generate_random_binary_message_with_logging functions.
        """
        binary_message_to_transfer = ''.join(format(i, '08b') for i in bytearray(message, encoding='utf-8'))
        return binary_message_to_transfer
    def generate_random_message(self, min_length=5, max_length=10):
        """
        - You can use this function if you want to create a random string, e.g. for the payload of the packet.
        """
        assert 0 < min_length, "min_length must be bigger than 0"
        assert min_length <= max_length, "min_length must be smaller than or equal to the max_length"
        letters_digits = string.ascii_letters + string.digits
        punctuation = ',?!'
        all_chars = " " * 50 + letters_digits * 5 + punctuation
        length = random.randint(min_length-1, max_length-1)
        random_string = ''.join(random.choice(all_chars) for _ in range(length))
        random_string += "."
        return random_string
    def generate_random_binary_message(self, min_length=50, max_length=100):
        """
        - It generates a random string whose length is between the min_length and max_length, and converts it to binary format.
        - "." is the stopping character for the covert channel communication, so that it adds "." at the of the generated string without ruining the length restrictions.
        - You must use this function to generate the message in binary format that will be transferred with covert channel communication.
        """
        random_message = self.generate_random_message(min_length=min_length, max_length=max_length)
        random_binary_message = self.convert_string_message_to_binary(message=random_message)
        return random_binary_message
    def generate_random_binary_message_with_logging(self, log_file_name, min_length=50, max_length=100):
        """
        - Same as generate_random_binary_message() function with logging option.
        """
        random_message = self.generate_random_message(min_length=min_length, max_length=max_length)
        random_binary_message = self.convert_string_message_to_binary(message=random_message)
        self.log_message(message=random_message, log_file_name=log_file_name)
        return random_binary_message
    def sleep_random_time_ms(self, start=1, end=10):
        """
        - For the covert timing channels, you can use this function if you want to wait random time in miliseconds between start and end.
        """
        time.sleep(random.uniform(start, end) / 1000)
    def convert_eight_bits_to_character(self, eight_bits):
        """
        - It can be used to convert the received eight bits to a character in the receiving operation.
        - Takes eight bits as a string, converts and returns.
        """
        return chr(int(eight_bits, 2))

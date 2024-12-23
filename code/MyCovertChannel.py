from CovertChannelBase import CovertChannelBase
from scapy.all import sniff

timestamp = 0
message = ""

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        """
        - You can edit __init__.
        """
        pass
    def send(self, log_file_name, parameter1, parameter2):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """

        randomMessage = self.generate_random_binary_message_with_logging(log_file_name)
        for i in range(len(randomMessage)):

            messageCount = CovertChannelBase.random.randint(2,6)

            for j in range(messageCount):
                CovertChannelBase.send(self.generate_random_binary_message())

            if(randomMessage[i] == '0'):

                CovertChannelBase.sleep_random_time_ms(20,30) # encodes 0

            else:

                CovertChannelBase.sleep_random_time_ms(10,19) # encodes 1

        
    def receive(self, parameter1, parameter2, parameter3, log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        self.log_message("", log_file_name)

        while(True):

            try:
                packet = sniff(prn=lambda packet: self.packet_handler(packet, log_file_name=log_file_name))
            except KeyboardInterrupt:
                break

    def packet_handler(self, packet, log_file_name):

        global timestamp
        global message

        currentTime = packet.time

        if(timestamp == 0):
            timestamp = currentTime

        else:
            timeDifferenceMs = (currentTime - timestamp) * 1000 # time difference between two packets in ms
            print(timeDifferenceMs)
            timestamp = currentTime
            if(timeDifferenceMs > 20):
                message += "0"
            elif(timeDifferenceMs < 20 and timeDifferenceMs > 10):
                message += "1"
            
            print(message)

            if(len(message) == 8):
                convertedMessage = CovertChannelBase.convert_eight_bits_to_character(message)

                if(convertedMessage == "."):
                    raise KeyboardInterrupt

                CovertChannelBase.log_message(convertedMessage, log_file_name=log_file_name)

                message = ""
            
        
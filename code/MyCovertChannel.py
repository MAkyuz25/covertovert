from CovertChannelBase import CovertChannelBase
import random
from scapy.all import sniff
from scapy.all import Ether, LLC, Raw, IP

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
            print(randomMessage[i])
            messageCount = random.randint(2,6)

            for j in range(messageCount):
                currentMessage = self.generate_random_message()
                packet = Ether() / IP(dst="172.18.0.3") / LLC(dsap=0xAA, ssap=0xAA, ctrl=0x03) / Raw(load=currentMessage)
                CovertChannelBase.send(self, packet=packet)

            if(randomMessage[i] == '1'):
              
                CovertChannelBase.sleep_random_time_ms(self, 800,850) # encodes 0

            else:

                CovertChannelBase.sleep_random_time_ms(self, 1010,1100) # encodes 1
            
        
    def receive(self, parameter1, parameter2, parameter3, log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        self.log_message("", log_file_name)

        while(True):

            try:
                packet = sniff(iface="eth0", prn=lambda packet: self.packet_handler(packet, log_file_name=log_file_name), filter="ip src 172.18.0.2")
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
            #print(f" Time differences between single packets: {timeDifferenceMs}" )
            timestamp = currentTime
            if(timeDifferenceMs > 1000):
                print(timeDifferenceMs)
                
                message += "0"
                print(message)
            elif(timeDifferenceMs < 1000 and timeDifferenceMs > 800):
                print(timeDifferenceMs)
                
                message += "1"
                print(message)
            
            

            if(len(message) == 8):
                convertedMessage = CovertChannelBase.convert_eight_bits_to_character(self, message)

                if(convertedMessage == "."):
                    raise KeyboardInterrupt

                CovertChannelBase.log_message(self, convertedMessage, log_file_name=log_file_name)

                message = ""
            
        
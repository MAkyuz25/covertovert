from CovertChannelBase import CovertChannelBase
import random
from scapy.all import sniff
from scapy.all import Ether, LLC, Raw, IP
import time

timestamp = 0
message = ""
lastconvertedMessage=""
lastmessage =""

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
    def send(self, log_file_name, min_packet_number = 2, max_packet_number =6, min_sleep_for_0 =200, max_sleep_for_0 = 250, min_sleep_for_1 =400, max_sleep_for_1 = 500):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        assert 0<min_packet_number
        assert min_packet_number<= max_packet_number
        assert 200<=min_sleep_for_0
        assert min_sleep_for_0<=max_sleep_for_0
        assert 400<=min_sleep_for_1
        assert min_sleep_for_1<= max_sleep_for_1
        randomMessage = self.generate_random_binary_message_with_logging(log_file_name)
        randomMessage += "0"
        len_of_randomMessage = len(randomMessage)
        for i in range(len_of_randomMessage):
            
            messageCount = random.randint(min_packet_number,max_packet_number)

            for j in range(messageCount):
                
                currentMessage = self.generate_random_message()
                # Create and send packet
                packet = Ether() / IP(dst="172.18.0.3") / LLC(dsap=0xAA, ssap=0xAA, ctrl=0x03) / Raw(load=currentMessage)
                CovertChannelBase.send(self, packet=packet)

            if(i == len_of_randomMessage-1):
                break
            elif(randomMessage[i] == '1'):
              
                CovertChannelBase.sleep_random_time_ms(self, min_sleep_for_0,max_sleep_for_0) # encodes 1
                

            else:

                CovertChannelBase.sleep_random_time_ms(self, min_sleep_for_1,max_sleep_for_1) # encodes 0
            
    def stop_sniffing(packet):
        global lastconvertedMessage
        return lastconvertedMessage =="."
        
    def receive(self, log_file_name,min_wait=200, max_wait =400):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        global lastconvertedMessage
        assert 200<=min_wait
        assert min_wait<= max_wait
        packet = sniff(iface="eth0",prn=lambda packet: self.packet_handler(packet, min_wait=min_wait, max_wait=max_wait), filter="ip src 172.18.0.2", stop_filter= lambda packet: self.stop_sniff(packet))
        CovertChannelBase.log_message(self, lastmessage, log_file_name=log_file_name)

    def stop_sniff(self, packet):
        global lastconvertedMessage
        return lastconvertedMessage == "."  # Stop sniffing when the message ends with "."

    def packet_handler(self, packet, min_wait, max_wait):

        global timestamp
        global message
        global lastconvertedMessage
        global lastmessage
        currentTime = packet.time
        
        
        if(timestamp == 0):
            timestamp = currentTime

        else:
            
            timeDifferenceMs = (currentTime - timestamp) * 1000
            timestamp = currentTime
            if(timeDifferenceMs >= max_wait):
                
                
                message += "0"
                
            elif(timeDifferenceMs < max_wait and timeDifferenceMs >= min_wait):
                message += "1"


            if(len(message) == 8):
                
                convertedMessage = CovertChannelBase.convert_eight_bits_to_character(self, message)
                message =""
                lastmessage = lastmessage +convertedMessage

                lastconvertedMessage =convertedMessage
                convertedMessage =""
            
        
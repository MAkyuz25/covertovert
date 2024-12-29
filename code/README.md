# Covert Timing Channel that exploits Idle Period Between Packet Bursts using LLC [Code: CTC-IPPB-LLC]

This repository implements "Idle Period Between Packet Bursts" type covert channel. Base class can be found in "CovertChannelBase.y", while the algorithm is implemented in "MyCOvertChannel.py".

MyCovertChannel.send() function creates the random binary message that we want to send. It then starts to send trivial packets (different number of packets each time), and waits between packet bursts to encode our message in bits. If we want to encode 0, it waits for a random time in the interval
(min_sleep_for_0, max_sleep_for_0). Likewise, if it wants to encode 1, it waits for a random time in the interval (min_sleep_for_1, max_sleep_for_1). Those time thresholds can be adjusted, as they are parameters. MyCovertChannel.receive() functions uses sniff function to catch packets sent, and uses the helper method MyCovertChannel.packet_handler() to measure time between packet bursts, and encodes the bit sent accordingly.

Send() Parameters:

max_network_delay: We detect that min_sleep_for_1 must be greater than max_network_delay + max_sleep_for_0 to encode 1, since after sleeping to encode 1, there is also network delay to send the first trivial packet of the packets that helps us to encode the following bit.

min_packet_number: minimum number of random packets in a burst. First packed is ignored since establishing the connection takes too much time and corrupts the encoding. Thus, it is also asserted that it is greater than or equal to 2.

max_packet_number: maximum number of random packets in a burst. It is also asserted that it is greater than or equal to min_packet_number.

min_sleep_for_0: minimum sleep time to wait between packet bursts to encode 0. It is also asserted that it is greater than or equal to max_network_delay.

max_sleep_for_0: maximum sleep time to wait between packet bursts to encode 0. It is also asserted that it is greater than min_sleep_for_0.

min_sleep_for_1: minimum sleep time to wait between packet bursts to encode 1. It is also asserted that it is greater than max_sleep_for_0 + max_network_delay.

max_sleep_for_1: maximum sleep time to wait between packet bursts to encode 1. It is also asserted that it is greater than or equal to min_sleep_for_1.

log_file_name: file name to log message into.

Receive() Parameters:

max_network_delay: It is similar to the max_network_delay in sender.

min_wait: minimum time to wait to encode 0. It is asserted to be greater than the max_network_delay.

max_wait: maximum time to wait to encode 0 and 1. If the time difference between packet bursts is greater than this value, we accept it as 1. It is asserted to be greater than the min_wait + max_network_delay to make the assertion that has been established in sender.

log_file_name: file name to log message into.

Covert Channel Capacity: 0.53
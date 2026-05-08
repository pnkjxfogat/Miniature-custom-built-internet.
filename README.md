# Miniature-custom-built-internet.
Instead of relying on your computer's operating system to handle all the complex networking invisibly, this project manually builds a networking stack from scratch. It demonstrates exactly what happens to a piece of data from the moment you hit "send" to the moment it is safely decoded on another screen.
Here is exactly what the code is doing under the hood, broken down by its main jobs:

1. It acts as a Post Office (Network Layer)
When you type a message (like "Hello"), the code doesn't just send the word. It attaches a "To" address (Destination IP) and a "From" address (Source IP). This creates a structured packet of data, just like putting a letter into an addressed envelope.

2. It acts as Quality Control (Data Link Layer)
Real-world networks are chaotic. Because bits can get flipped in transit, this layer protects the data.

Framing: It wraps your packet in special mathematical flags (the 01111110 sequence) so the receiving computer knows exactly where the message starts and ends.

Error Detection: It calculates a mathematical summary of your data (a Parity Bit). If the data gets corrupted during travel, the receiver's math won't match, and it will immediately realize the data is broken.

3. It creates a "Messy" Cable (Physical Layer)
To prove that our Quality Control works, we have to simulate a bad environment (like terrible Wi-Fi or static on a radio).

The code translates everything into raw binary (1s and 0s).

It intentionally injects noise by randomly flipping a few bits based on a set probability (e.g., a 1% chance a bit flips).

Finally, it shoots those raw bits across a UDP socket. We use UDP because it is a "dumb" connection—it acts like a raw copper wire or radio frequency, carrying whatever we give it without trying to fix anything.

Why is this valuable?
Normally, software developers never have to think about this stuff; they just use a library to send data. By writing these layers out manually, you are proving you understand how machines physically and logically communicate on a foundational level. It's a fantastic talking point for a portfolio or an interview.

Team Member 

Harsh Verma 
Pranshu Kureel
Puneet Kumar
Archit Thakur
Pankaj Fogat

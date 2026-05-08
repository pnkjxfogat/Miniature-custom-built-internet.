import socket
import random
import time

# ==========================================
# 1. PHYSICAL LAYER
# Deals with raw bits and channel noise
# ==========================================
class PhysicalLayer:
    @staticmethod
    def text_to_bits(text):
        """Converts raw text to a string of binary bits."""
        return ''.join(format(ord(i), '08b') for i in text)

    @staticmethod
    def bits_to_text(bits):
        """Converts a string of binary bits back to text."""
        chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
        return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

    @staticmethod
    def transmit_with_noise(bits, error_probability=0.02):
        """Simulates channel interference by randomly flipping bits."""
        noisy_bits = ""
        for bit in bits:
            if random.random() < error_probability:
                noisy_bits += '0' if bit == '1' else '1' # Flip the bit
            else:
                noisy_bits += bit
        return noisy_bits

# ==========================================
# 2. DATA LINK LAYER
# Deals with Framing and Error Detection
# ==========================================
class DataLinkLayer:
    FLAG = "01111110" # Standard framing flag to mark start/end of a frame

    @staticmethod
    def calculate_parity(bits):
        """Calculates Even Parity for error detection."""
        return '1' if bits.count('1') % 2 != 0 else '0'

    @classmethod
    def encapsulate_frame(cls, network_packet_bits):
        """Wraps the packet in flags and adds a parity bit."""
        parity = cls.calculate_parity(network_packet_bits)
        frame = cls.FLAG + parity + network_packet_bits + cls.FLAG
        print(f"[Data Link TX] Frame constructed: {len(frame)} bits.")
        return frame

    @classmethod
    def decapsulate_frame(cls, frame_bits):
        """Checks framing, detects errors, and extracts the packet."""
        # 1. Check Framing
        if not frame_bits.startswith(cls.FLAG) or not frame_bits.endswith(cls.FLAG):
            print("[Data Link RX] ERROR: Frame alignment lost. Dropping frame.")
            return None

        # Extract content (strip flags)
        content = frame_bits[len(cls.FLAG):-len(cls.FLAG)]
        if not content:
            return None

        # 2. Error Detection
        received_parity = content[0]
        payload = content[1:]
        
        if cls.calculate_parity(payload) != received_parity:
            print("[Data Link RX] ERROR: Parity check failed! Data corrupted in transit. Dropping frame.")
            return None
            
        print("[Data Link RX] Frame intact. Parity check passed.")
        return payload

# ==========================================
# 3. NETWORK LAYER
# Deals with Addressing and Routing
# ==========================================
class NetworkLayer:
    @staticmethod
    def create_packet(message, src_ip, dest_ip):
        """Creates a simple packet with Source IP, Dest IP, and Payload."""
        # Pad IPs to 15 chars for consistent bit-length in this simple model
        src = src_ip.ljust(15)
        dst = dest_ip.ljust(15)
        packet = f"SRC:{src}|DST:{dst}|MSG:{message}"
        print(f"[Network TX] Packet created. Routing to {dest_ip}")
        return PhysicalLayer.text_to_bits(packet)

    @staticmethod
    def read_packet(packet_bits):
        """Extracts IPs and message from the packet."""
        packet_text = PhysicalLayer.bits_to_text(packet_bits)
        parts = packet_text.split('|')
        if len(parts) >= 3:
            src = parts[0].replace("SRC:", "").strip()
            dst = parts[1].replace("DST:", "").strip()
            msg = parts[2].replace("MSG:", "")
            print(f"[Network RX] Packet received from {src}. Message: '{msg}'")
            return msg
        return None

# ==========================================
# MAIN EXECUTION: SENDER & RECEIVER NODES
# ==========================================
def run_sender():
    IP, PORT = "127.0.0.1", 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket
    
    print("\n--- SENDER NODE ---")
    message = input("Enter a message to send: ")
    
    # Network Layer
    packet_bits = NetworkLayer.create_packet(message, src_ip="192.168.1.10", dest_ip="192.168.1.20")
    
    # Data Link Layer
    frame_bits = DataLinkLayer.encapsulate_frame(packet_bits)
    
    # Physical Layer (Injecting noise before sending over the socket)
    transmitted_signal = PhysicalLayer.transmit_with_noise(frame_bits, error_probability=0.01)
    
    # Send via UDP (Simulating the physical wire/air)
    print("[Physical TX] Transmitting signals over UDP channel...")
    sock.sendto(transmitted_signal.encode(), (IP, PORT))
    print("Transmission complete.")

def run_receiver():
    IP, PORT = "127.0.0.1", 5005
    sock = socket.socket(socket.AF_INET, socket.socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    
    print("\n--- RECEIVER NODE ---")
    print(f"Listening on {IP}:{PORT}...")
    
    while True:
        data, addr = sock.recvfrom(4096)
        received_signal = data.decode()
        print("\n[Physical RX] Signal received from channel.")
        
        # Data Link Layer
        packet_bits = DataLinkLayer.decapsulate_frame(received_signal)
        
        if packet_bits is not None:
            # Network Layer
            NetworkLayer.read_packet(packet_bits)
        else:
            print("Action: Requesting retransmission (ARQ not fully implemented in this demo).")

if __name__ == "__main__":
    choice = input("Run as (1) Receiver or (2) Sender? ")
    if choice == '1':
        run_receiver()
    elif choice == '2':
        run_sender()
    else:
        print("Invalid choice.")

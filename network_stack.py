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

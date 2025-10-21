import struct
import time
import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import numpy as np
import matplotlib.pyplot as plt

class PresentCipher:
    """Lightweight PRESENT cipher implementation"""
    
    # PRESENT S-box
    SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
            0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
    
    # PRESENT inverse S-box
    SBOX_INV = [SBOX.index(x) for x in range(16)]
    
    def __init__(self, key, rounds=32):
        """Initialize with a 80 or 128-bit key"""
        self.rounds = rounds
        self.key = key
        self.round_keys = self._generate_round_keys()
    
    def _generate_round_keys(self):
        """Generate round keys for PRESENT"""
        key_len = len(self.key)
        if key_len not in [10, 16]:  # 80-bit or 128-bit key
            raise ValueError("Key must be 10 or 16 bytes (80 or 128 bits)")
        
        # Convert key to 128-bit state
        K = int.from_bytes(self.key, 'big')
        
        # For 80-bit key, pad with zeros to 128 bits
        if key_len == 10:
            K <<= 48  # 128 - 80 = 48 bits of padding
        
        round_keys = []
        for i in range(1, self.rounds + 1):
            # Extract round key (64 bits)
            round_key = (K >> 64) & 0xFFFFFFFFFFFFFFFF
            round_keys.append(round_key)
            
            # Key update
            K = ((K & 0x7FFFFFFFFFFFFFFF) << 61) | (K >> 67)
            
            # S-box application
            K_high = (K >> 60) & 0xF
            K_high = self.SBOX[K_high]
            K = (K & 0x0FFFFFFFFFFFFFFF) | (K_high << 60)
            
            # XOR with round counter
            K ^= (i << 15)
        
        return round_keys
    
    def _add_round_key(self, state, round_key):
        """Add round key to state"""
        return state ^ round_key
    
    def _sbox_layer(self, state, inverse=False):
        """Apply S-box to each nibble of the state"""
        sbox = self.SBOX_INV if inverse else self.SBOX
        result = 0
        for i in range(16):  # 64 bits / 4 bits per nibble = 16 nibbles
            nibble = (state >> (i * 4)) & 0xF
            result |= sbox[nibble] << (i * 4)
        return result
    
    def _p_layer(self, state, inverse=False):
        """Apply bit permutation"""
        result = 0
        for i in range(64):
            if inverse:
                # Inverse permutation: bit i comes from position p(i)
                j = (i * 16) % 63
                if i == 63:  # Special case for last bit
                    j = 63
            else:
                # Forward permutation: bit i moves to position p(i)
                if i == 0:
                    j = 0
                else:
                    j = (i * 16) % 63
            
            # Set bit j in result to bit i of state
            bit = (state >> i) & 1
            result |= (bit << j)
        
        return result
    
    def encrypt_block(self, plaintext):
        """Encrypt a single 64-bit block"""
        state = int.from_bytes(plaintext, 'big')
        
        for i in range(self.rounds - 1):
            state = self._add_round_key(state, self.round_keys[i])
            state = self._sbox_layer(state)
            state = self._p_layer(state)
        
        # Final round (no permutation)
        state = self._add_round_key(state, self.round_keys[-1])
        
        return state.to_bytes(8, 'big')
    
    def decrypt_block(self, ciphertext):
        """Decrypt a single 64-bit block"""
        state = int.from_bytes(ciphertext, 'big')
        
        # Final round (in reverse order)
        state = self._add_round_key(state, self.round_keys[-1])
        
        for i in range(self.rounds - 2, -1, -1):
            state = self._p_layer(state, inverse=True)
            state = self._sbox_layer(state, inverse=True)
            state = self._add_round_key(state, self.round_keys[i])
        
        return state.to_bytes(8, 'big')


def generate_salt(length=8):
    """Generate a random salt"""
    return os.urandom(length)


def xor_bytes(a, b):
    """XOR two byte strings of the same length"""
    return bytes(x ^ y for x, y in zip(a, b))


def cfb_encrypt(plaintext, key, salt, block_size=8):
    """
    CFB mode encryption with salt as IV
    
    Args:
        plaintext: Bytes to encrypt
        key: Encryption key (16 or 24 bytes for 3DES)
        salt: Random salt to use as IV (8 bytes for DES3)
        block_size: Block size in bytes (8 for DES3)
    
    Returns:
        Tuple of (ciphertext, salt)
    """
    if len(salt) != block_size:
        raise ValueError(f"Salt must be {block_size} bytes for CFB mode")
    
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Pad the plaintext if needed
    padded = pad(plaintext, block_size)
    
    # Encrypt the salt to get the first block of keystream
    keystream = cipher.encrypt(salt)
    
    # Split into blocks
    blocks = [padded[i:i+block_size] for i in range(0, len(padded), block_size)]
    ciphertext_blocks = []
    
    # First block uses salt as IV
    ciphertext_block = xor_bytes(blocks[0], keystream)
    ciphertext_blocks.append(ciphertext_block)
    
    # Subsequent blocks use previous ciphertext block as input
    for i in range(1, len(blocks)):
        keystream = cipher.encrypt(ciphertext_blocks[-1])
        ciphertext_block = xor_bytes(blocks[i], keystream)
        ciphertext_blocks.append(ciphertext_block)
    
    return b''.join(ciphertext_blocks), salt


def cfb_decrypt(ciphertext, key, salt, block_size=8):
    """
    CFB mode decryption with salt as IV
    
    Args:
        ciphertext: Bytes to decrypt
        key: Decryption key (16 or 24 bytes for 3DES)
        salt: Salt used as IV (8 bytes for DES3)
        block_size: Block size in bytes (8 for DES3)
    
    Returns:
        Decrypted plaintext
    """
    if len(salt) != block_size:
        raise ValueError(f"Salt must be {block_size} bytes for CFB mode")
    
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Split into blocks
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext_blocks = []
    
    # First block uses salt as IV
    keystream = cipher.encrypt(salt)
    plaintext_block = xor_bytes(blocks[0], keystream)
    plaintext_blocks.append(plaintext_block)
    
    # Subsequent blocks use previous ciphertext block as input
    for i in range(1, len(blocks)):
        keystream = cipher.encrypt(blocks[i-1])
        plaintext_block = xor_bytes(blocks[i], keystream)
        plaintext_blocks.append(plaintext_block)
    
    # Remove padding
    padded_plaintext = b''.join(plaintext_blocks)
    try:
        return unpad(padded_plaintext, block_size)
    except ValueError:
        # If unpadding fails, return the raw plaintext (might be incorrect key)
        return padded_plaintext


def cbc_encrypt(plaintext, key, salt, block_size=8):
    """
    CBC mode encryption with salt as IV
    
    Args:
        plaintext: Bytes to encrypt
        key: Encryption key (16 or 24 bytes for 3DES)
        salt: Random salt to use as IV (8 bytes for DES3)
        block_size: Block size in bytes (8 for DES3)
    
    Returns:
        Tuple of (ciphertext, salt)
    """
    if len(salt) != block_size:
        raise ValueError(f"Salt must be {block_size} bytes for CBC mode")
    
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Pad the plaintext
    padded = pad(plaintext, block_size)
    
    # Split into blocks
    blocks = [padded[i:i+block_size] for i in range(0, len(padded), block_size)]
    ciphertext_blocks = []
    previous = salt  # Use salt as IV for first block
    
    for block in blocks:
        # XOR with previous ciphertext (or IV for first block)
        xored = xor_bytes(block, previous)
        # Encrypt the result
        encrypted = cipher.encrypt(xored)
        ciphertext_blocks.append(encrypted)
        previous = encrypted
    
    return b''.join(ciphertext_blocks), salt


def cbc_decrypt(ciphertext, key, salt, block_size=8):
    """
    CBC mode decryption with salt as IV
    
    Args:
        ciphertext: Bytes to decrypt
        key: Decryption key (16 or 24 bytes for 3DES)
        salt: Salt used as IV (8 bytes for DES3)
        block_size: Block size in bytes (8 for DES3)
    
    Returns:
        Decrypted plaintext
    """
    if len(salt) != block_size:
        raise ValueError(f"Salt must be {block_size} bytes for CBC mode")
    
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Split into blocks
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext_blocks = []
    previous = salt  # Use salt as IV for first block
    
    for block in blocks:
        # Decrypt the block
        decrypted = cipher.decrypt(block)
        # XOR with previous ciphertext (or IV for first block)
        xored = xor_bytes(decrypted, previous)
        plaintext_blocks.append(xored)
        previous = block
    
    # Remove padding
    padded_plaintext = b''.join(plaintext_blocks)
    try:
        return unpad(padded_plaintext, block_size)
    except ValueError:
        # If unpadding fails, return the raw plaintext (might be incorrect key)
        return padded_plaintext


def measure_performance():
    """Measure and compare performance of different encryption methods"""
    import timeit
    import random
    import string
    
    # Generate test data
    test_sizes = [8, 64, 512, 4096, 32768]  # Test with different data sizes
    results = {
        'cfb_encrypt': [],
        'cfb_decrypt': [],
        'cbc_encrypt': [],
        'cbc_decrypt': []
    }
    
    # Generate random key and salt
    key = os.urandom(16)  # 128-bit key
    salt = os.urandom(8)  # 64-bit salt/IV
    
    for size in test_sizes:
        # Generate random test data
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()
        
        # Time CFB encryption/decryption
        cfb_enc_time = timeit.timeit(
            lambda: cfb_encrypt(data, key, salt),
            number=100
        ) / 100  # Average time per operation
        
        # Get ciphertext for decryption timing
        cfb_ciphertext, _ = cfb_encrypt(data, key, salt)
        cfb_dec_time = timeit.timeit(
            lambda: cfb_decrypt(cfb_ciphertext, key, salt),
            number=100
        ) / 100
        
        # Time CBC encryption/decryption
        cbc_enc_time = timeit.timeit(
            lambda: cbc_encrypt(data, key, salt),
            number=100
        ) / 100
        
        # Get ciphertext for decryption timing
        cbc_ciphertext, _ = cbc_encrypt(data, key, salt)
        cbc_dec_time = timeit.timeit(
            lambda: cbc_decrypt(cbc_ciphertext, key, salt),
            number=100
        ) / 100
        
        # Store results
        results['cfb_encrypt'].append((size, cfb_enc_time * 1000))  # Convert to ms
        results['cfb_decrypt'].append((size, cfb_dec_time * 1000))
        results['cbc_encrypt'].append((size, cbc_enc_time * 1000))
        results['cbc_decrypt'].append((size, cbc_dec_time * 1000))
        
        print(f"Size: {size} bytes")
        print(f"  CFB Encrypt: {cfb_enc_time * 1000:.4f} ms")
        print(f"  CFB Decrypt: {cfb_dec_time * 1000:.4f} ms")
        print(f"  CBC Encrypt: {cbc_enc_time * 1000:.4f} ms")
        print(f"  CBC Decrypt: {cbc_dec_time * 1000:.4f} ms")
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    # Plot encryption times
    plt.subplot(2, 1, 1)
    plt.plot(
        [x[0] for x in results['cfb_encrypt']],
        [x[1] for x in results['cfb_encrypt']],
        'b-', label='CFB Encrypt'
    )
    plt.plot(
        [x[0] for x in results['cbc_encrypt']],
        [x[1] for x in results['cbc_encrypt']],
        'r-', label='CBC Encrypt'
    )
    plt.title('Encryption Performance')
    plt.xlabel('Data Size (bytes)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    
    # Plot decryption times
    plt.subplot(2, 1, 2)
    plt.plot(
        [x[0] for x in results['cfb_decrypt']],
        [x[1] for x in results['cfb_decrypt']],
        'b--', label='CFB Decrypt'
    )
    plt.plot(
        [x[0] for x in results['cbc_decrypt']],
        [x[1] for x in results['cbc_decrypt']],
        'r--', label='CBC Decrypt'
    )
    plt.title('Decryption Performance')
    plt.xlabel('Data Size (bytes)')
    plt.ylabel('Time (ms)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('encryption_performance.png')
    print("Performance graphs saved as 'encryption_performance.png'")


if __name__ == "__main__":
    # Example usage
    key = os.urandom(16)  # 128-bit key for 3DES-EDE2
    salt = generate_salt(8)  # 64-bit salt/IV
    
    # Test data (64-bit block)
    test_data = b'TestData'  # 8 bytes = 64 bits
    
    print(f"Original data: {test_data}")
    
    # Test CFB mode
    print("\nTesting CFB mode:")
    cfb_cipher, _ = cfb_encrypt(test_data, key, salt)
    print(f"CFB Encrypted: {cfb_cipher.hex()}")
    cfb_plain = cfb_decrypt(cfb_cipher, key, salt)
    print(f"CFB Decrypted: {cfb_plain}")
    
    # Test CBC mode
    print("\nTesting CBC mode:")
    cbc_cipher, _ = cbc_encrypt(test_data, key, salt)
    print(f"CBC Encrypted: {cbc_cipher.hex()}")
    cbc_plain = cbc_decrypt(cbc_cipher, key, salt)
    print(f"CBC Decrypted: {cbc_plain}")
    
    # Run performance tests
    print("\nRunning performance tests...")
    measure_performance()

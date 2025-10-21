import os
import sys
import argparse
import base64
from present_cipher import (
    PresentCipher,
    generate_salt,
    cfb_encrypt, cfb_decrypt,
    cbc_encrypt, cbc_decrypt
)

# Default key (in a real application, this should be securely generated and stored)
DEFAULT_KEY = os.urandom(16)  # 128-bit key for 3DES-EDE2


def get_user_input(prompt, default=None, is_password=False):
    """Helper function to get user input with optional default"""
    if default is not None:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    if is_password:
        import getpass
        user_input = getpass.getpass(prompt)
    else:
        user_input = input(prompt)
    
    return user_input if user_input else default


def main():
    parser = argparse.ArgumentParser(description="Salted Cipher Modes - CFB and CBC with Salt")
    parser.add_argument('--mode', choices=['cfb', 'cbc', 'test'], help='Encryption mode (CFB or CBC) or test performance')
    parser.add_argument('--action', choices=['encrypt', 'decrypt', 'both'], help='Action to perform')
    parser.add_argument('--input', help='Input text or file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--key', help='Encryption key (base64 encoded)')
    parser.add_argument('--salt', help='Salt/IV (base64 encoded)')
    parser.add_argument('--generate-key', action='store_true', help='Generate a new random key and exit')
    
    args = parser.parse_args()
    
    if args.generate_key:
        key = os.urandom(16)  # 128-bit key
        print(f"Generated key (base64): {base64.b64encode(key).decode()}")
        print(f"Generated salt (base64): {base64.b64encode(generate_salt(8)).decode()}")
        return
    
    # Interactive mode if no arguments provided
    if not any(vars(args).values()):
        interactive_mode()
        return
    
    # Process command-line arguments
    key = None
    salt = None
    
    # Get or generate key
    if args.key:
        try:
            key = base64.b64decode(args.key)
        except Exception as e:
            print(f"Error decoding key: {e}")
            return
    else:
        key = DEFAULT_KEY
    
    # Get or generate salt
    if args.salt:
        try:
            salt = base64.b64decode(args.salt)
        except Exception as e:
            print(f"Error decoding salt: {e}")
            return
    else:
        salt = generate_salt(8)
    
    # Get input data
    input_data = None
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, 'rb') as f:
                input_data = f.read()
        else:
            input_data = args.input.encode('utf-8')
    else:
        input_data = input("Enter text to process: ").encode('utf-8')
    
    # Perform the requested action
    if args.mode == 'test':
        from present_cipher import measure_performance
        measure_performance()
        return
    
    if not args.mode or not args.action:
        print("Error: Both --mode and --action are required")
        return
    
    try:
        if args.mode == 'cfb':
            if args.action in ['encrypt', 'both']:
                ciphertext, used_salt = cfb_encrypt(input_data, key, salt)
                output_data = base64.b64encode(ciphertext).decode('utf-8')
                print(f"\nCFB Encryption successful!")
                print(f"Salt (base64): {base64.b64encode(used_salt).decode('utf-8')}")
                print(f"Ciphertext (base64): {output_data}")
                
                if args.output:
                    with open(args.output, 'wb') as f:
                        f.write(ciphertext)
                    print(f"Ciphertext saved to {args.output}")
            
            if args.action in ['decrypt', 'both'] and args.action != 'both':
                try:
                    if args.action == 'both':
                        # Use the ciphertext from encryption
                        plaintext = cfb_decrypt(ciphertext, key, used_salt)
                    else:
                        # For decryption only, we need to read the ciphertext
                        plaintext = cfb_decrypt(input_data, key, salt)
                    
                    print(f"\nCFB Decryption successful!")
                    try:
                        # Try to decode as text
                        print(f"Decrypted text: {plaintext.decode('utf-8')}")
                    except UnicodeDecodeError:
                        # If not text, show as hex
                        print(f"Decrypted data (hex): {plaintext.hex()}")
                    
                    if args.output and args.action != 'both':
                        with open(args.output, 'wb') as f:
                            f.write(plaintext)
                        print(f"Decrypted data saved to {args.output}")
                except Exception as e:
                    print(f"Decryption failed: {e}")
        
        elif args.mode == 'cbc':
            if args.action in ['encrypt', 'both']:
                ciphertext, used_salt = cbc_encrypt(input_data, key, salt)
                output_data = base64.b64encode(ciphertext).decode('utf-8')
                print(f"\nCBC Encryption successful!")
                print(f"Salt (base64): {base64.b64encode(used_salt).decode('utf-8')}")
                print(f"Ciphertext (base64): {output_data}")
                
                if args.output:
                    with open(args.output, 'wb') as f:
                        f.write(ciphertext)
                    print(f"Ciphertext saved to {args.output}")
            
            if args.action in ['decrypt', 'both'] and args.action != 'both':
                try:
                    if args.action == 'both':
                        # Use the ciphertext from encryption
                        plaintext = cbc_decrypt(ciphertext, key, used_salt)
                    else:
                        # For decryption only, we need to read the ciphertext
                        plaintext = cbc_decrypt(input_data, key, salt)
                    
                    print(f"\nCBC Decryption successful!")
                    try:
                        # Try to decode as text
                        print(f"Decrypted text: {plaintext.decode('utf-8')}")
                    except UnicodeDecodeError:
                        # If not text, show as hex
                        print(f"Decrypted data (hex): {plaintext.hex()}")
                    
                    if args.output and args.action != 'both':
                        with open(args.output, 'wb') as f:
                            f.write(plaintext)
                        print(f"Decrypted data saved to {args.output}")
                except Exception as e:
                    print(f"Decryption failed: {e}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        if args.action == 'both':
            print("Note: The 'both' action may not work with file inputs. Try encrypt and decrypt separately.")


def interactive_mode():
    """Run the application in interactive mode"""
    print("=== Salted Cipher Modes ===")
    print("This application demonstrates CFB and CBC encryption modes with salt/IV.")
    
    while True:
        print("\nMain Menu:")
        print("1. Encrypt data")
        print("2. Decrypt data")
        print("3. Generate new key and salt")
        print("4. Run performance tests")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            encrypt_menu()
        elif choice == '2':
            decrypt_menu()
        elif choice == '3':
            key = os.urandom(16)
            salt = generate_salt(8)
            print(f"\nNew key (base64): {base64.b64encode(key).decode()}")
            print(f"New salt (base64): {base64.b64encode(salt).decode()}")
            print("\nNote: In a real application, store these securely!")
        elif choice == '4':
            print("\nRunning performance tests...")
            from present_cipher import measure_performance
            measure_performance()
            print("\nPerformance test completed. Check 'encryption_performance.png' for results.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def encrypt_menu():
    """Interactive menu for encryption"""
    print("\n=== Encryption Menu ===")
    
    # Get encryption mode
    while True:
        mode = input("Select mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get input method
    print("\nInput options:")
    print("1. Enter text directly")
    print("2. Read from file")
    input_choice = input("Choose input method (1-2): ").strip()
    
    if input_choice == '1':
        input_data = input("\nEnter text to encrypt: ").encode('utf-8')
    elif input_choice == '2':
        file_path = input("Enter file path: ").strip()
        try:
            with open(file_path, 'rb') as f:
                input_data = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Invalid choice. Returning to main menu.")
        return
    
    # Get or generate key
    key_choice = input("Use default key? (y/n): ").lower().strip()
    if key_choice == 'n':
        key_b64 = input("Enter key (base64 encoded): ").strip()
        try:
            key = base64.b64decode(key_b64)
        except Exception as e:
            print(f"Error decoding key: {e}")
            return
    else:
        key = DEFAULT_KEY
    
    # Get or generate salt
    salt_choice = input("Generate new salt? (y/n): ").lower().strip()
    if salt_choice == 'n':
        salt_b64 = input("Enter salt (base64 encoded, 8 bytes): ").strip()
        try:
            salt = base64.b64decode(salt_b64)
            if len(salt) != 8:
                print("Salt must be 8 bytes (64 bits). Using random salt instead.")
                salt = generate_salt(8)
        except Exception as e:
            print(f"Error decoding salt: {e}. Using random salt.")
            salt = generate_salt(8)
    else:
        salt = generate_salt(8)
    
    # Perform encryption
    try:
        if mode == 'cfb':
            ciphertext, used_salt = cfb_encrypt(input_data, key, salt)
            mode_name = "CFB"
        else:  # cbc
            ciphertext, used_salt = cbc_encrypt(input_data, key, salt)
            mode_name = "CBC"
        
        print(f"\n{mode_name} Encryption successful!")
        print(f"Salt (base64): {base64.b64encode(used_salt).decode('utf-8')}")
        
        # Show first 100 chars of ciphertext in base64
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        display_text = ciphertext_b64[:100] + ('...' if len(ciphertext_b64) > 100 else '')
        print(f"Ciphertext (base64, first 100 chars): {display_text}")
        
        # Save to file option
        save_choice = input("\nSave ciphertext to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            file_path = input("Enter output file path: ").strip()
            try:
                with open(file_path, 'wb') as f:
                    f.write(ciphertext)
                print(f"Ciphertext saved to {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
    
    except Exception as e:
        print(f"Encryption failed: {e}")


def decrypt_menu():
    """Interactive menu for decryption"""
    print("\n=== Decryption Menu ===")
    
    # Get decryption mode
    while True:
        mode = input("Select mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get input method
    print("\nInput options:")
    print("1. Enter ciphertext as base64")
    print("2. Read from file")
    input_choice = input("Choose input method (1-2): ").strip()
    
    if input_choice == '1':
        ciphertext_b64 = input("\nEnter ciphertext (base64): ").strip()
        try:
            ciphertext = base64.b64decode(ciphertext_b64)
        except Exception as e:
            print(f"Error decoding base64: {e}")
            return
    elif input_choice == '2':
        file_path = input("Enter file path: ").strip()
        try:
            with open(file_path, 'rb') as f:
                ciphertext = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Invalid choice. Returning to main menu.")
        return
    
    # Get key
    key_choice = input("Use default key? (y/n): ").lower().strip()
    if key_choice == 'n':
        key_b64 = input("Enter key (base64 encoded): ").strip()
        try:
            key = base64.b64decode(key_b64)
        except Exception as e:
            print(f"Error decoding key: {e}")
            return
    else:
        key = DEFAULT_KEY
    
    # Get salt
    salt_b64 = input("Enter salt (base64 encoded, 8 bytes): ").strip()
    try:
        salt = base64.b64decode(salt_b64)
        if len(salt) != 8:
            print("Error: Salt must be 8 bytes (64 bits).")
            return
    except Exception as e:
        print(f"Error decoding salt: {e}")
        return
    
    # Perform decryption
    try:
        if mode == 'cfb':
            plaintext = cfb_decrypt(ciphertext, key, salt)
            mode_name = "CFB"
        else:  # cbc
            plaintext = cbc_decrypt(ciphertext, key, salt)
            mode_name = "CBC"
        
        print(f"\n{mode_name} Decryption successful!")
        
        # Try to decode as text, otherwise show hex
        try:
            plaintext_str = plaintext.decode('utf-8')
            print("Decrypted text:")
            print("-" * 50)
            print(plaintext_str)
            print("-" * 50)
        except UnicodeDecodeError:
            print("Decrypted data (hex):")
            print("-" * 50)
            print(plaintext.hex())
            print("-" * 50)
        
        # Save to file option
        save_choice = input("\nSave decrypted data to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            file_path = input("Enter output file path: ").strip()
            try:
                with open(file_path, 'wb') as f:
                    f.write(plaintext)
                print(f"Decrypted data saved to {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
    
    except Exception as e:
        print(f"Decryption failed: {e}")
        print("Possible reasons: Incorrect key, incorrect salt, or corrupted ciphertext.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

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
    print("\n" + "="*60)
    print("     SALTED CIPHER MODES - CFB & CBC ENCRYPTION")
    print("="*60)
    print("This application demonstrates secure encryption with salt/IV.")
    
    # Store key and salt for reuse in the session
    session_key = os.urandom(16)
    session_salt = generate_salt(8)
    
    print(f"\nSession Key (base64): {base64.b64encode(session_key).decode()}")
    print(f"Session Salt (base64): {base64.b64encode(session_salt).decode()}")
    print("\nYou can use these for multiple operations in this session.")
    
    while True:
        print("\n" + "-"*60)
        print("MAIN MENU:")
        print("-"*60)
        print("1. Encrypt text")
        print("2. Decrypt text")
        print("3. Encrypt file")
        print("4. Decrypt file")
        print("5. Generate new key and salt")
        print("6. Run performance tests")
        print("7. Run comprehensive cipher analysis")
        print("8. Exit")
        print("-"*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            encrypt_text_menu(session_key, session_salt)
        elif choice == '2':
            decrypt_text_menu(session_key, session_salt)
        elif choice == '3':
            encrypt_file_menu(session_key, session_salt)
        elif choice == '4':
            decrypt_file_menu(session_key, session_salt)
        elif choice == '5':
            session_key = os.urandom(16)
            session_salt = generate_salt(8)
            print(f"\n✓ New key (base64): {base64.b64encode(session_key).decode()}")
            print(f"✓ New salt (base64): {base64.b64encode(session_salt).decode()}")
        elif choice == '6':
            print("\nRunning performance tests...")
            from present_cipher import measure_performance
            measure_performance()
            print("\n✓ Performance test completed. Check 'encryption_performance.png' for results.")
        elif choice == '7':
            print("\nRunning comprehensive cipher analysis...")
            print("This will compare SaltedCipher with AES, DES, CFB, and CBC modes.")
            print("This may take a few minutes...\n")
            try:
                from performance_analysis import CipherBenchmark
                benchmark = CipherBenchmark()
                benchmark.run_benchmarks()
                benchmark.generate_comparison_table()
                benchmark.generate_graphs()
                benchmark.generate_detailed_report()
                print("\n✓ Analysis complete! Generated files:")
                print("  • comprehensive_cipher_analysis.png")
                print("  • cipher_comparison.csv")
                print("  • cipher_analysis_report.txt")
                print("  • ANALYSIS_SUMMARY.md")
            except ImportError:
                print("✗ performance_analysis module not found. Please ensure it's in the same directory.")
            except Exception as e:
                print(f"✗ Error running analysis: {e}")
        elif choice == '8':
            print("\nGoodbye!")
            break
        else:
            print("✗ Invalid choice. Please try again.")


def encrypt_text_menu(key, salt):
    """Encrypt text with improved UI"""
    print("\n" + "="*60)
    print("ENCRYPT TEXT")
    print("="*60)
    
    # Get encryption mode
    while True:
        mode = input("\nSelect mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("✗ Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get text to encrypt
    plaintext = input("\nEnter text to encrypt: ").strip()
    if not plaintext:
        print("✗ No text provided.")
        return
    
    input_data = plaintext.encode('utf-8')
    
    # Perform encryption
    try:
        if mode == 'cfb':
            ciphertext, used_salt = cfb_encrypt(input_data, key, salt)
            mode_name = "CFB"
        else:  # cbc
            ciphertext, used_salt = cbc_encrypt(input_data, key, salt)
            mode_name = "CBC"
        
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        salt_b64 = base64.b64encode(used_salt).decode('utf-8')
        
        print("\n" + "="*60)
        print(f"✓ {mode_name} ENCRYPTION SUCCESSFUL")
        print("="*60)
        print(f"\nOriginal text: {plaintext}")
        print(f"\nSalt (base64):\n{salt_b64}")
        print(f"\nCiphertext (base64):\n{ciphertext_b64}")
        print("\n" + "="*60)
        
        # Save to file option
        save_choice = input("\nSave ciphertext to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            file_path = input("Enter output file path: ").strip()
            try:
                with open(file_path, 'wb') as f:
                    f.write(ciphertext)
                print(f"✓ Ciphertext saved to {file_path}")
            except Exception as e:
                print(f"✗ Error saving file: {e}")
    
    except Exception as e:
        print(f"✗ Encryption failed: {e}")


def encrypt_file_menu(key, salt):
    """Encrypt file with improved UI"""
    print("\n" + "="*60)
    print("ENCRYPT FILE")
    print("="*60)
    
    # Get encryption mode
    while True:
        mode = input("\nSelect mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("✗ Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get file path
    file_path = input("\nEnter file path to encrypt: ").strip()
    try:
        with open(file_path, 'rb') as f:
            input_data = f.read()
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    # Perform encryption
    try:
        if mode == 'cfb':
            ciphertext, used_salt = cfb_encrypt(input_data, key, salt)
            mode_name = "CFB"
        else:  # cbc
            ciphertext, used_salt = cbc_encrypt(input_data, key, salt)
            mode_name = "CBC"
        
        salt_b64 = base64.b64encode(used_salt).decode('utf-8')
        
        print("\n" + "="*60)
        print(f"✓ {mode_name} ENCRYPTION SUCCESSFUL")
        print("="*60)
        print(f"\nFile: {file_path}")
        print(f"File size: {len(input_data)} bytes")
        print(f"Encrypted size: {len(ciphertext)} bytes")
        print(f"\nSalt (base64):\n{salt_b64}")
        print("\n" + "="*60)
        
        # Save encrypted file
        output_path = input("\nEnter output file path: ").strip()
        try:
            with open(output_path, 'wb') as f:
                f.write(ciphertext)
            print(f"✓ Encrypted file saved to {output_path}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")
    
    except Exception as e:
        print(f"✗ Encryption failed: {e}")


def decrypt_text_menu(key, salt):
    """Decrypt text with improved UI"""
    print("\n" + "="*60)
    print("DECRYPT TEXT")
    print("="*60)
    
    # Get decryption mode
    while True:
        mode = input("\nSelect mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("✗ Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get ciphertext
    ciphertext_b64 = input("\nEnter ciphertext (base64): ").strip()
    if not ciphertext_b64:
        print("✗ No ciphertext provided.")
        return
    
    try:
        ciphertext = base64.b64decode(ciphertext_b64)
    except Exception as e:
        print(f"✗ Error decoding base64: {e}")
        return
    
    # Perform decryption
    try:
        if mode == 'cfb':
            plaintext = cfb_decrypt(ciphertext, key, salt)
            mode_name = "CFB"
        else:  # cbc
            plaintext = cbc_decrypt(ciphertext, key, salt)
            mode_name = "CBC"
        
        print("\n" + "="*60)
        print(f"✓ {mode_name} DECRYPTION SUCCESSFUL")
        print("="*60)
        
        # Try to decode as text, otherwise show hex
        try:
            plaintext_str = plaintext.decode('utf-8')
            print(f"\nDecrypted text:\n{plaintext_str}")
        except UnicodeDecodeError:
            print(f"\nDecrypted data (hex):\n{plaintext.hex()}")
        
        print("\n" + "="*60)
        
        # Save to file option
        save_choice = input("\nSave decrypted data to file? (y/n): ").lower().strip()
        if save_choice == 'y':
            file_path = input("Enter output file path: ").strip()
            try:
                with open(file_path, 'wb') as f:
                    f.write(plaintext)
                print(f"✓ Decrypted data saved to {file_path}")
            except Exception as e:
                print(f"✗ Error saving file: {e}")
    
    except Exception as e:
        print(f"✗ Decryption failed: {e}")
        print("Possible reasons: Incorrect key, incorrect salt, or corrupted ciphertext.")


def decrypt_file_menu(key, salt):
    """Decrypt file with improved UI"""
    print("\n" + "="*60)
    print("DECRYPT FILE")
    print("="*60)
    
    # Get decryption mode
    while True:
        mode = input("\nSelect mode (cfb/cbc): ").lower().strip()
        if mode in ['cfb', 'cbc']:
            break
        print("✗ Invalid mode. Please enter 'cfb' or 'cbc'.")
    
    # Get file path
    file_path = input("\nEnter encrypted file path: ").strip()
    try:
        with open(file_path, 'rb') as f:
            ciphertext = f.read()
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    # Perform decryption
    try:
        if mode == 'cfb':
            plaintext = cfb_decrypt(ciphertext, key, salt)
            mode_name = "CFB"
        else:  # cbc
            plaintext = cbc_decrypt(ciphertext, key, salt)
            mode_name = "CBC"
        
        print("\n" + "="*60)
        print(f"✓ {mode_name} DECRYPTION SUCCESSFUL")
        print("="*60)
        print(f"\nFile: {file_path}")
        print(f"Encrypted size: {len(ciphertext)} bytes")
        print(f"Decrypted size: {len(plaintext)} bytes")
        print("\n" + "="*60)
        
        # Save decrypted file
        output_path = input("\nEnter output file path: ").strip()
        try:
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            print(f"✓ Decrypted file saved to {output_path}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")
    
    except Exception as e:
        print(f"✗ Decryption failed: {e}")
        print("Possible reasons: Incorrect key, incorrect salt, or corrupted ciphertext.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

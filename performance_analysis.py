"""
Comprehensive Performance Analysis: SaltedCipher vs AES, DES, CFB, CBC
Generates detailed graphs and comparison tables
"""

import os
import sys
import time
import timeit
import random
import string
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad, unpad
from present_cipher import cfb_encrypt, cfb_decrypt, cbc_encrypt, cbc_decrypt, generate_salt


class CipherBenchmark:
    """Benchmark different cipher modes and algorithms"""
    
    def __init__(self):
        self.results = {}
        self.test_sizes = [8, 64, 512, 4096, 32768, 262144]  # Up to 256KB
        self.key_16 = os.urandom(16)  # 128-bit key
        self.key_24 = os.urandom(24)  # 192-bit key (for 3DES)
        self.salt = os.urandom(8)  # 64-bit salt/IV
        self.iv_16 = os.urandom(16)  # 128-bit IV for AES
        
    def generate_test_data(self, size):
        """Generate random test data"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()
    
    def benchmark_aes_ecb_encrypt(self, data):
        """Benchmark AES ECB encryption"""
        cipher = AES.new(self.key_16, AES.MODE_ECB)
        padded = pad(data, 16)
        return cipher.encrypt(padded)
    
    def benchmark_aes_ecb_decrypt(self, ciphertext):
        """Benchmark AES ECB decryption"""
        cipher = AES.new(self.key_16, AES.MODE_ECB)
        return unpad(cipher.decrypt(ciphertext), 16)
    
    def benchmark_aes_cbc_encrypt(self, data):
        """Benchmark AES CBC encryption"""
        cipher = AES.new(self.key_16, AES.MODE_CBC, self.iv_16)
        padded = pad(data, 16)
        return cipher.encrypt(padded)
    
    def benchmark_aes_cbc_decrypt(self, ciphertext):
        """Benchmark AES CBC decryption"""
        cipher = AES.new(self.key_16, AES.MODE_CBC, self.iv_16)
        return unpad(cipher.decrypt(ciphertext), 16)
    
    def benchmark_aes_cfb_encrypt(self, data):
        """Benchmark AES CFB encryption"""
        cipher = AES.new(self.key_16, AES.MODE_CFB, self.iv_16)
        return cipher.encrypt(data)
    
    def benchmark_aes_cfb_decrypt(self, ciphertext):
        """Benchmark AES CFB decryption"""
        cipher = AES.new(self.key_16, AES.MODE_CFB, self.iv_16)
        return cipher.decrypt(ciphertext)
    
    def benchmark_des3_ecb_encrypt(self, data):
        """Benchmark 3DES ECB encryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_ECB)
        padded = pad(data, 8)
        return cipher.encrypt(padded)
    
    def benchmark_des3_ecb_decrypt(self, ciphertext):
        """Benchmark 3DES ECB decryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_ECB)
        return unpad(cipher.decrypt(ciphertext), 8)
    
    def benchmark_des3_cbc_encrypt(self, data):
        """Benchmark 3DES CBC encryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_CBC, self.salt)
        padded = pad(data, 8)
        return cipher.encrypt(padded)
    
    def benchmark_des3_cbc_decrypt(self, ciphertext):
        """Benchmark 3DES CBC decryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_CBC, self.salt)
        return unpad(cipher.decrypt(ciphertext), 8)
    
    def benchmark_des3_cfb_encrypt(self, data):
        """Benchmark 3DES CFB encryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_CFB, self.salt)
        return cipher.encrypt(data)
    
    def benchmark_des3_cfb_decrypt(self, ciphertext):
        """Benchmark 3DES CFB decryption"""
        cipher = DES3.new(self.key_24, DES3.MODE_CFB, self.salt)
        return cipher.decrypt(ciphertext)
    
    def benchmark_salted_cfb_encrypt(self, data):
        """Benchmark SaltedCipher CFB encryption"""
        ciphertext, _ = cfb_encrypt(data, self.key_16, self.salt)
        return ciphertext
    
    def benchmark_salted_cfb_decrypt(self, ciphertext):
        """Benchmark SaltedCipher CFB decryption"""
        return cfb_decrypt(ciphertext, self.key_16, self.salt)
    
    def benchmark_salted_cbc_encrypt(self, data):
        """Benchmark SaltedCipher CBC encryption"""
        ciphertext, _ = cbc_encrypt(data, self.key_16, self.salt)
        return ciphertext
    
    def benchmark_salted_cbc_decrypt(self, ciphertext):
        """Benchmark SaltedCipher CBC decryption"""
        return cbc_decrypt(ciphertext, self.key_16, self.salt)
    
    def run_benchmarks(self):
        """Run all benchmarks"""
        benchmarks = {
            'AES-ECB': {
                'encrypt': self.benchmark_aes_ecb_encrypt,
                'decrypt': self.benchmark_aes_ecb_decrypt,
            },
            'AES-CBC': {
                'encrypt': self.benchmark_aes_cbc_encrypt,
                'decrypt': self.benchmark_aes_cbc_decrypt,
            },
            'AES-CFB': {
                'encrypt': self.benchmark_aes_cfb_encrypt,
                'decrypt': self.benchmark_aes_cfb_decrypt,
            },
            '3DES-ECB': {
                'encrypt': self.benchmark_des3_ecb_encrypt,
                'decrypt': self.benchmark_des3_ecb_decrypt,
            },
            '3DES-CBC': {
                'encrypt': self.benchmark_des3_cbc_encrypt,
                'decrypt': self.benchmark_des3_cbc_decrypt,
            },
            '3DES-CFB': {
                'encrypt': self.benchmark_des3_cfb_encrypt,
                'decrypt': self.benchmark_des3_cfb_decrypt,
            },
            'SaltedCipher-CFB': {
                'encrypt': self.benchmark_salted_cfb_encrypt,
                'decrypt': self.benchmark_salted_cfb_decrypt,
            },
            'SaltedCipher-CBC': {
                'encrypt': self.benchmark_salted_cbc_encrypt,
                'decrypt': self.benchmark_salted_cbc_decrypt,
            },
        }
        
        print("\n" + "="*80)
        print("COMPREHENSIVE CIPHER PERFORMANCE BENCHMARK")
        print("="*80)
        
        for cipher_name, cipher_funcs in benchmarks.items():
            print(f"\nBenchmarking {cipher_name}...")
            self.results[cipher_name] = {
                'encrypt': [],
                'decrypt': [],
                'throughput': []
            }
            
            for size in self.test_sizes:
                data = self.generate_test_data(size)
                
                try:
                    # Benchmark encryption
                    enc_time = timeit.timeit(
                        lambda: cipher_funcs['encrypt'](data),
                        number=50
                    ) / 50
                    
                    # Get ciphertext for decryption
                    ciphertext = cipher_funcs['encrypt'](data)
                    
                    # Benchmark decryption
                    dec_time = timeit.timeit(
                        lambda: cipher_funcs['decrypt'](ciphertext),
                        number=50
                    ) / 50
                    
                    # Calculate throughput (MB/s)
                    throughput_enc = (size / (1024 * 1024)) / enc_time if enc_time > 0 else 0
                    throughput_dec = (size / (1024 * 1024)) / dec_time if dec_time > 0 else 0
                    throughput_avg = (throughput_enc + throughput_dec) / 2
                    
                    self.results[cipher_name]['encrypt'].append((size, enc_time * 1000))
                    self.results[cipher_name]['decrypt'].append((size, dec_time * 1000))
                    self.results[cipher_name]['throughput'].append((size, throughput_avg))
                    
                    print(f"  Size: {size:7d} bytes | Enc: {enc_time*1000:8.4f}ms | Dec: {dec_time*1000:8.4f}ms | Throughput: {throughput_avg:8.2f} MB/s")
                
                except Exception as e:
                    print(f"  Size: {size:7d} bytes | Error: {str(e)}")
    
    def generate_comparison_table(self):
        """Generate a comprehensive comparison table"""
        print("\n" + "="*80)
        print("PERFORMANCE COMPARISON TABLE (at 32KB data size)")
        print("="*80)
        
        # Find 32KB results
        target_size = 32768
        
        data = []
        for cipher_name, metrics in self.results.items():
            enc_results = metrics['encrypt']
            dec_results = metrics['decrypt']
            throughput_results = metrics['throughput']
            
            # Find closest size to target
            enc_time = next((t for s, t in enc_results if s == target_size), None)
            dec_time = next((t for s, t in dec_results if s == target_size), None)
            throughput = next((t for s, t in throughput_results if s == target_size), None)
            
            if enc_time and dec_time and throughput:
                data.append({
                    'Cipher': cipher_name,
                    'Encrypt (ms)': f"{enc_time:.4f}",
                    'Decrypt (ms)': f"{dec_time:.4f}",
                    'Total (ms)': f"{enc_time + dec_time:.4f}",
                    'Throughput (MB/s)': f"{throughput:.2f}"
                })
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        
        # Save to CSV
        df.to_csv('cipher_comparison.csv', index=False)
        print("\n✓ Comparison table saved to 'cipher_comparison.csv'")
        
        return df
    
    def generate_graphs(self):
        """Generate comprehensive comparison graphs"""
        fig = plt.figure(figsize=(16, 12))
        
        # Extract data for plotting
        ciphers = list(self.results.keys())
        colors = plt.cm.tab10(np.linspace(0, 1, len(ciphers)))
        
        # 1. Encryption Time Comparison
        ax1 = plt.subplot(2, 3, 1)
        for idx, cipher_name in enumerate(ciphers):
            enc_data = self.results[cipher_name]['encrypt']
            sizes = [x[0] for x in enc_data]
            times = [x[1] for x in enc_data]
            ax1.plot(sizes, times, marker='o', label=cipher_name, color=colors[idx], linewidth=2)
        
        ax1.set_xlabel('Data Size (bytes)', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Time (ms)', fontsize=10, fontweight='bold')
        ax1.set_title('Encryption Time Comparison', fontsize=12, fontweight='bold')
        ax1.set_xscale('log')
        ax1.legend(fontsize=8, loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 2. Decryption Time Comparison
        ax2 = plt.subplot(2, 3, 2)
        for idx, cipher_name in enumerate(ciphers):
            dec_data = self.results[cipher_name]['decrypt']
            sizes = [x[0] for x in dec_data]
            times = [x[1] for x in dec_data]
            ax2.plot(sizes, times, marker='s', label=cipher_name, color=colors[idx], linewidth=2)
        
        ax2.set_xlabel('Data Size (bytes)', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Time (ms)', fontsize=10, fontweight='bold')
        ax2.set_title('Decryption Time Comparison', fontsize=12, fontweight='bold')
        ax2.set_xscale('log')
        ax2.legend(fontsize=8, loc='upper left')
        ax2.grid(True, alpha=0.3)
        
        # 3. Throughput Comparison
        ax3 = plt.subplot(2, 3, 3)
        for idx, cipher_name in enumerate(ciphers):
            throughput_data = self.results[cipher_name]['throughput']
            sizes = [x[0] for x in throughput_data]
            throughputs = [x[1] for x in throughput_data]
            ax3.plot(sizes, throughputs, marker='^', label=cipher_name, color=colors[idx], linewidth=2)
        
        ax3.set_xlabel('Data Size (bytes)', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Throughput (MB/s)', fontsize=10, fontweight='bold')
        ax3.set_title('Throughput Comparison', fontsize=12, fontweight='bold')
        ax3.set_xscale('log')
        ax3.legend(fontsize=8, loc='best')
        ax3.grid(True, alpha=0.3)
        
        # 4. Encryption Speed at 32KB
        ax4 = plt.subplot(2, 3, 4)
        target_size = 32768
        enc_times_32k = []
        cipher_labels = []
        
        for cipher_name in ciphers:
            enc_data = self.results[cipher_name]['encrypt']
            enc_time = next((t for s, t in enc_data if s == target_size), None)
            if enc_time:
                enc_times_32k.append(enc_time)
                cipher_labels.append(cipher_name)
        
        bars = ax4.bar(range(len(cipher_labels)), enc_times_32k, color=colors[:len(cipher_labels)])
        ax4.set_ylabel('Time (ms)', fontsize=10, fontweight='bold')
        ax4.set_title('Encryption Time at 32KB', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(len(cipher_labels)))
        ax4.set_xticklabels(cipher_labels, rotation=45, ha='right', fontsize=8)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=8)
        
        # 5. Decryption Speed at 32KB
        ax5 = plt.subplot(2, 3, 5)
        dec_times_32k = []
        
        for cipher_name in ciphers:
            dec_data = self.results[cipher_name]['decrypt']
            dec_time = next((t for s, t in dec_data if s == target_size), None)
            if dec_time:
                dec_times_32k.append(dec_time)
        
        bars = ax5.bar(range(len(cipher_labels)), dec_times_32k, color=colors[:len(cipher_labels)])
        ax5.set_ylabel('Time (ms)', fontsize=10, fontweight='bold')
        ax5.set_title('Decryption Time at 32KB', fontsize=12, fontweight='bold')
        ax5.set_xticks(range(len(cipher_labels)))
        ax5.set_xticklabels(cipher_labels, rotation=45, ha='right', fontsize=8)
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=8)
        
        # 6. Throughput at 32KB
        ax6 = plt.subplot(2, 3, 6)
        throughputs_32k = []
        
        for cipher_name in ciphers:
            throughput_data = self.results[cipher_name]['throughput']
            throughput = next((t for s, t in throughput_data if s == target_size), None)
            if throughput:
                throughputs_32k.append(throughput)
        
        bars = ax6.bar(range(len(cipher_labels)), throughputs_32k, color=colors[:len(cipher_labels)])
        ax6.set_ylabel('Throughput (MB/s)', fontsize=10, fontweight='bold')
        ax6.set_title('Throughput at 32KB', fontsize=12, fontweight='bold')
        ax6.set_xticks(range(len(cipher_labels)))
        ax6.set_xticklabels(cipher_labels, rotation=45, ha='right', fontsize=8)
        ax6.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('comprehensive_cipher_analysis.png', dpi=300, bbox_inches='tight')
        print("\n✓ Comprehensive analysis graph saved as 'comprehensive_cipher_analysis.png'")
        plt.close()
    
    def generate_detailed_report(self):
        """Generate a detailed text report"""
        report = []
        report.append("="*80)
        report.append("COMPREHENSIVE CIPHER PERFORMANCE ANALYSIS REPORT")
        report.append("="*80)
        report.append("")
        
        report.append("TESTED CIPHERS:")
        report.append("-" * 80)
        report.append("1. AES-ECB (Advanced Encryption Standard - Electronic Codebook)")
        report.append("2. AES-CBC (Advanced Encryption Standard - Cipher Block Chaining)")
        report.append("3. AES-CFB (Advanced Encryption Standard - Cipher Feedback)")
        report.append("4. 3DES-ECB (Triple DES - Electronic Codebook)")
        report.append("5. 3DES-CBC (Triple DES - Cipher Block Chaining)")
        report.append("6. 3DES-CFB (Triple DES - Cipher Feedback)")
        report.append("7. SaltedCipher-CFB (Custom implementation with salt - CFB mode)")
        report.append("8. SaltedCipher-CBC (Custom implementation with salt - CBC mode)")
        report.append("")
        
        report.append("TEST PARAMETERS:")
        report.append("-" * 80)
        report.append(f"Data Sizes: {self.test_sizes}")
        report.append(f"AES Key Size: 128 bits")
        report.append(f"3DES Key Size: 192 bits")
        report.append(f"SaltedCipher Key Size: 128 bits")
        report.append(f"IV/Salt Size: 64-128 bits")
        report.append(f"Iterations per test: 50")
        report.append("")
        
        report.append("PERFORMANCE SUMMARY (at 32KB):")
        report.append("-" * 80)
        
        target_size = 32768
        summary_data = []
        
        for cipher_name, metrics in self.results.items():
            enc_results = metrics['encrypt']
            dec_results = metrics['decrypt']
            throughput_results = metrics['throughput']
            
            enc_time = next((t for s, t in enc_results if s == target_size), None)
            dec_time = next((t for s, t in dec_results if s == target_size), None)
            throughput = next((t for s, t in throughput_results if s == target_size), None)
            
            if enc_time and dec_time and throughput:
                summary_data.append({
                    'cipher': cipher_name,
                    'enc': enc_time,
                    'dec': dec_time,
                    'throughput': throughput
                })
                report.append(f"{cipher_name:20s} | Enc: {enc_time:8.4f}ms | Dec: {dec_time:8.4f}ms | Throughput: {throughput:8.2f} MB/s")
        
        report.append("")
        
        # Find best performers
        if summary_data:
            fastest_enc = min(summary_data, key=lambda x: x['enc'])
            fastest_dec = min(summary_data, key=lambda x: x['dec'])
            best_throughput = max(summary_data, key=lambda x: x['throughput'])
            
            report.append("BEST PERFORMERS:")
            report.append("-" * 80)
            report.append(f"Fastest Encryption:  {fastest_enc['cipher']:20s} ({fastest_enc['enc']:.4f}ms)")
            report.append(f"Fastest Decryption:  {fastest_dec['cipher']:20s} ({fastest_dec['dec']:.4f}ms)")
            report.append(f"Best Throughput:     {best_throughput['cipher']:20s} ({best_throughput['throughput']:.2f} MB/s)")
            report.append("")
        
        report.append("ANALYSIS & RECOMMENDATIONS:")
        report.append("-" * 80)
        report.append("• AES is significantly faster than 3DES due to modern hardware acceleration")
        report.append("• AES-ECB is fastest but NOT recommended for security (deterministic)")
        report.append("• AES-CBC and AES-CFB provide good security with excellent performance")
        report.append("• 3DES is slower but still secure for legacy systems")
        report.append("• SaltedCipher provides custom implementation with salt support")
        report.append("• CFB mode is stream cipher-like (no padding needed)")
        report.append("• CBC mode requires padding but offers better security properties")
        report.append("")
        
        report.append("SECURITY NOTES:")
        report.append("-" * 80)
        report.append("• ECB mode should NOT be used for sensitive data (deterministic)")
        report.append("• CBC and CFB modes are secure when used correctly")
        report.append("• Always use random IVs/salts for each encryption")
        report.append("• AES-256 recommended for highly sensitive data")
        report.append("• 3DES is deprecated; use AES for new systems")
        report.append("")
        
        report_text = "\n".join(report)
        
        # Save report
        with open('cipher_analysis_report.txt', 'w') as f:
            f.write(report_text)
        
        print(report_text)
        print("\n✓ Detailed report saved to 'cipher_analysis_report.txt'")


def main():
    """Main function"""
    print("\nInitializing Comprehensive Cipher Benchmark...")
    
    benchmark = CipherBenchmark()
    benchmark.run_benchmarks()
    benchmark.generate_comparison_table()
    benchmark.generate_graphs()
    benchmark.generate_detailed_report()
    
    print("\n" + "="*80)
    print("BENCHMARK COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  • comprehensive_cipher_analysis.png - Detailed comparison graphs")
    print("  • cipher_comparison.csv - Performance metrics in CSV format")
    print("  • cipher_analysis_report.txt - Detailed analysis report")
    print("\n")


if __name__ == "__main__":
    main()

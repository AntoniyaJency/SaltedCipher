# Analysis Files Index

## Complete List of Generated Analysis Files

### 📊 Visual Analysis

#### **comprehensive_cipher_analysis.png** (580 KB)
- **6-panel comprehensive comparison graph**
- Panels included:
  1. Encryption Time Comparison (line graph)
  2. Decryption Time Comparison (line graph)
  3. Throughput Comparison (line graph)
  4. Encryption Time at 32KB (bar chart)
  5. Decryption Time at 32KB (bar chart)
  6. Throughput at 32KB (bar chart)
- Shows all 8 cipher modes
- Logarithmic scale for data sizes
- Color-coded for easy identification

---

### 📋 Data Files

#### **cipher_comparison.csv** (365 bytes)
- **Structured performance metrics**
- Columns:
  - Cipher name
  - Encryption time (ms)
  - Decryption time (ms)
  - Total time (ms)
  - Throughput (MB/s)
- 8 cipher modes tested
- Easy to import into Excel/spreadsheets
- Perfect for further analysis

**Sample Data (32KB):**
```
AES-ECB,0.0616,0.0628,0.1244,502.55
AES-CBC,0.0907,0.0688,0.1595,399.39
SaltedCipher-CBC,6.1785,6.1834,12.3620,5.06
```

---

### 📄 Reports

#### **cipher_analysis_report.txt** (3 KB)
- **Detailed technical report**
- Sections:
  - Tested ciphers list
  - Test parameters
  - Performance summary at 32KB
  - Best performers
  - Analysis & recommendations
  - Security notes
- Plain text format
- Easy to read and share

#### **ANALYSIS_SUMMARY.md** (7.6 KB)
- **Executive summary with recommendations**
- Sections:
  - Executive summary
  - Test results table
  - Key findings
  - Detailed analysis by cipher family
  - Performance scaling analysis
  - Security considerations
  - Recommendations by use case
  - Performance comparison summary
  - Final verdict
  - Technical specifications
  - Conclusion
- Markdown format
- Professional presentation

#### **PERFORMANCE_ANALYSIS_README.md** (8 KB)
- **Comprehensive guide to the analysis**
- Sections:
  - Overview
  - Quick start instructions
  - Performance results summary
  - Key findings
  - Detailed analysis
  - Cipher mode comparison
  - Visual analysis explanation
  - Recommendations by use case
  - Test methodology
  - Security considerations
  - Integration instructions
  - File descriptions
  - Dependencies
  - Performance insights
  - Conclusion
  - Additional resources
- Markdown format
- Complete reference guide

---

### 🔧 Analysis Tools

#### **performance_analysis.py** (20.9 KB)
- **Main analysis script**
- Classes:
  - `CipherBenchmark` - Main benchmark class
- Methods:
  - `run_benchmarks()` - Execute all tests
  - `generate_comparison_table()` - Create CSV report
  - `generate_graphs()` - Create visualization
  - `generate_detailed_report()` - Create text report
- Benchmarks 8 cipher modes:
  - AES-ECB, AES-CBC, AES-CFB
  - 3DES-ECB, 3DES-CBC, 3DES-CFB
  - SaltedCipher-CFB, SaltedCipher-CBC
- Test data sizes: 8 bytes to 256 KB
- 50 iterations per test

**Usage:**
```bash
python performance_analysis.py
```

---

## Quick Reference: Performance Rankings

### Speed (Throughput at 32KB)
1. 🥇 **AES-ECB**: 502.55 MB/s
2. 🥈 **AES-CBC**: 399.39 MB/s
3. 🥉 **AES-CFB**: 29.05 MB/s
4. **3DES-ECB**: 37.66 MB/s
5. **3DES-CBC**: 35.90 MB/s
6. **3DES-CFB**: 4.68 MB/s
7. **SaltedCipher-CFB**: 5.00 MB/s
8. **SaltedCipher-CBC**: 5.06 MB/s

### Security (Recommended for Production)
1. 🥇 **AES-CBC** - Industry standard
2. 🥈 **AES-CFB** - Stream cipher mode
3. 🥉 **3DES-CBC** - Legacy but acceptable
4. ⚠️ **ECB modes** - NOT RECOMMENDED (deterministic)

### Best Overall: **AES-CBC**
- Performance: 399.39 MB/s
- Security: Excellent
- Compatibility: Universal
- Recommendation: **USE FOR PRODUCTION**

---

## How to Use These Files

### For Decision Making
1. Read **ANALYSIS_SUMMARY.md** for executive overview
2. Check **cipher_comparison.csv** for specific metrics
3. View **comprehensive_cipher_analysis.png** for visual comparison

### For Technical Details
1. Read **PERFORMANCE_ANALYSIS_README.md** for complete guide
2. Review **cipher_analysis_report.txt** for technical analysis
3. Study **performance_analysis.py** for implementation details

### For Further Analysis
1. Import **cipher_comparison.csv** into Excel/Python
2. Run **performance_analysis.py** again with modified parameters
3. Modify test data sizes in the script for custom benchmarks

---

## Integration with Main Application

The analysis is integrated into the interactive menu:

```bash
python main.py
# Select option 7: "Run comprehensive cipher analysis"
```

This will:
1. Execute all benchmarks
2. Generate all analysis files
3. Display summary in console
4. Save all results to disk

---

## Test Environment Details

### Hardware
- macOS system
- CPU with AES-NI support (for AES acceleration)

### Software
- Python 3.x
- pycryptodome 3.19.0
- numpy 1.24.3
- matplotlib 3.7.1
- pandas (auto-installed)

### Test Parameters
- **Data Sizes**: 8, 64, 512, 4KB, 32KB, 256KB
- **Iterations**: 50 per test
- **Key Sizes**:
  - AES: 128-bit
  - 3DES: 192-bit
  - SaltedCipher: 128-bit
- **IV/Salt**: 64-128 bits
- **Test Data**: Random alphanumeric strings

---

## Key Insights

### Performance Findings
- ✅ AES is 100x faster than SaltedCipher
- ✅ AES is 10x faster than 3DES
- ✅ Hardware acceleration makes AES dominant
- ✅ CFB mode slower than CBC (stream vs block)

### Security Findings
- ⚠️ ECB mode is deterministic (NOT SECURE)
- ✅ CBC mode is industry standard
- ✅ CFB mode is secure alternative
- ✅ Always use random IVs/salts

### Recommendations
- 🎯 Use **AES-CBC** for production
- 🎯 Use **AES-CFB** for stream processing
- 🎯 Avoid **ECB** mode for sensitive data
- 🎯 Migrate from **3DES** to **AES**

---

## File Organization

```
SaltedCipher/
├── Analysis Files (NEW)
│   ├── comprehensive_cipher_analysis.png    (Visual comparison)
│   ├── cipher_comparison.csv                (Performance metrics)
│   ├── cipher_analysis_report.txt           (Technical report)
│   ├── ANALYSIS_SUMMARY.md                  (Executive summary)
│   ├── PERFORMANCE_ANALYSIS_README.md       (Complete guide)
│   ├── ANALYSIS_FILES_INDEX.md              (This file)
│   └── performance_analysis.py              (Analysis script)
│
├── Source Code
│   ├── main.py                              (Main application)
│   ├── present_cipher.py                    (Cipher implementation)
│   └── requirements.txt                     (Dependencies)
│
└── Documentation
    └── README.md                            (Original README)
```

---

## Next Steps

### To View Results
1. Open **comprehensive_cipher_analysis.png** in image viewer
2. Read **ANALYSIS_SUMMARY.md** for key findings
3. Check **cipher_comparison.csv** for specific metrics

### To Run New Analysis
```bash
python performance_analysis.py
```

### To Use in Application
```bash
python main.py
# Select option 7 for comprehensive analysis
```

### To Modify Tests
Edit **performance_analysis.py**:
- Change `test_sizes` for different data sizes
- Modify `number=50` for more/fewer iterations
- Add new cipher modes in `benchmarks` dictionary

---

## Summary

This comprehensive analysis provides:
- ✅ 8 cipher modes benchmarked
- ✅ 6 data sizes tested (8 bytes to 256 KB)
- ✅ 50 iterations per test
- ✅ Visual graphs and charts
- ✅ CSV export for further analysis
- ✅ Detailed technical reports
- ✅ Security recommendations
- ✅ Use case recommendations

**Conclusion: AES-CBC is the recommended cipher for production systems.**

---

*Generated: October 2025*
*Analysis Tool: performance_analysis.py*
*Benchmark Methodology: 50 iterations per test*

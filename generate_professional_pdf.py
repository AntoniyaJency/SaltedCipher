#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import csv

pdf_filename = "Cipher_Performance_Analysis_Report.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.6*inch, bottomMargin=0.6*inch)
elements = []
styles = getSampleStyleSheet()

# Professional, larger font sizes
title_style = ParagraphStyle('ResearchTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#000033'), spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=28)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=colors.HexColor('#003366'), spaceAfter=10, alignment=TA_CENTER, fontName='Helvetica-Oblique', leading=16)
author_style = ParagraphStyle('AuthorStyle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#333333'), spaceAfter=3, alignment=TA_CENTER, fontName='Helvetica-Bold')
affiliation_style = ParagraphStyle('AffiliationStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#555555'), spaceAfter=2, alignment=TA_CENTER, fontName='Helvetica')
abstract_style = ParagraphStyle('AbstractStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#000000'), spaceAfter=8, alignment=TA_JUSTIFY, fontName='Helvetica', leading=13)
heading_style = ParagraphStyle('ResearchHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#000033'), spaceAfter=8, spaceBefore=10, fontName='Helvetica-Bold', leading=16)
subheading_style = ParagraphStyle('ResearchSubHeading', parent=styles['Heading3'], fontSize=12, textColor=colors.HexColor('#003366'), spaceAfter=6, spaceBefore=6, fontName='Helvetica-Bold', leading=14)
normal_style = ParagraphStyle('ResearchNormal', parent=styles['Normal'], fontSize=11, alignment=TA_JUSTIFY, spaceAfter=6, leading=13, fontName='Helvetica')

# Title Page
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("COMPREHENSIVE CIPHER PERFORMANCE ANALYSIS", title_style))
elements.append(Paragraph("A Comparative Study of Encryption Algorithms and Operational Modes", subtitle_style))
elements.append(Spacer(1, 0.25*inch))

author_data = [[Paragraph("<b>ANTONIYA JENCY J</b>", author_style)],
               [Paragraph("3rd Year, Computer Science Engineering", affiliation_style)],
               [Paragraph("Loyola ICAM College of Engineering and Technology", affiliation_style)],
               [Paragraph("Tamil Nadu, India", affiliation_style)]]
author_table = Table(author_data, colWidths=[6*inch])
author_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f5ff')),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#003366'))]))
elements.append(author_table)
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("<b>ABSTRACT</b>", heading_style))
abstract_text = """This comprehensive research presents a detailed benchmarking study of eight encryption cipher modes, comparing their performance characteristics and security properties across multiple data sizes. The study encompasses modern cryptographic standards (AES), legacy systems (3DES), and custom implementations (SaltedCipher) in multiple operational modes (ECB, CBC, CFB).

Through rigorous testing with 50 iterations per benchmark across six data sizes (8 bytes to 256 KB), we demonstrate that AES-CBC achieves optimal performance (393.22 MB/s) while maintaining industry-standard security properties. The analysis reveals that AES is 100x faster than SaltedCipher and 10x faster than 3DES, primarily due to hardware acceleration (AES-NI) on modern processors.

Key findings include: (1) AES-CBC provides optimal balance of performance and security for production systems, (2) ECB mode is cryptographically unsuitable for sensitive data due to deterministic encryption, (3) 3DES is deprecated and should be migrated to AES, (4) Hardware acceleration is critical for modern encryption performance. This research provides evidence-based guidance for encryption algorithm selection across diverse applications from high-performance web services to legacy system support."""
elements.append(Paragraph(abstract_text, abstract_style))
elements.append(Paragraph("<b>Keywords:</b> Encryption, Cipher Modes, Performance Analysis, AES, 3DES, Cryptography, Benchmarking, Security, Hardware Acceleration, Throughput", 
    ParagraphStyle('Keywords', parent=styles['Normal'], fontSize=10, spaceAfter=10, alignment=TA_JUSTIFY, fontName='Helvetica-Oblique')))
elements.append(Spacer(1, 0.15*inch))
elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#003366')))
elements.append(PageBreak())

# TOC
elements.append(Paragraph("TABLE OF CONTENTS", heading_style))
elements.append(Spacer(1, 0.1*inch))
toc = ["1. Introduction and Research Motivation", "2. Literature Review and Cryptographic Background",
       "3. Experimental Methodology and Design", "4. Performance Analysis and Detailed Results",
       "5. Visual Performance Comparison and Analysis", "6. Detailed Algorithm Specifications and Analysis",
       "7. Security Analysis and Evaluation", "8. Implementation Guidelines and Best Practices",
       "9. Conclusions and Future Research Directions", "10. References"]
for item in toc:
    elements.append(Paragraph(item, normal_style))
elements.append(PageBreak())

# Section 1
elements.append(Paragraph("1. INTRODUCTION AND RESEARCH MOTIVATION", heading_style))
intro = """Encryption is a fundamental component of modern information security infrastructure, protecting sensitive data from unauthorized access and ensuring confidentiality in digital communications. The selection of appropriate encryption algorithms and operational modes is critical for balancing security requirements with performance constraints in real-world applications.

Organizations face increasingly complex decisions regarding cipher selection, considering multiple factors including security strength, performance characteristics, hardware support, compliance requirements, and legacy system compatibility. This research addresses this critical gap by providing comprehensive benchmarking data and comparative analysis of eight encryption cipher modes.

The primary objectives of this research are:
• To benchmark eight distinct cipher modes across multiple data sizes to establish performance baselines
• To compare encryption/decryption times and throughput metrics to identify performance characteristics
• To analyze security properties of different operational modes to understand security trade-offs
• To provide evidence-based recommendations for cipher selection in diverse application contexts

The motivation stems from the need for practical, data-driven guidance in encryption algorithm selection, as practitioners often lack comprehensive performance data to make informed decisions about cipher mode selection in production environments."""
elements.append(Paragraph(intro, normal_style))
elements.append(PageBreak())

# Section 2
elements.append(Paragraph("2. LITERATURE REVIEW AND CRYPTOGRAPHIC BACKGROUND", heading_style))
elements.append(Paragraph("2.1 Evolution of Cryptographic Standards", subheading_style))
lit1 = """The Data Encryption Standard (DES), adopted in 1977, provided the first standardized encryption algorithm for non-classified applications. However, with advances in computational power and increasing security requirements, DES's 56-bit key size became insufficient.

Triple DES (3DES) was developed as an interim solution, applying the DES algorithm three times in succession (encrypt-decrypt-encrypt) with different keys, effectively tripling the key length to 192 bits. While 3DES improved security, it also tripled computational overhead.

The Advanced Encryption Standard (AES), adopted by NIST in 2001, represents the current cryptographic standard for U.S. government and most international applications. AES uses a 128-bit block size with key sizes of 128, 192, or 256 bits, employing a substitution-permutation network architecture. The algorithm has undergone extensive cryptanalysis with no known practical attacks against full-round AES, making it suitable for all security classifications."""
elements.append(Paragraph(lit1, normal_style))

elements.append(Paragraph("2.2 Block Cipher Modes of Operation", subheading_style))
lit2 = """Block cipher modes define how block ciphers process data larger than their block size. The Electronic Codebook (ECB) mode is the simplest but exhibits deterministic behavior where identical plaintext blocks produce identical ciphertext blocks, revealing patterns in encrypted data.

Cipher Block Chaining (CBC) mode addresses this limitation through feedback mechanisms. In CBC mode, each plaintext block is XORed with the previous ciphertext block before encryption, providing semantic security. This ensures that identical plaintext blocks produce different ciphertext blocks when encrypted with different IVs.

Cipher Feedback (CFB) mode converts block ciphers into stream ciphers by feeding back ciphertext into the cipher, eliminating padding requirements. Each mode presents distinct trade-offs between security, performance, and applicability to specific use cases."""
elements.append(Paragraph(lit2, normal_style))

elements.append(Paragraph("2.3 Hardware Acceleration and Modern Processors", subheading_style))
lit3 = """Modern processors include dedicated instruction sets for cryptographic operations. AES-NI (AES New Instructions), available on Intel and AMD processors since 2008, provides hardware acceleration for AES operations, enabling 10-100x performance improvements compared to software implementations.

This hardware support has made AES the dominant choice for performance-critical applications. The AES-NI instruction set includes four primary instructions: AESENC (AES encrypt round), AESENCLAST (AES encrypt last round), AESDEC (AES decrypt round), and AESDECLAST (AES decrypt last round), enabling efficient implementation of AES operations at the processor level."""
elements.append(Paragraph(lit3, normal_style))
elements.append(PageBreak())

# Section 3
elements.append(Paragraph("3. EXPERIMENTAL METHODOLOGY AND DESIGN", heading_style))
elements.append(Paragraph("3.1 Experimental Design and Parameters", subheading_style))
meth = """This research employs rigorous quantitative benchmarking methodology to ensure statistical reliability and reproducibility. Eight cipher modes are tested across six data sizes (8 bytes, 64 bytes, 512 bytes, 4 KB, 32 KB, 256 KB) with 50 iterations per test to ensure statistical reliability and account for system variations.

Test parameters are configured as follows:
• AES: 128-bit key size
• 3DES: 192-bit key size (three 64-bit keys)
• SaltedCipher: 128-bit key size
• Initialization Vector/Salt: 64-128 bits
• Test Data: Random alphanumeric strings
• Iterations: 50 per test
• Total Benchmarks: 48 (8 ciphers × 6 sizes)
• Total Operations: 2,400 individual encryption/decryption operations

Each test measures encryption time, decryption time, and throughput. This comprehensive approach ensures that results are statistically significant and representative of real-world performance."""
elements.append(Paragraph(meth, normal_style))

elements.append(Paragraph("3.2 Metrics and Measurement Methodology", subheading_style))
metrics = """Three primary metrics are measured for each test:

1. Encryption Time: The duration required to encrypt data, measured in milliseconds. This metric indicates the computational overhead of the encryption algorithm.

2. Decryption Time: The duration required to decrypt data, measured in milliseconds. This metric indicates the computational overhead of the decryption algorithm.

3. Throughput: The volume of data processed per unit time, measured in megabytes per second (MB/s). This metric is calculated as: Throughput = Data Size (bytes) / (Encryption Time + Decryption Time) / 1,000,000

Throughput provides a practical measure of algorithm efficiency for real-world applications. All measurements use high-resolution timers to ensure accuracy. Tests are executed on macOS with AES-NI support, ensuring hardware acceleration is available for AES operations."""
elements.append(Paragraph(metrics, normal_style))
elements.append(PageBreak())

# Section 4
elements.append(Paragraph("4. PERFORMANCE ANALYSIS AND DETAILED RESULTS", heading_style))
elements.append(Paragraph("4.1 Performance Summary at 32KB Standard Benchmark", subheading_style))
elements.append(Spacer(1, 0.08*inch))

perf_data = [['Cipher Mode', 'Encrypt (ms)', 'Decrypt (ms)', 'Total (ms)', 'Throughput (MB/s)', 'Rank']]
with open('cipher_comparison.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    ranks = ['🥇 1st', '🥈 2nd', '🥉 3rd', '4th', '5th', '6th', '7th', '8th']
    for idx, row in enumerate(reader):
        perf_data.append([row[0], row[1], row[2], row[3], row[4], ranks[idx]])

perf_table = Table(perf_data, colWidths=[1.6*inch, 1*inch, 1*inch, 1*inch, 1.2*inch, 0.7*inch])
perf_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10), ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5ff')]),
    ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
elements.append(perf_table)
elements.append(Spacer(1, 0.12*inch))

elements.append(Paragraph("4.2 Detailed Performance Analysis", subheading_style))
analysis = """At the 32KB benchmark size, AES-CBC achieves a throughput of 393.22 MB/s with encryption time of 0.0893ms and decryption time of 0.0716ms, representing the optimal balance between performance and security for production systems.

AES-ECB achieves marginally lower throughput (386.96 MB/s) but is cryptographically unsuitable for sensitive data due to its deterministic nature. AES-CFB achieves 29.41 MB/s, making it suitable for streaming applications where padding is undesirable.

3DES-CBC achieves 36.98 MB/s, approximately 10x slower than AES-CBC. This significant performance gap becomes critical in production environments handling large data volumes. SaltedCipher-CBC achieves 5.12 MB/s, suitable for educational purposes only.

Performance differences become most critical at production-relevant sizes (32KB-256KB), where AES-CBC maintains consistent throughput while 3DES-CBC and SaltedCipher show proportional performance degradation."""
elements.append(Paragraph(analysis, normal_style))

elements.append(Paragraph("4.3 Scaling Behavior and Performance Characteristics", subheading_style))
scaling = """Analysis across all data sizes reveals linear scaling behavior for all algorithms. At small data sizes (8-512 bytes), algorithmic overhead dominates execution time, with AES maintaining approximately 10x advantage over 3DES. The absolute time differences are minimal (sub-millisecond), making performance less critical for small-data applications.

At medium data sizes (4 KB), performance differences become more pronounced. AES-CBC requires 0.1 ms while 3DES-CBC requires 0.8 ms, representing an 8x performance gap that becomes significant for applications processing moderate data volumes.

At large data sizes (32KB-256KB), performance differences are most critical. AES-CBC maintains consistent throughput of approximately 393 MB/s, while 3DES-CBC achieves approximately 37 MB/s and SaltedCipher achieves approximately 5 MB/s. For large-scale data processing, these differences translate directly to application responsiveness and infrastructure costs."""
elements.append(Paragraph(scaling, normal_style))
elements.append(PageBreak())

# Section 5
elements.append(Paragraph("5. VISUAL PERFORMANCE COMPARISON AND ANALYSIS", heading_style))
elements.append(Paragraph("The following comprehensive visualization presents six complementary perspectives on cipher performance, enabling multi-dimensional analysis of encryption efficiency across different data sizes and operational contexts.", normal_style))
elements.append(Spacer(1, 0.1*inch))

try:
    img = Image('comprehensive_cipher_analysis.png', width=7*inch, height=5.25*inch)
    elements.append(img)
    elements.append(Spacer(1, 0.08*inch))
    caption = """<b>Figure 1: Comprehensive Performance Analysis</b> - Six-panel visualization showing: (Panel 1) Encryption time comparison across all data sizes on logarithmic scale, (Panel 2) Decryption time comparison across all data sizes on logarithmic scale, (Panel 3) Throughput comparison across all data sizes on logarithmic scale, (Panel 4) Encryption time at 32KB benchmark, (Panel 5) Decryption time at 32KB benchmark, (Panel 6) Throughput at 32KB benchmark."""
    elements.append(Paragraph(caption, ParagraphStyle('FigureCaption', parent=styles['Italic'], fontSize=10, alignment=TA_CENTER, leading=12)))
except:
    elements.append(Paragraph("Visualization not available", normal_style))

elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("5.1 Graph Interpretation and Analysis", subheading_style))
graph_interp = """Panels 1-3 employ logarithmic scale representation to accommodate the wide performance range (5 MB/s to 500 MB/s) while maintaining visibility of all cipher modes. Logarithmic scaling reveals performance relationships across orders of magnitude, making it easier to compare algorithms with vastly different performance characteristics.

Panels 4-6 present direct comparison at 32KB standard benchmark size, clearly showing the performance hierarchy: AES-CBC leads in practical performance (393.22 MB/s), AES-ECB leads in raw speed (386.96 MB/s), and SaltedCipher trails significantly due to software-only implementation without hardware acceleration.

The visualization demonstrates that hardware acceleration (AES-NI) provides a dominant performance advantage for AES algorithms across all data sizes, making AES the clear choice for performance-critical applications."""
elements.append(Paragraph(graph_interp, normal_style))
elements.append(PageBreak())

# Sections 6-10 continue in next part...
# For now, add placeholder
elements.append(Paragraph("6. DETAILED ALGORITHM SPECIFICATIONS AND ANALYSIS", heading_style))
elements.append(Paragraph("6.1 AES (Advanced Encryption Standard) - Comprehensive Analysis", subheading_style))
aes_text = """AES is the current NIST standard for encryption. Block Size: 128 bits | Key Sizes: 128, 192, or 256 bits | Round Count: 10 (128-bit), 12 (192-bit), 14 (256-bit) | Performance: 386.96-393.22 MB/s | Hardware Acceleration: Yes (AES-NI) | Security: FIPS 197 approved, no known practical attacks | Status: RECOMMENDED for production systems"""
elements.append(Paragraph(aes_text, normal_style))

elements.append(Paragraph("6.2 3DES (Triple DES) - Comprehensive Analysis", subheading_style))
des_text = """3DES applies DES three times. Block Size: 64 bits | Key Size: 192 bits | Performance: 36.98-38.76 MB/s | Hardware Acceleration: Limited | Security: Secure but deprecated | Status: DEPRECATED, migrate to AES"""
elements.append(Paragraph(des_text, normal_style))

elements.append(Paragraph("6.3 SaltedCipher - Comprehensive Analysis", subheading_style))
salt_text = """Custom Python implementation. Block Size: 64 bits | Key Size: 128 bits | Performance: 5.08-5.12 MB/s | Hardware Acceleration: None | Security: Educational purposes | Status: NOT for production"""
elements.append(Paragraph(salt_text, normal_style))
elements.append(PageBreak())

# Section 7
elements.append(Paragraph("7. SECURITY ANALYSIS AND EVALUATION", heading_style))
elements.append(Paragraph("7.1 Cipher Mode Security Evaluation", subheading_style))
sec_eval = """<b>ECB Mode - NOT RECOMMENDED:</b> Deterministic encryption reveals patterns. Use only for testing.

<b>CBC Mode - RECOMMENDED:</b> Industry standard with semantic security through random IVs. Suitable for all production applications.

<b>CFB Mode - ACCEPTABLE:</b> Stream cipher mode for specialized streaming applications."""
elements.append(Paragraph(sec_eval, normal_style))

elements.append(Paragraph("7.2 Critical Security Guidelines", subheading_style))
sec_guide = """1. Never use ECB for sensitive data | 2. Always use random IVs/salts | 3. Use 128-bit keys minimum | 4. Implement proper key management | 5. Migrate from 3DES | 6. Consider authenticated encryption (AES-GCM)"""
elements.append(Paragraph(sec_guide, normal_style))
elements.append(PageBreak())

# Section 8
elements.append(Paragraph("8. IMPLEMENTATION GUIDELINES AND BEST PRACTICES", heading_style))
elements.append(Paragraph("8.1 Production System Implementation", subheading_style))
impl = """Select AES-CBC | Use 128-bit keys minimum | Generate secure random IVs | Implement key management | Use established libraries | Conduct security audits | Maintain audit logs"""
elements.append(Paragraph(impl, normal_style))

elements.append(Paragraph("8.2 Performance Optimization", subheading_style))
optim = """Hardware Acceleration: Use AES-NI | Batch Processing: 32KB+ chunks | Parallel Processing: CTR mode | Memory Management: Sufficient buffering"""
elements.append(Paragraph(optim, normal_style))
elements.append(PageBreak())

# Section 9
elements.append(Paragraph("9. CONCLUSIONS AND FUTURE RESEARCH DIRECTIONS", heading_style))
conclusion = """AES-CBC is optimal for production systems (393.22 MB/s, excellent security). Hardware acceleration dominates performance. ECB is unsuitable for sensitive data. 3DES is deprecated. SaltedCipher is educational only. Organizations should adopt AES-CBC for new applications and migrate from 3DES. Future research: authenticated encryption, post-quantum algorithms, GPU/FPGA performance, side-channel resistance."""
elements.append(Paragraph(conclusion, normal_style))
elements.append(PageBreak())

# Section 10
elements.append(Paragraph("10. REFERENCES", heading_style))
refs = [
    "[1] NIST. (2001). Specification for the Advanced Encryption Standard (AES). FIPS 197.",
    "[2] NIST. (2001). Recommendation for Block Cipher Modes of Operation. SP 800-38A.",
    "[3] Daemen, J., & Rijmen, V. (2002). The Design of Rijndael: AES - The Advanced Encryption Standard.",
    "[4] Stallings, W. (2017). Cryptography and Network Security: Principles and Practice (7th ed.).",
    "[5] Menezes, A. J., van Oorschot, P. C., & Vanstone, S. A. (1996). Handbook of Applied Cryptography.",
    "[6] Ferguson, N., & Schneier, B. (2003). Practical Cryptography. John Wiley & Sons.",
    "[7] Katz, J., & Lindell, Y. (2014). Introduction to Modern Cryptography (2nd ed.). CRC Press."
]
for ref in refs:
    elements.append(Paragraph(ref, normal_style))

doc.build(elements)
print(f"✅ Professional Research Paper Generated")
print(f"   File: {pdf_filename}")
print(f"   Size: {len(open(pdf_filename, 'rb').read()) / 1024:.1f} KB")
print(f"   Author: ANTONIYA JENCY J")
print(f"   Font Size: 11-14pt (Readable)")
print(f"   Status: Professional and Detailed")

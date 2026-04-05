# Rabin-Karp Document Fingerprinting 

High-performance Python engine for detecting document similarity and potential plagiarism. Optimized for large text datasets using rolling hashes and winnowing-based sub-sampling.

##  Overview
Standard string comparison algorithms suffer from high time and space complexities when processing massive documents. This project solves those bottlenecks by leveraging **K-grams** for structural robustness, the **Rabin-Karp algorithm** to achieve linear time complexity $\mathcal{O}(N)$, and the **Winnowing algorithm** to drastically compress memory footprint.

## The Algorithmic Pipeline

This analyzer processes text through a strict, 5-phase optimization pipeline:

1. **Data Normalization (Pre-processing)**
   * Converts all text to lowercase, strips whitespace, and removes punctuation using optimized C-level translation tables to ensure comparisons are based purely on semantic content.
2. **Sliding Window (K-Gram Generation)**
   * Slices the normalized text into overlapping contiguous substrings (K-grams). The overlapping nature guarantees the system remains robust against localized edits, insertions, and deletions.
3. **Polynomial String Hashing (Rabin-Karp)**
   * Converts textual K-grams into integer hashes. Instead of calculating hashes naively in $\mathcal{O}(N \times k)$ time, it utilizes a rolling mathematical formula to reuse previously computed values, bringing time complexity down to **$\mathcal{O}(N)$**.
4. **Document Comparison (Jaccard Similarity)**
   * Evaluates the similarity between documents using Set Theory. It calculates the intersection over the union of the two hash sets to determine a highly accurate match percentage.
5. **Memory Compression (Winnowing Algorithm)**
   * To prevent memory overflow on massive datasets, the Winnowing algorithm acts as a deterministic sub-sampling technique. By selecting only the local minimum hash within a secondary sliding window, it reduces space complexity by **~80%** while mathematically guaranteeing the retention of structural anchors.

##  Getting Started

### Prerequisites
* Python 3.x

### Installation & Execution
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/UnEthicalMK/rabin-karp-document-fingerprinting.git

2. Navigate to the project directory:
   ```bash
   cd rabin-karp-document-fingerprinting

3. Run the analyzer:
   ```bash
   python main.py

> **Note:** The `main.py` file contains a built-in demo block with sample documents. 
> You can replace or modify the `Source_Document`, `Sneaky_Document` and `Unrelated_Document` files in the main branch 
> to test with your own text.

##  Tech Stack & Concepts

* **Language:** Python 3

* **Core Algorithms:** Rabin-Karp Rolling Hash, Winnowing Sub-sampling

* **Concepts:** Sliding Window, Set Theory, Hashing, Modulo Arithmetic, Big-O Optimization

* **Time Complexity:** O(N) for hash generation

* **Space Complexity:** Optimized via deterministic sub-sampling (~80% memory reduction)

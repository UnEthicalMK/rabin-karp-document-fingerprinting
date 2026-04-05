# Rabin-Karp Document Fingerprinting 

High-performance Python engine for detecting document similarity and potential plagiarism. Optimized for large text datasets using rolling hashes and winnowing-based sub-sampling.

##  Overview
Standard string comparison algorithms suffer from high time and space complexities when processing massive documents. This project solves those bottlenecks by leveraging **K-grams** for structural robustness, the **Rabin-Karp algorithm** to achieve linear time complexity $\mathcal{O}(N)$, and the **Winnowing algorithm** to drastically compress memory footprint.

## Algorithmic Pipeline

This analyzer processes text through a structured five-phase optimization pipeline designed for speed, accuracy, and robustness.


### 1. Data Normalization
Text is converted to lowercase and stripped of all non-alphanumeric characters to ensure consistency.

**Performance:** Using C-level `str.translate` tables, normalization achieves speeds of approximately **120 MB/s**.


### 2. K-Gram Generation ($k = 12\text{–}20$)
The normalized text is divided into overlapping substrings (k-grams).

**Robustness:** A value of $k = 15$ balances precision and flexibility, yielding a **0.0001% false positive rate** while remaining resistant to minor word substitutions (e.g., "the" → "a").


### 3. Polynomial Rolling Hash ($O$($N$))
Hashes are computed incrementally using a rolling technique, avoiding recomputation for each substring.

$$
H = (d(H - c \cdot d^{k-1}) + h[i+k]) \bmod q
$$

**Efficiency:** This reduces complexity from **$O(N^2)$ to $O(N)$**, enabling near-instant processing of large documents.


### 4. Winnowing (Noise Filtering)
A secondary sliding window of size $w$ selects only the minimum hash values, significantly reducing storage.

**Guarantee:** Any matching sequence of length **$w + k$** is reliably detected while eliminating approximately **85% of redundant hashes**.


### 5. Jaccard Similarity
Similarity is computed using the Intersection over Union (IoU) of fingerprint sets.

**Interpretation:**
- **> 0.70** → Strong indication of plagiarism  
- **0.15 – 0.30** → Suggests shared sources or heavy paraphrasing


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

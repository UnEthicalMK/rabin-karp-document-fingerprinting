import string
import os

def read_text_file(file_path:str):
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            return file.read()
        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{file_path}'. Please check the path.")
        return ""
    
    except Exception as e:
        print(f"An Error occured while reading '{file_path}':{e}")
        return ""

#Phase 1: Data Normalization

def normalize_text(text:str):

    """
    Normalize text for comparison by removing formatting differences
    (case, whitespace, punctuation).
    """

    #Guard clause: ensure input is a string
    if not isinstance(text,str):
        return ''
    
    #Makes comparison case-insensitive
    text=text.lower()

    #Remove all whitespace (spaces, tabs, newlines)
    text="".join(text.split())

    #Strip punctuation efficiently using translation table
    translator=str.maketrans('','',string.punctuation)
    normalized_text=text.translate(translator)

    return normalized_text

#Phase 2 & 3: K-Grams & Rabin-Karp hashing

def generate_rabin_karp_hashes(normalized_text:str,k:int=12):

    """
    Moves a window of size k over the text to compute hash values for 
    each substring. Applies the Rabin–Karp rolling hash to reuse previous
    results, reducing time complexity from O(N·k) to O(N).
    """

    n=len(normalized_text)
    if n<k:
        return []
    
    #Constants for polynomial string hashing
    base=256
    modulus=10**9+7          #Large Prime No. to prevent integer overflow
    hashes=[]
    current_hash=0

    highest_power=pow(base,k-1,modulus)

    #Calculate the hash for the very first K-gram window
    for i in range(k):
        char_value=ord(normalized_text[i])
        current_hash=(current_hash * base + char_value)%modulus
    hashes.append(current_hash)

    #Slide the window and use the Rolling Hash formula for O(1) transitions
    for i in range(1,n-k+1):
        char_out=ord(normalized_text[i-1])
        char_in=ord(normalized_text[i+k-1])

        #Step 1: Remove outgoing character
        current_hash=(current_hash - char_out * highest_power)%modulus

        #Step 2: Shift base and add incoming character
        current_hash=(current_hash * base + char_in)%modulus

        #Ensure hash remains positive in Python
        current_hash=(current_hash + modulus)%modulus
        hashes.append(current_hash)

    return hashes

#Phase 4: Document comparision(Jaccard Similarity)

def calculate_jaccard_similarity(hashes_a:list,hashes_b:list):
    """
    Calculates the Jaccard Similarity between two sets of document hashes.
    Formula: Intersection / Union
    """

    set_a=set(hashes_a)
    set_b=set(hashes_b)

    #Handles edge case for empty documents
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    
    #Calculate Intersection(shared hashes) and Union(total unique hashes)
    intersection=set_a&set_b
    union=set_a|set_b

    return len(intersection)/len(union)

# Phase 5: Scaling Optimization(Winnowing)

def winnow(hashes:list,w:int=4):
    """
    Reduces memory footprint by ~80% while retaining structural integrity.
    Slides a window of size 'w' over the hashes and selects the minimum hash.
    The minimum hash acts as a geographical anchor that survives localized text edits.
    """

    fingerprints=[]
    recorded_indices=set()

    for i in range(len(hashes)-w+1):
        window=hashes[i:i+w]
        min_hash=min(window)

        #Rule: If multiple identical minimums exist, pick the right-most one
        min_index_in_window=w-1-window[::-1].index(min_hash)
        global_min_index=i+min_index_in_window

        #Only store the hash if we haven't already recorded this exact positional instance
        if global_min_index not in recorded_indices:
            recorded_indices.add(global_min_index)
            fingerprints.append(min_hash)

    return fingerprints

#Execution Part

#Parameters
k_gram_size=12
window_size=4

#Helper Function
def run_similarity_test(doc_a:str,doc_b:str,test_name:str):
    print(f"Test: {test_name}")

    #Process doc_a
    normalize_a=normalize_text(doc_a)
    hashes_a=generate_rabin_karp_hashes(normalize_a,k_gram_size)
    fingerprints_a=winnow(hashes_a,window_size)

    #Process doc_b
    normalize_b=normalize_text(doc_b)
    hashes_b=generate_rabin_karp_hashes(normalize_b,k_gram_size)
    fingerprints_b=winnow(hashes_b,window_size)

    #Calculate Jaccard Similarity
    similarity=calculate_jaccard_similarity(fingerprints_a,fingerprints_b)*100

    #Display Results
    print(f"Doc A fingerprints: {len(fingerprints_a)} (from {len(hashes_a)})")
    print(f"Doc B fingerprints: {len(fingerprints_b)} (from {len(hashes_b)})")
    print(f"Similarity: {similarity:.2f}%")

    result="High Similarity Detected!" if similarity>=80 else "Documents are Unique!"
    print(f"Result: {result}\n")

def get_multiline_input(prompt_msg):
    print(prompt_msg)
    lines=[]
    while True:
        line=input()
        if not line:  
            break
        lines.append(line)
    return "\n".join(lines).strip()

if __name__=="__main__":
    print("Initializing Rabin-Karp Document Fingerprinting")
    print("1. Compare two text files (.txt)")
    print("2. Compare raw text (Type or paste directly)")
    print("3. Run built-in demo")
    print("4. Exit")
    print("="*50)
    3
    choice = input("Select an option (1-4): ").strip()
    
    if choice == '1':
        file_1 = input("Enter path for Document A (e.g., docA.txt): ").strip()
        file_2 = input("Enter path for Document B (e.g., docB.txt): ").strip()
        
        text_a = read_text_file(file_1)
        text_b = read_text_file(file_2)
        
        if text_a and text_b:
            run_similarity_test(text_a, text_b, "File Comparison")
        else:
            print("Analysis aborted: Could not read one or both files.")

    elif choice == '2':
        text_a = get_multiline_input("> Paste your text for Document A (Press Enter TWICE when done):")
        text_b = get_multiline_input("> Paste your text for Document B (Press Enter TWICE when done):")
        
        if text_a and text_b:
            run_similarity_test(text_a, text_b, "Direct Text Comparison")
        else:
            print("Analysis aborted: Both strings must contain text.")

    elif choice == '3':
        source_doc = """Baking a perfect chocolate cake requires precise measurements and timing. 
        Start by creaming butter and sugar, then slowly fold in flour, cocoa, and eggs. Bake at 
        350°F until a toothpick comes out clean.
        """

        plagiarized_doc = """To make a delicious chocolate cake, carefully measure ingredients and 
        follow steps. Mix butter with sugar, gently add flour, cocoa, and eggs, and bake at 350 degrees 
        Fahrenheit until fully cooked.
        """
        
        run_similarity_test(source_doc, plagiarized_doc, "Portfolio Demo (Source vs Sneaky Copy)")

    elif choice == '4':
        print("Exiting tool. Goodbye!")
    else:
        print("Invalid selection. Please run the script again and choose 1, 2, 3, or 4.")

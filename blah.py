import hashlib
import base64
import itertools
from multiprocessing import Pool, cpu_count
import time

# Target hash
TARGET_HASH = 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw='

# Column data provided by user
COLUMNS = [
    ['I', 'D', 'S', 'O', 'M', 'H', 'E', 'A', 'R', 'B', 'N', 'C'],  # col1
    ['A', 'S', 'A', 'D', 'I', 'B', 'E', 'R', 'N', 'A', 'F', 'A', 'S', 'C'],  # col2
    ['I', 'K', 'R', 'E', 'D', 'S', 'N', 'A', 'T', 'U', 'B', 'C'],  # col3
    ['D', 'D', 'S', 'B', 'R', 'B', 'W', 'N', 'E', 'A', 'E', 'I', 'C'],  # col4
    ['D', 'R', 'I', 'B', 'U', 'S', 'H', 'O', 'N', 'C', 'O', 'A', 'E'],  # col5
    ['I', 'N', 'K', 'I', 'R', 'E', 'M', 'A', 'D', 'R', 'N', 'B', 'S', 'C'],  # col6
    ['D', 'I', 'E', 'U', 'B', 'C', 'D', 'E', 'S', 'A', 'N', 'D', 'R', 'C'],  # col7
    ['R', 'A', 'E', 'S', 'H', 'S', 'E', 'N', 'D', 'I', 'B', 'C'],  # col8
    ['S', 'B', 'R', 'S', 'I', 'D', 'A', 'E', 'A', 'T', 'N', 'C']   # col9
]

def check_hash(combination):
    """Check if a combination produces the target hash"""
    # Build the first 35 characters from the combination
    # Based on the grid structure, we need to figure out how the 35 chars are arranged
    # From the QUOTE constant, it appears to be a 9-column grid
    # The first 35 characters would be roughly the first 4 rows (9*4 = 36, so first 35)

    first_35 = ''.join(combination[:35]) if len(combination) >= 35 else ''.join(combination)

    # Calculate hash
    hash_obj = hashlib.sha256(first_35.encode())
    hash_b64 = base64.b64encode(hash_obj.digest()).decode()

    return hash_b64 == TARGET_HASH, first_35, hash_b64

def generate_combinations_batch(start_idx, batch_size, total_combinations):
    """Generate a batch of combinations starting from start_idx"""
    combinations = []

    # Calculate column lengths for iteration
    col_lengths = [len(col) for col in COLUMNS]

    current_idx = start_idx
    count = 0

    while count < batch_size and current_idx < total_combinations:
        # Convert index to combination indices
        combination_indices = []
        temp_idx = current_idx

        for col_len in reversed(col_lengths):
            combination_indices.append(temp_idx % col_len)
            temp_idx //= col_len

        combination_indices.reverse()

        # Build the actual combination
        combination = []
        for i, col_idx in enumerate(combination_indices):
            combination.append(COLUMNS[i][col_idx])

        combinations.append(combination)
        current_idx += 1
        count += 1

    return combinations

def process_batch(args):
    """Process a batch of combinations"""
    start_idx, batch_size, total_combinations = args

    combinations = generate_combinations_batch(start_idx, batch_size, total_combinations)

    for i, combination in enumerate(combinations):
        is_match, first_35, calculated_hash = check_hash(combination)

        if is_match:
            return {
                'found': True,
                'combination': combination,
                'first_35': first_35,
                'hash': calculated_hash,
                'index': start_idx + i
            }

        # Print progress every 100000 combinations
        if (start_idx + i) % 100000 == 0:
            print(f"Checked {start_idx + i:,} combinations... Current: {first_35[:10]}...")

    return {'found': False, 'checked': len(combinations)}

def brute_force_parallel():
    """Brute force with parallel processing"""
    print("Starting brute force attack on the hash...")
    print(f"Target hash: {TARGET_HASH}")
    print(f"Columns: {len(COLUMNS)}")
    print(f"Column lengths: {[len(col) for col in COLUMNS]}")

    # Calculate total possible combinations
    total_combinations = 1
    for col in COLUMNS:
        total_combinations *= len(col)

    print(f"Total combinations to check: {total_combinations:,}")

    # Set up parallel processing
    num_processes = 8
    batch_size = 10000  # Process 10k combinations per batch

    print(f"Using {num_processes} processes with batch size {batch_size}")

    # Create batches
    batches = []
    for start_idx in range(0, total_combinations, batch_size):
        batches.append((start_idx, batch_size, total_combinations))

    print(f"Created {len(batches)} batches")

    start_time = time.time()

    # Process batches in parallel
    with Pool(num_processes) as pool:
        for result in pool.imap_unordered(process_batch, batches):
            if result['found']:
                elapsed = time.time() - start_time
                print(f"\n🎉 FOUND MATCH!")
                print(f"Combination: {result['combination']}")
                print(f"First 35 chars: {result['first_35']}")
                print(f"Calculated hash: {result['hash']}")
                print(f"Index: {result['index']:,}")
                print(f"Time elapsed: {elapsed:.2f} seconds")
                return result

    elapsed = time.time() - start_time
    print(f"\nNo match found after checking all {total_combinations:,} combinations")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    return None

def brute_force_simple():
    """Simple single-threaded brute force for testing"""
    print("Starting simple brute force...")

    # Calculate total combinations
    total_combinations = 1
    for col in COLUMNS:
        total_combinations *= len(col)

    print(f"Total combinations: {total_combinations:,}")

    count = 0
    start_time = time.time()

    # Generate all possible combinations
    for combination in itertools.product(*COLUMNS):
        is_match, first_35, calculated_hash = check_hash(combination)

        if is_match:
            elapsed = time.time() - start_time
            print(f"\n🎉 FOUND MATCH!")
            print(f"Combination: {list(combination)}")
            print(f"First 35 chars: {first_35}")
            print(f"Calculated hash: {calculated_hash}")
            print(f"Checked {count:,} combinations")
            print(f"Time elapsed: {elapsed:.2f} seconds")
            return {
                'combination': list(combination),
                'first_35': first_35,
                'hash': calculated_hash,
                'count': count
            }

        count += 1
        if count % 100000 == 0:
            elapsed = time.time() - start_time
            rate = count / elapsed if elapsed > 0 else 0
            print(f"Checked {count:,} combinations ({rate:.0f}/sec)... Current: {first_35[:10]}...")

    print("No match found!")
    return None

if __name__ == "__main__":
    print("Hash Brute Force Tool")
    print("=" * 50)

    # Test a few combinations first
    print("\nTesting a few sample combinations:")
    for i in range(3):
        combination = [col[0] for col in COLUMNS]  # First letter from each column
        if i == 1:
            combination = [col[1] if len(col) > 1 else col[0] for col in COLUMNS]
        elif i == 2:
            combination = [col[-1] for col in COLUMNS]  # Last letter from each column

        is_match, first_35, calculated_hash = check_hash(combination)
        print(f"  Test {i+1}: {combination} -> {first_35[:10]}... -> {calculated_hash[:20]}...")

    print("\nStarting full brute force...")

    # Use parallel processing for faster execution
    result = brute_force_parallel()

    if result:
        print(f"\nSuccess! The combination is: {result['combination']}")
        print(f"Grid representation (first 35 chars): {result['first_35']}")
    else:
        print("\nNo solution found. Double-check the column data and target hash.")
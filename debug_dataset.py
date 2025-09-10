"""
Debug script to examine the dataset structure.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datasets import load_dataset
from rag.utils import normalize_schema, validate_verse_data


def debug_dataset():
    """Debug the dataset structure."""
    print("Debugging Bhagavad Gita Dataset")
    print("=" * 50)
    
    try:
        # Load the dataset
        print("Loading dataset...")
        dataset = load_dataset("JDhruv14/Bhagavad-Gita_Dataset")
        
        # Get the train split
        data = dataset['train']
        print(f"Dataset loaded: {len(data)} entries")
        
        # Look at the first few entries
        print("\nFirst 3 entries:")
        for i in range(min(3, len(data))):
            print(f"\nEntry {i}:")
            print(f"Raw data: {data[i]}")
            
            # Try to normalize
            normalized = normalize_schema(data[i])
            print(f"Normalized: {normalized}")
            
            # Try to validate
            is_valid = validate_verse_data(normalized)
            print(f"Valid: {is_valid}")
            
            if not is_valid:
                print("Validation failed!")
                print(f"Missing fields: {[k for k in ['chapter', 'verse', 'text'] if k not in normalized or not normalized[k]]}")
        
        # Check column names
        print(f"\nColumn names: {data.column_names}")
        
        # Check data types
        print(f"\nData types: {data.features}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_dataset()

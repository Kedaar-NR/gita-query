"""
Utility functions for the Bhagavad Gita chatbot.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class Verse:
    """Represents a single verse from the Bhagavad Gita."""
    id: str
    chapter: int
    verse: int
    text: str
    sanskrit: Optional[str] = None


def normalize_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize field names from the dataset to ensure consistency.
    Handles variations in field naming across different dataset versions.
    """
    normalized = {}
    
    # Map possible field variations
    field_mappings = {
        'chapter': ['chapter', 'Chapter', 'ch'],
        'verse': ['verse', 'Verse', 'v'],
        'sanskrit': ['sanskrit', 'Sanskrit', 'sa'],
        'hindi': ['hindi', 'Hindi', 'hi'],
        'english': ['english', 'English', 'en', 'translation']
    }
    
    for standard_field, possible_fields in field_mappings.items():
        for possible_field in possible_fields:
            if possible_field in data:
                normalized[standard_field] = data[possible_field]
                break
    
    return normalized


def build_citation(chapter: int, verse: int) -> str:
    """Build a citation string in the format [chapter.verse]."""
    return f"[{chapter}.{verse}]"


def extract_citations_from_text(text: str) -> List[str]:
    """Extract all citations from text in the format [chapter.verse]."""
    pattern = r'\[(\d+)\.(\d+)\]'
    matches = re.findall(pattern, text)
    return [f"[{match[0]}.{match[1]}]" for match in matches]


def format_context_block(passages: List[Dict[str, Any]]) -> str:
    """
    Format retrieved passages into a compact context block for the generator.
    """
    context_parts = []
    for passage in passages:
        citation = build_citation(passage['chapter'], passage['verse'])
        context_parts.append(f"{citation} {passage['text']}")
    
    return "\n\n".join(context_parts)


def safety_check(query: str) -> bool:
    """
    Simple safety check to prevent medical/legal advice requests.
    Returns True if query is safe, False otherwise.
    """
    medical_keywords = [
        'medical', 'medicine', 'doctor', 'treatment', 'diagnosis', 'symptoms',
        'prescription', 'drug', 'therapy', 'cure', 'illness', 'disease'
    ]
    
    legal_keywords = [
        'legal', 'lawyer', 'court', 'lawsuit', 'legal advice', 'attorney',
        'litigation', 'contract', 'legal opinion', 'jurisdiction'
    ]
    
    query_lower = query.lower()
    
    for keyword in medical_keywords + legal_keywords:
        if keyword in query_lower:
            return False
    
    return True


def validate_verse_data(verse_data: Dict[str, Any]) -> bool:
    """
    Validate that verse data contains required fields and is not empty.
    """
    required_fields = ['chapter', 'verse', 'text']
    
    for field in required_fields:
        if field not in verse_data or not verse_data[field]:
            return False
    
    # Check that chapter and verse are valid numbers
    try:
        chapter = int(verse_data['chapter'])
        verse = int(verse_data['verse'])
        if chapter < 1 or chapter > 18 or verse < 1:
            return False
    except (ValueError, TypeError):
        return False
    
    # Check that text is not just whitespace
    if not verse_data['text'].strip():
        return False
    
    return True


def create_verse_id(chapter: int, verse: int) -> str:
    """Create a unique ID for a verse."""
    return f"{chapter:02d}.{verse:02d}"


def clean_text(text: str) -> str:
    """Clean and normalize text for better processing."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove any non-printable characters except newlines
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    
    return text

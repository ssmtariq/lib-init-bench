import time
start_time = time.perf_counter()

# Inefficient: Eagerly import all NLP capabilities
import nltk
from sentence_transformers import SentenceTransformer

# Download required NLTK data at import time (more I/O!)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Initialize transformer model at import (heavy!)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Calculate import time
import_time = time.perf_counter() - start_time

def basic_analysis(text: str) -> dict:
    """
    Perform basic text analysis.
    This could be done with string operations,
    but we loaded all of NLTK just for this.
    """
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_word_length': sum(len(w) for w in words) / len(words)
    }

def advanced_analysis(text: str) -> dict:
    """
    Perform advanced NLP analysis.
    This is rarely used but we loaded everything at import.
    """
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    named_entities = nltk.ne_chunk(pos_tags)
    embedding = model.encode(text)
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'pos_tags': [tag for _, tag in pos_tags],
        'named_entities': str(named_entities),
        'embedding_dim': len(embedding)
    }

def lambda_handler(event, context):
    """Analyze text using NLP capabilities."""
    text = event.get('text', '')
    analysis_type = event.get('analysis_type', 'basic')
    
    if not text:
        return {
            'error': 'No text provided',
            'import_time': import_time
        }
    
    try:
        # Most users just need basic analysis
        # but we loaded everything anyway
        if analysis_type == 'basic':
            result = basic_analysis(text)
        else:
            result = advanced_analysis(text)
            
        result['import_time'] = import_time
        result['analysis_type'] = analysis_type
        
        # Add metadata about loaded capabilities
        result['nltk_data_path'] = nltk.data.path[0]
        result['transformer_model'] = model.get_sentence_embedding_dimension()
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }
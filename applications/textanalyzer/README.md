# Text Analyzer

A serverless service that analyzes text using various NLP capabilities.

## Dependencies

```
nltk==3.*
sentence-transformers==2.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"text": "This is a simple sentence to analyze.", "analysis_type": "basic"}'
```

Expected output:
```json
{
  "word_count": 7,
  "sentence_count": 1,
  "avg_word_length": 4.57,
  "import_time": 2.345  // Actual time will vary
}
```

## Local Testing

```bash
sam local invoke -e events/test.json
```

## Clean Up

```bash
sam delete
```

## Inefficiency Details

### Pattern: C8 – Eager Loading of Optional Plugins

This application demonstrates the inefficiency of eagerly loading all available NLP capabilities at import time, even though most invocations only use basic text analysis features.

### Why this exhibits the inefficiency

The application eagerly imports at module level:
1. NLTK components:
   - Tokenizers
   - Taggers
   - Parsers
   - Language models
2. Sentence Transformers:
   - BERT models
   - Embedding generators
   - Vectorizers

However, the actual Lambda handler:
1. Usually performs basic text analysis:
   - Word counting
   - Sentence splitting
   - Simple statistics
2. Rarely needs advanced features:
   - Sentiment analysis
   - Text similarity
   - Named entity recognition

This creates significant cold-start overhead because all NLP capabilities are loaded even when only basic features are needed.

### Mitigation Notes

To fix this inefficiency:
1. Move advanced imports into functions:
   ```python
   def get_sentiment(text):
       from transformers import pipeline
       analyzer = pipeline("sentiment-analysis")
       return analyzer(text)
   ```
2. Use lazy loading patterns:
   ```python
   def get_nlp():
       if not hasattr(get_nlp, "nltk"):
           import nltk
           get_nlp.nltk = nltk
       return get_nlp.nltk
   ```
3. Split functionality into separate handlers:
   - Basic analysis Lambda (fast cold start)
   - Advanced analysis Lambda (accepts longer cold start)
4. Consider using simpler alternatives for basic operations
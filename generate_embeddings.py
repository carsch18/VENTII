import json
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

API_KEY = "YOUR_CEREBRAS_API_KEY_HERE"  # Replace with your Cerebras API key

def get_embedding_from_llm(text):
    """Generate embedding using Cerebras LLM response as vector"""
    url = "https://api.cerebras.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3.1-8b",
        "messages": [{"role": "user", "content": f"Summarize in exactly 10 keywords: {text[:500]}"}],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return ""

# Load dataset
with open('dataset.json') as f:
    dataset = json.load(f)

print(f"Generating embeddings for {len(dataset)} documents...")

# Generate semantic embeddings using TF-IDF on LLM-enhanced text
documents = []
for i, item in enumerate(dataset):
    if i % 20 == 0:
        print(f"Processing {i}/{len(dataset)}...")
    
    # Use LLM to enhance document representation
    llm_keywords = get_embedding_from_llm(item['search_document'])
    enhanced_doc = f"{item['search_document']} {llm_keywords}"
    documents.append(enhanced_doc)
    item['llm_keywords'] = llm_keywords

# Create TF-IDF embeddings (semantic representation)
vectorizer = TfidfVectorizer(max_features=384, ngram_range=(1, 2))
embeddings = vectorizer.fit_transform(documents).toarray()

# Save embeddings and enhanced dataset
np.save('embeddings.npy', embeddings)
with open('dataset_enhanced.json', 'w') as f:
    json.dump(dataset, f, indent=2)

import pickle
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print(f"✓ Generated embeddings: {embeddings.shape}")
print(f"✓ Saved to embeddings.npy")
print(f"✓ Enhanced dataset saved to dataset_enhanced.json")

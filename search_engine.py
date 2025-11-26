import json
import numpy as np
import pickle
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

API_KEY = "csk-d45v9f85n3k98tf89m5e6rfrh5dtnk6r9pn3j5fkmhe2wy43"

class HybridSearchEngine:
    def __init__(self):
        with open('dataset_enhanced.json') as f:
            self.dataset = json.load(f)
        self.embeddings = np.load('embeddings.npy')
        with open('vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)
        
    def get_llm_keywords(self, text):
        """Use Cerebras to enhance query"""
        url = "https://api.cerebras.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3.1-8b",
            "messages": [{"role": "user", "content": f"Extract 5 search keywords from: {text}"}],
            "max_tokens": 30,
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return text
    
    def semantic_search(self, query):
        """Compute semantic similarity using embeddings"""
        llm_enhanced = self.get_llm_keywords(query)
        query_vec = self.vectorizer.transform([f"{query} {llm_enhanced}"]).toarray()
        similarities = cosine_similarity(query_vec, self.embeddings)[0]
        return (similarities - similarities.min()) / (similarities.max() - similarities.min() + 1e-10)
    
    def lexical_search(self, query):
        """Keyword + TF-IDF matching"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        scores = []
        for item in self.dataset:
            doc = item['search_document'].lower()
            
            # Keyword matching
            keyword_score = sum(1 for word in query_words if word in doc) / len(query_words)
            
            # TF-IDF similarity
            doc_vec = self.vectorizer.transform([doc]).toarray()
            query_vec = self.vectorizer.transform([query]).toarray()
            tfidf_score = cosine_similarity(query_vec, doc_vec)[0][0]
            
            # Combined lexical score
            scores.append(0.5 * keyword_score + 0.5 * tfidf_score)
        
        scores = np.array(scores)
        return (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
    
    def hybrid_search(self, query, top_k=5):
        """Hybrid ranking: 0.7 semantic + 0.3 lexical"""
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        semantic_scores = self.semantic_search(query)
        lexical_scores = self.lexical_search(query)
        
        final_scores = 0.7 * semantic_scores + 0.3 * lexical_scores
        
        top_indices = np.argsort(final_scores)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            item = self.dataset[idx]
            result = {
                'rank': rank,
                'id': item['id'],
                'title': item['title'],
                'description': item['description'],
                'category': item['category'],
                'tags': item['tags'],
                'price': item['metadata']['price'],
                'rating': item['metadata']['rating'],
                'semantic_score': float(semantic_scores[idx]),
                'lexical_score': float(lexical_scores[idx]),
                'final_score': float(final_scores[idx])
            }
            results.append(result)
            
            print(f"\n{rank}. {item['title']} (ID: {item['id']})")
            print(f"   Category: {item['category']} | Price: ${item['metadata']['price']} | Rating: {item['metadata']['rating']}/5")
            print(f"   Description: {item['description']}")
            print(f"   Tags: {', '.join(item['tags'])}")
            print(f"   📊 Semantic: {semantic_scores[idx]:.3f} | Lexical: {lexical_scores[idx]:.3f} | Final: {final_scores[idx]:.3f}")
        
        return results
    
    def explain_results(self, query, results):
        """Use LLM to explain why results were selected"""
        url = "https://api.cerebras.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        top_items = [f"{r['title']} ({r['category']})" for r in results[:3]]
        prompt = f"Query: '{query}'. Top results: {', '.join(top_items)}. Explain in 2 sentences why these are relevant."
        
        data = {
            "model": "llama3.1-8b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            explanation = response.json()['choices'][0]['message']['content']
            print(f"\n💡 LLM Explanation:\n{explanation}")
            return explanation
        return ""

# Test queries
if __name__ == "__main__":
    engine = HybridSearchEngine()
    
    test_queries = [
        "wireless headphones for music",
        "organic healthy food products",
        "comfortable running shoes",
        "professional camera equipment",
        "educational toys for kids"
    ]
    
    all_results = {}
    for query in test_queries:
        results = engine.hybrid_search(query, top_k=5)
        explanation = engine.explain_results(query, results)
        all_results[query] = {
            'results': results,
            'explanation': explanation
        }
    
    # Save results
    with open('search_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("✓ Search results saved to search_results.json")
    print(f"{'='*60}")

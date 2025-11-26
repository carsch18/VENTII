from search_engine import HybridSearchEngine

print("🔍 Hybrid Search Engine Demo")
print("="*60)

engine = HybridSearchEngine()

while True:
    query = input("\nEnter search query (or 'quit' to exit): ").strip()
    
    if query.lower() in ['quit', 'exit', 'q']:
        print("👋 Goodbye!")
        break
    
    if not query:
        continue
    
    results = engine.hybrid_search(query, top_k=5)
    engine.explain_results(query, results)

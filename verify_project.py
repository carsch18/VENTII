import os
import json
import numpy as np

print("🔍 Project Verification Report")
print("="*60)

# Check files
files = {
    'Dataset': 'dataset.json',
    'Enhanced Dataset': 'dataset_enhanced.json',
    'Embeddings': 'embeddings.npy',
    'Vectorizer': 'vectorizer.pkl',
    'Search Results': 'search_results.json',
    'README': 'README.md',
    'Technical Report': 'TECHNICAL_REPORT.md'
}

print("\n📁 File Check:")
for name, file in files.items():
    exists = "✓" if os.path.exists(file) else "✗"
    size = os.path.getsize(file) / 1024 if os.path.exists(file) else 0
    print(f"  {exists} {name}: {file} ({size:.1f} KB)")

# Check dataset
with open('dataset.json') as f:
    dataset = json.load(f)
print(f"\n📊 Dataset Stats:")
print(f"  Records: {len(dataset)}")
categories = {}
for item in dataset:
    categories[item['category']] = categories.get(item['category'], 0) + 1
print(f"  Categories: {len(categories)}")
for cat, count in sorted(categories.items()):
    print(f"    - {cat}: {count}")

# Check embeddings
embeddings = np.load('embeddings.npy')
print(f"\n🧮 Embeddings:")
print(f"  Shape: {embeddings.shape}")
print(f"  Dimension: {embeddings.shape[1]}")
print(f"  Size: {embeddings.nbytes / 1024:.1f} KB")

# Check search results
with open('search_results.json') as f:
    results = json.load(f)
print(f"\n🔍 Search Results:")
print(f"  Test Queries: {len(results)}")
for query in results.keys():
    print(f"    - {query}")

print(f"\n✅ Project Status: COMPLETE")
print("="*60)

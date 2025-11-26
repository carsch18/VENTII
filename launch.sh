#!/bin/bash

echo "🚀 Launching VENTI Search Engine UI..."
echo ""
echo "📊 Project Stats:"
echo "   - 200 documents"
echo "   - 10 categories"
echo "   - 384-dimensional embeddings"
echo "   - Hybrid search (70% semantic + 30% lexical)"
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo ""
echo "⌨️  Press Ctrl+C to stop"
echo ""

cd /Users/carsch18/Desktop/VENTI
python3 -m http.server 8000

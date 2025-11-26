// Global state
let dataset = [];
let embeddings = [];
let nodes = [];
let camera = { x: 0, y: 0, zoom: 1 };
let selectedNode = null;
let searchResults = [];

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Category colors - grayscale theme
const categoryColors = {
    'Electronics': '#1a1a1a',
    'Books': '#4a4a4a',
    'Clothing': '#6a6a6a',
    'Food': '#8a8a8a',
    'Home': '#aaaaaa',
    'Sports': '#2a2a2a',
    'Beauty': '#5a5a5a',
    'Toys': '#7a7a7a',
    'Music': '#9a9a9a',
    'Garden': '#bababa'
};

// Initialize
async function init() {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    await loadData();
    projectEmbeddings();
    animate();
    
    document.getElementById('loading').style.display = 'none';
    
    // Enter key to search
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') search();
    });
}

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}

async function loadData() {
    try {
        const response = await fetch('dataset_enhanced.json');
        dataset = await response.json();
        
        embeddings = dataset.map(() => ({
            x: Math.random() * 2 - 1,
            y: Math.random() * 2 - 1
        }));
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function projectEmbeddings() {
    const categoryOffsets = {
        'Electronics': { x: -0.6, y: -0.6 },
        'Books': { x: 0.6, y: -0.6 },
        'Clothing': { x: -0.6, y: 0.6 },
        'Food': { x: 0.6, y: 0.6 },
        'Home': { x: 0, y: -0.8 },
        'Sports': { x: -0.8, y: 0 },
        'Beauty': { x: 0.8, y: 0 },
        'Toys': { x: 0, y: 0.8 },
        'Music': { x: -0.4, y: 0 },
        'Garden': { x: 0.4, y: 0 }
    };
    
    nodes = dataset.map((item, i) => {
        const offset = categoryOffsets[item.category] || { x: 0, y: 0 };
        return {
            id: item.id,
            x: embeddings[i].x * 0.3 + offset.x,
            y: embeddings[i].y * 0.3 + offset.y,
            category: item.category,
            title: item.title,
            data: item,
            radius: 4,
            highlighted: false
        };
    });
}

function worldToScreen(x, y) {
    return {
        x: (x - camera.x) * camera.zoom * 300 + canvas.width / 2,
        y: (y - camera.y) * camera.zoom * 300 + canvas.height / 2
    };
}

function drawNodes() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw connections for highlighted nodes
    if (searchResults.length > 0) {
        ctx.strokeStyle = 'rgba(26, 26, 26, 0.08)';
        ctx.lineWidth = 1;
        searchResults.forEach(result => {
            const node = nodes.find(n => n.id === result.id);
            if (node) {
                searchResults.forEach(other => {
                    const otherNode = nodes.find(n => n.id === other.id);
                    if (otherNode && node.id !== otherNode.id) {
                        const pos1 = worldToScreen(node.x, node.y);
                        const pos2 = worldToScreen(otherNode.x, otherNode.y);
                        ctx.beginPath();
                        ctx.moveTo(pos1.x, pos1.y);
                        ctx.lineTo(pos2.x, pos2.y);
                        ctx.stroke();
                    }
                });
            }
        });
    }
    
    // Draw nodes
    nodes.forEach(node => {
        const pos = worldToScreen(node.x, node.y);
        
        if (pos.x < -50 || pos.x > canvas.width + 50 || 
            pos.y < -50 || pos.y > canvas.height + 50) return;
        
        const isHighlighted = searchResults.some(r => r.id === node.id);
        const isSelected = selectedNode && selectedNode.id === node.id;
        
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, node.radius * camera.zoom, 0, Math.PI * 2);
        
        if (isSelected) {
            ctx.fillStyle = '#ffffff';
            ctx.strokeStyle = '#1a1a1a';
            ctx.lineWidth = 2.5;
            ctx.fill();
            ctx.stroke();
        } else if (isHighlighted) {
            ctx.fillStyle = categoryColors[node.category] || '#666';
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 2;
            ctx.fill();
            ctx.stroke();
        } else {
            ctx.fillStyle = categoryColors[node.category] || '#999';
            ctx.globalAlpha = 0.4;
            ctx.fill();
            ctx.globalAlpha = 1;
        }
        
        if ((isHighlighted || isSelected) && camera.zoom > 0.5) {
            ctx.fillStyle = '#1a1a1a';
            ctx.font = `${11 * camera.zoom}px -apple-system, BlinkMacSystemFont, 'Segoe UI'`;
            ctx.textAlign = 'center';
            ctx.fillText(node.title.substring(0, 20), pos.x, pos.y - 12 * camera.zoom);
        }
    });
}

function animate() {
    drawNodes();
    requestAnimationFrame(animate);
}

function zoomToNode(nodeId) {
    const node = nodes.find(n => n.id === nodeId);
    if (!node) return;
    
    selectedNode = node;
    
    const targetZoom = 2;
    const targetX = node.x;
    const targetY = node.y;
    
    const duration = 800;
    const startTime = Date.now();
    const startZoom = camera.zoom;
    const startX = camera.x;
    const startY = camera.y;
    
    function animateZoom() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        
        camera.zoom = startZoom + (targetZoom - startZoom) * eased;
        camera.x = startX + (targetX - startX) * eased;
        camera.y = startY + (targetY - startY) * eased;
        
        if (progress < 1) {
            requestAnimationFrame(animateZoom);
        }
    }
    
    animateZoom();
}

function resetCamera() {
    const duration = 600;
    const startTime = Date.now();
    const startZoom = camera.zoom;
    const startX = camera.x;
    const startY = camera.y;
    
    function animateReset() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        
        camera.zoom = startZoom + (1 - startZoom) * eased;
        camera.x = startX + (0 - startX) * eased;
        camera.y = startY + (0 - startY) * eased;
        
        if (progress < 1) {
            requestAnimationFrame(animateReset);
        }
    }
    
    animateReset();
    selectedNode = null;
}

async function search() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
        resetCamera();
        searchResults = [];
        displayResults([]);
        return;
    }
    
    const results = dataset
        .map(item => {
            const searchText = `${item.title} ${item.description} ${item.tags.join(' ')} ${item.category}`.toLowerCase();
            const queryWords = query.toLowerCase().split(' ');
            const score = queryWords.reduce((acc, word) => 
                acc + (searchText.includes(word) ? 1 : 0), 0) / queryWords.length;
            
            return {
                ...item,
                score: score + (item.llm_keywords?.toLowerCase().includes(query.toLowerCase()) ? 0.3 : 0)
            };
        })
        .filter(item => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 5);
    
    searchResults = results;
    displayResults(results);
    
    if (results.length > 0) {
        zoomToNode(results[0].id);
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-title">No results found</div>
                <div class="empty-state-text">Try a different search query</div>
            </div>
        `;
        return;
    }
    
    resultsDiv.innerHTML = results.map((item, index) => `
        <div class="result-item ${index === 0 ? 'active' : ''}" onclick="zoomToNode(${item.id})">
            <div class="result-header">
                <div class="result-title">${item.title}</div>
                <div class="result-score">${(item.score * 100).toFixed(0)}%</div>
            </div>
            <div class="result-meta">
                <span>${item.category}</span>
                <span>$${item.metadata.price}</span>
                <span>${item.metadata.rating}/5</span>
            </div>
            <div class="result-description">${item.description}</div>
            <div class="result-tags">
                ${item.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// Mouse interaction
canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomSpeed = 0.1;
    const delta = e.deltaY > 0 ? -zoomSpeed : zoomSpeed;
    camera.zoom = Math.max(0.5, Math.min(5, camera.zoom + delta));
});

let isDragging = false;
let lastMouse = { x: 0, y: 0 };

canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    lastMouse = { x: e.clientX, y: e.clientY };
});

canvas.addEventListener('mousemove', (e) => {
    if (isDragging) {
        const dx = (e.clientX - lastMouse.x) / (camera.zoom * 300);
        const dy = (e.clientY - lastMouse.y) / (camera.zoom * 300);
        camera.x -= dx;
        camera.y -= dy;
        lastMouse = { x: e.clientX, y: e.clientY };
    }
});

canvas.addEventListener('mouseup', () => {
    isDragging = false;
});

canvas.addEventListener('mouseleave', () => {
    isDragging = false;
});

init();

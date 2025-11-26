# How to Add Images to README

## Method 1: Using GitHub (Recommended)

### Step 1: Create Images Folder
```bash
mkdir images
```

### Step 2: Add Your Screenshots
Take screenshots and save them:
- `images/ui-screenshot.png` - Main UI screenshot
- `images/search-demo.gif` - Animated search demo
- `images/vector-space.png` - Vector visualization

### Step 3: Update README.md
Uncomment and use these lines in README.md:

```markdown
![VENTI UI](images/ui-screenshot.png)
![Search Demo](images/search-demo.gif)
![Vector Space](images/vector-space.png)
```

### Step 4: Commit and Push
```bash
git add images/
git commit -m "Add screenshots"
git push
```

## Method 2: Using External URLs

If images are hosted elsewhere (e.g., imgur, your website):

```markdown
![VENTI UI](https://your-url.com/screenshot.png)
```

## Recommended Screenshots

### 1. Main UI Screenshot
**What to capture**: Full browser window showing:
- Left panel with search results
- Right panel with vector visualization
- Header with stats

**How to take**:
1. Run `./launch.sh`
2. Open http://localhost:8000
3. Search for "wireless headphones"
4. Take full-screen screenshot
5. Save as `images/ui-screenshot.png`

### 2. Search Demo GIF
**What to capture**: Animated demo showing:
1. Typing a query
2. Results appearing
3. Clicking a result
4. Zoom animation to node

**Tools**:
- Mac: Use QuickTime Screen Recording → Convert to GIF
- Windows: Use ScreenToGif
- Online: CloudConvert (MP4 to GIF)

**Save as**: `images/search-demo.gif`

### 3. Vector Space Close-up
**What to capture**: Zoomed-in view showing:
- Nodes with labels
- Category clustering
- Selected node highlighted

**How to take**:
1. Search for something
2. Zoom in on the canvas
3. Take screenshot
4. Save as `images/vector-space.png`

## Image Optimization

Before adding to repository:

### Compress Images
```bash
# Using ImageOptim (Mac)
# Or use online tools like TinyPNG

# Target sizes:
# - PNG screenshots: < 500KB
# - GIF demos: < 2MB
```

### Recommended Dimensions
- Full UI screenshot: 1920x1080 or 1440x900
- Vector space: 800x600
- GIF demo: 1280x720 (max 10 seconds)

## Markdown Image Syntax

### Basic Image
```markdown
![Alt Text](path/to/image.png)
```

### Image with Link
```markdown
[![Alt Text](path/to/image.png)](https://link-url.com)
```

### Image with Size (HTML)
```markdown
<img src="path/to/image.png" width="600" alt="Alt Text">
```

### Centered Image (HTML)
```markdown
<p align="center">
  <img src="path/to/image.png" width="800" alt="Alt Text">
</p>
```

## Example README Structure with Images

```markdown
# VENTI - Hybrid Search Engine

<p align="center">
  <img src="images/ui-screenshot.png" width="800" alt="VENTI UI">
</p>

## Features

### Interactive Search
![Search Demo](images/search-demo.gif)

### Vector Visualization
<p align="center">
  <img src="images/vector-space.png" width="600" alt="Vector Space">
</p>
```

## Quick Screenshot Checklist

Before taking screenshots:

- [ ] UI is clean (no debug info)
- [ ] Search has relevant results
- [ ] Vector space is zoomed appropriately
- [ ] Browser window is full-screen
- [ ] No personal information visible
- [ ] Good lighting/contrast

## Alternative: Use Badges Instead

If you don't want to add images, use badges:

```markdown
![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-production-green)
![License](https://img.shields.io/badge/license-MIT-green)
```

## Current README Image Placeholders

The README.md currently has these commented placeholders:

1. Line 6: `<!-- ![VENTI UI](images/ui-screenshot.png) -->`
2. Line 28: `<!-- ![Search Demo](images/search-demo.gif) -->`
3. Line 115: `<!-- ![Vector Space](images/vector-space.png) -->`

To activate them:
1. Create `images/` folder
2. Add your screenshots
3. Uncomment the lines (remove `<!--` and `-->`)
4. Commit and push

## Pro Tips

1. **Use descriptive alt text** for accessibility
2. **Optimize file sizes** before committing
3. **Use relative paths** for portability
4. **Test on GitHub** after pushing
5. **Consider dark mode** users (use light backgrounds)

---

**Note**: Images are optional but highly recommended for showcasing your UI!

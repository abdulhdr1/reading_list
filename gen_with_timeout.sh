#!/bin/bash
# Generate images with proper macOS-compatible timeout
export GEMINI_API_KEY="AIzaSyDgRiAEFxyGdQLhZQMtk1EmfQco4wOyqIc"
TOOL="/Users/abdul/.asdf/installs/nodejs/25.6.1/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py"
IMAGES="/Users/abdul/.openclaw/workspace/reading_list/images"
TIMEOUT=90

cd /Users/abdul/.openclaw/workspace/reading_list

# Get all slugs that need images
python3 -c "
import json, hashlib, os
with open('data/links.json') as f:
    items = json.load(f)
for item in items:
    s = hashlib.md5(item['url'].split('?')[0].encode()).hexdigest()[:10]
    if not os.path.exists(f'images/{s}.png'):
        tags = item.get('tags', [])
        primary = tags[0] if tags else 'engineering'
        print(f'{s}|{primary}')
" > /tmp/slugs_to_gen.txt

TOTAL=$(wc -l < /tmp/slugs_to_gen.txt | tr -d ' ')
echo "Generating $TOTAL images..."
COUNT=0

get_visual() {
    case "$1" in
        ai) echo "glowing geometric nodes connected by thin luminous lines";;
        startup) echo "ascending angular forms reaching upward";;
        engineering) echo "interlocking mechanical gears and precise grid patterns";;
        design) echo "flowing organic curves intersecting with sharp geometric shapes";;
        frontend) echo "layered translucent rectangles with rounded corners";;
        product) echo "concentric circles radiating outward like ripples";;
        leadership) echo "a singular bold form standing above smaller shapes";;
        career) echo "a winding path through abstract landscape of geometric hills";;
        culture) echo "overlapping circles forming a mosaic pattern";;
        marketing) echo "radiating arrows and expanding wave patterns";;
        productivity) echo "stacked horizontal bars in ascending order";;
        vc) echo "diamond shapes arranged in a constellation pattern";;
        *) echo "abstract geometric composition";;
    esac
}

while IFS='|' read -r slug tag; do
    [ -z "$slug" ] && continue
    COUNT=$((COUNT + 1))
    
    # Skip if already exists (in case of restart)
    [ -f "$IMAGES/${slug}.png" ] && echo "[$COUNT/$TOTAL] $slug ⏭ exists" && continue
    
    VISUAL=$(get_visual "$tag")
    PROMPT="Minimalist abstract editorial illustration. ${VISUAL}. Warm muted palette: amber, terracotta, sage, cream, charcoal. No text, no words, no letters. Clean modern magazine feel. Subtle paper texture."
    
    echo -n "[$COUNT/$TOTAL] $slug ($tag) ... "
    
    # Run with background + kill after timeout
    uv run "$TOOL" --prompt "$PROMPT" --filename "$IMAGES/${slug}.png" --resolution 1K > /dev/null 2>&1 &
    PID=$!
    
    # Wait with timeout
    ELAPSED=0
    while kill -0 $PID 2>/dev/null; do
        sleep 1
        ELAPSED=$((ELAPSED + 1))
        if [ $ELAPSED -ge $TIMEOUT ]; then
            kill -9 $PID 2>/dev/null
            wait $PID 2>/dev/null
            break
        fi
    done
    wait $PID 2>/dev/null
    
    if [ -f "$IMAGES/${slug}.png" ]; then
        echo "✓ $(du -k "$IMAGES/${slug}.png" | cut -f1)KB"
    else
        echo "✗ timeout/fail, retry..."
        sleep 10
        
        uv run "$TOOL" --prompt "$PROMPT" --filename "$IMAGES/${slug}.png" --resolution 1K > /dev/null 2>&1 &
        PID=$!
        ELAPSED=0
        while kill -0 $PID 2>/dev/null; do
            sleep 1
            ELAPSED=$((ELAPSED + 1))
            if [ $ELAPSED -ge $TIMEOUT ]; then
                kill -9 $PID 2>/dev/null
                wait $PID 2>/dev/null
                break
            fi
        done
        wait $PID 2>/dev/null
        
        if [ -f "$IMAGES/${slug}.png" ]; then
            echo "  ✓ retry success"
        else
            echo "  ⚠ skipped"
        fi
    fi
    
    sleep 5
done < /tmp/slugs_to_gen.txt

echo "Done! $(ls $IMAGES/*.png | wc -l) total images"

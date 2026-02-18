#!/bin/bash
# Generate images for reading list articles
export GEMINI_API_KEY="AIzaSyDgRiAEFxyGdQLhZQMtk1EmfQco4wOyqIc"
TOOL="/Users/abdul/.asdf/installs/nodejs/25.6.1/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py"
IMAGES="/Users/abdul/.openclaw/workspace/reading_list/images"

# Get all slugs that need images
cd /Users/abdul/.openclaw/workspace/reading_list
SLUGS=$(python3 -c "
import json, hashlib
with open('data/links.json') as f:
    items = json.load(f)
import os
for item in items:
    s = hashlib.md5(item['url'].split('?')[0].encode()).hexdigest()[:10]
    if not os.path.exists(f'images/{s}.png'):
        tags = item.get('tags', [])
        primary = tags[0] if tags else 'engineering'
        print(f'{s}|{primary}')
")

TAG_AI="glowing geometric nodes connected by thin luminous lines"
TAG_STARTUP="ascending angular forms reaching upward"
TAG_ENGINEERING="interlocking mechanical gears and precise grid patterns"
TAG_DESIGN="flowing organic curves intersecting with sharp geometric shapes"
TAG_FRONTEND="layered translucent rectangles with rounded corners"
TAG_PRODUCT="concentric circles radiating outward like ripples"
TAG_LEADERSHIP="a singular bold form standing above smaller shapes"
TAG_CAREER="a winding path through abstract landscape of geometric hills"
TAG_CULTURE="overlapping circles forming a mosaic pattern"
TAG_MARKETING="radiating arrows and expanding wave patterns"
TAG_PRODUCTIVITY="stacked horizontal bars in ascending order"
TAG_VC="diamond shapes arranged in a constellation pattern"

get_visual() {
    case "$1" in
        ai) echo "$TAG_AI";;
        startup) echo "$TAG_STARTUP";;
        engineering) echo "$TAG_ENGINEERING";;
        design) echo "$TAG_DESIGN";;
        frontend) echo "$TAG_FRONTEND";;
        product) echo "$TAG_PRODUCT";;
        leadership) echo "$TAG_LEADERSHIP";;
        career) echo "$TAG_CAREER";;
        culture) echo "$TAG_CULTURE";;
        marketing) echo "$TAG_MARKETING";;
        productivity) echo "$TAG_PRODUCTIVITY";;
        vc) echo "$TAG_VC";;
        *) echo "abstract geometric composition";;
    esac
}

COUNT=0
TOTAL=$(echo "$SLUGS" | wc -l | tr -d ' ')
echo "Generating $TOTAL images..."

echo "$SLUGS" | while IFS='|' read -r slug tag; do
    [ -z "$slug" ] && continue
    COUNT=$((COUNT + 1))
    
    VISUAL=$(get_visual "$tag")
    PROMPT="Minimalist abstract editorial illustration. ${VISUAL}. Warm muted palette: amber, terracotta, sage, cream, charcoal. No text, no words, no letters. Clean modern magazine feel. Subtle paper texture."
    
    echo "[$COUNT/$TOTAL] $slug ($tag)"
    
    uv run "$TOOL" --prompt "$PROMPT" --filename "$IMAGES/${slug}.png" --resolution 1K > /dev/null 2>&1
    
    if [ -f "$IMAGES/${slug}.png" ]; then
        echo "  ✓ created"
    else
        echo "  ✗ failed, retrying..."
        sleep 15
        uv run "$TOOL" --prompt "$PROMPT" --filename "$IMAGES/${slug}.png" --resolution 1K > /dev/null 2>&1
        if [ -f "$IMAGES/${slug}.png" ]; then
            echo "  ✓ created (retry)"
        else
            echo "  ⚠ skipped"
        fi
    fi
    
    sleep 5
done
echo "Done!"

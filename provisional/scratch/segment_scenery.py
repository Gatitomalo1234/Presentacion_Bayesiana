from PIL import Image
import os

def segment_scenery(input_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    alpha = img.getchannel('A')
    
    # We'll use a flood-fill or connected components approach to find objects
    visited = set()
    objects = []
    
    data = alpha.load()
    
    for y in range(h):
        for x in range(w):
            if data[x, y] > 0 and (x, y) not in visited:
                # New object found, find its bounds
                q = [(x, y)]
                visited.add((x, y))
                min_x, min_y = x, y
                max_x, max_y = x, y
                
                # Simple BFS to find the whole island
                idx = 0
                while idx < len(q):
                    cx, cy = q[idx]
                    idx += 1
                    min_x = min(min_x, cx)
                    min_y = min(min_y, cy)
                    max_x = max(max_x, cx)
                    max_y = max(max_y, cy)
                    
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and data[nx, ny] > 0 and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            q.append((nx, ny))
                
                # Save object if it's large enough
                if (max_x - min_x) > 5 and (max_y - min_y) > 5:
                    obj_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
                    objects.append(obj_img)

    # Save the interesting ones with meaningful names
    # We'll manually name the most obvious ones by index
    # Based on the view_file output:
    # 0: Sword in stone, 1: Rocks, 2: Gargoyles... etc.
    # Note: BFS order depends on scanline, so we'll just save them all
    for i, obj in enumerate(objects):
        obj.save(os.path.join(output_dir, f"scenery_{i}.png"))
    
    print(f"Extracted {len(objects)} scenery objects to {output_dir}")

if __name__ == "__main__":
    input_file = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/PIXEL ART/misc_scenery.png"
    output_dir = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/PIXEL ART/extracted"
    segment_scenery(input_file, output_dir)

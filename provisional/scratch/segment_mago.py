from PIL import Image
import os

def is_bg(pixel, bg_color, tol=20):
    return all(abs(pixel[i] - bg_color[i]) < tol for i in range(3))

def extract_clean_sheet(input_path, output_path, target_size=32):
    img = Image.open(input_path).convert("RGB")
    w, h = img.size
    data = img.load()
    bg_color = data[0, 0]
    
    # Identify active rows and columns
    row_active = [any(not is_bg(data[x, y], bg_color) for x in range(w)) for y in range(h)]
    col_active = [any(not is_bg(data[x, y], bg_color) for y in range(h)) for x in range(w)]
    
    def get_segments(active_list, min_size=10):
        segments = []
        start = None
        for i, active in enumerate(active_list):
            if active and start is None:
                start = i
            elif not active and start is not None:
                if i - start >= min_size:
                    segments.append((start, i))
                start = None
        return segments

    row_segments = get_segments(row_active)
    col_segments = get_segments(col_active)
    
    collected_tiles = []
    for rs, re in row_segments:
        # For each active row, scan columns specifically within that row height
        row_slice_active = [any(not is_bg(data[x, y], bg_color) for y in range(rs, re)) for x in range(w)]
        row_cols = get_segments(row_slice_active)
        
        for cs, ce in row_cols:
            tile = img.crop((cs, rs, ce, re))
            # Skip very thin lines or artifacts
            if tile.size[0] > 15 and tile.size[1] > 15:
                collected_tiles.append(tile)
    
    if not collected_tiles:
        print("No tiles found")
        return

    grid_w = 6
    grid_h = (len(collected_tiles) + grid_w - 1) // grid_w
    new_sheet = Image.new("RGBA", (grid_w * target_size, grid_h * target_size), (0,0,0,0))
    
    for i, tile in enumerate(collected_tiles):
        # Transparency and Centering
        max_dim = max(tile.size)
        square = Image.new("RGBA", (max_dim, max_dim), (0,0,0,0))
        rgba_tile = tile.convert("RGBA")
        
        t_data = rgba_tile.getdata()
        new_data = []
        for item in t_data:
            if is_bg(item, bg_color, 30):
                new_data.append((0, 0, 0, 0))
            else:
                new_data.append(item)
        rgba_tile.putdata(new_data)
        
        square.paste(rgba_tile, ((max_dim - tile.size[0]) // 2, (max_dim - tile.size[1]) // 2))
        small_tile = square.resize((target_size, target_size), Image.NEAREST)
        
        tx = (i % grid_w) * target_size
        ty = (i // grid_w) * target_size
        new_sheet.paste(small_tile, (tx, ty))
        
    new_sheet.save(output_path)
    print(f"Success! Detected {len(collected_tiles)} sprites.")

if __name__ == "__main__":
    input_file = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/mago.png"
    output_file = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/mago_final_sheet.png"
    extract_clean_sheet(input_file, output_file)

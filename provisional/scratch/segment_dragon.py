from PIL import Image
import os

def extract_dragon(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    # Coordinates for the 2048x1152 sheet
    # Format: (x_start, y, x_step, frames, width, height)
    # Estimates based on the 2048 width
    anims = [
        {"name": "idle", "x": 780, "y": 55, "step": 305, "f": 4, "w": 280, "h": 180},
        {"name": "attack", "x": 780, "y": 445, "step": 305, "f": 4, "w": 300, "h": 180},
        {"name": "fire", "x": 920, "y": 860, "step": 0, "f": 1, "w": 300, "h": 100}
    ]

    collected_tiles = []
    
    for anim in anims:
        for i in range(anim["f"]):
            left = anim["x"] + i * anim["step"]
            top = anim["y"]
            tile = img.crop((left, top, left + anim["w"], top + anim["h"]))
            collected_tiles.append(tile)

    # Re-assemble into a clean sheet
    # We'll use 128x128 as a standard "Boss" size for the game
    target_size = 128
    grid_w = 4
    grid_h = (len(collected_tiles) + grid_w - 1) // grid_w
    
    new_sheet = Image.new("RGBA", (grid_w * target_size, grid_h * target_size), (0,0,0,0))
    
    for i, tile in enumerate(collected_tiles):
        # Center in square
        max_dim = max(tile.size)
        square = Image.new("RGBA", (max_dim, max_dim), (0,0,0,0))
        square.paste(tile, ((max_dim - tile.size[0]) // 2, (max_dim - tile.size[1]) // 2))
        
        # Resize to target
        small_tile = square.resize((target_size, target_size), Image.LANCZOS)
        
        tx = (i % grid_w) * target_size
        ty = (i // grid_w) * target_size
        new_sheet.paste(small_tile, (tx, ty))
        
    new_sheet.save(output_path)
    print(f"Assembled {len(collected_tiles)} dragon frames to {output_path}")

if __name__ == "__main__":
    input_file = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/dragon_no_bg.png"
    output_file = "/Users/nicolas/Documents/PRESENTACION BAYESIANA/dragon_sheet.png"
    extract_dragon(input_file, output_file)

#!/usr/bin/env python3
"""
Flatten Unknown Folder

Moves all images from exotic fruit subfolders into the main 'unknown' folder.
This ensures the AI treats all exotic fruits as a single 'unknown' class.
"""

from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).parent.parent
UNKNOWN_DIR = PROJECT_ROOT / "image_data" / "unknown"


def flatten_unknown_folder():
    """Move all images from subfolders to the unknown folder."""
    print("🔄 Flattening unknown folder...")
    print(f"   Target: {UNKNOWN_DIR}")
    
    if not UNKNOWN_DIR.exists():
        print("❌ Error: unknown folder not found")
        return
    
    moved_count = 0
    subfolders_removed = 0
    
    # Find all subfolders
    subfolders = [d for d in UNKNOWN_DIR.iterdir() if d.is_dir()]
    
    if not subfolders:
        print("✅ No subfolders found - already flat!")
        return
    
    print(f"   Found {len(subfolders)} subfolders")
    
    # Move all images from subfolders to main folder
    for subfolder in subfolders:
        print(f"   Processing: {subfolder.name}")
        
        # Get all image files
        images = list(subfolder.glob("*.jpg")) + list(subfolder.glob("*.jpeg")) + list(subfolder.glob("*.png"))
        
        for image in images:
            # Create new filename with subfolder prefix to avoid conflicts
            new_name = f"{subfolder.name}_{image.name}"
            new_path = UNKNOWN_DIR / new_name
            
            # Move image
            shutil.move(str(image), str(new_path))
            moved_count += 1
        
        # Remove empty subfolder
        try:
            subfolder.rmdir()
            subfolders_removed += 1
            print(f"      ✅ Moved {len(images)} images, removed subfolder")
        except OSError as e:
            print(f"      ⚠️  Could not remove subfolder: {e}")
    
    print(f"\n✅ Complete!")
    print(f"   Images moved: {moved_count}")
    print(f"   Subfolders removed: {subfolders_removed}")
    
    # Count final images
    final_images = list(UNKNOWN_DIR.glob("*.jpg")) + list(UNKNOWN_DIR.glob("*.jpeg")) + list(UNKNOWN_DIR.glob("*.png"))
    print(f"   Total images in unknown/: {len(final_images)}")


if __name__ == "__main__":
    flatten_unknown_folder()

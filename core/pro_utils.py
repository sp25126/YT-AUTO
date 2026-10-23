import os
import cv2
import numpy as np

def create_smooth_bottom_gradient_png(out_png: str = "temp/smooth_vignette.png") -> str:
    """
    Creates a 1080x1920 RGBA PNG with a butter-smooth cubic alpha gradient
    from y=1050 (0% opacity) to y=1920 (88% opacity).
    Completely eliminates the ugly horizontal drawbox cut line!
    """
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    h, w = 1920, 1080
    rgba = np.zeros((h, w, 4), dtype=np.uint8)

    start_y = 1050
    for y in range(start_y, h):
        prog = (y - start_y) / float(h - start_y)
        # Smooth cubic/exponential curve so there is NEVER a visible seam
        alpha = int(225 * (prog ** 1.8))
        rgba[y, :, 3] = alpha

    cv2.imwrite(out_png, rgba)
    return out_png

def clean_spoken_words(words: list) -> list:
    """Fixes broken podcast stutters like 'net.' -> 'network' so captions read cleanly."""
    cleaned = []
    fixes = {"net.": "network", "net": "network", "cat": ""}
    for w in words:
        raw = w["word"].strip()
        low = raw.lower().strip(".,?!")
        if low in fixes:
            if fixes[low] == "":
                continue
            w = {**w, "word": fixes[low]}
        cleaned.append(w)
    return cleaned

import os
import subprocess

OUT_DIR = r"C:\Users\saumy\.gemini\antigravity-ide\brain\81220eb9-52be-4b9a-b578-1814f56cbf14"
VID_DIR = r"c:\Users\saumy\OneDrive\Desktop\YT\outputs\5_viral_styles"

videos = {
    "style1": ("01_IG_Luxury_Glass.mp4", [1.0, 3.5, 11.5, 22.0]),
    "style2": ("02_DaVinci_Fusion_Editorial.mp4", [3.5, 11.2, 11.8, 22.5]),
    "style3": ("03_Curved_Cinema_Pyramid.mp4", [1.5, 4.0, 12.0, 23.0]),
    "style4": ("04_Vox_Pro_Documentary.mp4", [3.5, 12.0, 22.5, 29.0]),
    "style5": ("05_MarkSoy_MixedMedia_Wrapper.mp4", [3.5, 11.8, 22.5, 29.0])
}

for prefix, (fname, timestamps) in videos.items():
    vpath = os.path.join(VID_DIR, fname)
    if not os.path.exists(vpath):
        print(f"Missing {vpath}")
        continue
    for ts in timestamps:
        out_jpg = os.path.join(OUT_DIR, f"verify_{prefix}_{ts:.1f}s.jpg")
        cmd = [
            "ffmpeg", "-y", "-ss", str(ts), "-i", vpath,
            "-vframes", "1", "-q:v", "2", out_jpg
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted {out_jpg}")

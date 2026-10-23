import os
import subprocess

COMPOSITIONS = [
    # Style 1 Pills
    ("Style1-Pill1", "temp/style1_pill1.mp4"),
    ("Style1-Pill2", "temp/style1_pill2.mp4"),
    ("Style1-Pill3", "temp/style1_pill3.mp4"),
    ("Style1-Pill4", "temp/style1_pill4.mp4"),
    # Style 2 Paper
    ("Style2-Paper1", "temp/style2_paper1.mp4"),
    ("Style2-Paper2", "temp/style2_paper2.mp4"),
    # Style 4 Vox
    ("Style4-BarChart", "temp/style4_bar.mp4"),
    ("Style4-BellCurve", "temp/style4_curve.mp4"),
    ("Style4-Blueprint", "temp/style4_blue.mp4"),
    # Style 5 Mark Soy
    ("Style5-CardZoom", "temp/style5_card.mp4"),
    ("Style5-CornerBlocks", "temp/style5_blocks.mp4"),
    ("Style5-CreamSerif1", "temp/style5_cream1.mp4"),
    ("Style5-CreamSerif2", "temp/style5_cream2.mp4"),
]

def render_all():
    os.makedirs("temp", exist_ok=True)
    for comp_id, out_file in COMPOSITIONS:
        if os.path.exists(out_file) and os.path.getsize(out_file) > 50000:
            print(f"[OK] Already rendered: {out_file}")
            continue

        print(f"[*] Rendering {comp_id} -> {out_file}...")
        rel_out = os.path.relpath(out_file, "remotion_studio")
        cmd = [
            "npx", "remotion", "render",
            "src/index.ts", comp_id,
            rel_out,
            "--concurrency=6"
        ]
        subprocess.run(cmd, cwd="remotion_studio", shell=True, check=True)
        print(f"[OK] Rendered {comp_id}: {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    render_all()

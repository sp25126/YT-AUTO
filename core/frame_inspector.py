import os
import cv2
import shutil
import numpy as np
import subprocess

ARTIFACTS_DIR = r"C:\Users\saumy\.gemini\antigravity-ide\brain\81220eb9-52be-4b9a-b578-1814f56cbf14"

def generate_qa_inspection_sheet(video_path: str, timestamps: list, out_dir: str = "temp/qa_frames"):
    """
    Extracts exact frames at critical beat timestamps so Claude Code can visually inspect
    every single section for alignment, typography contrast, cutout quality, and VFX fit.
    """
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    thumbs = []
    extracted_files = []

    for idx, t in enumerate(timestamps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ret, frame = cap.read()
        if not ret:
            continue
        f_path = os.path.join(out_dir, f"beat_{idx+1:02d}_at_{t:.1f}s.jpg")
        cv2.imwrite(f_path, frame)
        extracted_files.append(f_path)

        # Mirror copy to artifacts dir for immediate view_file access
        if os.path.exists(ARTIFACTS_DIR):
            art_frame = os.path.join(ARTIFACTS_DIR, f"qa_beat_{idx+1:02d}_{t:.1f}s.jpg")
            cv2.imwrite(art_frame, frame)

        thumb = cv2.resize(frame, (360, 640))
        cv2.rectangle(thumb, (0, 0), (360, 52), (0, 0, 0), -1)
        cv2.putText(thumb, f"Beat {idx+1} ({t:.1f}s)", (14, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 128), 2)
        thumbs.append(thumb)

    cap.release()

    if thumbs:
        cols = 4
        while len(thumbs) % cols != 0:
            thumbs.append(np.zeros((640, 360, 3), dtype=np.uint8))
        rows = [np.hstack(thumbs[i:i+cols]) for i in range(0, len(thumbs), cols)]
        sheet_path = os.path.join(out_dir, "QA_CONTACT_SHEET.jpg")
        cv2.imwrite(sheet_path, np.vstack(rows))
        
        if os.path.exists(ARTIFACTS_DIR):
            shutil.copy(sheet_path, os.path.join(ARTIFACTS_DIR, "QA_CONTACT_SHEET.jpg"))
            
        print(f"[OK] Extracted {len(extracted_files)} beat frames + {sheet_path}")
        return sheet_path, extracted_files
    return "", []

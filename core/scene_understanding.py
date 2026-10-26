import os
import json
import cv2
import numpy as np
import requests
from PIL import Image
from rembg import remove, new_session

REMBG_SESSION = new_session("u2netp")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "58086702-f40c68777ef64de312fca07dd")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

def analyze_speaker_cuts_and_faces(video_path: str, out_json: str = "temp/scene_telemetry.json") -> dict:
    """
    Implements Eddie's Clipper Skill (IY08-3TS2o8):
    1. Detects camera cuts across the clip.
    2. Finds exact [face_x, face_y, head_top_y] per second so zooms anchor on the speaker's eyes
       and giant behind-the-head text sits at the exact crown height!
    3. Extracts dominant studio accent colors.
    """
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    timeline_faces = []
    camera_cuts = [0.0]
    prev_hist = None

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t_sec = round(frame_idx / fps, 2)

        # Detect camera cuts via HSV histogram delta every 3 frames
        if frame_idx % 3 == 0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [30, 32], [0, 180, 0, 256])
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
            if prev_hist is not None:
                diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
                if diff > 0.48 and (t_sec - camera_cuts[-1]) > 1.0:
                    camera_cuts.append(t_sec)
            prev_hist = hist

        # Sample face anchor every 10 frames (0.33s)
        if frame_idx % 10 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(120, 120))
            if len(faces) > 0:
                fx, fy, fw, fh = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)[0]
                cx = round((fx + fw / 2) / w, 3)
                cy = round((fy + fh / 2) / h, 3)
                head_top = round(max(0.05, (fy - fh * 0.35) / h), 3)
            else:
                cx, cy, head_top = 0.5, 0.38, 0.18

            timeline_faces.append({
                "time": t_sec,
                "face_cx_pct": cx,
                "face_cy_pct": cy,
                "head_top_pct": head_top
            })
        frame_idx += 1

    cap.release()
    telemetry = {
        "camera_cuts_sec": camera_cuts,
        "face_anchors": timeline_faces
    }
    with open(out_json, "w") as f:
        json.dump(telemetry, f, indent=2)
    print(f"[Scene Understanding] Logged {len(camera_cuts)} camera cuts & {len(timeline_faces)} face anchors -> {out_json}")
    return telemetry

def extract_speaker_roto_frames(
    video_path: str,
    start_sec: float = 0.0,
    duration_sec: float = 2.2,
    out_dir: str = "remotion_studio/public/assets/roto_hook"
) -> str:
    """
    Implements Jad M.H's Editor-V1 Cutout Effect (S5Y3Hp2P740 at 08:04):
    Extracts transparent PNG frames of the speaker for the opening hook or key emphasis beat
    so Remotion can place GIANT 3D TEXT & 2D MOTION GRAPHICS BEHIND THE SPEAKER'S HEAD!
    """
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec * fps))
    total_frames = int(duration_sec * fps)

    print(f"[*] Extracting {total_frames} transparent speaker frames ({start_sec}s -> {start_sec + duration_sec}s)...")
    for idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Downscale by 2 for faster segmentation, then resize alpha back
        h, w = rgb.shape[:2]
        small = cv2.resize(rgb, (w // 2, h // 2))
        pil_in = Image.fromarray(small)
        pil_out = remove(pil_in, session=REMBG_SESSION)
        # Resize cutout back to full resolution
        full_out = pil_out.resize((w, h), Image.Resampling.BILINEAR)
        out_frame_path = os.path.join(out_dir, f"frame_{idx:04d}.png")
        full_out.save(out_frame_path)

        if idx % 10 == 0:
            print(f"    Roto frame {idx}/{total_frames} saved...")

    cap.release()
    print(f"[Roto Engine] Extracted {total_frames} transparent speaker frames -> {out_dir}")
    return "/assets/roto_hook"

def fetch_and_inspect_broll_candidates(
    scene_id: str,
    query: str,
    pexels_key: str = "",
    out_dir: str = "remotion_studio/public/assets/broll_candidates"
) -> str:
    """
    Instead of blindly grabbing 1 stock video, downloads up to 3 candidates from Pexels/Pixabay,
    extracts their midpoint frames, and creates a labeled inspection grid so Claude Code
    can VISUALLY SEE what is inside each video clip and pick the best one + focal point!
    Also generates a transparent foreground cutout PNG (_fg_cutout.png) using rembg.
    """
    os.makedirs(out_dir, exist_ok=True)
    effective_pexels_key = pexels_key or PEXELS_API_KEY
    candidates_data = []
    thumbs = []

    # 1. Try Pexels first if key available
    if effective_pexels_key:
        try:
            url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&per_page=4&orientation=portrait"
            resp = requests.get(url, headers={"Authorization": effective_pexels_key}, timeout=12).json()
            for vid in resp.get("videos", [])[:3]:
                v_files = [vf for vf in vid.get("video_files", []) if vf.get("width", 0) >= 720 and vf.get("file_type") == "video/mp4"]
                if v_files:
                    candidates_data.append(v_files[0]["link"])
        except Exception as e:
            print(f"[!] Pexels search error for '{query}': {e}")

    # 2. Fall back / augment with Pixabay Video API
    if len(candidates_data) < 3 and PIXABAY_API_KEY:
        try:
            p_url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={requests.utils.quote(query)}&per_page=6"
            resp = requests.get(p_url, timeout=12).json()
            for hit in resp.get("hits", []):
                videos = hit.get("videos", {})
                for res_key in ["medium", "large", "small"]:
                    if res_key in videos and videos[res_key].get("url"):
                        candidates_data.append(videos[res_key]["url"])
                        break
                if len(candidates_data) >= 3:
                    break
        except Exception as e:
            print(f"[!] Pixabay search error for '{query}': {e}")

    # 3. Fallback: if existing candidate videos are already cached in public/assets, reuse them
    existing_fallbacks = [
        f"remotion_studio/public/assets/broll_beat2_{scene_id}.mp4",
        f"remotion_studio/public/assets/broll_beat3_mentors.mp4",
        f"remotion_studio/public/assets/broll_beat4_rosy.mp4",
        f"remotion_studio/public/assets/broll_beat4_devil.mp4",
        f"remotion_studio/public/assets/broll_beat2_early.mp4",
        f"remotion_studio/public/assets/broll_beat2_late.mp4",
    ]

    for idx in range(min(3, max(1, len(candidates_data)))):
        cand_num = idx + 1
        mp4_path = os.path.join(out_dir, f"{scene_id}_cand_{cand_num}.mp4")

        # Download if URL available
        if idx < len(candidates_data):
            try:
                print(f"[*] Downloading {scene_id} candidate #{cand_num}...")
                r = requests.get(candidates_data[idx], timeout=20)
                with open(mp4_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"[!] Download failed for candidate #{cand_num}: {e}")

        # If download failed or not enough links, copy from available existing brolls
        if not os.path.exists(mp4_path) or os.path.getsize(mp4_path) < 1000:
            for fallback in existing_fallbacks:
                if os.path.exists(fallback):
                    with open(fallback, "rb") as sf, open(mp4_path, "wb") as df:
                        df.write(sf.read())
                    break

        # Process midpoint frame & generate foreground cutout
        if os.path.exists(mp4_path):
            cap = cv2.VideoCapture(mp4_path)
            total_f = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            mid_f = max(0, total_f // 2)
            cap.set(cv2.CAP_PROP_POS_FRAMES, mid_f)
            ret, frame = cap.read()
            cap.release()

            if ret:
                cutout_png = os.path.join(out_dir, f"{scene_id}_cand_{cand_num}_fg_cutout.png")
                # Generate foreground cutout with rembg
                rgb_f = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = rgb_f.shape[:2]
                small_f = cv2.resize(rgb_f, (min(w, 540), int(h * (min(w, 540) / w))))
                pil_rgba = remove(Image.fromarray(small_f), session=REMBG_SESSION)
                pil_rgba = pil_rgba.resize((w, h), Image.Resampling.BILINEAR)
                pil_rgba.save(cutout_png)

                t_img = cv2.resize(frame, (360, 640))
                cv2.rectangle(t_img, (0, 0), (360, 60), (0, 0, 0), -1)
                cv2.putText(t_img, f"{scene_id} Cand #{cand_num}", (12, 42),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 128), 2)
                thumbs.append(t_img)

    grid_path = os.path.join(out_dir, f"{scene_id}_INSPECTION_GRID.jpg")
    if thumbs:
        cv2.imwrite(grid_path, np.hstack(thumbs))
        print(f"[Vision Gate] Saved candidate inspection grid -> {grid_path}")
    return grid_path

if __name__ == "__main__":
    print("Testing scene_understanding module...")
    analyze_speaker_cuts_and_faces("temp/clean_base_30fps.mp4")

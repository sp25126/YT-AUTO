import cv2
import numpy as np
import subprocess
import os

class CPUFaceFramingEngine:
    def __init__(self, model_path="assets/models/face_detection_yunet_2023mar.onnx"):
        # Download YuNet ONNX once (only 350 KB):
        # https://github.com/opencv/opencv_zoo/tree/master/models/face_detection_yunet
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            import urllib.request
            url = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
            try:
                print(f"[*] Downloading YuNet ONNX model to {model_path}...")
                urllib.request.urlretrieve(url, model_path)
                print("[OK] YuNet model downloaded.")
            except Exception as e:
                print(f"[!] Warning: Could not download YuNet model: {e}")
            
        if os.path.exists(model_path):
            self.detector = cv2.FaceDetectorYN.create(
                model_path, "", (320, 320), score_threshold=0.6, nms_threshold=0.3, top_k=5000
            )
        else:
            self.detector = None

    def analyze_faces_trajectory(self, video_path: str, start_s: float, duration_s: float):
        """Scans sampled frames on CPU to map speaker coordinates."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 1920, 1080, []
            
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        cap.set(cv2.CAP_PROP_POS_MSEC, start_s * 1000)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1920
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 1080
        if self.detector is not None:
            self.detector.setInputSize((width, height))

        total_frames = int(duration_s * fps)
        trajectories = [] # stores list of detected face centers per sampled frame

        frame_idx = 0
        while frame_idx < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            # Sample every 5th frame for CPU speed
            if frame_idx % 5 == 0:
                detected = []
                if self.detector is not None:
                    try:
                        _, faces = self.detector.detect(frame)
                        if faces is not None:
                            for f in faces:
                                box = f[0:4].astype(int)
                                center_x = box[0] + box[2] // 2
                                center_y = box[1] + box[3] // 2
                                detected.append((center_x, center_y, box[2]))
                    except Exception:
                        pass
                trajectories.append((frame_idx / fps, detected))
            frame_idx += 1
        cap.release()
        return width, height, trajectories

    def compute_crop_filter(self, mode: str, width: int, height: int, trajectories: list, punch_in_times=None):
        """Builds hardware-free FFmpeg crop filter strings based on the chosen mode."""
        target_w = int(height * (9 / 16))
        if target_w % 2 != 0:
            target_w -= 1
        max_x = max(0, width - target_w)

        if mode == "dual_split":
            # Crop left speaker (host) and right speaker (guest), then vstack them
            left_x = int(width * 0.15)
            right_x = int(width * 0.55)
            box_h = height // 2
            return (
                f"[0:v]split=2[top_raw][bot_raw];"
                f"[top_raw]crop={target_w}:{box_h}:{left_x}:0,scale=1080:960[v_top];"
                f"[bot_raw]crop={target_w}:{box_h}:{right_x}:{box_h//2},scale=1080:960[v_bot];"
                f"[v_top][v_bot]vstack[framed_v]"
            )

        elif mode == "smooth_follow":
            # Calculate smoothed X-coordinate using Exponential Moving Average
            centers = []
            for _, faces in trajectories:
                if faces:
                    # Sort by face size to prioritize the closest/main speaker
                    faces.sort(key=lambda item: item[2], reverse=True)
                    centers.append(faces[0][0])
                elif centers:
                    centers.append(centers[-1])
                else:
                    centers.append(width // 2)

            # Apply smoothing
            smooth_x = centers[0] if centers else width // 2
            ema_centers = []
            alpha = 0.08  # Lower alpha produces smoother pans
            for c in centers:
                smooth_x = alpha * c + (1 - alpha) * smooth_x
                crop_x = int(np.clip(smooth_x - target_w // 2, 0, max_x))
                ema_centers.append(crop_x)

            median_x = int(np.median(ema_centers)) if ema_centers else (width - target_w) // 2
            return f"[0:v]crop={target_w}:{height}:{median_x}:0,scale=1080:1920[framed_v]"

        elif mode == "reaction_punch":
            # Dynamic punch-in: scale to 125% during punch_in_times
            base_x = (width - target_w) // 2
            punch_cond = "1"
            if punch_in_times:
                conds = [f"between(t,{p['start']:.2f},{p['end']:.2f})" for p in punch_in_times]
                punch_cond = " + ".join(conds)

            return (
                f"[0:v]crop={target_w}:{height}:{base_x}:0[clean_crop];"
                f"[clean_crop]scale=eval=frame:w='if({punch_cond},1350,1080)':h='if({punch_cond},2400,1920)',"
                f"crop=1080:1920[framed_v]"
            )

        else: # Default: blurred letterbox background
            return (
                f"[0:v]split=2[bg_raw][fg_raw];"
                f"[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg_blur];"
                f"[fg_raw]scale=1080:-1[fg_crisp];"
                f"[bg_blur][fg_crisp]overlay=(W-w)/2:(H-h)/2[framed_v]"
            )

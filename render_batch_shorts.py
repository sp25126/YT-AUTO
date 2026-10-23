import os
import sys
import json
import subprocess

sys.path.insert(0, os.path.abspath("."))
from core.presets import ARCHETYPE_PRESETS

OUTPUT_DIR = "outputs/FO572"
TEMP_DIR = "temp/clips_test"
SOURCE_VIDEO = "inputs/startup_raj_shamani.mp4"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

CLIPS_DATA = [
    {
        "id": "clip_01",
        "title": "Coders Are The First To Go (The Brutal Truth About AI)",
        "headline": "CODERS ARE FIRST TO BE REPLACED",
        "start": 1655.0,
        "end": 1707.0,
        "archetype": "tech_intellectual",
        "bgm": "dark_synth_drive.mp3",
        "ducking": 0.12,
        "beats": [
            {"start": 0.0, "end": 7.0, "tone": "shock"},
            {"start": 7.0, "end": 28.0, "tone": "neutral"},
            {"start": 28.0, "end": 50.0, "tone": "shock"}
        ],
        "sfx_markers": [
            {"time_rel": 0.5, "effect": "whoosh"},
            {"time_rel": 4.5, "effect": "braam_hit"},
            {"time_rel": 33.0, "effect": "braam_hit"}
        ],
        "silence_windows": [
            {"start_rel": 4.0, "end_rel": 5.5}
        ],
        "yt_title": "Coders Are The First To Go 🚨 | Sravanth Aluru on AI Disruption #shorts",
        "ig_caption": "Are programmers really first on the AI chopping block? 🤯 Sravanth Aluru breaks down why the next decade of software is going through an industrial revolution. \n\nDrop your thoughts in the comments 👇\n\n#rajshamani #figuringout #sravanthaluru #ai #coding #techstartups #futureofwork #shorts",
        "thumbnail_prompt": "Cinematic close-up of Sravanth Aluru looking intensely with futuristic glowing binary code reflections and bold neon text 'CODERS REPLACED FIRST?'"
    },
    {
        "id": "clip_02",
        "title": "AI Is Making People Dumber (Stupidity Is Originality)",
        "headline": "IS AI MAKING US DUMB?",
        "start": 3868.0,
        "end": 3914.0,
        "archetype": "comedy_banter",
        "bgm": "pizzicato_comedy.mp3",
        "ducking": 0.08,
        "beats": [
            {"start": 0.0, "end": 5.0, "tone": "shock"},
            {"start": 5.0, "end": 26.0, "tone": "neutral"},
            {"start": 26.0, "end": 35.0, "tone": "comedy"},
            {"start": 35.0, "end": 46.0, "tone": "shock"}
        ],
        "sfx_markers": [
            {"time_rel": 0.5, "effect": "whoosh"},
            {"time_rel": 2.2, "effect": "record_scratch"},
            {"time_rel": 27.0, "effect": "vinyl_stop"},
            {"time_rel": 41.5, "effect": "pop"}
        ],
        "silence_windows": [
            {"start_rel": 2.0, "end_rel": 3.0},
            {"start_rel": 27.0, "end_rel": 28.5}
        ],
        "yt_title": "Why AI is Making Your Team Dumber 🧠❌ | Sravanth Aluru x Raj Shamani #shorts",
        "ig_caption": "\"Until unless there's an element of stupidity, you don't have an original idea.\" 💡 Why over-relying on AI kills critical judgment in teams.\n\nTag a friend who uses ChatGPT for everything! 😂\n\n#rajshamani #figuringout #ai #originality #entrepreneurship #productivity #chatgpt #startups",
        "thumbnail_prompt": "Shocked expression of Raj Shamani with comic stylized warning icon and big yellow text 'AI MAKES YOU DUMB?'"
    },
    {
        "id": "clip_03",
        "title": "Why 90% of Startups Die (The Brutal Truth About Timing)",
        "headline": "WHY STARTUPS ACTUALLY DIE",
        "start": 2043.0,
        "end": 2088.0,
        "archetype": "hustle_alpha",
        "bgm": "dark_synth_drive.mp3",
        "ducking": 0.14,
        "beats": [
            {"start": 0.0, "end": 9.0, "tone": "shock"},
            {"start": 9.0, "end": 30.0, "tone": "neutral"},
            {"start": 30.0, "end": 45.0, "tone": "shock"}
        ],
        "sfx_markers": [
            {"time_rel": 0.5, "effect": "whoosh"},
            {"time_rel": 3.8, "effect": "braam_hit"},
            {"time_rel": 6.8, "effect": "braam_hit"},
            {"time_rel": 22.0, "effect": "whoosh"}
        ],
        "silence_windows": [
            {"start_rel": 6.5, "end_rel": 8.0}
        ],
        "yt_title": "Startups Don't Die From Bad Ideas... It's TIMING ⏳ | Raj Shamani #shorts",
        "ig_caption": "Most startups don't fail because the idea was bad—they die because of WRONG TIMING. Too early or too late. Here's how to evaluate when to jump into a new market. 🔥\n\nSave this for your next startup plan 📌\n\n#startupadvice #timing #venturecapital #founder #entrepreneur #rajshamani #figuringout",
        "thumbnail_prompt": "Dramatic split screen of melting clock and startup graph crashing with bold green headline 'WRONG TIMING KILLS STARTUPS'"
    },
    {
        "id": "clip_04",
        "title": "In 1999 HTML Coders Made $1M (AI Will Democratize ML)",
        "headline": "THE $1,000,000 CODER TRAP",
        "start": 5367.0,
        "end": 5415.0,
        "archetype": "tech_intellectual",
        "bgm": "warm_ambient_piano.mp3",
        "ducking": 0.10,
        "beats": [
            {"start": 0.0, "end": 10.0, "tone": "shock"},
            {"start": 10.0, "end": 32.0, "tone": "neutral"},
            {"start": 32.0, "end": 48.0, "tone": "shock"}
        ],
        "sfx_markers": [
            {"time_rel": 0.5, "effect": "whoosh"},
            {"time_rel": 6.5, "effect": "braam_hit"},
            {"time_rel": 25.0, "effect": "whoosh"},
            {"time_rel": 40.0, "effect": "pop"}
        ],
        "silence_windows": [
            {"start_rel": 6.2, "end_rel": 7.5}
        ],
        "yt_title": "In 1999 HTML Coders Made $1,000,000 💰 | The Next AI Crash? #shorts",
        "ig_caption": "In 1999, HTML programmers were offered $1,000,000 salaries. Today, AI writes websites in 5 seconds. The exact same cycle is coming for $100M ML salaries. 📉\n\nAre you prepared for the democratization of AI?\n\n#techhistory #aijobs #machinelearning #softwareengineering #webdev #rajshamani #figuringout",
        "thumbnail_prompt": "Vintage 1999 retro computer screen juxtaposed with futuristic neural network and bold text '$1M FOR HTML CODING?'"
    },
    {
        "id": "clip_05",
        "title": "Your Startup Idea Must Sound Stupid (Paradigm Shifts)",
        "headline": "YOUR IDEA MUST SOUND STUPID",
        "start": 221.0,
        "end": 264.0,
        "archetype": "hustle_alpha",
        "bgm": "dark_synth_drive.mp3",
        "ducking": 0.14,
        "beats": [
            {"start": 0.0, "end": 14.0, "tone": "shock"},
            {"start": 14.0, "end": 32.0, "tone": "neutral"},
            {"start": 32.0, "end": 43.0, "tone": "shock"}
        ],
        "sfx_markers": [
            {"time_rel": 0.5, "effect": "whoosh"},
            {"time_rel": 6.8, "effect": "braam_hit"},
            {"time_rel": 12.0, "effect": "braam_hit"},
            {"time_rel": 30.0, "effect": "whoosh"}
        ],
        "silence_windows": [
            {"start_rel": 6.5, "end_rel": 8.0}
        ],
        "yt_title": "If Your Idea Isn't Called Stupid, It's NOT A Paradigm Shift 🚀 #shorts",
        "ig_caption": "\"If the world already knows your secret, then there is no secret to start with.\" 🧠 Why real breakthrough companies always look ridiculous at the beginning.\n\nShare this with a founder building something unconventional! 🚀\n\n#startups #exponentialgrowth #disruption #businessmindset #rajshamani #figuringout #sravanthaluru",
        "thumbnail_prompt": "High-contrast portrait of Sravanth Aluru gesturing with vibrant electric green typography 'STUPID IDEAS WIN'"
    }
]

def generate_custom_ass(clip_data, words, output_ass):
    dur = clip_data["end"] - clip_data["start"]
    headline = clip_data["headline"]
    beats = clip_data.get("beats", [])
    arch = clip_data.get("archetype", "tech_intellectual")
    
    # Archetype color configs
    if arch == "hustle_alpha":
        hl_color = r"\c&H002BF746&"  # Nuclear Green
    elif arch == "comedy_banter":
        hl_color = r"\c&H0000D4FF&"  # Warm Yellow
    else:
        hl_color = r"\c&H00FFA500&"  # Amber Gold

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BaseTone,Montserrat ExtraBold,76,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H90000000&,-1,0,0,0,100,100,0,0,1,8,3,2,60,60,450,1
Style: Banner,Montserrat Black,50,&H00FFFFFF&,&H00000000&,&H00000000&,&HB0000000&,-1,0,0,0,100,100,2,0,3,6,0,8,40,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    
    # Add headline banner event for full duration
    s_full = "0:00:00.00"
    e_full = f"{int(dur//3600):01d}:{int((dur%3600)//60):02d}:{dur%60:05.2f}"
    lines.append(f"Dialogue: 1,{s_full},{e_full},Banner,,0,0,0,, {headline} ")

    # Add kinetic subtitle chunks
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        line_start = max(0.0, chunk[0]["start"])
        line_end = max(0.1, chunk[-1]["end"])
        mid_time = chunk[0]["start"]

        current_tone = "neutral"
        for beat in beats:
            if beat["start"] <= mid_time <= beat["end"]:
                current_tone = beat.get("tone", "neutral")
                break

        if current_tone == "shock":
            tone_tags = f"{{\\fs88{hl_color}\\i0\\frz0}}"
        elif current_tone == "comedy":
            tone_tags = r"{\fs82\c&H0000D4FF&\i0\frz-3}"
        else:
            tone_tags = r"{\fs76\c&H00FFFFFF&\i0\frz0}"

        s_fmt = f"{int(line_start//3600):01d}:{int((line_start%3600)//60):02d}:{line_start%60:05.2f}"
        e_fmt = f"{int(line_end//3600):01d}:{int((line_end%3600)//60):02d}:{line_end%60:05.2f}"

        karaoke_text = ""
        for w in chunk:
            dur_cs = max(1, int((w["end"] - w["start"]) * 100))
            word_str = w['word'].upper()
            if current_tone == "shock":
                anim = r"{\t(0,80,\fscx120\fscy120)\t(80,180,\fscx100\fscy100)}"
                karaoke_text += f"{{\\k{dur_cs}}}{anim}{word_str} "
            else:
                karaoke_text += f"{{\\k{dur_cs}}}{word_str} "

        lines.append(f"Dialogue: 0,{s_fmt},{e_fmt},BaseTone,,0,0,0,,{tone_tags}{karaoke_text.strip()}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines))
    print(f"Generated ASS: {output_ass}")

def render_clip(clip):
    cid = clip["id"]
    start_t = clip["start"]
    end_t = clip["end"]
    duration = end_t - start_t
    out_mp4 = os.path.join(OUTPUT_DIR, f"{cid}.mp4")
    
    # Load transcript words
    transcript_file = os.path.join(TEMP_DIR, f"{cid}_transcript.json")
    with open(transcript_file, "r", encoding="utf-8") as fp:
        tdata = json.load(fp)
    words = tdata["words"]
    
    # Generate custom ASS
    ass_path = os.path.join(TEMP_DIR, f"{cid}.ass")
    generate_custom_ass(clip, words, ass_path)
    
    # Music & SFX configuration
    bgm_path = os.path.join("assets/music", clip.get("bgm", "chill_lofi.mp3"))
    has_bgm = os.path.exists(bgm_path)
    
    inputs = [
        "-ss", str(start_t), "-t", str(duration), "-i", SOURCE_VIDEO
    ]
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
        
    sfx_library = {
        "record_scratch": "assets/sfx/record_scratch.wav",
        "crickets": "assets/sfx/crickets.wav",
        "braam_hit": "assets/sfx/braam.wav",
        "pop": "assets/sfx/pop.wav",
        "whoosh": "assets/sfx/whoosh.wav",
        "vinyl_stop": "assets/sfx/vinyl_stop.wav"
    }
    
    sfx_inputs_map = {}
    idx = 2 if has_bgm else 1
    for sfx in clip.get("sfx_markers", []):
        eff = sfx.get("effect")
        if eff in sfx_library and os.path.exists(sfx_library[eff]) and eff not in sfx_inputs_map:
            inputs.extend(["-i", sfx_library[eff]])
            sfx_inputs_map[eff] = idx
            idx += 1
            
    # Video Filtergraph (Blurred 9:16 background + 16:9 centered fg + ASS subtitles)
    cfg = ARCHETYPE_PRESETS.get(clip["archetype"], ARCHETYPE_PRESETS["tech_intellectual"])
    fg_filter = f"[fg_raw]scale=1080:-1,{cfg['color_filter']}[fg_graded];"
    clean_ass = os.path.relpath(ass_path).replace("\\", "/")
    
    filter_graph = [
        "[0:v]split=2[bg_raw][fg_raw];",
        "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg_blur];",
        fg_filter,
        "[bg_blur][fg_graded]overlay=(W-w)/2:(H-h)/2[base_canvas];",
        f"[base_canvas]subtitles=filename='{clean_ass}'[v_out];"
    ]
    
    # Audio Filtergraph (BGM with silence drops + SFX delays)
    if has_bgm:
        bgm_vol = clip.get("ducking", 0.12)
        silence_windows = clip.get("silence_windows", [])
        if silence_windows:
            vol_conditions = " * ".join(
                [f"(1-between(t,{w['start_rel']:.2f},{w['end_rel']:.2f}))" for w in silence_windows]
            )
            bgm_filter = f"[1:a]volume=eval=frame:volume='{bgm_vol}*{vol_conditions}'[bgm_processed];"
        else:
            bgm_filter = f"[1:a]volume={bgm_vol}[bgm_processed];"
        filter_graph.append(bgm_filter)
        filter_graph.append("[0:a][bgm_processed]amix=inputs=2:duration=first[speech_bgm];")
    else:
        filter_graph.append("[0:a]acopy[speech_bgm];")
        
    audio_branches = ["[speech_bgm]"]
    for i, sfx in enumerate(clip.get("sfx_markers", [])):
        eff = sfx.get("effect")
        if eff in sfx_inputs_map:
            input_idx = sfx_inputs_map[eff]
            delay_ms = max(0, int(sfx["time_rel"] * 1000))
            branch = f"[sfx_{i}]"
            filter_graph.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},volume=0.45{branch};")
            audio_branches.append(branch)
            
    if len(audio_branches) > 1:
        filter_graph.append(f"{''.join(audio_branches)}amix=inputs={len(audio_branches)}:duration=first[a_out]")
    else:
        filter_graph.append("[speech_bgm]acopy[a_out]")
        
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_graph),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    
    print(f"\n=======================================================")
    print(f"Rendering {cid}: {clip['title']} ({duration:.1f}s)")
    print(f"=======================================================")
    subprocess.run(cmd, check=True)
    print(f"[OK] Rendered {out_mp4}")
    
    # Save clip metadata file
    meta_path = os.path.join(OUTPUT_DIR, f"{cid}_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(clip, f, indent=2)

def main():
    print("=== STARTING BATCH PRODUCTION: 5 VIRAL SHORTS ===")
    for clip in CLIPS_DATA:
        render_clip(clip)
        
    # Write consolidated manifest
    manifest_path = os.path.join(OUTPUT_DIR, "batch_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(CLIPS_DATA, f, indent=2)
    print("\n[ALL COMPLETE] All 5 clips rendered and manifest saved to", manifest_path)

if __name__ == "__main__":
    main()

import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Video,
  Img,
  Easing,
  staticFile,
} from 'remotion';

export interface PhraseGroup {
  start: number;
  end: number;
  words: { word: string; start: number; end: number }[];
}

const POWER_SET = new Set([
  'timing', 'startups', 'die', 'trend', 'wrong', 'early', 'late',
  'right', 'time', 'space', 'learn', 'business', 'one', 'internet',
  'advisor', 'network', 'first', 'people', 'outside', 'rosy', 'devil', 'detail', 'details'
]);

export const MasterpieceShort: React.FC<{
  speakerVideoUrl: string;
  rotoFolderUrl: string;
  // High-res Photo Parallax Plates (Prevents Moving-Video Ghost Cloning!)
  earlyBgImg: string;
  earlyFgCutout: string;
  lateBgImg: string;
  lateFgCutout: string;
  mentorBgImg: string;
  mentorFgCutout: string;
  rosyBgImg: string;
  rosyFgCutout: string;
  detailBgImg: string;
  detailFgCutout: string;
  phrases: PhraseGroup[];
}> = ({
  speakerVideoUrl,
  rotoFolderUrl,
  earlyBgImg,
  earlyFgCutout,
  lateBgImg,
  lateFgCutout,
  mentorBgImg,
  mentorFgCutout,
  rosyBgImg,
  rosyFgCutout,
  detailBgImg,
  detailFgCutout,
  phrases,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // ==========================================================================
  // 1. TRUE 5-LAYER 2.5D PARALLAX ENGINE WITH AFTER-IMAGE ECHO TRAIL
  //    (Uses Blurred BG Plate + Sharp FG Cutout -> ZERO Double-Vision Ghosting!)
  // ==========================================================================
  const renderParallaxDepthScene = (
    bgPlate: string,
    fgCutout: string,
    kickerTag: string,
    heroTitle: string,
    accentHex: string,
    localFrame: number
  ) => {
    const enter = spring({ frame: localFrame, fps, config: { damping: 14, stiffness: 180, mass: 0.8 } });
    // Opposing Z-Depth Camera Curves: Background pushes slowly (1.10 -> 1.02) and blurs,
    // while Foreground pulls toward camera (0.95 -> 1.12) for authentic 3D separation!
    const bgScale = interpolate(localFrame, [0, 80], [1.10, 1.02]);
    const fgScale = interpolate(localFrame, [0, 80], [0.95, 1.12], {
      easing: Easing.bezier(0.22, 1, 0.36, 1),
    });
    const fgSlideY = interpolate(enter, [0, 1], [140, 0]);
    const textSlideY = interpolate(enter, [0, 1], [220, 0]);

    // After-Image Ghost Echo Offsets (Trails 3 & 6 frames behind during entry whip)
    const echo1Y = interpolate(
      spring({ frame: Math.max(0, localFrame - 3), fps, config: { damping: 14, stiffness: 180 } }),
      [0, 1],
      [220, 0]
    );
    const echo2Y = interpolate(
      spring({ frame: Math.max(0, localFrame - 6), fps, config: { damping: 14, stiffness: 180 } }),
      [0, 1],
      [220, 0]
    );

    return (
      <AbsoluteFill style={{ backgroundColor: '#05070B', overflow: 'hidden' }}>
        {/* Z-LAYER 0 (BACKPLATE): Defocused & Darkened Environment Plate (blur=14px prevents ghosting!) */}
        <div
          style={{
            position: 'absolute',
            inset: -40,
            transform: `scale(${bgScale})`,
            filter: 'blur(14px) brightness(0.38) contrast(1.2) saturate(1.1)',
            zIndex: 1,
          }}
        >
          <Img src={bgPlate} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>

        {/* Z-LAYER 1 (ARCHITECTURAL GRID & RADIAL GLOW) */}
        <AbsoluteFill
          style={{
            backgroundImage: `
              radial-gradient(circle at 50% 32%, ${accentHex}38 0%, transparent 62%),
              linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)
            `,
            backgroundSize: '100% 100%, 54px 54px, 54px 54px',
            zIndex: 2,
          }}
        />

        {/* Z-LAYER 2 (AFTER-IMAGE ECHO TRAILS BEHIND HERO TEXT) */}
        {[echo2Y, echo1Y].map((ey, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: 165 + ey,
              width: '100%',
              textAlign: 'center',
              fontSize: 182,
              fontWeight: 900,
              color: 'transparent',
              WebkitTextStroke: `2.5px ${accentHex}`,
              opacity: localFrame < 24 ? (i + 1) * 0.18 : 0,
              letterSpacing: -6,
              zIndex: 3,
            }}
          >
            {heroTitle}
          </div>
        ))}

        {/* Z-LAYER 3 (MIDGROUND HERO TYPOGRAPHY — Sits cleanly in Upper 35% Safe Zone) */}
        <div
          style={{
            position: 'absolute',
            top: 165 + textSlideY,
            width: '100%',
            textAlign: 'center',
            zIndex: 4,
          }}
        >
          <div
            style={{
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: 28,
              fontWeight: 800,
              color: accentHex,
              letterSpacing: 5,
              marginBottom: 8,
              textTransform: 'uppercase',
            }}
          >
            // {kickerTag}
          </div>
          <div
            style={{
              fontSize: 182,
              fontWeight: 900,
              lineHeight: 0.9,
              color: '#FFFFFF',
              letterSpacing: -6,
              textShadow: `0 24px 60px rgba(0,0,0,0.95), 0 0 50px ${accentHex}55`,
            }}
          >
            {heroTitle}
          </div>
        </div>

        {/* Z-LAYER 4 (FOREGROUND ISOLATED SUBJECT CUTOUT — Centered in Lower-Mid Frame y=360..1480) */}
        <div
          style={{
            position: 'absolute',
            top: 360 + fgSlideY,
            left: '50%',
            width: 880,
            height: 1120,
            transform: `translateX(-50%) scale(${fgScale})`,
            filter: `drop-shadow(0 -20px 50px rgba(0,0,0,0.95)) drop-shadow(0 0 28px ${accentHex}35)`,
            zIndex: 6,
          }}
        >
          <Img src={fgCutout} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
        </div>

        {/* Z-LAYER 5 (SMOOTH CINEMA VIGNETTE — Zero Boxed Pills!) */}
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 720,
            background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.88) 48%, #04060A 100%)',
            zIndex: 8,
          }}
        />
      </AbsoluteFill>
    );
  };

  // ==========================================================================
  // 2. BORDERLESS CINEMA SUBTITLES (Zero Stacked Pill Clutter!)
  // ==========================================================================
  const activePhrase = phrases.find((p) => t >= p.start - 0.03 && t <= p.end + 0.14);

  const renderBorderlessSubtitles = () => {
    if (!activePhrase) return null;
    const pop = spring({
      frame: Math.max(0, Math.round((t - activePhrase.start) * fps)),
      fps,
      config: { damping: 13, stiffness: 220 },
    });

    let pIdx = -1;
    activePhrase.words.forEach((w, i) => {
      if (POWER_SET.has(w.word.toLowerCase().replace(/[^a-z0-9]/g, ''))) pIdx = i;
    });

    return (
      <div
        style={{
          position: 'absolute',
          bottom: 210,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'baseline',
          gap: 18,
          transform: `scale(${0.9 + 0.1 * pop})`,
          filter: 'drop-shadow(0 10px 28px rgba(0,0,0,0.98))',
          zIndex: 50,
        }}
      >
        {activePhrase.words.map((w, i) => {
          const isSpokenNow = t >= w.start && t <= w.end + 0.1;
          const isKeyword = i === pIdx;
          return (
            <span
              key={i}
              style={
                isKeyword
                  ? {
                      fontSize: 86,
                      fontFamily: 'Georgia, Playfair Display, serif',
                      fontStyle: 'italic',
                      fontWeight: 700,
                      color: '#FACC15',
                      textShadow: '0 0 32px rgba(250, 204, 21, 0.65)',
                      transform: isSpokenNow ? 'scale(1.08)' : 'scale(1)',
                      display: 'inline-block',
                    }
                  : {
                      fontSize: 72,
                      fontWeight: 900,
                      color: isSpokenNow ? '#FFFFFF' : 'rgba(255,255,255,0.78)',
                      letterSpacing: -2,
                    }
              }
            >
              {w.word}
            </span>
          );
        })}
      </div>
    );
  };

  // ==========================================================================
  // SECOND-BY-SECOND TIMELINE ROUTER
  // ==========================================================================

  // BEAT 0 (0:00.0 - 0:02.2): LEFT-ALIGNED ROTO HOOK (Never Blocked by Raj's Head on Right!)
  if (t < 2.2) {
    const s = spring({ frame, fps, config: { damping: 13, stiffness: 190 } });
    const rotoIdx = Math.min(64, frame);
    const cleanRotoFolder = rotoFolderUrl.replace(/^\//, '');
    const rotoPng = staticFile(`${cleanRotoFolder}/frame_${String(rotoIdx).padStart(4, '0')}.png`);

    return (
      <AbsoluteFill style={{ backgroundColor: '#05070C', fontFamily: 'Inter, Montserrat, sans-serif' }}>
        <Video src={speakerVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.42)' }} />

        {/* Left-Aligned Stacked Title in the Open Negative Space (x=65..620) so 'TIMING' is 100% Visible! */}
        <div
          style={{
            position: 'absolute',
            top: 210,
            left: 65,
            transform: `translateX(${(1 - s) * -180}px)`,
            zIndex: 3,
          }}
        >
          <div style={{ fontSize: 32, fontWeight: 900, color: '#38BDF8', letterSpacing: 4, marginBottom: 6 }}>
            #1 STARTUP KILLER
          </div>
          <div
            style={{
              fontSize: 185,
              fontWeight: 900,
              color: '#FFFFFF',
              lineHeight: 0.88,
              letterSpacing: -6,
              textShadow: '0 20px 60px rgba(0,0,0,0.95), 0 0 60px rgba(56,189,248,0.55)',
            }}
          >
            TIMING
          </div>
        </div>

        <Img
          src={rotoPng}
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', zIndex: 6 }}
        />
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 640,
            background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 70%, #04060A 100%)',
            zIndex: 8,
          }}
        />
        {renderBorderlessSubtitles()}
      </AbsoluteFill>
    );
  }

  // BEAT 1 (0:02.2 - 0:06.2): PRO FINANCIAL TELEMETRY CHART (Area Gradient + Grid + Glowing Node)
  if (t >= 2.2 && t < 6.2) {
    const lf = Math.round((t - 2.2) * fps);
    const pct = Math.round(interpolate(lf, [3, 45], [0, 90], { extrapolateRight: 'clamp' }));
    const draw = interpolate(lf, [4, 52], [0, 1000], { extrapolateRight: 'clamp', easing: Easing.bezier(0.22, 1, 0.36, 1) });

    return (
      <AbsoluteFill style={{ backgroundColor: '#06080F', fontFamily: 'Inter, Montserrat, sans-serif', padding: '130px 65px' }}>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 28, color: '#FF2E4C', letterSpacing: 4, fontWeight: 800 }}>
            // STARTUP POST-MORTEM DATA
          </div>
          <div style={{ fontSize: 245, fontWeight: 900, color: '#FFF', lineHeight: 0.92, letterSpacing: -8, textShadow: '0 0 70px rgba(255,46,76,0.55)' }}>
            {pct}%
          </div>
          <div style={{ fontSize: 54, fontWeight: 900, color: '#FACC15', letterSpacing: -1, marginBottom: 45 }}>
            DIE FROM WRONG TIMING
          </div>
        </div>

        {/* High-Craft SVG Financial Crash Area Chart */}
        <svg width="950" height="620" viewBox="0 0 950 620">
          <defs>
            <linearGradient id="crashGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#FF2E4C" stopOpacity="0.48" />
              <stop offset="100%" stopColor="#FF2E4C" stopOpacity="0.0" />
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="950" height="620" rx="32" fill="#0B0F1C" stroke="rgba(255,255,255,0.12)" strokeWidth="2.5" />
          {[140, 280, 420].map((gy) => (
            <line key={gy} x1="50" y1={gy} x2="900" y2={gy} stroke="rgba(255,255,255,0.06)" strokeWidth="2" strokeDasharray="10 10" />
          ))}
          <path d="M 70 130 C 280 130, 420 220, 560 390 C 680 510, 780 520, 880 530 L 880 560 L 70 560 Z" fill="url(#crashGrad)" opacity={lf / 45} />
          <path
            d="M 70 130 C 280 130, 420 220, 560 390 C 680 510, 780 520, 880 530"
            fill="none"
            stroke="#FF2E4C"
            strokeWidth="12"
            strokeDasharray="1000"
            strokeDashoffset={1000 - draw}
            strokeLinecap="round"
          />
          <circle cx="880" cy="530" r={lf > 44 ? 18 : 0} fill="#FFFFFF" stroke="#FF2E4C" strokeWidth="8" />
          <text x="80" y="490" fill="#94A3B8" fontSize="28" fontWeight="700">BAD PRODUCT / TREND: 10%</text>
          <text x="80" y="540" fill="#FF2E4C" fontSize="36" fontWeight="900">WRONG MARKET TIMING: 90%</text>
        </svg>

        {renderBorderlessSubtitles()}
      </AbsoluteFill>
    );
  }

  // BEAT 2A (0:10.6 - 0:12.8): 5-LAYER PARALLAX -> "TOO EARLY"
  if (t >= 10.6 && t < 12.8) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {renderParallaxDepthScene(earlyBgImg, earlyFgCutout, 'TRAP 01 // ZERO DEMAND', 'TOO EARLY', '#38BDF8', Math.round((t - 10.6) * fps))}
        {renderBorderlessSubtitles()}
      </>
    );
  }

  // BEAT 2B (0:12.8 - 0:15.4): 5-LAYER PARALLAX -> "CRUSHED"
  if (t >= 12.8 && t < 15.4) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {renderParallaxDepthScene(lateBgImg, lateFgCutout, 'TRAP 02 // MONOPOLIZED', 'CRUSHED', '#FF2E4C', Math.round((t - 12.8) * fps))}
        {renderBorderlessSubtitles()}
      </>
    );
  }

  // BEAT 3 (0:20.8 - 0:26.0): 5-LAYER PARALLAX -> "VETERANS"
  if (t >= 20.8 && t < 26.0) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {renderParallaxDepthScene(mentorBgImg, mentorFgCutout, 'STEP 01 // THE SHIELD', 'VETERANS', '#10B981', Math.round((t - 20.8) * fps))}
        {renderBorderlessSubtitles()}
      </>
    );
  }

  // BEAT 4A (0:27.9 - 0:30.2): 5-LAYER PARALLAX -> "ALL ROSY"
  if (t >= 27.9 && t < 30.2) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {renderParallaxDepthScene(rosyBgImg, rosyFgCutout, 'OUTSIDE ILLUSION', 'ALL ROSY', '#10B981', Math.round((t - 27.9) * fps))}
        {renderBorderlessSubtitles()}
      </>
    );
  }

  // BEAT 4B (0:30.2 - 0:32.85): 5-LAYER PARALLAX -> "DETAILS"
  if (t >= 30.2) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {renderParallaxDepthScene(detailBgImg, detailFgCutout, 'INSIDE REALITY', 'THE DETAILS', '#FACC15', Math.round((t - 30.2) * fps))}
        {renderBorderlessSubtitles()}
      </>
    );
  }

  // TALKING HEAD SEGMENTS (0:06.2-0:10.6, 0:15.4-0:20.8, 0:26.0-0:27.9)
  const zoom = 1.04 + 0.08 * Math.sin(t * 1.4);
  return (
    <AbsoluteFill style={{ backgroundColor: '#000', fontFamily: 'Inter, Montserrat, sans-serif' }}>
      <div style={{ width: '100%', height: '100%', transform: `scale(${zoom})`, transformOrigin: '50% 30%' }}>
        <Video src={speakerVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          width: '100%',
          height: 680,
          background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 70%, #04060A 100%)',
        }}
      />
      {renderBorderlessSubtitles()}
    </AbsoluteFill>
  );
};

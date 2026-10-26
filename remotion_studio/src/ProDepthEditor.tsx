import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Video,
  Img,
  staticFile,
} from 'remotion';

export interface WordToken {
  word: string;
  start: number;
  end: number;
}

const POWER_WORDS = new Set([
  'timing', 'startups', 'die', 'trend', 'wrong', 'early', 'late',
  'right', 'time', 'space', 'learn', 'business', 'one', 'internet',
  'advisor', 'network', 'first', 'people', 'outside', 'rosy', 'devil', 'detail', 'details'
]);

export const ProDepthEditor: React.FC<{
  speakerVideoUrl: string;
  rotoFolderUrl: string;      // "/assets/roto_hook" or "assets/roto_hook"
  brollEarlyVideo: string;
  brollEarlyCutout: string;   // Foreground PNG cutout from the B-roll scene!
  brollLateVideo: string;
  brollLateCutout: string;
  brollMentorVideo: string;
  brollMentorCutout: string;
  brollRosyVideo: string;
  brollRosyCutout: string;
  brollDetailVideo: string;
  brollDetailCutout: string;
  words: WordToken[];
}> = ({
  speakerVideoUrl,
  rotoFolderUrl,
  brollEarlyVideo,
  brollEarlyCutout,
  brollLateVideo,
  brollLateCutout,
  brollMentorVideo,
  brollMentorCutout,
  brollRosyVideo,
  brollRosyCutout,
  brollDetailVideo,
  brollDetailCutout,
  words,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // ==========================================================================
  // HELPER: 3-Layer Depth Sandwich Scene (Video BG + 2D Vector/Text Mid + Cutout FG)
  // ==========================================================================
  const renderDepthSandwichScene = (
    bgVideoUrl: string,
    fgCutoutUrl: string,
    topBadge: string,
    giantBehindText: string,
    subMetricText: string,
    accentColor: string,
    localFrame: number,
    vectorType: 'desert_radar' | 'giant_crush_arrows' | 'network_nodes' | 'rosy_vs_detail_gauge'
  ) => {
    const enterSpring = spring({ frame: localFrame, fps, config: { damping: 14, stiffness: 170 } });
    const bgScale = interpolate(localFrame, [0, 90], [1.02, 1.16]);
    const textRiseY = interpolate(enterSpring, [0, 1], [180, 0]);
    const fgScale = interpolate(localFrame, [0, 90], [1.04, 1.22]); // Foreground moves faster than BG for true 2.5D parallax!
    const svgDraw = interpolate(localFrame, [5, 45], [0, 1000], { extrapolateRight: 'clamp' });

    return (
      <AbsoluteFill style={{ backgroundColor: '#05070B', overflow: 'hidden' }}>
        {/* LAYER 0 (BACK, zIndex=1): Moving B-Roll Video + Dark Cinema Tint */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            transform: `scale(${bgScale})`,
            filter: 'brightness(0.52) contrast(1.18) saturate(1.15)',
            zIndex: 1,
          }}
        >
          <Video src={bgVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
        </div>

        {/* LAYER 1 (MIDGROUND A, zIndex=2): 2D Animated Vector Motion Graphics INSIDE the Scene */}
        <svg
          width="1080"
          height="1920"
          viewBox="0 0 1080 1920"
          style={{ position: 'absolute', inset: 0, zIndex: 2 }}
        >
          {/* Subtle 2D Blueprint Crosshairs & Grid Lines */}
          <line x1="540" y1="0" x2="540" y2="1920" stroke="rgba(255,255,255,0.07)" strokeWidth="2" strokeDasharray="12 12" />
          <line x1="0" y1="680" x2="1080" y2="680" stroke="rgba(255,255,255,0.07)" strokeWidth="2" strokeDasharray="12 12" />

          {vectorType === 'desert_radar' && (
            <>
              {/* Animated 2D Radar Sweep Circle Behind Subject */}
              <circle
                cx="540"
                cy="740"
                r={interpolate(enterSpring, [0, 1], [50, 380])}
                fill="none"
                stroke={accentColor}
                strokeWidth="5"
                strokeDasharray="24 14"
                opacity="0.75"
              />
              <circle cx="540" cy="740" r="240" fill={`${accentColor}18`} stroke={accentColor} strokeWidth="3" />
            </>
          )}

          {vectorType === 'giant_crush_arrows' && (
            <>
              {/* Animated 2D Downward Compression Vectors & Red Danger Zone */}
              <path
                d="M 120 350 L 540 820 L 960 350"
                fill="none"
                stroke={accentColor}
                strokeWidth="14"
                strokeDasharray="1000"
                strokeDashoffset={1000 - svgDraw}
                strokeLinecap="round"
              />
              <rect x="140" y="960" width="800" height="18" rx="9" fill={accentColor} opacity="0.85" />
            </>
          )}

          {vectorType === 'network_nodes' && (
            <>
              {/* Animated 2D Node Triangle Connecting Behind the Mentors */}
              <polygon
                points="540,260 180,980 900,980"
                fill="rgba(16, 185, 129, 0.12)"
                stroke="#10B981"
                strokeWidth="6"
                strokeDasharray="16 10"
              />
              <circle cx="540" cy="260" r="22" fill="#10B981" />
              <circle cx="180" cy="980" r="22" fill="#10B981" />
              <circle cx="900" cy="980" r="22" fill="#10B981" />
            </>
          )}

          {vectorType === 'rosy_vs_detail_gauge' && (
            <>
              {/* Animated 2D Trend Curve Dropping into Reality */}
              <path
                d="M 90 880 Q 380 420 540 640 T 990 920"
                fill="none"
                stroke={accentColor}
                strokeWidth="12"
                strokeDasharray="1000"
                strokeDashoffset={1000 - svgDraw}
              />
            </>
          )}
        </svg>

        {/* LAYER 2 (MIDGROUND B, zIndex=3): Giant Typography Tucked BEHIND the Foreground Cutout */}
        <div
          style={{
            position: 'absolute',
            top: 210 + textRiseY,
            width: '100%',
            textAlign: 'center',
            zIndex: 3,
          }}
        >
          <div
            style={{
              display: 'inline-block',
              backgroundColor: 'rgba(8, 12, 20, 0.85)',
              border: `3px solid ${accentColor}`,
              color: accentColor,
              padding: '10px 32px',
              borderRadius: 40,
              fontSize: 30,
              fontWeight: 900,
              letterSpacing: 2,
              marginBottom: 16,
              boxShadow: `0 0 35px ${accentColor}50`,
            }}
          >
            {topBadge}
          </div>

          <div
            style={{
              fontSize: 175,
              fontWeight: 900,
              lineHeight: 0.92,
              color: '#FFFFFF',
              letterSpacing: -5,
              textTransform: 'uppercase',
              textShadow: '0 22px 55px rgba(0,0,0,0.95)',
            }}
          >
            {giantBehindText}
          </div>
        </div>

        {/* LAYER 3 (FOREGROUND, zIndex=6): Subject Cutout Popping IN FRONT of the Text & 2D Graphics! */}
        {fgCutoutUrl && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              transform: `scale(${fgScale})`,
              filter: 'drop-shadow(0 -18px 45px rgba(0,0,0,0.9))',
              zIndex: 6,
            }}
          >
            <Img src={fgCutoutUrl} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
        )}

        {/* LAYER 4 (FOREGROUND HUD CARD & VIGNETTE, zIndex=8) */}
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 760,
            background: 'linear-gradient(180deg, transparent 0%, rgba(5,7,12,0.88) 52%, #05070C 100%)',
            zIndex: 8,
          }}
        />

        <div
          style={{
            position: 'absolute',
            bottom: 430,
            left: '50%',
            transform: `translateX(-50%) scale(${enterSpring})`,
            backgroundColor: 'rgba(13, 18, 30, 0.90)',
            backdropFilter: 'blur(16px)',
            border: `2.5px solid ${accentColor}`,
            borderRadius: 24,
            padding: '18px 42px',
            zIndex: 9,
            boxShadow: '0 20px 50px rgba(0,0,0,0.8)',
          }}
        >
          <span style={{ fontSize: 34, fontWeight: 800, color: '#F8FAFC' }}>{subMetricText}</span>
        </div>
      </AbsoluteFill>
    );
  };

  // ==========================================================================
  // SUBTITLE ENGINE (Semantic Power-Word Gold Italic Serif in Safe Lower Zone)
  // ==========================================================================
  const cleanWords = words.filter((w) => w.start <= 32.85);
  const currentIdx = cleanWords.findIndex((w) => t >= w.start - 0.04 && t <= w.end + 0.18);
  const chunkStart = currentIdx >= 0 ? Math.floor(currentIdx / 3) * 3 : -1;
  const activeChunk = chunkStart >= 0 ? cleanWords.slice(chunkStart, chunkStart + 3) : [];

  let highlightIdx = -1;
  activeChunk.forEach((w, idx) => {
    const clean = w.word.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (POWER_WORDS.has(clean)) highlightIdx = idx;
  });

  const renderCaptions = () => {
    if (activeChunk.length === 0) return null;
    return (
      <div
        style={{
          position: 'absolute',
          bottom: 185,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          zIndex: 50,
        }}
      >
        <div
          style={{
            backgroundColor: 'rgba(7, 10, 18, 0.85)',
            backdropFilter: 'blur(14px)',
            padding: '14px 38px 18px',
            borderRadius: 26,
            border: '2px solid rgba(255,255,255,0.14)',
            boxShadow: '0 18px 45px rgba(0,0,0,0.9)',
            display: 'flex',
            alignItems: 'baseline',
            gap: 18,
          }}
        >
          {activeChunk.map((w, i) => (
            <span
              key={i}
              style={
                i === highlightIdx
                  ? {
                      fontSize: 78,
                      fontFamily: 'Georgia, Playfair Display, serif',
                      fontStyle: 'italic',
                      fontWeight: 700,
                      color: '#FACC15',
                      textShadow: '0 0 28px rgba(250, 204, 21, 0.5)',
                    }
                  : {
                      fontSize: 66,
                      fontWeight: 800,
                      color: '#FFFFFF',
                      letterSpacing: -1.5,
                    }
              }
            >
              {w.word}
            </span>
          ))}
        </div>
      </div>
    );
  };

  // ==========================================================================
  // TIMELINE ROUTER ACROSS ALL DIRECTED SCENES
  // ==========================================================================

  // 1. BEAT 0 (0:00.0 - 0:02.2): JAD M.H SPEAKER ROTO "WORD BEHIND HEAD" HOOK!
  if (t < 2.2) {
    const hookSpring = spring({ frame, fps, config: { damping: 13, stiffness: 190 } });
    const rotoIdx = Math.min(64, frame);
    const cleanRotoFolder = rotoFolderUrl.replace(/^\//, '');
    const rotoPng = staticFile(`${cleanRotoFolder}/frame_${String(rotoIdx).padStart(4, '0')}.png`);

    return (
      <AbsoluteFill style={{ backgroundColor: '#05070C', fontFamily: 'Inter, Montserrat, sans-serif' }}>
        {/* Layer 0: Original Speaker Video Darkened in Background */}
        <Video
          src={speakerVideoUrl}
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.45)' }}
        />

        {/* Layer 1: Giant Word "TIMING?" Rising BEHIND Raj Shamani's Head (S5Y3Hp2P740 08:04 Effect!) */}
        <div
          style={{
            position: 'absolute',
            top: 230,
            width: '100%',
            textAlign: 'center',
            transform: `scale(${hookSpring})`,
            zIndex: 3,
          }}
        >
          <div style={{ fontSize: 40, fontWeight: 800, color: '#38BDF8', letterSpacing: 4 }}>
            THE #1 STARTUP KILLER
          </div>
          <div
            style={{
              fontSize: 235,
              fontWeight: 900,
              color: '#FFFFFF',
              lineHeight: 0.9,
              letterSpacing: -6,
              textShadow: '0 0 80px rgba(56, 189, 248, 0.75)',
            }}
          >
            TIMING
          </div>
        </div>

        {/* Layer 2: Rotoscoped Speaker Cutout Standing IN FRONT of the Giant Word! */}
        <Img
          src={rotoPng}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            zIndex: 6,
            filter: 'drop-shadow(0 -12px 35px rgba(0,0,0,0.85))',
          }}
        />

        {renderCaptions()}
      </AbsoluteFill>
    );
  }

  // 2. BEAT 1 (0:02.2 - 0:06.2): FULL-SCREEN 2D VECTOR ANIMATION (90% CRASH TELEMETRY)
  if (t >= 2.2 && t < 6.2) {
    const lf = Math.round((t - 2.2) * fps);
    const count90 = Math.round(interpolate(lf, [4, 48], [0, 90], { extrapolateRight: 'clamp' }));
    const curveDraw = interpolate(lf, [6, 55], [0, 1200], { extrapolateRight: 'clamp' });

    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#070A12',
          backgroundImage: `
            radial-gradient(circle at 50% 35%, rgba(239, 68, 68, 0.22) 0%, transparent 65%),
            linear-gradient(rgba(255,255,255,0.04) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(255,255,255,0.04) 1.5px, transparent 1.5px)
          `,
          backgroundSize: '100% 100%, 48px 48px, 48px 48px',
          fontFamily: 'Inter, Montserrat, sans-serif',
        }}
      >
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />

        <div style={{ padding: '130px 70px', textAlign: 'center' }}>
          <div
            style={{
              display: 'inline-block',
              backgroundColor: 'rgba(239, 68, 68, 0.18)',
              border: '3px solid #EF4444',
              color: '#EF4444',
              padding: '10px 34px',
              borderRadius: 40,
              fontSize: 32,
              fontWeight: 900,
              letterSpacing: 2,
            }}
          >
            ⚠️ AUTOPSY OF FAILED STARTUPS
          </div>

          <div
            style={{
              fontSize: 250,
              fontWeight: 900,
              color: '#FFFFFF',
              lineHeight: 0.95,
              marginTop: 20,
              textShadow: '0 18px 60px rgba(239, 68, 68, 0.6)',
            }}
          >
            {count90}%
          </div>

          <div style={{ fontSize: 58, fontWeight: 900, color: '#FACC15', marginBottom: 40 }}>
            DIE FROM WRONG TIMING
          </div>

          {/* 2D Animated Vector Crash Graph + Comparison Bars */}
          <svg width="940" height="580" viewBox="0 0 940 580" style={{ overflow: 'visible' }}>
            <rect x="0" y="0" width="940" height="580" rx="32" fill="#0F1422" stroke="rgba(255,255,255,0.14)" strokeWidth="3" />
            {/* Animated Plunging Valuation Curve */}
            <path
              d="M 70 140 Q 280 120 420 260 T 860 490"
              fill="none"
              stroke="#EF4444"
              strokeWidth="14"
              strokeDasharray="1200"
              strokeDashoffset={1200 - curveDraw}
              strokeLinecap="round"
            />
            <circle cx="860" cy="490" r={lf > 48 ? 22 : 0} fill="#EF4444" />
            <text x="90" y="420" fill="#94A3B8" fontSize="30" fontWeight="800">BAD IDEA / TREND: ONLY 10%</text>
            <text x="90" y="480" fill="#EF4444" fontSize="38" fontWeight="900">WRONG MARKET TIMING: 90%</text>
          </svg>
        </div>

        {renderCaptions()}
      </AbsoluteFill>
    );
  }

  // 3. BEAT 2A (0:10.6 - 0:12.8): 3-LAYER DEPTH SANDWICH -> "TOO EARLY"
  if (t >= 10.6 && t < 12.8) {
    return (
      <>
        {renderDepthSandwichScene(
          brollEarlyVideo,
          brollEarlyCutout,
          'TRAP #1: PREMATURE ENTRY',
          'TOO EARLY',
          '⏳ Zero Market Demand Ready',
          '#38BDF8',
          Math.round((t - 10.6) * fps),
          'desert_radar'
        )}
        {renderCaptions()}
      </>
    );
  }

  // 4. BEAT 2B (0:12.8 - 0:15.4): 3-LAYER DEPTH SANDWICH -> "TOO LATE (CRUSHED)"
  if (t >= 12.8 && t < 15.4) {
    return (
      <>
        {renderDepthSandwichScene(
          brollLateVideo,
          brollLateCutout,
          'TRAP #2: SATURATED ENTRY',
          'CRUSHED',
          '🏢 Monopolized By Tech Giants',
          '#EF4444',
          Math.round((t - 12.8) * fps),
          'giant_crush_arrows'
        )}
        {renderCaptions()}
      </>
    );
  }

  // 5. BEAT 3 (0:20.8 - 0:26.0): 3-LAYER DEPTH SANDWICH -> "ADVISOR NETWORK"
  if (t >= 20.8 && t < 26.0) {
    return (
      <>
        {renderDepthSandwichScene(
          brollMentorVideo,
          brollMentorCutout,
          'FOUNDER PLAYBOOK #1',
          'VETERANS',
          '🛡️ Talk To 20-Year Operators First',
          '#10B981',
          Math.round((t - 20.8) * fps),
          'network_nodes'
        )}
        {renderCaptions()}
      </>
    );
  }

  // 6. BEAT 4A (0:27.9 - 0:30.2): 3-LAYER DEPTH SANDWICH -> "OUTSIDE: LOOKS ROSY"
  if (t >= 27.9 && t < 30.2) {
    return (
      <>
        {renderDepthSandwichScene(
          brollRosyVideo,
          brollRosyCutout,
          'THE SURFACE ILLUSION',
          'ALL ROSY',
          '✨ What Outsiders See On Social Media',
          '#10B981',
          Math.round((t - 27.9) * fps),
          'rosy_vs_detail_gauge'
        )}
        {renderCaptions()}
      </>
    );
  }

  // 7. BEAT 4B (0:30.2 - 0:32.85): 3-LAYER DEPTH SANDWICH -> "DEVIL IN THE DETAILS"
  if (t >= 30.2) {
    return (
      <>
        {renderDepthSandwichScene(
          brollDetailVideo,
          brollDetailCutout,
          'THE BRUTAL REALITY',
          'DETAILS',
          '🔍 Where Real Startups Live Or Die',
          '#FACC15',
          Math.round((t - 30.2) * fps),
          'rosy_vs_detail_gauge'
        )}
        {renderCaptions()}
      </>
    );
  }

  // 8. DEFAULT TALKING-HEAD SEGMENTS (0:06.2-0:10.6, 0:15.4-0:20.8, 0:26.0-0:27.9)
  // Uses Eddie's Clipper Skill Face-Anchored Zoom + Over-The-Shoulder Kinetic Badges!
  const zoomFactor = 1.05 + 0.09 * Math.sin(t * 1.4);
  const showTooEarlyPill = t >= 6.8 && t < 8.8;
  const showTooLatePill = t >= 7.6 && t < 9.2;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000', fontFamily: 'Inter, Montserrat, sans-serif' }}>
      <div
        style={{
          width: '100%',
          height: '100%',
          transform: `scale(${zoomFactor})`,
          transformOrigin: '50% 32%', // Anchored directly on the speaker's eyes/face!
        }}
      >
        <Video src={speakerVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>

      {/* Over-the-Shoulder Pop-Up Callouts at 0:06.8 ("Either too early or too late") */}
      {showTooEarlyPill && (
        <div
          style={{
            position: 'absolute',
            top: 240,
            left: 65,
            backgroundColor: 'rgba(12, 18, 30, 0.9)',
            border: '3px solid #38BDF8',
            padding: '16px 32px',
            borderRadius: 20,
            fontSize: 34,
            fontWeight: 900,
            color: '#38BDF8',
            boxShadow: '0 20px 45px rgba(0,0,0,0.8)',
          }}
        >
          ⏪ TOO EARLY
        </div>
      )}
      {showTooLatePill && (
        <div
          style={{
            position: 'absolute',
            top: 240,
            right: 65,
            backgroundColor: 'rgba(12, 18, 30, 0.9)',
            border: '3px solid #EF4444',
            padding: '16px 32px',
            borderRadius: 20,
            fontSize: 34,
            fontWeight: 900,
            color: '#EF4444',
            boxShadow: '0 20px 45px rgba(0,0,0,0.8)',
          }}
        >
          TOO LATE ⏩
        </div>
      )}

      {/* Smooth Bottom Feathered Vignette */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          width: '100%',
          height: 680,
          background: 'linear-gradient(180deg, transparent 0%, rgba(5,7,12,0.92) 75%, #05070C 100%)',
        }}
      />

      {renderCaptions()}
    </AbsoluteFill>
  );
};

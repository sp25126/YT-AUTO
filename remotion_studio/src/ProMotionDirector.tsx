import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from 'remotion';

export interface WordToken {
  word: string;
  start: number;
  end: number;
}

const POWER_KEYWORDS = new Set([
  'timing', 'startups', 'die', 'trend', 'wrong', 'early', 'late',
  'right', 'time', 'space', 'learn', 'business', 'one', 'internet',
  'advisor', 'network', 'first', 'people', 'outside', 'rosy', 'devil', 'detail', 'details'
]);

const STOP_WORDS = new Set([
  'a', 'an', 'the', 'of', 'to', 'in', 'on', 'for', 'and', 'or', 'but', 'is', 'are', 'be', 'so', 'that', 'this'
]);

export const ProMotionDirector: React.FC<{
  speakerVideoUrl: string;
  brollEarlyUrl: string;
  brollLateUrl: string;
  brollMentorUrl: string;
  brollRosyUrl: string;
  brollDetailUrl: string;
  words: WordToken[];
}> = ({
  speakerVideoUrl,
  brollEarlyUrl,
  brollLateUrl,
  brollMentorUrl,
  brollRosyUrl,
  brollDetailUrl,
  words,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // ==========================================================================
  // 1. CONTINUOUS SPRING MORPHING BETWEEN MODES (ZERO HARD JUMP CUTS!)
  // ==========================================================================
  // Speaker Fullscreen Windows: [6.2s - 10.6s], [15.4s - 20.8s], [26.0s - 27.9s]
  const inFull1 = spring({ frame: frame - Math.round(6.2 * fps), fps, config: { damping: 15, stiffness: 160 } })
                - spring({ frame: frame - Math.round(10.6 * fps), fps, config: { damping: 15, stiffness: 160 } });
  const inFull2 = spring({ frame: frame - Math.round(15.4 * fps), fps, config: { damping: 15, stiffness: 160 } })
                - spring({ frame: frame - Math.round(20.8 * fps), fps, config: { damping: 15, stiffness: 160 } });
  const inFull3 = spring({ frame: frame - Math.round(26.0 * fps), fps, config: { damping: 15, stiffness: 160 } })
                - spring({ frame: frame - Math.round(27.9 * fps), fps, config: { damping: 15, stiffness: 160 } });

  const fullScreenMorph = Math.min(1, Math.max(0, inFull1 + inFull2 + inFull3));

  // Dual Comparison Windows: [10.6s - 15.4s] and [27.9s - 32.85s]
  const inDual1 = spring({ frame: frame - Math.round(10.6 * fps), fps, config: { damping: 14, stiffness: 170 } })
                - spring({ frame: frame - Math.round(15.4 * fps), fps, config: { damping: 14, stiffness: 170 } });
  const inDual2 = spring({ frame: frame - Math.round(27.9 * fps), fps, config: { damping: 14, stiffness: 170 } });
  const dualShowcaseMorph = Math.min(1, Math.max(0, inDual1 + inDual2));

  // Top Floating Studio Window visibility (Active when neither FullScreen nor DualShowcase is dominant)
  const studioWindowMorph = Math.max(0, 1 - fullScreenMorph - dualShowcaseMorph);

  // Transition Flash Overlay on Mode Switches (Simulates @remotion/effects lightLeak / zoomBlur)
  const cutTimestamps = [6.2, 10.6, 15.4, 20.8, 26.0, 27.9];
  const minDistToCut = Math.min(...cutTimestamps.map((ct) => Math.abs(t - ct)));
  const flashOpacity = minDistToCut < 0.14 ? (1 - minDistToCut / 0.14) * 0.38 : 0;

  // ==========================================================================
  // 2. SEMANTIC SUBTITLE PHRASE & POWER-WORD ENGINE (NEVER HIGHLIGHTS 'A'/'OF')
  // ==========================================================================
  const cleanWords = words.filter((w) => w.start <= 32.85);
  const currentIdx = cleanWords.findIndex((w) => t >= w.start - 0.04 && t <= w.end + 0.18);
  const chunkStart = currentIdx >= 0 ? Math.floor(currentIdx / 3) * 3 : -1;
  const activeChunk = chunkStart >= 0 ? cleanWords.slice(chunkStart, chunkStart + 3) : [];

  // Pick which word in the 3-word chunk gets the Gold/Cyan Italic Serif highlight
  let highlightIdx = -1;
  activeChunk.forEach((w, idx) => {
    const clean = w.word.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (POWER_KEYWORDS.has(clean)) highlightIdx = idx;
  });
  if (highlightIdx === -1 && activeChunk.length > 0) {
    // Fallback: pick the longest non-stopword
    activeChunk.forEach((w, idx) => {
      const clean = w.word.toLowerCase().replace(/[^a-z0-9]/g, '');
      if (!STOP_WORDS.has(clean)) highlightIdx = idx;
    });
  }

  // Dynamic Y-position of subtitle: smoothly moves from y=935 (Studio Seam) to y=1510 (FullScreen/Dual)
  const subtitleY = interpolate(studioWindowMorph, [0, 1], [1510, 935]);

  // ==========================================================================
  // 3. CONTINUOUS SPEAKER CONTAINER GEOMETRY (MORPHS CARD <-> FULLSCREEN)
  // ==========================================================================
  const spkWidth = interpolate(fullScreenMorph, [0, 1], [920, 1080]);
  const spkHeight = interpolate(fullScreenMorph, [0, 1], [800, 1920]);
  const spkBottom = interpolate(fullScreenMorph, [0, 1], [45, 0]);
  const spkRadius = interpolate(fullScreenMorph, [0, 1], [46, 0]);
  const spkScaleDown = interpolate(dualShowcaseMorph, [0, 1], [1, 0.85]);
  const spkOpacity = interpolate(dualShowcaseMorph, [0, 0.85], [1, 0], { extrapolateRight: 'clamp' });

  const isMentorStudio = t >= 18.0;
  const count90 = Math.round(interpolate(t, [0.4, 2.2], [0, 90], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const calloutScale = spring({ frame: Math.max(0, frame - 42), fps, config: { damping: 12, stiffness: 210 } });

  // Dual Showcase Dynamic Center-to-Split Choreography (Fixes the 1.5s Empty Bottom Space!)
  const isRosyDual = t >= 27.0;
  const dualStartSec = isRosyDual ? 27.9 : 10.6;
  const secondCardTriggerSec = isRosyDual ? 29.8 : 12.1;
  const dualLocalFrame = Math.max(0, Math.round((t - dualStartSec) * fps));
  const secondCardProgress = spring({
    frame: Math.max(0, Math.round((t - secondCardTriggerSec) * fps)),
    fps,
    config: { damping: 14, stiffness: 175 },
  });

  // Card 1 starts centered at y=420, then smoothly slides up to y=90 when Card 2 enters!
  const card1Top = interpolate(secondCardProgress, [0, 1], [420, 90]);
  const card1Scale = interpolate(secondCardProgress, [0, 1], [1.05, 1.0]);
  const card2Top = interpolate(secondCardProgress, [0, 1], [1950, 760]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090C14',
        backgroundImage: `
          radial-gradient(circle at 50% 25%, rgba(29, 99, 255, 0.20) 0%, transparent 62%),
          linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)
        `,
        backgroundSize: '100% 100%, 44px 44px, 44px 44px',
        fontFamily: 'Inter, Montserrat, sans-serif',
        overflow: 'hidden',
      }}
    >
      {/* ==================================================================== */}
      {/* LAYER 1: MORPHING SPEAKER CARD <-> FULLSCREEN SPEAKER                */}
      {/* ==================================================================== */}
      <div
        style={{
          position: 'absolute',
          bottom: spkBottom,
          left: '50%',
          width: spkWidth,
          height: spkHeight,
          borderRadius: spkRadius,
          transform: `translateX(-50%) scale(${spkScaleDown})`,
          opacity: spkOpacity,
          overflow: 'hidden',
          border: fullScreenMorph > 0.8 ? 'none' : '3px solid rgba(255,255,255,0.16)',
          boxShadow: '0 -20px 60px rgba(0,0,0,0.75)',
          backgroundColor: '#000',
          zIndex: 10,
        }}
      >
        <Video
          src={speakerVideoUrl}
          style={{
            width: '100%',
            height: fullScreenMorph > 0.5 ? '104%' : '135%',
            objectFit: 'cover',
            objectPosition: '55% 22%',
            transform: `scale(${1.0 + 0.05 * Math.sin(t * 1.3)})`,
          }}
        />
        {/* Feathered Bottom Vignette when Full-Screen so Captions Pop over Blue Jacket */}
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 680,
            opacity: fullScreenMorph,
            background: 'linear-gradient(180deg, transparent 0%, rgba(5,7,12,0.92) 75%, #05070C 100%)',
          }}
        />
      </div>

      {/* ==================================================================== */}
      {/* LAYER 2: TOP FLOATING STUDIO HEADER & INTERACTIVE BROWSER WINDOW     */}
      {/* ==================================================================== */}
      {studioWindowMorph > 0.01 && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            width: '100%',
            opacity: studioWindowMorph,
            transform: `translateY(${(1 - studioWindowMorph) * -420}px) scale(${0.92 + 0.08 * studioWindowMorph})`,
            filter: studioWindowMorph < 0.85 ? `blur(${(1 - studioWindowMorph) * 14}px)` : 'none',
            zIndex: 20,
          }}
        >
          {/* Editorial 2-Line Header */}
          <div style={{ paddingTop: 80, textAlign: 'center' }}>
            <div style={{ fontSize: 50, fontWeight: 800, color: '#F8FAFC', letterSpacing: -1 }}>
              {isMentorStudio ? 'Founder Playbook Step #1' : 'Why 90% Of Startups Collapse'}
            </div>
            <div
              style={{
                display: 'inline-block',
                marginTop: 10,
                backgroundColor: '#1D63FF',
                padding: '6px 34px 12px',
                borderRadius: 14,
                boxShadow: '0 14px 35px rgba(29, 99, 255, 0.45)',
              }}
            >
              <span
                style={{
                  fontSize: 58,
                  fontFamily: 'Georgia, Playfair Display, serif',
                  fontStyle: 'italic',
                  fontWeight: 700,
                  color: '#FFFFFF',
                }}
              >
                {isMentorStudio ? 'Advisor Network' : 'Wrong Timing'}
              </span>
            </div>
          </div>

          {/* Interactive Browser Window */}
          <div
            style={{
              margin: '34px auto 0',
              width: 940,
              height: 590,
              backgroundColor: '#111622',
              borderRadius: 28,
              border: '2.5px solid rgba(255,255,255,0.18)',
              boxShadow: '0 30px 75px rgba(0,0,0,0.75)',
              position: 'relative',
              overflow: 'visible',
            }}
          >
            {/* Traffic Lights Bar */}
            <div
              style={{
                height: 52,
                backgroundColor: '#181F30',
                borderTopLeftRadius: 26,
                borderTopRightRadius: 26,
                display: 'flex',
                alignItems: 'center',
                padding: '0 24px',
                gap: 12,
              }}
            >
              <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#EF4444' }} />
              <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#F59E0B' }} />
              <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#10B981' }} />
              <div
                style={{
                  margin: '0 auto',
                  backgroundColor: '#0D111A',
                  padding: '4px 28px',
                  borderRadius: 8,
                  fontSize: 20,
                  color: '#94A3B8',
                  fontWeight: 600,
                }}
              >
                {isMentorStudio ? 'advisor-shield.io/veterans' : 'startup-autopsy.io/timing-report'}
              </div>
            </div>

            {!isMentorStudio ? (
              <div style={{ padding: '34px 44px' }}>
                <div style={{ display: 'flex', gap: 16, marginBottom: 28 }}>
                  {['Timing Risk 90%', 'Product 7%', 'Trend 3%'].map((pill, i) => (
                    <div
                      key={i}
                      style={{
                        padding: '10px 24px',
                        borderRadius: 30,
                        fontSize: 24,
                        fontWeight: 700,
                        backgroundColor: i === 0 ? 'rgba(29, 99, 255, 0.25)' : 'rgba(255,255,255,0.05)',
                        border: i === 0 ? '2.5px solid #38BDF8' : '1.5px solid rgba(255,255,255,0.12)',
                        color: i === 0 ? '#38BDF8' : '#94A3B8',
                      }}
                    >
                      {pill}
                    </div>
                  ))}
                </div>

                <div style={{ fontSize: 27, color: '#CBD5E1', fontWeight: 700, marginBottom: 10 }}>
                  Startups Killed By Premature Or Late Entry
                </div>
                <div style={{ height: 46, width: '100%', backgroundColor: '#1E293B', borderRadius: 14, overflow: 'hidden', marginBottom: 24 }}>
                  <div style={{ height: '100%', width: `${count90}%`, backgroundColor: '#EF4444', borderRadius: 14 }} />
                </div>

                <div style={{ fontSize: 27, color: '#94A3B8', fontWeight: 600, marginBottom: 10 }}>
                  Startups Killed By Bad Idea / Trend
                </div>
                <div style={{ height: 34, width: '16%', backgroundColor: '#334155', borderRadius: 12 }} />

                {/* Magnifying Pop-Out Callout Card */}
                {t >= 1.4 && (
                  <div
                    style={{
                      position: 'absolute',
                      top: 160,
                      left: '50%',
                      transform: `translateX(-50%) scale(${calloutScale})`,
                      backgroundColor: '#FFFFFF',
                      padding: '26px 52px',
                      borderRadius: 28,
                      boxShadow: '0 35px 90px rgba(0,0,0,0.85), 0 0 0 4px #1D63FF',
                      textAlign: 'center',
                      zIndex: 35,
                    }}
                  >
                    <div style={{ fontSize: 102, fontWeight: 900, color: '#1D63FF', lineHeight: 0.95 }}>
                      {count90}%
                    </div>
                    <div style={{ fontSize: 30, fontWeight: 800, color: '#0F172A', marginTop: 8 }}>
                      die from wrong timing
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div style={{ width: '100%', height: 538, position: 'relative', overflow: 'hidden', borderBottomLeftRadius: 26, borderBottomRightRadius: 26 }}>
                <Video
                  src={brollMentorUrl}
                  style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center 25%' }}
                  muted
                />
                <div
                  style={{
                    position: 'absolute',
                    top: 26,
                    left: 26,
                    backgroundColor: 'rgba(10, 14, 23, 0.9)',
                    border: '2.5px solid #38BDF8',
                    padding: '12px 28px',
                    borderRadius: 30,
                    fontSize: 26,
                    fontWeight: 800,
                    color: '#FFFFFF',
                  }}
                >
                  ✓ 20-Year Industry Veterans
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* LAYER 3: DYNAMIC CENTER-TO-SPLIT SHOWCASE (ZERO EMPTY DEAD SPACE!)   */}
      {/* ==================================================================== */}
      {dualShowcaseMorph > 0.01 && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            opacity: dualShowcaseMorph,
            transform: `scale(${0.92 + 0.08 * dualShowcaseMorph})`,
            zIndex: 30,
          }}
        >
          {/* Card 1: Starts Centered (y=420), Smoothly Slides Up to y=90 when Card 2 Enters */}
          <div
            style={{
              position: 'absolute',
              top: card1Top,
              left: 65,
              width: 950,
              height: 630,
              borderRadius: 32,
              backgroundColor: '#131826',
              border: '3px solid rgba(255,255,255,0.2)',
              overflow: 'hidden',
              boxShadow: '0 30px 70px rgba(0,0,0,0.75)',
              transform: `scale(${card1Scale})`,
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 24,
                left: 24,
                zIndex: 10,
                backgroundColor: 'rgba(15, 23, 42, 0.92)',
                color: '#F8FAFC',
                padding: '10px 26px',
                borderRadius: 14,
                fontSize: 28,
                fontWeight: 800,
                border: '2px solid #38BDF8',
              }}
            >
              {isRosyDual ? '✨ Outside Illusion: Looks All Rosy' : '⏳ Trap #1: Launching Too Early (0 Market)'}
            </div>
            <Video
              src={isRosyDual ? brollRosyUrl : brollEarlyUrl}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                objectPosition: 'center 25%',
                transform: `scale(${1.0 + 0.08 * (dualLocalFrame / 120)})`,
              }}
              muted
            />
          </div>

          {/* Card 2: Whips Up into y=760 right as the second contrast phrase starts */}
          <div
            style={{
              position: 'absolute',
              top: card2Top,
              left: 65,
              width: 950,
              height: 630,
              borderRadius: 32,
              backgroundColor: '#131826',
              border: '3.5px solid #FACC15',
              overflow: 'hidden',
              boxShadow: '0 35px 80px rgba(0,0,0,0.85)',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 24,
                left: 24,
                zIndex: 10,
                backgroundColor: '#1D63FF',
                color: '#FFFFFF',
                padding: '10px 26px',
                borderRadius: 14,
                fontSize: 28,
                fontWeight: 800,
                border: '2px solid #FACC15',
              }}
            >
              {isRosyDual ? '🔍 Inside Reality: The Devil Is In The Details' : '🏢 Trap #2: Too Late (Crushed By Giants)'}
            </div>
            <Video
              src={isRosyDual ? brollDetailUrl : brollLateUrl}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                objectPosition: 'center 20%', // Top-biased so faces/heads are NEVER cropped off!
                transform: `scale(${1.0 + 0.08 * (dualLocalFrame / 120)})`,
              }}
              muted
            />
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* LAYER 4: SEMANTIC POWER-WORD SUBTITLES (100% CONTRAST ON JACKET!)    */}
      {/* ==================================================================== */}
      {activeChunk.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: subtitleY,
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: 16,
            zIndex: 50,
            padding: '0 40px',
          }}
        >
          <div
            style={{
              backgroundColor: 'rgba(8, 11, 18, 0.82)',
              backdropFilter: 'blur(12px)',
              padding: '12px 34px 16px',
              borderRadius: 24,
              border: '2px solid rgba(255,255,255,0.12)',
              boxShadow: '0 14px 36px rgba(0,0,0,0.85)',
              display: 'flex',
              alignItems: 'baseline',
              gap: 16,
            }}
          >
            {activeChunk.map((w, idx) => {
              const isPower = idx === highlightIdx;
              return (
                <span
                  key={idx}
                  style={
                    isPower
                      ? {
                          fontSize: 74,
                          fontFamily: 'Georgia, Playfair Display, serif',
                          fontStyle: 'italic',
                          fontWeight: 700,
                          color: '#FACC15', // High-contrast Warm Gold (never blends into blue jacket!)
                          textShadow: '0 0 24px rgba(250, 204, 21, 0.45)',
                        }
                      : {
                          fontSize: 64,
                          fontWeight: 800,
                          color: '#FFFFFF',
                          letterSpacing: -1.5,
                        }
                  }
                >
                  {w.word}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* LAYER 5: LIGHT-LEAK / ZOOM-BLUR TRANSITION FLASH ON MODE SWITCHES    */}
      {/* ==================================================================== */}
      {flashOpacity > 0.01 && (
        <AbsoluteFill
          style={{
            background: 'radial-gradient(circle, rgba(56, 189, 248, 0.85) 0%, rgba(29, 99, 255, 0.3) 60%, transparent 100%)',
            opacity: flashOpacity,
            mixBlendMode: 'screen',
            zIndex: 60,
          }}
        />
      )}
    </AbsoluteFill>
  );
};

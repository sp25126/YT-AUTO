import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from 'remotion';

export interface WordItem {
  word: string;
  start: number;
  end: number;
}

export const EditorialStudioMaster: React.FC<{
  speakerVideoUrl: string;
  brollEarlyUrl: string;
  brollLateUrl: string;
  brollMentorUrl: string;
  brollRosyUrl: string;
  brollDetailUrl: string;
  words: WordItem[];
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
  // 1. DIRECTED 3-MODE PACING SCHEDULE (Matched to 33.4s Startup Timing Clip)
  // ==========================================================================
  // 0.0s - 6.3s: MODE A (Floating Studio) -> 90% Fail Rate + Magnifying Callout Pop
  // 6.3s - 10.6s: MODE C (Full-Screen Speaker Punch-In) -> "Either too early or too late... How do you pick?"
  // 10.6s - 15.4s: MODE B (Full-Screen 2-Card Comparison Showcase) -> "Too Early" vs "Too Late"
  // 15.4s - 20.8s: MODE C (Full-Screen Speaker Punch-In) -> "Number one, you can't just be on the internet..."
  // 20.8s - 26.2s: MODE A (Floating Studio) -> Interactive Filter Pills + Mentor Video + Cursor Click
  // 26.2s - 28.0s: MODE C (Full-Screen Speaker Punch-In) -> "Because what happens is..."
  // 28.0s - 33.4s: MODE B (Full-Screen 2-Card Comparison Showcase) -> "Outside: Rosy" vs "Inside: The Details"
  const isFullSpeaker =
    (t >= 6.3 && t < 10.6) || (t >= 15.4 && t < 20.8) || (t >= 26.2 && t < 28.0);
  const isDualShowcase = (t >= 10.6 && t < 15.4) || t >= 28.0;

  // Active 2-word phrase for Mixed-Font Editorial Subtitles
  const currentIdx = words.findIndex((w) => t >= w.start && t <= w.end + 0.15);
  const pairStart = currentIdx >= 0 ? Math.floor(currentIdx / 2) * 2 : -1;
  const activePair = pairStart >= 0 ? words.slice(pairStart, pairStart + 2) : [];

  // Studio background with subtle radial spotlight
  const studioBg: React.CSSProperties = {
    backgroundColor: '#0B0E17',
    backgroundImage: `
      radial-gradient(circle at 50% 28%, rgba(29, 99, 255, 0.18) 0%, transparent 60%),
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)
    `,
    backgroundSize: '100% 100%, 44px 44px, 44px 44px',
    width: 1080,
    height: 1920,
    fontFamily: 'Inter, Montserrat, sans-serif',
    overflow: 'hidden',
  };

  // ==========================================================================
  // RENDER HELPER: Nick Automates Mixed-Font Editorial Caption (Sans + Italic Serif)
  // ==========================================================================
  const renderMixedCaption = (yPos: number) => {
    if (activePair.length === 0) return null;
    const firstWord = activePair[0]?.word || '';
    const secondWord = activePair[1]?.word || '';

    return (
      <div
        style={{
          position: 'absolute',
          top: yPos,
          width: '100%',
          textAlign: 'center',
          zIndex: 40,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'baseline',
          gap: 18,
          filter: 'drop-shadow(0 8px 24px rgba(0,0,0,0.85))',
        }}
      >
        <span
          style={{
            fontSize: 68,
            fontWeight: 800,
            color: '#FFFFFF',
            letterSpacing: -1.5,
          }}
        >
          {firstWord}
        </span>
        {secondWord && (
          <span
            style={{
              fontSize: 76,
              fontFamily: 'Georgia, Playfair Display, serif',
              fontStyle: 'italic',
              fontWeight: 700,
              color: '#3B82F6',
            }}
          >
            {secondWord}
          </span>
        )}
      </div>
    );
  };

  // ==========================================================================
  // MODE C: FULL-SCREEN SPEAKER EMPHASIS PUNCH-IN (0:06.3-0:10.6, 0:15.4-0:20.8)
  // ==========================================================================
  if (isFullSpeaker) {
    const pushZoom = 1.04 + 0.08 * Math.sin(t * 1.1);
    return (
      <AbsoluteFill style={{ backgroundColor: '#000' }}>
        <div
          style={{
            width: '100%',
            height: '100%',
            transform: `scale(${pushZoom})`,
          }}
        >
          <Video
            src={speakerVideoUrl}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>
        {/* Smooth bottom vignette for caption contrast */}
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 620,
            background:
              'linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.88) 100%)',
          }}
        />
        {renderMixedCaption(1520)}
      </AbsoluteFill>
    );
  }

  // ==========================================================================
  // MODE B: FULL-SCREEN 2-CARD COMPARISON SHOWCASE (like 0:21 in bHIMNW_4mlg)
  // ==========================================================================
  if (isDualShowcase) {
    const isRosyBeat = t >= 28.0;
    const localFrame = Math.round((t - (isRosyBeat ? 28.0 : 10.6)) * fps);
    const topCardSpring = spring({
      frame: localFrame,
      fps,
      config: { damping: 14, stiffness: 180 },
    });
    const botCardSpring = spring({
      frame: Math.max(0, localFrame - 45),
      fps,
      config: { damping: 14, stiffness: 180 },
    });
    const topLabel = isRosyBeat
      ? 'Outside Illusion: Looks Rosy'
      : 'Trap #1: Launching Too Early';
    const botLabel = isRosyBeat
      ? 'Inside Reality: Devil in the Details'
      : 'Trap #2: Too Late (Crushed by Giants)';
    const vidTop = isRosyBeat ? brollRosyUrl : brollEarlyUrl;
    const vidBot = isRosyBeat ? brollDetailUrl : brollLateUrl;

    return (
      <AbsoluteFill style={studioBg}>
        {/* Keep Original Audio Running Silently via Hidden Video Element */}
        <Video
          src={speakerVideoUrl}
          style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }}
        />
        <div
          style={{
            padding: '90px 65px',
            display: 'flex',
            flexDirection: 'column',
            gap: 36,
          }}
        >
          {/* Top Comparison Window */}
          <div
            style={{
              height: 640,
              borderRadius: 32,
              backgroundColor: '#131826',
              border: '3px solid rgba(255,255,255,0.15)',
              overflow: 'hidden',
              position: 'relative',
              boxShadow: '0 25px 60px rgba(0,0,0,0.65)',
              transform: `scale(${topCardSpring})`,
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 24,
                left: 24,
                zIndex: 10,
                backgroundColor: '#1E293B',
                color: '#FFFFFF',
                padding: '10px 24px',
                borderRadius: 14,
                fontSize: 28,
                fontWeight: 800,
                border: '2px solid rgba(255,255,255,0.2)',
              }}
            >
              {topLabel}
            </div>
            <Video
              src={vidTop}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              muted
            />
          </div>

          {/* Bottom Comparison Window (Pops in on Second Half of Phrase) */}
          <div
            style={{
              height: 640,
              borderRadius: 32,
              backgroundColor: '#131826',
              border: '3px solid #3B82F6',
              overflow: 'hidden',
              position: 'relative',
              boxShadow: '0 30px 70px rgba(29, 99, 255, 0.35)',
              transform: `scale(${botCardSpring})`,
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
                padding: '10px 24px',
                borderRadius: 14,
                fontSize: 28,
                fontWeight: 800,
              }}
            >
              {botLabel}
            </div>
            <Video
              src={vidBot}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              muted
            />
          </div>
        </div>

        {renderMixedCaption(1560)}
      </AbsoluteFill>
    );
  }

  // ==========================================================================
  // MODE A: NICK AUTOMATES 4-ZONE FLOATING STUDIO LAYOUT (0:00-0:06.3 & 0:20.8-0:26.2)
  // ==========================================================================
  const isMentorBeat = t >= 20.8;
  const beatFrame = Math.round((t - (isMentorBeat ? 20.8 : 0.0)) * fps);
  const windowSpring = spring({
    frame: beatFrame,
    fps,
    config: { damping: 14, stiffness: 170 },
  });
  const calloutPop = spring({
    frame: Math.max(0, beatFrame - 48),
    fps,
    config: { damping: 12, stiffness: 210 },
  });

  const countVal = Math.round(
    interpolate(beatFrame, [15, 65], [0, 90], { extrapolateRight: 'clamp' })
  );
  const cursorX = interpolate(beatFrame, [10, 45], [680, 260], {
    extrapolateRight: 'clamp',
  });
  const cursorY = interpolate(beatFrame, [10, 45], [420, 145], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={studioBg}>
      {/* ZONE 1: Top Editorial 2-Line Header with Royal Blue Italic Serif Brush Box */}
      <div style={{ paddingTop: 85, textAlign: 'center', zIndex: 20 }}>
        <div
          style={{
            fontSize: 52,
            fontWeight: 700,
            color: '#F8FAFC',
            letterSpacing: -1,
          }}
        >
          {isMentorBeat
            ? 'Founder Playbook Step #1'
            : 'Why 90% Of Startups Collapse'}
        </div>
        <div
          style={{
            display: 'inline-block',
            marginTop: 10,
            backgroundColor: '#1D63FF',
            padding: '6px 32px 12px',
            borderRadius: 14,
            boxShadow: '0 12px 35px rgba(29, 99, 255, 0.45)',
            transform: `scale(${windowSpring})`,
          }}
        >
          <span
            style={{
              fontSize: 60,
              fontFamily: 'Georgia, Playfair Display, serif',
              fontStyle: 'italic',
              fontWeight: 700,
              color: '#FFFFFF',
            }}
          >
            {isMentorBeat ? 'Advisor Network' : 'Wrong Timing'}
          </span>
        </div>
      </div>

      {/* ZONE 2: Center Interactive macOS Browser Window + Magnifying Callout Pop-Out */}
      <div
        style={{
          margin: '38px auto 0',
          width: 940,
          height: 590,
          backgroundColor: '#111622',
          borderRadius: 28,
          border: '2.5px solid rgba(255,255,255,0.16)',
          boxShadow: '0 30px 70px rgba(0,0,0,0.7)',
          overflow: 'visible',
          position: 'relative',
          transform: `scale(${0.92 + 0.08 * windowSpring})`,
          zIndex: 25,
        }}
      >
        {/* macOS Window Traffic Lights Bar */}
        <div
          style={{
            height: 54,
            backgroundColor: '#181F30',
            borderTopLeftRadius: 26,
            borderTopRightRadius: 26,
            display: 'flex',
            alignItems: 'center',
            padding: '0 24px',
            gap: 12,
            borderBottom: '1px solid rgba(255,255,255,0.08)',
          }}
        >
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: 7,
              backgroundColor: '#EF4444',
            }}
          />
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: 7,
              backgroundColor: '#F59E0B',
            }}
          />
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: 7,
              backgroundColor: '#10B981',
            }}
          />
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
            {isMentorBeat
              ? 'network-audit.ai/veterans'
              : 'startup-autopsy.io/timing-report'}
          </div>
        </div>

        {/* Interactive Window Body */}
        {!isMentorBeat ? (
          <div style={{ padding: '36px 45px' }}>
            {/* Filter Pills like 0:14 in bHIMNW_4mlg */}
            <div style={{ display: 'flex', gap: 16, marginBottom: 32 }}>
              {['Timing Risk 90%', 'Product 7%', 'Trend 3%'].map((pill, i) => (
                <div
                  key={i}
                  style={{
                    padding: '10px 24px',
                    borderRadius: 30,
                    fontSize: 24,
                    fontWeight: 700,
                    backgroundColor:
                      i === 0
                        ? 'rgba(29, 99, 255, 0.25)'
                        : 'rgba(255,255,255,0.05)',
                    border:
                      i === 0
                        ? '2.5px solid #3B82F6'
                        : '1.5px solid rgba(255,255,255,0.12)',
                    color: i === 0 ? '#60A5FA' : '#94A3B8',
                  }}
                >
                  {pill}
                </div>
              ))}
            </div>

            {/* Animated Progress Bars */}
            <div
              style={{
                fontSize: 28,
                color: '#CBD5E1',
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              Startups Killed By Premature Or Late Entry
            </div>
            <div
              style={{
                height: 48,
                width: '100%',
                backgroundColor: '#1E293B',
                borderRadius: 14,
                overflow: 'hidden',
                marginBottom: 28,
              }}
            >
              <div
                style={{
                  height: '100%',
                  width: `${countVal}%`,
                  backgroundColor: '#EF4444',
                  borderRadius: 14,
                }}
              />
            </div>

            <div
              style={{
                fontSize: 28,
                color: '#94A3B8',
                fontWeight: 600,
                marginBottom: 12,
              }}
            >
              Startups Killed By Bad Idea / Trend
            </div>
            <div
              style={{
                height: 36,
                width: '18%',
                backgroundColor: '#334155',
                borderRadius: 12,
              }}
            />

            {/* MAGNIFYING POP-OUT CALLOUT CARD (Exact 0:09 effect from bHIMNW_4mlg!) */}
            {calloutPop > 0.01 && (
              <div
                style={{
                  position: 'absolute',
                  top: 165,
                  left: '50%',
                  transform: `translateX(-50%) scale(${calloutPop})`,
                  backgroundColor: '#FFFFFF',
                  color: '#0F172A',
                  padding: '28px 54px',
                  borderRadius: 28,
                  boxShadow:
                    '0 35px 90px rgba(0,0,0,0.85), 0 0 0 4px #1D63FF',
                  textAlign: 'center',
                  zIndex: 35,
                }}
              >
                <div
                  style={{
                    fontSize: 104,
                    fontWeight: 900,
                    color: '#1D63FF',
                    lineHeight: 0.95,
                  }}
                >
                  {countVal}%
                </div>
                <div
                  style={{
                    fontSize: 30,
                    fontWeight: 800,
                    color: '#334155',
                    marginTop: 8,
                  }}
                >
                  die from wrong timing
                </div>
              </div>
            )}
          </div>
        ) : (
          <div
            style={{
              width: '100%',
              height: 536,
              position: 'relative',
              overflow: 'hidden',
              borderBottomLeftRadius: 26,
              borderBottomRightRadius: 26,
            }}
          >
            <Video
              src={brollMentorUrl}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              muted
            />
            {/* Floating Pill Tag Overlay + Animated Cursor Click */}
            <div
              style={{
                position: 'absolute',
                top: 28,
                left: 28,
                backgroundColor: 'rgba(15, 23, 42, 0.88)',
                border: '2.5px solid #3B82F6',
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

        {/* Animated macOS Pointer Cursor (like 0:14 in bHIMNW_4mlg) */}
        <svg
          width="46"
          height="46"
          viewBox="0 0 24 24"
          style={{
            position: 'absolute',
            left: cursorX,
            top: cursorY,
            zIndex: 50,
            filter: 'drop-shadow(0 6px 12px rgba(0,0,0,0.65))',
          }}
        >
          <path
            d="M5.5 3.21V20.8c0 .45.54.67.85.35l4.86-4.86a.5.5 0 0 1 .35-.15h6.87c.45 0 .67-.54.35-.85L6.35 2.86a.5.5 0 0 0-.85.35Z"
            fill="#FFFFFF"
            stroke="#000000"
            strokeWidth="1.8"
          />
        </svg>
      </div>

      {/* ZONE 3: Center-Seam Mixed-Font Subtitle (y=935) */}
      {renderMixedCaption(935)}

      {/* ZONE 4: Bottom Rounded Speaker Portrait Card (y=1065..1875) */}
      <div
        style={{
          position: 'absolute',
          bottom: 45,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 920,
          height: 800,
          borderRadius: 46,
          overflow: 'hidden',
          border: '3px solid rgba(255,255,255,0.14)',
          boxShadow: '0 -15px 50px rgba(0,0,0,0.65)',
          backgroundColor: '#000',
        }}
      >
        <Video
          src={speakerVideoUrl}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: '55% 22%',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

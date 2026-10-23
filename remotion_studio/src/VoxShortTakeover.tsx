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

export interface TakeoverProps {
  mode: 'stat_counter' | 'split_comparison' | 'network_nodes' | 'rosy_vs_devil';
  mediaUrlA?: string;
  mediaUrlB?: string;
}

export const VoxShortTakeover: React.FC<TakeoverProps> = ({
  mode,
  mediaUrlA,
  mediaUrlB,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrySpring = spring({ frame, fps, config: { damping: 14, stiffness: 150 } });
  const secondBeatSpring = spring({
    frame: Math.max(0, frame - 45),
    fps,
    config: { damping: 13, stiffness: 160 },
  });

  // Helper to resolve staticFile if it starts with /
  const resolveMedia = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
      return url;
    }
    return staticFile(url.startsWith('/') ? url.slice(1) : url);
  };

  const srcA = resolveMedia(mediaUrlA);
  const srcB = resolveMedia(mediaUrlB);

  // Warm Vox tactile paper background with dot grid
  const bgStyle: React.CSSProperties = {
    backgroundColor: '#F4F1EA',
    backgroundImage: 'radial-gradient(#C8C2B4 2px, transparent 2px)',
    backgroundSize: '36px 36px',
    fontFamily: 'Montserrat, Inter, sans-serif',
    color: '#141413',
    overflow: 'hidden',
  };

  if (mode === 'stat_counter') {
    const count = Math.round(
      interpolate(frame, [5, 45], [0, 90], { extrapolateRight: 'clamp' })
    );
    const barWidth = interpolate(frame, [8, 50], [0, 100], { extrapolateRight: 'clamp' });
    const highlightWipe = interpolate(frame, [25, 42], [0, 100], { extrapolateRight: 'clamp' });

    return (
      <AbsoluteFill style={bgStyle}>
        <div style={{ padding: '140px 80px', display: 'flex', flexDirection: 'column', gap: 45 }}>
          {/* Stamp Tag */}
          <div
            style={{
              alignSelf: 'flex-start',
              border: '5px solid #E63946',
              color: '#E63946',
              padding: '12px 28px',
              fontSize: 38,
              fontWeight: 900,
              transform: `scale(${entrySpring}) rotate(-3deg)`,
            }}
          >
            STARTUP AUTOPSY REPORT
          </div>

          {/* Giant Animated Counter */}
          <div style={{ fontSize: 210, fontWeight: 900, lineHeight: 1, letterSpacing: -6 }}>
            {count}%
          </div>

          <div style={{ fontSize: 68, fontWeight: 800, lineHeight: 1.15 }}>
            DIE FROM{' '}
            <span
              style={{
                background: `linear-gradient(90deg, #FFE600 ${highlightWipe}%, transparent ${highlightWipe}%)`,
                padding: '0 14px',
              }}
            >
              WRONG TIMING
            </span>
          </div>

          {/* Animated Vox Bar Comparison */}
          <div style={{ marginTop: 40, display: 'flex', flexDirection: 'column', gap: 28 }}>
            <div>
              <div style={{ fontSize: 34, fontWeight: 700, marginBottom: 10 }}>
                WRONG TIMING (TOO EARLY / LATE)
              </div>
              <div style={{ height: 64, width: `${barWidth}%`, backgroundColor: '#E63946', borderRadius: 12 }} />
            </div>
            <div>
              <div style={{ fontSize: 34, fontWeight: 700, marginBottom: 10, opacity: 0.6 }}>
                BAD IDEA OR TREND (10%)
              </div>
              <div style={{ height: 64, width: `${barWidth * 0.15}%`, backgroundColor: '#141413', borderRadius: 12 }} />
            </div>
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  if (mode === 'network_nodes') {
    const nodePulse = Math.sin(frame / 6) * 4;
    return (
      <AbsoluteFill style={bgStyle}>
        <div style={{ padding: '120px 70px', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <div>
            <div
              style={{
                alignSelf: 'flex-start',
                display: 'inline-block',
                border: '5px solid #10B981',
                color: '#10B981',
                padding: '10px 26px',
                fontSize: 36,
                fontWeight: 900,
                transform: `scale(${entrySpring}) rotate(-2deg)`,
                marginBottom: 24,
              }}
            >
              STEP 1: ADVISOR NETWORK
            </div>
            <div style={{ fontSize: 72, fontWeight: 900, lineHeight: 1.1, color: '#141413' }}>
              TALK TO <span style={{ backgroundColor: '#FFE600', padding: '0 12px' }}>20-YR VETERANS</span>
            </div>
          </div>

          {/* Media Card (Senior Mentors Video/Image) */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: 28,
              padding: 30,
              boxShadow: '0 24px 50px rgba(0,0,0,0.18)',
              transform: `scale(${entrySpring}) rotate(-1.5deg)`,
              border: '4px solid #141413',
            }}
          >
            <div style={{ height: 680, borderRadius: 20, overflow: 'hidden', backgroundColor: '#000' }}>
              {srcB && mediaUrlB?.endsWith('.mp4') ? (
                <Video src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
              ) : srcB ? (
                <Img src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              ) : srcA && mediaUrlA?.endsWith('.mp4') ? (
                <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
              ) : srcA ? (
                <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              ) : null}
            </div>
          </div>

          {/* Network Badges */}
          <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
            {['VETERAN OPERATORS', 'TECHNICAL ARCHITECTS', 'CAPITAL MENTORS'].map((pill, i) => (
              <div
                key={pill}
                style={{
                  backgroundColor: i === 0 ? '#141413' : '#FFFFFF',
                  color: i === 0 ? '#FFFFFF' : '#141413',
                  border: '3px solid #141413',
                  borderRadius: 16,
                  padding: '14px 24px',
                  fontSize: 28,
                  fontWeight: 800,
                  transform: `scale(${secondBeatSpring}) translateY(${i === 0 ? nodePulse : 0}px)`,
                }}
              >
                {pill}
              </div>
            ))}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // Full-Screen Comparison Cutouts (Used for Too Early vs Too Late & Rosy vs Devil in Details)
  const isRosy = mode === 'rosy_vs_devil';
  return (
    <AbsoluteFill style={bgStyle}>
      <div style={{ padding: '110px 70px', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
        {/* Top Card (Beat A) */}
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: 28,
            padding: 36,
            boxShadow: '0 24px 50px rgba(0,0,0,0.16)',
            transform: `scale(${entrySpring}) rotate(-2deg)`,
            border: '4px solid #141413',
          }}
        >
          <div style={{ fontSize: 36, fontWeight: 900, color: isRosy ? '#10B981' : '#E63946', marginBottom: 16 }}>
            {isRosy ? 'OUTSIDE ILLUSION: "LOOKS ALL ROSY"' : 'TRAP #1: LAUNCHING TOO EARLY'}
          </div>
          {srcA && (
            <div style={{ height: 480, borderRadius: 18, overflow: 'hidden', backgroundColor: '#000' }}>
              {mediaUrlA?.endsWith('.mp4') ? (
                <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
              ) : (
                <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              )}
            </div>
          )}
        </div>

        {/* Bottom Card (Beat B pops in on second phrase) */}
        <div
          style={{
            backgroundColor: '#141413',
            color: '#FFFFFF',
            borderRadius: 28,
            padding: 36,
            boxShadow: '0 28px 60px rgba(0,0,0,0.32)',
            transform: `scale(${secondBeatSpring}) rotate(2deg)`,
            border: '4px solid #FFE600',
          }}
        >
          <div style={{ fontSize: 36, fontWeight: 900, color: '#FFE600', marginBottom: 16 }}>
            {isRosy ? 'REALITY: THE DEVIL IS IN THE DETAILS' : 'TRAP #2: TOO LATE = CRUSHED BY GIANTS'}
          </div>
          {srcB && (
            <div style={{ height: 480, borderRadius: 18, overflow: 'hidden', backgroundColor: '#222' }}>
              {mediaUrlB?.endsWith('.mp4') ? (
                <Video src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
              ) : (
                <Img src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              )}
            </div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

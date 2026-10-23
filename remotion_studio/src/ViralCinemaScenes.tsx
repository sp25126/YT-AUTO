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

export const ViralCinemaScenes: React.FC<{
  scene: 'shatter_90' | 'stickman_timing' | 'veteran_shield' | 'rosy_rip';
  mediaA?: string;
  mediaB?: string;
}> = ({ scene, mediaA, mediaB }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Helper to resolve media from public static folder or remote URLs
  const resolveMedia = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
      return url;
    }
    const cleanPath = url.startsWith('/') ? url.slice(1) : url;
    return staticFile(cleanPath);
  };

  const isVideo = (url?: string) => {
    if (!url) return false;
    return url.toLowerCase().includes('.mp4') || url.toLowerCase().includes('.webm');
  };

  const srcA = resolveMedia(mediaA);
  const srcB = resolveMedia(mediaB);

  // Continuous 3D After-Effects Camera Drift (Never static!)
  const camScale = interpolate(frame, [0, 150], [0.95, 1.07], { extrapolateRight: 'clamp' });
  const camRotateY = interpolate(frame, [0, 150], [-5, 4], { extrapolateRight: 'clamp' });
  const camRotateX = interpolate(frame, [0, 150], [4, -2], { extrapolateRight: 'clamp' });

  // Entry Whip-Zoom (First 8 frames)
  const entryPop = spring({ frame, fps, config: { damping: 13, stiffness: 190 } });

  const stageStyle: React.CSSProperties = {
    backgroundColor: '#090B10',
    backgroundImage: `
      radial-gradient(circle at 50% 35%, rgba(16, 185, 129, 0.12) 0%, transparent 68%),
      linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)
    `,
    backgroundSize: '100% 100%, 48px 48px, 48px 48px',
    width: 1080,
    height: 1920,
    color: '#FFFFFF',
    fontFamily: 'Montserrat, sans-serif',
    perspective: '1200px',
    overflow: 'hidden',
  };

  const cameraRigStyle: React.CSSProperties = {
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '80px 60px 240px',
    transform: `scale(${camScale * entryPop}) rotateY(${camRotateY}deg) rotateX(${camRotateX}deg)`,
    transformStyle: 'preserve-3d',
  };

  // =========================================================================
  // SCENE 1: 9 OUT OF 10 STARTUPS SHATTER RED (0:02.2 - 0:06.2)
  // =========================================================================
  if (scene === 'shatter_90') {
    const count = Math.round(interpolate(frame, [4, 42], [0, 90], { extrapolateRight: 'clamp' }));

    return (
      <AbsoluteFill style={stageStyle}>
        <div style={cameraRigStyle}>
          <div style={{
            backgroundColor: 'rgba(230, 57, 70, 0.18)',
            border: '3px solid #FF3B5C',
            color: '#FF3B5C',
            padding: '10px 32px',
            borderRadius: 50,
            fontSize: 34,
            fontWeight: 900,
            letterSpacing: 2,
            marginBottom: 20,
            boxShadow: '0 0 35px rgba(255, 59, 92, 0.4)'
          }}>
            ⚠️ THE STARTUP GRAVEYARD
          </div>

          <div style={{
            fontSize: 250,
            fontWeight: 900,
            lineHeight: 0.95,
            color: '#FFFFFF',
            textShadow: '0 15px 60px rgba(255, 59, 92, 0.65)',
          }}>
            {count}%
          </div>

          <div style={{
            fontSize: 64,
            fontWeight: 900,
            color: '#FFE600',
            marginTop: 10,
            marginBottom: 60,
            textTransform: 'uppercase',
            letterSpacing: 2,
          }}>
            WRONG TIMING
          </div>

          {/* 10 Startup Rocket Icons: 9 Turn Crimson 💀 & Drop as Counter Rises */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(5, 1fr)',
            gap: 28,
            width: '100%',
            maxWidth: 860,
          }}>
            {Array.from({ length: 10 }).map((_, i) => {
              const triggerFrame = 6 + i * 4;
              const isDead = i < 9 && frame >= triggerFrame;
              const cardSpring = spring({
                frame: Math.max(0, frame - triggerFrame),
                fps,
                config: { damping: 10, stiffness: 220 },
              });
              return (
                <div
                  key={i}
                  style={{
                    height: 170,
                    borderRadius: 24,
                    backgroundColor: isDead ? 'rgba(255, 59, 92, 0.22)' : 'rgba(16, 185, 129, 0.22)',
                    border: `4px solid ${isDead ? '#FF3B5C' : '#10B981'}`,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transform: isDead
                      ? `scale(${1 - 0.08 * cardSpring}) rotate(${(i % 2 === 0 ? -1 : 1) * 6 * cardSpring}deg)`
                      : 'scale(1)',
                    boxShadow: isDead ? '0 0 25px rgba(255,59,92,0.35)' : '0 0 30px rgba(16,185,129,0.4)',
                  }}
                >
                  <span style={{ fontSize: 64 }}>{isDead ? '💀' : '🚀'}</span>
                </div>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // SCENE 2: FULL-STAGE STICKMAN TIMING DILEMMA (0:10.5 - 0:15.4)
  // =========================================================================
  if (scene === 'stickman_timing') {
    const isLatePhase = frame >= 65; // Switches from TOO EARLY to TOO LATE at midpoint
    const crushY = interpolate(frame, [68, 84], [-500, 0], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
    const stickSquash = interpolate(frame, [76, 88], [1, 0.36], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' });
    const tumbleweedX = interpolate(frame, [0, 65], [-100, 950]);

    return (
      <AbsoluteFill style={stageStyle}>
        <div style={cameraRigStyle}>
          <div style={{
            fontSize: 66,
            fontWeight: 900,
            color: isLatePhase ? '#FF3B5C' : '#38BDF8',
            textAlign: 'center',
            marginBottom: 36,
            textShadow: '0 8px 30px rgba(0,0,0,0.8)',
          }}>
            {isLatePhase ? '❌ TOO LATE: CRUSHED' : '🏜️ TOO EARLY: 0 BUYERS'}
          </div>

          {/* Full-Stage Interactive 2D Vector Theatre */}
          <div style={{
            width: 900,
            height: 920,
            borderRadius: 36,
            backgroundColor: '#121621',
            border: `5px solid ${isLatePhase ? '#FF3B5C' : '#38BDF8'}`,
            position: 'relative',
            overflow: 'hidden',
            boxShadow: '0 30px 80px rgba(0,0,0,0.65)',
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'center',
          }}>
            {!isLatePhase ? (
              <>
                {/* Empty Desert Horizon + Rolling Tumbleweed + Confused Stickman */}
                <svg width="900" height="920" viewBox="0 0 900 920">
                  <line x1="0" y1="740" x2="900" y2="740" stroke="#38BDF8" strokeWidth="6" />
                  {/* Rolling Tumbleweed */}
                  <g transform={`translate(${tumbleweedX}, 680) rotate(${frame * 12})`}>
                    <circle cx="0" cy="0" r="45" fill="none" stroke="#F59E0B" strokeWidth="6" strokeDasharray="18 12" />
                    <circle cx="0" cy="0" r="25" fill="none" stroke="#F59E0B" strokeWidth="5" strokeDasharray="10 8" />
                  </g>
                  {/* Stickman Holding Question Alone */}
                  <g transform={`translate(450, 420)`}>
                    <circle cx="0" cy="0" r="48" fill="#FFFFFF" />
                    <text x="65" y="-30" fill="#38BDF8" fontSize="72" fontWeight="900">?</text>
                    <line x1="0" y1="48" x2="0" y2="200" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                    <line x1="0" y1="90" x2="-90" y2="150" stroke="#FFFFFF" strokeWidth="14" strokeLinecap="round" />
                    <line x1="0" y1="90" x2="110" y2="40" stroke="#FFFFFF" strokeWidth="14" strokeLinecap="round" />
                    <line x1="0" y1="200" x2="-55" y2="320" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                    <line x1="0" y1="200" x2="55" y2="320" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                  </g>
                </svg>
              </>
            ) : (
              <>
                {/* Giant Monolithic "GIANTS" Block Slamming Down on Stickman */}
                <svg width="900" height="920" viewBox="0 0 900 920">
                  <line x1="0" y1="780" x2="900" y2="780" stroke="#FF3B5C" strokeWidth="8" />
                  {/* Squashed Stickman */}
                  <g transform={`translate(450, 780) scale(1, ${stickSquash}) translate(0, -320)`}>
                    <circle cx="0" cy="0" r="48" fill="#FF3B5C" />
                    <line x1="0" y1="48" x2="0" y2="200" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                    <line x1="0" y1="100" x2="-110" y2="40" stroke="#FFFFFF" strokeWidth="14" strokeLinecap="round" />
                    <line x1="0" y1="100" x2="110" y2="40" stroke="#FFFFFF" strokeWidth="14" strokeLinecap="round" />
                    <line x1="0" y1="200" x2="-70" y2="320" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                    <line x1="0" y1="200" x2="70" y2="320" stroke="#FFFFFF" strokeWidth="16" strokeLinecap="round" />
                  </g>
                  {/* Falling Giant Anvil Block */}
                  <g transform={`translate(150, ${180 + crushY})`}>
                    <rect x="0" y="0" width="600" height="320" rx="28" fill="#FF3B5C" stroke="#FFFFFF" strokeWidth="6" />
                    <text x="300" y="190" textAnchor="middle" fill="#FFFFFF" fontSize="92" fontWeight="900">GIANTS</text>
                  </g>
                </svg>
              </>
            )}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // SCENE 3: VETERAN SHIELD DEFLECTING RISKS (0:21.2 - 0:26.0)
  // =========================================================================
  if (scene === 'veteran_shield') {
    const shieldPulse = 1 + Math.sin(frame * 0.2) * 0.04;
    return (
      <AbsoluteFill style={stageStyle}>
        <div style={cameraRigStyle}>
          <div style={{ fontSize: 64, fontWeight: 900, color: '#10B981', marginBottom: 35 }}>
            🛡️ 20-YR ADVISOR SHIELD
          </div>

          <div style={{
            width: 900,
            height: 620,
            borderRadius: 32,
            overflow: 'hidden',
            border: '5px solid #10B981',
            position: 'relative',
            boxShadow: '0 0 60px rgba(16, 185, 129, 0.35)',
          }}>
            {srcA && isVideo(mediaA) ? (
              <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            ) : srcA ? (
              <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : null}
          </div>

          {/* 3 Giant High-Contrast Glowing Nodes (Zero Tiny Text!) */}
          <div style={{
            display: 'flex',
            gap: 28,
            marginTop: 45,
            transform: `scale(${shieldPulse})`,
          }}>
            {['TECH', 'CAPITAL', 'SCALE'].map((label, idx) => (
              <div key={idx} style={{
                backgroundColor: '#121824',
                border: '4px solid #10B981',
                borderRadius: 24,
                padding: '28px 42px',
                fontSize: 44,
                fontWeight: 900,
                color: '#FFFFFF',
                boxShadow: '0 15px 40px rgba(0,0,0,0.5)',
              }}>
                ✓ {label}
              </div>
            ))}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // SCENE 4: FULL-SCREEN ILLUSION RIP -> REALITY (0:28.0 - 0:33.4)
  // =========================================================================
  const ripProgress = spring({
    frame: Math.max(0, frame - 55),
    fps,
    config: { damping: 14, stiffness: 180 },
  });

  return (
    <AbsoluteFill style={stageStyle}>
      <div style={cameraRigStyle}>
        <div style={{
          fontSize: 64,
          fontWeight: 900,
          color: frame < 55 ? '#10B981' : '#FFE600',
          marginBottom: 35,
        }}>
          {frame < 55 ? '✨ OUTSIDE: LOOKS ROSY' : '🔍 INSIDE: THE DETAILS'}
        </div>

        <div style={{
          width: 920,
          height: 980,
          borderRadius: 36,
          overflow: 'hidden',
          position: 'relative',
          border: `6px solid ${frame < 55 ? '#10B981' : '#FFE600'}`,
          boxShadow: '0 30px 80px rgba(0,0,0,0.7)',
        }}>
          {/* Base Layer: Luxury Yacht Illusion */}
          {srcA && (
            <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
          )}

          {/* At frame 55 ("once you go in..."), Reality Layer Wipes Across Full Frame */}
          {srcB && (
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              clipPath: `inset(0 ${100 - ripProgress * 100}% 0 0)`,
              borderRight: '8px solid #FFE600',
            }}>
              <Video src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            </div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Img,
  Video,
  staticFile,
} from 'remotion';

// --- Procedural Animated Stickman Component ---
const AnimatedStickman: React.FC<{
  pose: 'confused_timing' | 'pointing_chart' | 'running_crushed';
  frame: number;
  fps: number;
}> = ({ pose, frame, fps }) => {
  const wiggle = Math.sin(frame * 0.25) * 4;

  if (pose === 'confused_timing') {
    // Stickman tapping chin, questioning hourglass / clock
    const armAngle = interpolate(Math.sin(frame * 0.15), [-1, 1], [-25, -45]);
    return (
      <svg width="280" height="420" viewBox="0 0 200 300" style={{ overflow: 'visible' }}>
        {/* Head with tilted confusion */}
        <circle cx={100 + wiggle * 0.5} cy="60" r="28" fill="#141413" />
        {/* Confused Question Mark */}
        <text x="135" y="45" fontSize="42" fontWeight="900" fill="#E63946">?</text>
        {/* Spine */}
        <line x1={100 + wiggle * 0.5} y1="88" x2={98 + wiggle * 0.2} y2="185" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
        {/* Left Arm scratching head */}
        <path d={`M 100 110 Q 60 90 75 60`} fill="none" stroke="#141413" strokeWidth="8" strokeLinecap="round" />
        {/* Right Arm pointing with wiggle */}
        <path d={`M 100 110 Q 140 120 160 ${130 + armAngle}`} fill="none" stroke="#141413" strokeWidth="8" strokeLinecap="round" />
        {/* Legs */}
        <line x1="98" y1="185" x2="68" y2="275" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
        <line x1="98" y1="185" x2="128" y2="275" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
      </svg>
    );
  }

  // Crushed / overwhelmed pose for "TOO LATE = CRUSHED BY GIANTS"
  const squash = interpolate(frame, [10, 25], [1.0, 0.45], { extrapolateRight: 'clamp' });
  return (
    <svg width="320" height="320" viewBox="0 0 200 200" style={{ transform: `scaleY(${squash})`, transformOrigin: 'bottom center' }}>
      <circle cx="100" cy="50" r="25" fill="#E63946" />
      <line x1="100" y1="75" x2="100" y2="150" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
      <line x1="100" y1="100" x2="40" y2="130" stroke="#141413" strokeWidth="8" strokeLinecap="round" />
      <line x1="100" y1="100" x2="160" y2="130" stroke="#141413" strokeWidth="8" strokeLinecap="round" />
      <line x1="100" y1="150" x2="50" y2="195" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
      <line x1="100" y1="150" x2="150" y2="195" stroke="#141413" strokeWidth="9" strokeLinecap="round" />
    </svg>
  );
};

export const StickmanVoxTakeover: React.FC<{
  sceneType: 'timing_dilemma' | 'advisor_graph' | 'rosy_vs_detail';
  mediaA?: string;
  mediaB?: string;
}> = ({ sceneType, mediaA, mediaB }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const popSpring = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  const secondBeatSpring = spring({ frame: Math.max(0, frame - 35), fps, config: { damping: 14, stiffness: 160 } });
  const graphProgress = interpolate(frame, [8, 38], [0, 100], { extrapolateRight: 'clamp' });

  const resolveMedia = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
      return url;
    }
    return staticFile(url.startsWith('/') ? url.slice(1) : url);
  };

  const srcA = resolveMedia(mediaA);
  const srcB = resolveMedia(mediaB);

  // Grid texture matching Vox editorial style
  const bgStyle: React.CSSProperties = {
    backgroundColor: '#F5F2EB',
    backgroundImage: 'radial-gradient(#CBC4B4 2.2px, transparent 2.2px)',
    backgroundSize: '34px 34px',
    width: '1080px',
    height: '1920px',
    color: '#141413',
    fontFamily: 'Montserrat, sans-serif',
    padding: '110px 70px',
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    overflow: 'hidden',
  };

  if (sceneType === 'timing_dilemma') {
    return (
      <AbsoluteFill style={bgStyle}>
        {/* Animated Stamp Header */}
        <div style={{
          alignSelf: 'flex-start',
          border: '4px solid #E63946',
          color: '#E63946',
          padding: '8px 24px',
          fontWeight: 900,
          fontSize: 32,
          transform: `scale(${popSpring}) rotate(-3deg)`
        }}>
          MARKET TIMING SIMULATION
        </div>

        {/* Headline with Yellow Highlighter Wipe */}
        <h1 style={{ fontSize: 68, fontWeight: 900, margin: '26px 0 16px', lineHeight: 1.15 }}>
          WHY STARTUPS <span style={{
            background: `linear-gradient(90deg, #FFE600 ${graphProgress}%, transparent ${graphProgress}%)`,
            padding: '2px 12px'
          }}>COLLAPSE</span>
        </h1>

        {/* Center Canvas: Interactive Stickman analyzing the Two Paths */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', margin: '30px 0 35px' }}>
          <AnimatedStickman pose="confused_timing" frame={frame} fps={fps} />
          
          {/* Animated Interactive Bar Graph with Dashed Marker */}
          <div style={{ width: 560, backgroundColor: '#FFFFFF', padding: 32, borderRadius: 24, boxShadow: '0 20px 45px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: 26, fontWeight: 800, marginBottom: 8 }}>PREMATURE LAUNCH</div>
            <div style={{ height: 42, width: `${graphProgress}%`, backgroundColor: '#E63946', borderRadius: 8 }} />
            <div style={{ fontSize: 22, color: '#666', marginTop: 6 }}>Zero audience readiness</div>

            <div style={{ fontSize: 26, fontWeight: 800, margin: '24px 0 8px' }}>PROPER EXECUTION</div>
            <div style={{ height: 42, width: `${graphProgress * 0.25}%`, backgroundColor: '#10B981', borderRadius: 8 }} />
            <div style={{ fontSize: 22, color: '#666', marginTop: 6 }}>Strategic entry window</div>
          </div>
        </div>

        {/* Bottom Media Card with Dynamic Corner Badges (Ends above y=1680) */}
        {srcA && (
          <div style={{
            height: 460,
            borderRadius: 24,
            overflow: 'hidden',
            border: '5px solid #141413',
            boxShadow: '0 25px 50px rgba(0,0,0,0.2)',
            transform: `scale(${popSpring}) rotate(1deg)`,
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute', top: 20, left: 20, zIndex: 10,
              backgroundColor: '#141413', color: '#FFE600', padding: '6px 18px',
              fontWeight: 900, fontSize: 24, borderRadius: 8
            }}>
              HISTORICAL CASE STUDY
            </div>
            {mediaA?.endsWith('.mp4') ? (
              <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            ) : (
              <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        )}
      </AbsoluteFill>
    );
  }

  if (sceneType === 'advisor_graph') {
    const lineDashOffset = -frame * 2;
    return (
      <AbsoluteFill style={bgStyle}>
        <div style={{
          alignSelf: 'flex-start',
          border: '4px solid #10B981',
          color: '#10B981',
          padding: '8px 24px',
          fontWeight: 900,
          fontSize: 32,
          transform: `scale(${popSpring}) rotate(-2deg)`
        }}>
          FOUNDER PLAYBOOK: STEP 1
        </div>

        <h1 style={{ fontSize: 68, fontWeight: 900, margin: '24px 0 30px' }}>
          BUILD THE <span style={{ color: '#10B981' }}>VETERAN</span> SHIELD
        </h1>

        {/* Node Graph Overlay with Animated Connecting Lines */}
        <div style={{ position: 'relative', height: 600, margin: '10px 0 20px' }}>
          <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0, zIndex: 1 }}>
            <line x1="220" y1="120" x2="720" y2="120" stroke="#141413" strokeWidth="6" strokeDasharray="14 10" strokeDashoffset={lineDashOffset} />
            <line x1="470" y1="120" x2="470" y2="380" stroke="#141413" strokeWidth="6" strokeDasharray="14 10" strokeDashoffset={lineDashOffset} />
          </svg>

          {/* Node A: Technical Architect */}
          <div style={{
            position: 'absolute', top: 70, left: 30, zIndex: 2,
            backgroundColor: '#FFFFFF', padding: '20px 28px', borderRadius: 20,
            border: '4px solid #141413', boxShadow: '0 15px 35px rgba(0,0,0,0.12)',
            transform: `scale(${popSpring})`
          }}>
            <div style={{ fontSize: 28, fontWeight: 900 }}>TECH ARCHITECT</div>
            <div style={{ color: '#10B981', fontWeight: 800 }}>20-YR VETERAN</div>
          </div>

          {/* Node B: Capital Operator */}
          <div style={{
            position: 'absolute', top: 70, right: 30, zIndex: 2,
            backgroundColor: '#FFFFFF', padding: '20px 28px', borderRadius: 20,
            border: '4px solid #141413', boxShadow: '0 15px 35px rgba(0,0,0,0.12)',
            transform: `scale(${popSpring})`
          }}>
            <div style={{ fontSize: 28, fontWeight: 900 }}>CAPITAL ADVISOR</div>
            <div style={{ color: '#10B981', fontWeight: 800 }}>3X FOUNDER</div>
          </div>

          {/* Center Node: The Founder */}
          <div style={{
            position: 'absolute', top: 320, left: '50%', transform: `translateX(-50%) scale(${secondBeatSpring})`, zIndex: 2,
            backgroundColor: '#141413', color: '#FFFFFF', padding: '24px 40px', borderRadius: 24,
            border: '5px solid #FFE600', boxShadow: '0 25px 60px rgba(0,0,0,0.3)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: 34, fontWeight: 900 }}>YOU (THE FOUNDER)</div>
            <div style={{ color: '#FFE600', fontWeight: 800 }}>PROTECTED EXECUTION</div>
          </div>
        </div>

        {/* Video Card: Real Moving Senior Executives Stock Footage (Ends above y=1680) */}
        {srcB && (
          <div style={{
            height: 440,
            borderRadius: 24,
            overflow: 'hidden',
            border: '4px solid #141413',
            boxShadow: '0 20px 45px rgba(0,0,0,0.18)',
            transform: `scale(${popSpring}) rotate(-1deg)`,
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute', top: 16, left: 16, zIndex: 10,
              backgroundColor: '#10B981', color: '#FFFFFF', padding: '6px 16px',
              fontWeight: 900, fontSize: 22, borderRadius: 8
            }}>
              LIVE MENTOR ADVISORY SESSION
            </div>
            {mediaB?.endsWith('.mp4') ? (
              <Video src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            ) : (
              <Img src={srcB} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        )}
      </AbsoluteFill>
    );
  }

  // Scene 4: Rosy vs Devil in Details
  return (
    <AbsoluteFill style={bgStyle}>
      <div style={{
        alignSelf: 'flex-start',
        border: '4px solid #E63946',
        color: '#E63946',
        padding: '8px 24px',
        fontWeight: 900,
        fontSize: 32,
        transform: `scale(${popSpring}) rotate(-2deg)`
      }}>
        FOUNDER REALITY CHECK
      </div>

      <h1 style={{ fontSize: 64, fontWeight: 900, margin: '20px 0 30px', lineHeight: 1.15 }}>
        THE TWO SIDES OF <span style={{ color: '#E63946' }}>STARTUPS</span>
      </h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 30 }}>
        {/* Top Card: Outside Looks All Rosy */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: 24,
          padding: 24,
          boxShadow: '0 18px 40px rgba(0,0,0,0.12)',
          border: '4px solid #10B981',
          transform: `scale(${popSpring}) rotate(-1deg)`
        }}>
          <div style={{ fontSize: 28, fontWeight: 900, color: '#10B981', marginBottom: 12 }}>
            OUTSIDE ILLUSION: "LOOKS ALL ROSY"
          </div>
          {srcA && (
            <div style={{ height: 380, borderRadius: 16, overflow: 'hidden', backgroundColor: '#000' }}>
              {mediaA?.endsWith('.mp4') ? (
                <Video src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
              ) : (
                <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              )}
            </div>
          )}
        </div>

        {/* Bottom Card: Inside Devil in Details */}
        <div style={{
          backgroundColor: '#141413',
          color: '#FFFFFF',
          borderRadius: 24,
          padding: 24,
          boxShadow: '0 24px 50px rgba(0,0,0,0.25)',
          border: '4px solid #FFE600',
          transform: `scale(${secondBeatSpring}) rotate(1deg)`
        }}>
          <div style={{ fontSize: 28, fontWeight: 900, color: '#FFE600', marginBottom: 12 }}>
            INSIDE REALITY: THE DEVIL IS IN THE DETAILS
          </div>
          {srcB && (
            <div style={{ height: 380, borderRadius: 16, overflow: 'hidden', backgroundColor: '#111' }}>
              {mediaB?.endsWith('.mp4') ? (
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

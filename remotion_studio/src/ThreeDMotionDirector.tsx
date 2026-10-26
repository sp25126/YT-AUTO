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
import { ThreeCanvas } from '@remotion/three';

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

// ============================================================================
// REAL THREE.JS 3D WEBGL SCENE BACKGROUND (Renders 3D Wireframe Geometry & 3D Cubes)
// ============================================================================
const ThreeDBackdrop: React.FC<{
  frame: number;
  accentHex: string;
  mode: 'crash_pillars' | 'early_sphere' | 'crush_monoliths' | 'network_lattice';
}> = ({ frame, accentHex, mode }) => {
  const rotY = frame * 0.025;
  const rotX = frame * 0.015;

  return (
    <ThreeCanvas
      width={1080}
      height={1920}
      style={{ position: 'absolute', inset: 0, zIndex: 1 }}
      camera={{ position: [0, 0, 7], fov: 50 }}
    >
      <ambientLight intensity={0.6} />
      <pointLight position={[5, 6, 5]} intensity={2.2} color={accentHex} />
      <pointLight position={[-5, -4, 3]} intensity={1.2} color="#ffffff" />

      {mode === 'early_sphere' && (
        <group rotation={[rotX, rotY, 0]} position={[0, 1.3, 0]}>
          <mesh>
            <icosahedronGeometry args={[1.65, 2]} />
            <meshStandardMaterial color={accentHex} wireframe transparent opacity={0.35} />
          </mesh>
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <torusGeometry args={[2.2, 0.03, 16, 64]} />
            <meshStandardMaterial color={accentHex} emissive={accentHex} emissiveIntensity={0.8} />
          </mesh>
        </group>
      )}

      {mode === 'crush_monoliths' && (
        <group rotation={[0.25, rotY * 0.7, 0]} position={[0, 1.2, 0]}>
          {[-1.5, 0, 1.5].map((xPos, i) => {
            const dropY = Math.max(0, 2.2 - (frame * 0.08 - i * 0.3));
            return (
              <mesh key={i} position={[xPos, dropY, -i * 0.5]}>
                <boxGeometry args={[1.05, 2.6, 1.05]} />
                <meshStandardMaterial color={accentHex} wireframe={i !== 1} transparent opacity={0.45} />
              </mesh>
            );
          })}
        </group>
      )}

      {mode === 'network_lattice' && (
        <group rotation={[rotX * 0.6, rotY, 0]} position={[0, 1.1, 0]}>
          <mesh>
            <octahedronGeometry args={[1.9, 1]} />
            <meshStandardMaterial color="#10B981" wireframe transparent opacity={0.4} />
          </mesh>
        </group>
      )}

      {mode === 'crash_pillars' && (
        <group rotation={[0.2, -0.35 + frame * 0.008, 0]} position={[0, -0.8, 0]}>
          {[-2.1, -0.7, 0.7, 2.1].map((x, idx) => {
            const targetH = [3.2, 2.3, 1.4, 0.5][idx];
            const h = Math.min(targetH, (frame / 30) * targetH);
            return (
              <mesh key={idx} position={[x, h / 2 - 1.5, 0]}>
                <boxGeometry args={[0.85, Math.max(0.1, h), 0.85]} />
                <meshStandardMaterial color={accentHex} transparent opacity={0.28} />
              </mesh>
            );
          })}
        </group>
      )}
    </ThreeCanvas>
  );
};

export const ThreeDMotionDirector: React.FC<{
  speakerVideoUrl: string;
  rotoFolderUrl: string;
  brollEarlyVideo: string;
  brollLateVideo: string;
  brollMentorVideo: string;
  brollRosyVideo: string;
  brollDetailVideo: string;
  phrases: PhraseGroup[];
}> = ({
  speakerVideoUrl,
  rotoFolderUrl,
  brollEarlyVideo,
  brollLateVideo,
  brollMentorVideo,
  brollRosyVideo,
  brollDetailVideo,
  phrases,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // ==========================================================================
  // 1. 3D PERSPECTIVE GLASS CINEMA STAGE (Eliminates Floating Desk Cutoffs!)
  // ==========================================================================
  const render3DCinemaStage = (
    videoSrc: string,
    kicker: string,
    heroTitle: string,
    floatingPills: string[],
    accentHex: string,
    localFrame: number,
    threeMode: 'early_sphere' | 'crush_monoliths' | 'network_lattice'
  ) => {
    const enter = spring({ frame: localFrame, fps, config: { damping: 14, stiffness: 175 } });
    const tiltY = interpolate(localFrame, [0, 90], [-11, 6]);
    const tiltX = interpolate(localFrame, [0, 90], [8, -3]);
    const cardScale = interpolate(enter, [0, 1], [0.78, 1.0]);

    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#05070D',
          backgroundImage: `
            radial-gradient(circle at 50% 28%, ${accentHex}32 0%, transparent 65%),
            linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)
          `,
          backgroundSize: '100% 100%, 52px 52px, 52px 52px',
          perspective: '1300px',
          fontFamily: 'Inter, Montserrat, sans-serif',
          overflow: 'hidden',
        }}
      >
        {/* LAYER 1: Real Three.js 3D WebGL Geometry Rotating in Background Space */}
        <ThreeDBackdrop frame={localFrame} accentHex={accentHex} mode={threeMode} />

        {/* LAYER 2: Single-Line Hero Header (Auto-scaled so it NEVER wraps onto 2 lines!) */}
        <div
          style={{
            position: 'absolute',
            top: 135,
            width: '100%',
            textAlign: 'center',
            transform: `translateY(${(1 - enter) * -120}px)`,
            zIndex: 10,
          }}
        >
          <div
            style={{
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: 27,
              fontWeight: 800,
              color: accentHex,
              letterSpacing: 5,
              marginBottom: 10,
            }}
          >
            // {kicker}
          </div>
          <div
            style={{
              fontSize: heroTitle.length > 9 ? 128 : 156,
              fontWeight: 900,
              lineHeight: 0.95,
              color: '#FFFFFF',
              letterSpacing: -5,
              whiteSpace: 'nowrap',
              textShadow: `0 20px 55px rgba(0,0,0,0.95), 0 0 45px ${accentHex}60`,
            }}
          >
            {heroTitle}
          </div>
        </div>

        {/* LAYER 3: 3D Perspective Tilted Glass Cinema Window Framing Moving Video */}
        <div
          style={{
            position: 'absolute',
            top: 430,
            left: '50%',
            width: 900,
            height: 820,
            transform: `translateX(-50%) scale(${cardScale}) rotateY(${tiltY}deg) rotateX(${tiltX}deg)`,
            transformStyle: 'preserve-3d',
            borderRadius: 38,
            backgroundColor: '#0D121F',
            border: `3.5px solid ${accentHex}`,
            boxShadow: `0 45px 95px rgba(0,0,0,0.9), 0 0 55px ${accentHex}35`,
            zIndex: 15,
          }}
        >
          {/* Top macOS/HUD Telemetry Bar inside the 3D Card */}
          <div
            style={{
              height: 54,
              backgroundColor: 'rgba(10, 14, 24, 0.95)',
              borderTopLeftRadius: 34,
              borderTopRightRadius: 34,
              display: 'flex',
              alignItems: 'center',
              padding: '0 26px',
              gap: 12,
              borderBottom: '1px solid rgba(255,255,255,0.1)',
            }}
          >
            <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#EF4444' }} />
            <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#F59E0B' }} />
            <div style={{ width: 14, height: 14, borderRadius: 7, backgroundColor: '#10B981' }} />
            <span style={{ marginLeft: 'auto', fontFamily: 'JetBrains Mono, monospace', fontSize: 20, color: accentHex, fontWeight: 700 }}>
              LIVE TELEMETRY // 3D VIEW
            </span>
          </div>

          {/* Moving HD Video Framed Cleanly Inside the 3D Card (Zero Harsh Floating Desk Cutoffs!) */}
          <div style={{ width: '100%', height: 766, overflow: 'hidden', borderBottomLeftRadius: 34, borderBottomRightRadius: 34, position: 'relative' }}>
            <Video
              src={videoSrc}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                transform: `scale(${1.02 + (localFrame / 90) * 0.12})`,
                filter: 'contrast(1.12) saturate(1.12)',
              }}
              muted
            />
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(180deg, transparent 55%, rgba(5,7,13,0.85) 100%)',
              }}
            />
          </div>

          {/* LAYER 4: 3D Pop-Out Motion Graphic Pills Floating +60px in Z-Space IN FRONT of the Video! */}
          <div
            style={{
              position: 'absolute',
              bottom: -36,
              left: 40,
              right: 40,
              display: 'flex',
              justifyContent: 'center',
              gap: 20,
              transform: 'translateZ(65px)',
            }}
          >
            {floatingPills.map((pillText, idx) => {
              const pSpring = spring({
                frame: Math.max(0, localFrame - 10 - idx * 6),
                fps,
                config: { damping: 12, stiffness: 200 },
              });
              return (
                <div
                  key={idx}
                  style={{
                    backgroundColor: '#0B0F1A',
                    border: `2.5px solid ${accentHex}`,
                    padding: '16px 30px',
                    borderRadius: 22,
                    fontSize: 28,
                    fontWeight: 900,
                    color: '#FFFFFF',
                    boxShadow: '0 22px 45px rgba(0,0,0,0.85)',
                    transform: `scale(${pSpring})`,
                  }}
                >
                  {pillText}
                </div>
              );
            })}
          </div>
        </div>

        {/* Bottom Smooth Vignette for Borderless Subtitles */}
        <div
          style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 620,
            background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 60%, #04060A 100%)',
            zIndex: 20,
          }}
        />
      </AbsoluteFill>
    );
  };

  // ==========================================================================
  // 2. BORDERLESS SUBTITLES WITH GUARANTEED WORD SPACING (Fixes 'create aadvisor'!)
  // ==========================================================================
  const activePhrase = phrases.find((p) => t >= p.start - 0.03 && t <= p.end + 0.14);

  const renderCleanSubtitles = () => {
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
          bottom: 195,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'baseline',
          flexWrap: 'wrap',
          padding: '0 50px',
          transform: `scale(${0.92 + 0.08 * pop})`,
          filter: 'drop-shadow(0 12px 28px rgba(0,0,0,0.98))',
          zIndex: 50,
        }}
      >
        {activePhrase.words.map((w, i) => {
          const isKeyword = i === pIdx;
          const displayWord = (w.word.toLowerCase() === 'a' && activePhrase.words[i + 1]?.word.toLowerCase().replace(/[^a-z0-9]/g, '') === 'advisor') ? 'an' : w.word;
          return (
            <span
              key={i}
              style={{
                marginRight: i < activePhrase.words.length - 1 ? 22 : 0, // Explicit 22px margin prevents 'create aadvisor' & 'talk topeople'!
                display: 'inline-block',
                ...(isKeyword
                  ? {
                      fontSize: 84,
                      fontFamily: 'Georgia, Playfair Display, serif',
                      fontStyle: 'italic',
                      fontWeight: 700,
                      color: '#FACC15',
                      textShadow: '0 0 32px rgba(250, 204, 21, 0.65)',
                    }
                  : {
                      fontSize: 70,
                      fontWeight: 900,
                      color: '#FFFFFF',
                      letterSpacing: -1.5,
                    }),
              }}
            >
              {displayWord}
            </span>
          );
        })}
      </div>
    );
  };

  // ==========================================================================
  // TIMELINE ROUTER ACROSS ALL SCENES
  // ==========================================================================

  // BEAT 0 (0:00.0 - 0:02.2): LEFT-ALIGNED ROTO HOOK
  if (t < 2.2) {
    const s = spring({ frame, fps, config: { damping: 13, stiffness: 190 } });
    const rotoIdx = Math.min(64, frame);
    const cleanRotoFolder = rotoFolderUrl.replace(/^\//, '');
    const rotoPng = staticFile(`${cleanRotoFolder}/frame_${String(rotoIdx).padStart(4, '0')}.png`);

    return (
      <AbsoluteFill style={{ backgroundColor: '#05070C', fontFamily: 'Inter, Montserrat, sans-serif' }}>
        <Video src={speakerVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.42)' }} />
        <div style={{ position: 'absolute', top: 210, left: 65, transform: `translateX(${(1 - s) * -180}px)`, zIndex: 3 }}>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#38BDF8', letterSpacing: 4, marginBottom: 6 }}>
            #1 STARTUP KILLER
          </div>
          <div style={{ fontSize: 185, fontWeight: 900, color: '#FFF', lineHeight: 0.88, letterSpacing: -6, textShadow: '0 20px 60px rgba(0,0,0,0.95), 0 0 60px rgba(56,189,248,0.55)' }}>
            TIMING
          </div>
        </div>
        <Img src={rotoPng} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', zIndex: 6 }} />
        <div style={{ position: 'absolute', bottom: 0, width: '100%', height: 640, background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 70%, #04060A 100%)', zIndex: 8 }} />
        {renderCleanSubtitles()}
      </AbsoluteFill>
    );
  }

  // BEAT 1 (0:02.2 - 0:06.2): 3D CRASH PILLARS + AREA TELEMETRY CHART
  if (t >= 2.2 && t < 6.2) {
    const lf = Math.round((t - 2.2) * fps);
    const pct = Math.round(interpolate(lf, [3, 45], [0, 90], { extrapolateRight: 'clamp' }));
    const draw = interpolate(lf, [4, 52], [0, 1000], { extrapolateRight: 'clamp', easing: Easing.bezier(0.22, 1, 0.36, 1) });

    return (
      <AbsoluteFill style={{ backgroundColor: '#06080F', fontFamily: 'Inter, Montserrat, sans-serif', padding: '130px 65px', perspective: '1200px' }}>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        <ThreeDBackdrop frame={lf} accentHex="#FF2E4C" mode="crash_pillars" />

        <div style={{ textAlign: 'center', position: 'relative', zIndex: 10 }}>
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

        <svg width="950" height="600" viewBox="0 0 950 600" style={{ position: 'relative', zIndex: 10, transform: 'rotateX(8deg)' }}>
          <defs>
            <linearGradient id="crashGrad3D" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#FF2E4C" stopOpacity="0.52" />
              <stop offset="100%" stopColor="#FF2E4C" stopOpacity="0.0" />
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="950" height="600" rx="32" fill="rgba(11, 15, 28, 0.88)" stroke="rgba(255,46,76,0.4)" strokeWidth="3" />
          {[140, 280, 420].map((gy) => (
            <line key={gy} x1="50" y1={gy} x2="900" y2={gy} stroke="rgba(255,255,255,0.07)" strokeWidth="2" strokeDasharray="10 10" />
          ))}
          <path d="M 70 130 C 280 130, 420 220, 560 390 C 680 510, 780 520, 880 530 L 880 560 L 70 560 Z" fill="url(#crashGrad3D)" opacity={lf / 45} />
          <path d="M 70 130 C 280 130, 420 220, 560 390 C 680 510, 780 520, 880 530" fill="none" stroke="#FF2E4C" strokeWidth="13" strokeDasharray="1000" strokeDashoffset={1000 - draw} strokeLinecap="round" />
          <circle cx="880" cy="530" r={lf > 44 ? 18 : 0} fill="#FFFFFF" stroke="#FF2E4C" strokeWidth="8" />
          <text x="80" y="485" fill="#94A3B8" fontSize="28" fontWeight="700">BAD PRODUCT / TREND: 10%</text>
          <text x="80" y="538" fill="#FF2E4C" fontSize="36" fontWeight="900">WRONG MARKET TIMING: 90%</text>
        </svg>

        {renderCleanSubtitles()}
      </AbsoluteFill>
    );
  }

  // BEAT 2A (0:10.6 - 0:12.8): 3D WIREFRAME SPHERE + 3D GLASS CINEMA WINDOW ("TOO EARLY")
  if (t >= 10.6 && t < 12.8) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {render3DCinemaStage(
          brollEarlyVideo,
          'TRAP 01 // PREMATURE LAUNCH',
          'TOO EARLY',
          ['⏳ 0% Market Readiness', '📉 Burn Runway Waiting'],
          '#38BDF8',
          Math.round((t - 10.6) * fps),
          'early_sphere'
        )}
        {renderCleanSubtitles()}
      </>
    );
  }

  // BEAT 2B (0:12.8 - 0:15.4): 3D MONOLITH DROP + 3D GLASS CINEMA WINDOW ("CRUSHED")
  if (t >= 12.8 && t < 15.4) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {render3DCinemaStage(
          brollLateVideo,
          'TRAP 02 // SATURATED MARKET',
          'CRUSHED',
          ['🏢 Giants Own Distribution', '❌ 10x Higher CAC'],
          '#FF2E4C',
          Math.round((t - 12.8) * fps),
          'crush_monoliths'
        )}
        {renderCleanSubtitles()}
      </>
    );
  }

  // BEAT 3 (0:20.8 - 0:26.0): 3D NETWORK LATTICE + 3D MENTOR CINEMA WINDOW ("VETERANS")
  if (t >= 20.8 && t < 26.0) {
    return (
      <>
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        {render3DCinemaStage(
          brollMentorVideo,
          'STEP 01 // THE UNFAIR ADVANTAGE',
          'VETERANS',
          ['🛡️ 20-Yr Operators', '⚡ Skip Fatal Mistakes'],
          '#10B981',
          Math.round((t - 20.8) * fps),
          'network_lattice'
        )}
        {renderCleanSubtitles()}
      </>
    );
  }

  // BEAT 4 (0:27.9 - 0:32.85): 3D 180-DEGREE FLIPPING CARD ("ALL ROSY" -> FLIPS IN 3D TO -> "THE DETAILS")
  if (t >= 27.9) {
    const isFlipped = t >= 30.2;
    const flipSpring = spring({
      frame: Math.max(0, Math.round((t - 30.2) * fps)),
      fps,
      config: { damping: 14, stiffness: 160 },
    });
    const rotYDeg = interpolate(flipSpring, [0, 1], [0, 180]);
    const activeAccent = isFlipped ? '#FACC15' : '#10B981';

    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#05070D',
          perspective: '1400px',
          fontFamily: 'Inter, Montserrat, sans-serif',
          overflow: 'hidden',
        }}
      >
        <Video src={speakerVideoUrl} style={{ width: 1, height: 1, opacity: 0, position: 'absolute' }} />
        <ThreeDBackdrop frame={Math.round((t - 27.9) * fps)} accentHex={activeAccent} mode="network_lattice" />

        {/* Single-Line Header Above the 3D Flipping Card */}
        <div style={{ position: 'absolute', top: 135, width: '100%', textAlign: 'center', zIndex: 10 }}>
          <div style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: 27, fontWeight: 800, color: activeAccent, letterSpacing: 5, marginBottom: 10 }}>
            {isFlipped ? '// INSIDE REALITY' : '// OUTSIDE ILLUSION'}
          </div>
          <div
            style={{
              fontSize: 132,
              fontWeight: 900,
              lineHeight: 0.95,
              color: '#FFFFFF',
              letterSpacing: -5,
              whiteSpace: 'nowrap', // Prevents 'THE DETAILS' from wrapping onto 2 lines!
              textShadow: `0 20px 55px rgba(0,0,0,0.95), 0 0 45px ${activeAccent}55`,
            }}
          >
            {isFlipped ? 'THE DETAILS' : 'ALL ROSY'}
          </div>
        </div>

        {/* 3D Card Container that Physically Rotates 180 Degrees on Y-Axis at 0:30.2 */}
        <div
          style={{
            position: 'absolute',
            top: 420,
            left: '50%',
            width: 900,
            height: 830,
            transform: `translateX(-50%) rotateY(${rotYDeg}deg)`,
            transformStyle: 'preserve-3d',
            zIndex: 15,
          }}
        >
          {!isFlipped ? (
            <div
              style={{
                width: '100%',
                height: '100%',
                borderRadius: 38,
                overflow: 'hidden',
                border: '4px solid #10B981',
                boxShadow: '0 40px 90px rgba(0,0,0,0.9), 0 0 50px rgba(16,185,129,0.35)',
                backgroundColor: '#0D121F',
              }}
            >
              <Video src={brollRosyVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            </div>
          ) : (
            <div
              style={{
                width: '100%',
                height: '100%',
                borderRadius: 38,
                overflow: 'hidden',
                border: '4px solid #FACC15',
                boxShadow: '0 40px 90px rgba(0,0,0,0.9), 0 0 50px rgba(250,204,21,0.35)',
                backgroundColor: '#0D121F',
                transform: 'scaleX(-1)', // Un-mirrors the back face after 180deg Y-rotation!
              }}
            >
              <Video src={brollDetailVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
            </div>
          )}
        </div>

        <div style={{ position: 'absolute', bottom: 0, width: '100%', height: 620, background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 60%, #04060A 100%)', zIndex: 20 }} />
        {renderCleanSubtitles()}
      </AbsoluteFill>
    );
  }

  // TALKING HEAD SEGMENTS (0:06.2-0:10.6, 0:15.4-0:20.8, 0:26.0-0:27.9)
  const zoom = 1.04 + 0.08 * Math.sin(t * 1.4);
  return (
    <AbsoluteFill style={{ backgroundColor: '#000', fontFamily: 'Inter, Montserrat, sans-serif' }}>
      <div style={{ width: '100%', height: '100%', transform: `scale(${zoom})`, transformOrigin: '50% 30%' }}>
        <Video src={speakerVideoUrl} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div style={{ position: 'absolute', bottom: 0, width: '100%', height: 680, background: 'linear-gradient(180deg, transparent 0%, rgba(4,6,10,0.92) 70%, #04060A 100%)' }} />
      {renderCleanSubtitles()}
    </AbsoluteFill>
  );
};

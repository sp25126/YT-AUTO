import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Video,
  staticFile,
} from 'remotion';

export type EditStyle =
  | 'iman_documentary'
  | 'hormozi_hud'
  | 'apple_bento'
  | 'magnates_dossier'
  | 'pip_reactor';

export type BeatId = 'beat1_90_fail' | 'beat2_timing' | 'beat3_network' | 'beat4_rosy_details';

export const FiveStyleDirector: React.FC<{
  styleVariant: EditStyle;
  beat: BeatId;
  videoA: string;
  videoB?: string;
}> = ({ styleVariant, beat, videoA, videoB }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const resolveVideo = (src: string) => {
    if (!src) return '';
    if (src.startsWith('http')) return src;
    return staticFile(src.replace(/^\//, ''));
  };

  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 180 } });
  const isSecondHalf = frame >= 60 && Boolean(videoB);
  const activeVideo = resolveVideo(isSecondHalf ? videoB! : videoA);
  const count90 = Math.round(interpolate(frame, [3, 38], [0, 90], { extrapolateRight: 'clamp' }));
  const barProg = interpolate(frame, [5, 42], [0, 100], { extrapolateRight: 'clamp' });
  const zoomDrift = interpolate(frame, [0, 150], [1.0, 1.14]);

  const titles: Record<BeatId, [string, string]> = {
    beat1_90_fail: ['90% STARTUP FAILURE', 'CAUSE: WRONG TIMING'],
    beat2_timing: ['TOO EARLY = ZERO MARKET', 'TOO LATE = CRUSHED BY GIANTS'],
    beat3_network: ['STEP 1: ADVISOR NETWORK', '20-YEAR INDUSTRY VETERANS'],
    beat4_rosy_details: ['OUTSIDE: LOOKS ALL ROSY', 'INSIDE: DEVIL IN THE DETAILS'],
  };
  const [headlineA, headlineB] = titles[beat];
  const currentHeadline = isSecondHalf ? headlineB : headlineA;
  const isDanger = beat === 'beat1_90_fail' || (beat === 'beat2_timing' && isSecondHalf) || (beat === 'beat4_rosy_details' && isSecondHalf);
  const accent = isDanger ? '#FF2E4C' : '#10B981';

  // =========================================================================
  // STYLE 1: IMAN GADZHI DOCUMENTARY (Full-Bleed 1080x1920 Moving Video + Glass HUD)
  // Also baseline for PIP REACTOR
  // =========================================================================
  if (styleVariant === 'iman_documentary' || styleVariant === 'pip_reactor') {
    return (
      <AbsoluteFill style={{ backgroundColor: '#000', overflow: 'hidden', fontFamily: 'Montserrat, sans-serif' }}>
        {/* Full-Screen Moving HD Video with Slow Push-In & Dark Cinema Grade */}
        <div style={{ width: '100%', height: '100%', transform: `scale(${zoomDrift})`, filter: 'contrast(1.15) brightness(0.68)' }}>
          <Video src={activeVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
        </div>

        {/* Smooth Radial & Bottom Vignette */}
        <AbsoluteFill style={{
          background: 'linear-gradient(180deg, rgba(0,0,0,0.75) 0%, transparent 30%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0.95) 100%)',
        }} />

        {/* Sleek Top Glassmorphic HUD Card */}
        <div style={{
          position: 'absolute',
          top: 110,
          left: 60,
          right: 60,
          padding: '36px 44px',
          borderRadius: 28,
          backgroundColor: 'rgba(12, 15, 24, 0.78)',
          backdropFilter: 'blur(20px)',
          border: `3px solid ${accent}`,
          boxShadow: `0 25px 60px rgba(0,0,0,0.75), 0 0 40px ${accent}40`,
          transform: `translateY(${(1 - pop) * -120}px)`,
        }}>
          <div style={{ fontSize: 28, fontWeight: 800, color: accent, letterSpacing: 2, marginBottom: 8 }}>
            ● CASE STUDY TELEMETRY
          </div>
          <div style={{ fontSize: 52, fontWeight: 900, color: '#FFF', lineHeight: 1.1 }}>
            {beat === 'beat1_90_fail' ? `${count90}% FAIL FROM TIMING` : currentHeadline}
          </div>
          <div style={{ height: 14, width: '100%', backgroundColor: 'rgba(255,255,255,0.12)', borderRadius: 8, marginTop: 22 }}>
            <div style={{ height: '100%', width: `${barProg}%`, backgroundColor: accent, borderRadius: 8 }} />
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // STYLE 2: ALEX HORMOZI OVER-THE-SHOULDER FLOATING WIDGET (Transparent Lower Half!)
  // =========================================================================
  if (styleVariant === 'hormozi_hud') {
    // Renders over #00FF00 green screen chroma key so it overlays cleanly over the speaker
    return (
      <AbsoluteFill style={{ backgroundColor: '#00FF00', fontFamily: 'Montserrat, sans-serif' }}>
        <div style={{
          margin: '95px 55px 0',
          padding: '38px 46px',
          borderRadius: 32,
          backgroundColor: '#0D1017',
          border: `4px solid ${accent}`,
          boxShadow: '0 30px 70px rgba(0,0,0,0.9)',
          transform: `scale(${pop})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 32,
        }}>
          <div style={{ flex: 1 }}>
            <div style={{
              display: 'inline-block',
              padding: '6px 18px',
              borderRadius: 10,
              backgroundColor: `${accent}25`,
              color: accent,
              fontSize: 26,
              fontWeight: 900,
              marginBottom: 14,
            }}>
              {isDanger ? '⚠️ CRITICAL RISK' : '✅ PROVEN PLAYBOOK'}
            </div>
            <div style={{ fontSize: 48, fontWeight: 900, color: '#FFF', lineHeight: 1.12 }}>
              {beat === 'beat1_90_fail' ? `${count90}% STARTUP DEATHS` : currentHeadline}
            </div>
          </div>
          {/* Mini Circular Moving Video Thumbnail Inside the Floating Card */}
          <div style={{
            width: 210,
            height: 210,
            borderRadius: 24,
            overflow: 'hidden',
            border: `3px solid ${accent}`,
            flexShrink: 0,
          }}>
            <Video src={activeVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // STYLE 3: ALI ABDAAL / APPLE KEYNOTE 3D BENTO GRID
  // =========================================================================
  if (styleVariant === 'apple_bento') {
    return (
      <AbsoluteFill style={{
        backgroundColor: '#08090C',
        padding: '100px 55px 520px',
        fontFamily: 'Montserrat, sans-serif',
        display: 'flex',
        flexDirection: 'column',
        gap: 28,
      }}>
        {/* Top Row: Two Side-by-Side Bento Metric Cards */}
        <div style={{ display: 'flex', gap: 28, height: 320, transform: `scale(${pop})` }}>
          <div style={{
            flex: 1,
            backgroundColor: '#13161F',
            borderRadius: 32,
            padding: 36,
            border: '2px solid rgba(255,255,255,0.08)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
          }}>
            <div style={{ fontSize: 30, color: '#9CA3AF', fontWeight: 700 }}>FAILURE RATE</div>
            <div style={{ fontSize: 110, fontWeight: 900, color: accent, lineHeight: 1 }}>
              {beat === 'beat1_90_fail' ? `${count90}%` : isSecondHalf ? 'LATE' : 'EARLY'}
            </div>
          </div>

          <div style={{
            flex: 1.2,
            backgroundColor: '#13161F',
            borderRadius: 32,
            padding: 36,
            border: '2px solid rgba(255,255,255,0.08)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
          }}>
            <div style={{ fontSize: 28, color: '#9CA3AF', fontWeight: 700, marginBottom: 12 }}>PRIMARY FACTOR</div>
            <div style={{ fontSize: 42, fontWeight: 900, color: '#FFF', lineHeight: 1.15 }}>
              {currentHeadline}
            </div>
          </div>
        </div>

        {/* Bottom Bento Card: High-Res Moving Video Window */}
        <div style={{
          flex: 1,
          borderRadius: 36,
          overflow: 'hidden',
          border: `3px solid ${accent}`,
          position: 'relative',
          boxShadow: '0 25px 60px rgba(0,0,0,0.65)',
        }}>
          <Video src={activeVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // STYLE 4: MAGNATES MEDIA INVESTIGATIVE DOSSIER (Tilted Polaroid Video + Highlighter)
  // =========================================================================
  return (
    <AbsoluteFill style={{
      backgroundColor: '#0B090A',
      backgroundImage: 'radial-gradient(circle at 50% 35%, rgba(220, 38, 38, 0.22) 0%, transparent 70%)',
      padding: '120px 65px 540px',
      fontFamily: 'Montserrat, sans-serif',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div style={{
        backgroundColor: '#FFE600',
        color: '#000',
        padding: '10px 30px',
        fontSize: 34,
        fontWeight: 900,
        transform: `rotate(-2deg) scale(${pop})`,
        marginBottom: 30,
      }}>
        EVIDENCE FILE #{beat === 'beat1_90_fail' ? '01' : beat === 'beat2_timing' ? '02' : '03'}
      </div>

      {/* Framed Tilted Polaroid Holding Moving HD Video */}
      <div style={{
        width: 900,
        backgroundColor: '#F4F4F6',
        padding: '28px 28px 95px 28px',
        borderRadius: 16,
        boxShadow: '0 35px 80px rgba(0,0,0,0.85)',
        transform: `rotate(${isSecondHalf ? '2deg' : '-2deg'}) scale(${pop})`,
      }}>
        <div style={{ width: '100%', height: 680, overflow: 'hidden', backgroundColor: '#000' }}>
          <Video src={activeVideo} style={{ width: '100%', height: '100%', objectFit: 'cover' }} muted />
        </div>
        <div style={{
          color: '#111',
          fontSize: 44,
          fontWeight: 900,
          textAlign: 'center',
          marginTop: 24,
          letterSpacing: -1,
        }}>
          {currentHeadline}
        </div>
      </div>
    </AbsoluteFill>
  );
};

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

export const CapCutCollageScenes: React.FC<{
  scene: 'stat_behind_cutout' | 'early_vs_late_collage' | 'torn_paper_advisor' | 'red_circle_reality';
  cutoutPngA: string;
  cutoutPngB?: string;
  bgVideo?: string;
}> = ({ scene, cutoutPngA, cutoutPngB, bgVideo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const resolveMedia = (url?: string) => {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
      return url;
    }
    const cleanPath = url.startsWith('/') ? url.slice(1) : url;
    return staticFile(cleanPath);
  };

  const srcA = resolveMedia(cutoutPngA);
  const srcB = resolveMedia(cutoutPngB);
  const srcVideo = resolveMedia(bgVideo);

  // Fast CapCut Whip-Slide Entry with Motion Blur (First 7 frames)
  const slideSpring = spring({ frame, fps, config: { damping: 13, stiffness: 220, mass: 0.7 } });
  const motionBlurPx = interpolate(frame, [0, 7], [18, 0], { extrapolateRight: 'clamp' });
  const slowPush = interpolate(frame, [0, 160], [1.0, 1.12], { extrapolateRight: 'clamp' });

  // Dark Emerald / Crimson Perspective Grid (Exact Winter Media 0:06 & Cosmocuts 0:09 backdrop)
  const isRedTheme = scene === 'stat_behind_cutout' || scene === 'red_circle_reality';
  const glowColor = isRedTheme ? 'rgba(235, 45, 58, 0.28)' : 'rgba(16, 185, 129, 0.26)';
  const gridLineColor = isRedTheme ? 'rgba(235, 45, 58, 0.14)' : 'rgba(16, 185, 129, 0.14)';

  const gridBgStyle: React.CSSProperties = {
    backgroundColor: '#050608',
    backgroundImage: `
      radial-gradient(circle at 50% 42%, ${glowColor} 0%, transparent 62%),
      linear-gradient(${gridLineColor} 1.5px, transparent 1.5px),
      linear-gradient(90deg, ${gridLineColor} 1.5px, transparent 1.5px)
    `,
    backgroundSize: '100% 100%, 56px 56px, 56px 56px',
    width: 1080,
    height: 1920,
    overflow: 'hidden',
    fontFamily: 'Montserrat, sans-serif',
  };

  // 1. WINTER MEDIA (0:10) STYLE: Giant "$450,000 / 90%" Rising BEHIND a B&W Founder Cutout with Red Eye-Bar
  if (scene === 'stat_behind_cutout') {
    const numCount = Math.round(interpolate(frame, [2, 36], [0, 90], { extrapolateRight: 'clamp' }));
    const textRiseY = interpolate(slideSpring, [0, 1], [240, 0]);
    const subjectSlideY = interpolate(slideSpring, [0, 1], [500, 0]);

    return (
      <AbsoluteFill style={gridBgStyle}>
        <div style={{ width: '100%', height: '100%', position: 'relative', transform: `scale(${slowPush})` }}>
          {/* LAYER 1 (BACK/MIDGROUND): Giant Metallic Text Rising BEHIND the Cutout's Head */}
          <div style={{
            position: 'absolute',
            top: 210 + textRiseY,
            width: '100%',
            textAlign: 'center',
            zIndex: 2,
            filter: `blur(${motionBlurPx * 0.5}px)`,
          }}>
            <div style={{
              fontSize: 48,
              fontFamily: 'Georgia, serif',
              fontStyle: 'italic',
              color: '#D4D4D8',
              letterSpacing: 1,
            }}>
              Startup Failure Rate
            </div>
            <div style={{
              fontSize: 320,
              fontWeight: 900,
              lineHeight: 0.88,
              background: 'linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              filter: 'drop-shadow(0 20px 45px rgba(0,0,0,0.95))',
            }}>
              {numCount}%
            </div>
          </div>

          {/* LAYER 2 (FOREGROUND): B&W Founder Cutout with Red Eye-Bar Positioned in Front of "90%" */}
          <div style={{
            position: 'absolute',
            bottom: 280 - subjectSlideY,
            left: '50%',
            transform: 'translateX(-50%)',
            width: 860,
            height: 980,
            zIndex: 5,
            filter: `blur(${motionBlurPx}px) drop-shadow(0 -15px 40px rgba(0,0,0,0.85))`,
          }}>
            {srcA && <Img src={srcA} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />}
          </div>

          {/* LAYER 3 (BOTTOM VIGNETTE GRADIENT for Chest-Level Glowing Subtitles) */}
          <div style={{
            position: 'absolute',
            bottom: 0,
            width: '100%',
            height: 750,
            background: 'linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.92) 55%, #000000 100%)',
            zIndex: 8,
          }} />
        </div>
      </AbsoluteFill>
    );
  }

  // 2. COSMOCUTS (0:09 & 0:15) STYLE: Vibrant Red / Green Halftone Circle + Pop-Out B&W Cutout + 2-Cut Switch
  const isSecondCut = frame >= 62 && Boolean(srcB);
  const activeCutout = isSecondCut ? srcB : srcA;
  const cutSpring = spring({
    frame: isSecondCut ? frame - 62 : frame,
    fps,
    config: { damping: 12, stiffness: 210 },
  });

  return (
    <AbsoluteFill style={gridBgStyle}>
      <div style={{ width: '100%', height: '100%', position: 'relative', transform: `scale(${slowPush})` }}>
        {/* Optional Subtle Background Video Inside Dark Mask */}
        {srcVideo && (
          <Video
            src={srcVideo}
            style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              opacity: 0.22,
              filter: 'grayscale(100%) contrast(140%)',
            }}
            muted
          />
        )}

        {/* LAYER 1: Vibrant Crimson / Emerald Circle Behind Subject (Cosmocuts 0:09 / 0:15) */}
        <div style={{
          position: 'absolute',
          top: 360,
          left: '50%',
          width: 720,
          height: 720,
          borderRadius: '50%',
          background: isSecondCut
            ? 'radial-gradient(circle, #FF2A4B 0%, #8A081C 100%)'
            : 'radial-gradient(circle, #10B981 0%, #054E37 100%)',
          transform: `translateX(-50%) scale(${cutSpring})`,
          boxShadow: isSecondCut
            ? '0 0 90px rgba(255, 42, 75, 0.55)'
            : '0 0 90px rgba(16, 185, 129, 0.55)',
          zIndex: 2,
        }} />

        {/* LAYER 2: Giant Bold Label Behind Subject's Shoulders */}
        <div style={{
          position: 'absolute',
          top: 240,
          width: '100%',
          textAlign: 'center',
          fontSize: 110,
          fontWeight: 900,
          color: '#FFFFFF',
          letterSpacing: -2,
          textTransform: 'uppercase',
          zIndex: 3,
          transform: `scale(${cutSpring})`,
          textShadow: '0 18px 40px rgba(0,0,0,0.9)',
        }}>
          {scene === 'early_vs_late_collage'
            ? (isSecondCut ? 'TOO LATE' : 'TOO EARLY')
            : scene === 'torn_paper_advisor'
            ? 'VETERAN NETWORK'
            : (isSecondCut ? 'THE DETAILS' : 'LOOKS ROSY')}
        </div>

        {/* LAYER 3: B&W Photographic Cutout Popping Out of the Circle */}
        <div style={{
          position: 'absolute',
          top: 330,
          left: '50%',
          width: 820,
          height: 880,
          transform: `translateX(-50%) translateY(${(1 - cutSpring) * 260}px) scale(${0.85 + 0.15 * cutSpring})`,
          zIndex: 5,
          filter: 'drop-shadow(0 25px 45px rgba(0,0,0,0.9))',
        }}>
          {activeCutout && (
            <Img src={activeCutout} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
          )}
        </div>

        {/* LAYER 4: Deep Bottom Vignette so Chest-Level Glowing Subtitles Pop Cleanly */}
        <div style={{
          position: 'absolute',
          bottom: 0,
          width: '100%',
          height: 760,
          background: 'linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.94) 55%, #000000 100%)',
          zIndex: 8,
        }} />
      </div>
    </AbsoluteFill>
  );
};

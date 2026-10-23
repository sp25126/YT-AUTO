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

export type ArchetypeId =
  | 'marksoy_card_zoom'
  | 'marksoy_corner_blocks'
  | 'marksoy_cream_serif'
  | 'vox_bell_curve'
  | 'vox_bar_chart'
  | 'davinci_paper_mask'
  | 'apple_glass_pill';

export const FiveArchetypeEngine: React.FC<{
  archetype: ArchetypeId;
  speakerCutoutPng?: string;
  brollVideo?: string;
  brollImg?: string;
  headlineTop?: string;
  headlineBottom?: string;
  accentColor?: string;
}> = ({
  archetype,
  speakerCutoutPng = '/assets/cutout_founder_eyebar.png',
  brollVideo,
  brollImg,
  headlineTop = 'most startups',
  headlineBottom = 'die from timing',
  accentColor = '#10B981',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const resolvePath = (src?: string) => {
    if (!src) return '';
    if (src.startsWith('http') || src.startsWith('data:')) return src;
    return staticFile(src.replace(/^\//, ''));
  };

  // ============================================================================
  // STYLE 5A: MARK SOY (MoVlt-ptxIk) SPEAKER CUTOUT CARD 3D ZOOM-OUT
  // ============================================================================
  if (archetype === 'marksoy_card_zoom') {
    const zoomOut = interpolate(frame, [0, 45], [1.35, 0.82], { extrapolateRight: 'clamp' });
    const tiltY = interpolate(frame, [0, 45], [0, -14], { extrapolateRight: 'clamp' });
    const tiltX = interpolate(frame, [0, 45], [0, 8], { extrapolateRight: 'clamp' });

    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#1B4332',
          backgroundImage: 'radial-gradient(circle at 50% 20%, #2D6A4F 0%, #081C15 100%)',
          perspective: 1200,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'Montserrat, sans-serif',
        }}
      >
        <div
          style={{
            width: 860,
            height: 1180,
            backgroundColor: '#D8F3DC',
            borderRadius: 44,
            overflow: 'hidden',
            position: 'relative',
            boxShadow: '0 45px 100px rgba(0,0,0,0.65)',
            transform: `scale(${zoomOut}) rotateY(${tiltY}deg) rotateX(${tiltX}deg)`,
            border: '6px solid rgba(255,255,255,0.4)',
          }}
        >
          {/* Top Half Text inside Card */}
          <div
            style={{
              position: 'absolute',
              top: 110,
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              padding: '0 65px',
              fontSize: 78,
              fontWeight: 900,
              color: '#081C15',
              letterSpacing: -3,
            }}
          >
            <span>90% fail</span>
            <span style={{ fontFamily: 'Georgia, serif', fontStyle: 'italic', fontWeight: 400 }}>
              timing
            </span>
          </div>

          {/* B&W Speaker Cutout Rising in Center of Card */}
          {speakerCutoutPng && (
            <Img
              src={resolvePath(speakerCutoutPng)}
              style={{
                position: 'absolute',
                bottom: 0,
                left: '50%',
                transform: 'translateX(-50%)',
                width: 780,
                height: 920,
                objectFit: 'contain',
                filter: 'grayscale(100%) contrast(1.25)',
              }}
            />
          )}
        </div>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 5B: MARK SOY DARK GRID + COLORED GEOMETRIC CORNER BLOCKS + RED PILL
  // ============================================================================
  if (archetype === 'marksoy_corner_blocks') {
    const s1 = spring({ frame, fps, config: { damping: 13, stiffness: 190 } });
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#040814',
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.06) 1.5px, transparent 1.5px),
            linear-gradient(90deg, rgba(255,255,255,0.06) 1.5px, transparent 1.5px)
          `,
          backgroundSize: '80px 80px',
          fontFamily: 'Montserrat, sans-serif',
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* Top-Left Orange Rounded Block */}
        <div
          style={{
            position: 'absolute',
            top: -60,
            left: 40,
            width: 340,
            height: 280,
            backgroundColor: '#F97316',
            borderRadius: 36,
            transform: `translateY(${(1 - s1) * -200}px)`,
          }}
        />

        {/* Top-Right Indigo Rounded Block */}
        <div
          style={{
            position: 'absolute',
            top: -40,
            right: -50,
            width: 380,
            height: 440,
            backgroundColor: '#3730A3',
            borderRadius: 42,
            transform: `translateX(${(1 - s1) * 200}px)`,
          }}
        />

        {/* Bottom-Left Crimson Rounded Block */}
        <div
          style={{
            position: 'absolute',
            bottom: 220,
            left: -40,
            width: 480,
            height: 520,
            backgroundColor: '#DC2626',
            borderRadius: 46,
            transform: `translateY(${(1 - s1) * 250}px)`,
          }}
        />

        {/* Center Kinetic Typography with Red Highlight Pill */}
        <div
          style={{
            zIndex: 10,
            padding: '0 80px',
            fontSize: 68,
            fontWeight: 800,
            color: '#FFFFFF',
            lineHeight: 1.22,
            letterSpacing: -2,
            transform: `scale(${0.85 + 0.15 * s1})`,
          }}
        >
          either they launch{' '}
          <span
            style={{
              backgroundColor: '#EF4444',
              padding: '4px 20px',
              borderRadius: 14,
              display: 'inline-block',
            }}
          >
            too early
          </span>{' '}
          or get crushed{' '}
          <span
            style={{
              fontFamily: 'Georgia, serif',
              fontStyle: 'italic',
              fontWeight: 400,
              color: '#FDE047',
            }}
          >
            too late.
          </span>
        </div>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 5C: MARK SOY WARM CREAM EDITORIAL TYPOGRAPHY SNAP (#F5F2DC)
  // ============================================================================
  if (archetype === 'marksoy_cream_serif') {
    const word1 = spring({ frame, fps, config: { damping: 14, stiffness: 220 } });
    const word2 = spring({ frame: Math.max(0, frame - 14), fps, config: { damping: 13, stiffness: 200 } });
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#F5F2DC',
          padding: '0 95px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          color: '#111111',
          fontFamily: 'Montserrat, sans-serif',
        }}
      >
        <div
          style={{
            fontSize: 82,
            fontWeight: 900,
            letterSpacing: -3,
            lineHeight: 1.05,
            opacity: word1,
            transform: `translateY(${(1 - word1) * 40}px)`,
          }}
        >
          {headlineTop}
        </div>
        <div
          style={{
            fontSize: 124,
            fontFamily: 'Georgia, Times New Roman, serif',
            fontStyle: 'italic',
            fontWeight: 400,
            letterSpacing: -4,
            lineHeight: 0.95,
            marginTop: 14,
            opacity: word2,
            transform: `translateY(${(1 - word2) * 50}px)`,
            color: '#991B1B',
          }}
        >
          {headlineBottom}
        </div>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 4A: PRO VOX ANIMATED BELL-CURVE & HIGHLIGHTER CHART
  // ============================================================================
  if (archetype === 'vox_bell_curve') {
    const drawProg = interpolate(frame, [4, 48], [0, 1000], { extrapolateRight: 'clamp' });
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#F3EFE6',
          backgroundImage: `
            linear-gradient(rgba(20,20,19,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(20,20,19,0.06) 1px, transparent 1px)
          `,
          backgroundSize: '36px 36px',
          padding: '130px 75px',
          fontFamily: 'Montserrat, sans-serif',
          color: '#141413',
        }}
      >
        <div
          style={{
            fontFamily: 'Courier New, monospace',
            fontSize: 30,
            fontWeight: 700,
            letterSpacing: 2,
            borderBottom: '4px solid #141413',
            paddingBottom: 12,
            marginBottom: 30,
          }}
        >
          FIG 02 // MARKET TIMING BELL CURVE
        </div>
        <div style={{ fontSize: 68, fontWeight: 900, lineHeight: 1.1, marginBottom: 50 }}>
          THE <span style={{ backgroundColor: '#FFE600', padding: '0 14px' }}>GOLDILOCKS</span> ENTRY WINDOW
        </div>

        {/* Animated SVG Bell Curve with Too Early / Sweet Spot / Too Late Zones */}
        <svg width="930" height="620" viewBox="0 0 930 620" style={{ overflow: 'visible' }}>
          <line x1="40" y1="520" x2="890" y2="520" stroke="#141413" strokeWidth="5" />
          <line x1="40" y1="60" x2="40" y2="520" stroke="#141413" strokeWidth="5" />
          <rect x="330" y="80" width="260" height="440" fill="rgba(16, 185, 129, 0.18)" />
          <line x1="330" y1="80" x2="330" y2="520" stroke="#10B981" strokeWidth="4" strokeDasharray="12 10" />
          <line x1="590" y1="80" x2="590" y2="520" stroke="#E63946" strokeWidth="4" strokeDasharray="12 10" />
          <path
            d="M 40 515 C 180 510, 260 440, 340 240 C 410 70, 510 70, 580 240 C 660 440, 750 510, 890 515"
            fill="none"
            stroke="#141413"
            strokeWidth="12"
            strokeDasharray="1200"
            strokeDashoffset={1200 - drawProg}
            strokeLinecap="round"
          />
          <text x="175" y="575" textAnchor="middle" fontSize="28" fontWeight="900" fill="#E63946">
            TOO EARLY (0 DEMAND)
          </text>
          <text x="460" y="575" textAnchor="middle" fontSize="28" fontWeight="900" fill="#10B981">
            OPTIMAL ENTRY
          </text>
          <text x="745" y="575" textAnchor="middle" fontSize="28" fontWeight="900" fill="#E63946">
            TOO LATE (GIANTS)
          </text>
        </svg>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 4B: PRO VOX BAR CHART & ODOMETER
  // ============================================================================
  if (archetype === 'vox_bar_chart') {
    const count = Math.round(interpolate(frame, [4, 40], [0, 90], { extrapolateRight: 'clamp' }));
    const barWidth = interpolate(frame, [4, 40], [0, 820], { extrapolateRight: 'clamp' });
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#F3EFE6',
          backgroundImage: `
            linear-gradient(rgba(20,20,19,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(20,20,19,0.06) 1px, transparent 1px)
          `,
          backgroundSize: '36px 36px',
          padding: '130px 75px',
          fontFamily: 'Montserrat, sans-serif',
          color: '#141413',
        }}
      >
        <div
          style={{
            fontFamily: 'Courier New, monospace',
            fontSize: 30,
            fontWeight: 700,
            letterSpacing: 2,
            borderBottom: '4px solid #141413',
            paddingBottom: 12,
            marginBottom: 30,
          }}
        >
          FIG 01 // STARTUP MORTALITY AUDIT
        </div>
        <div style={{ fontSize: 62, fontWeight: 900, lineHeight: 1.1, marginBottom: 50 }}>
          MORTALITY RATE <span style={{ backgroundColor: '#FFE600', padding: '0 14px' }}>BY TIMING</span>
        </div>
        <div style={{ fontSize: 130, fontWeight: 900, color: '#E63946', marginBottom: 20 }}>
          {count}%
        </div>
        <div
          style={{
            width: '100%',
            height: 48,
            backgroundColor: '#D1CDC2',
            borderRadius: 12,
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              width: `${barWidth}px`,
              height: '100%',
              backgroundColor: '#E63946',
            }}
          />
        </div>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 2: DAVINCI RESOLVE FUSION TEXTURED PAPER & MASK
  // ============================================================================
  if (archetype === 'davinci_paper_mask') {
    const pop = spring({ frame, fps, config: { damping: 14, stiffness: 200 } });
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#ECEAE4',
          backgroundImage: 'radial-gradient(circle at 50% 50%, #F5F3ED 0%, #D8D5CD 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'Montserrat, sans-serif',
          padding: '100px 60px',
        }}
      >
        <div
          style={{
            width: 880,
            backgroundColor: '#FFFFFF',
            padding: '24px 24px 80px 24px',
            borderRadius: 16,
            boxShadow: '0 30px 70px rgba(0,0,0,0.25)',
            transform: `rotate(-1.5deg) scale(${pop})`,
          }}
        >
          <div
            style={{
              width: '100%',
              height: 700,
              overflow: 'hidden',
              borderRadius: 8,
              backgroundColor: '#000',
            }}
          >
            {brollVideo && (
              <Video
                src={resolvePath(brollVideo)}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                muted
              />
            )}
          </div>
          <div
            style={{
              marginTop: 24,
              fontSize: 48,
              fontWeight: 900,
              color: '#111',
              textAlign: 'center',
              letterSpacing: -1,
            }}
          >
            {headlineTop.toUpperCase()}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // ============================================================================
  // STYLE 1: APPLE GLASS NOTIFICATION PILL
  // ============================================================================
  const slideIn = spring({ frame, fps, config: { damping: 15, stiffness: 210 } });
  return (
    <AbsoluteFill style={{ backgroundColor: 'transparent', fontFamily: 'Montserrat, sans-serif' }}>
      <div
        style={{
          position: 'absolute',
          top: 140,
          left: '50%',
          transform: `translateX(-50%) translateY(${(1 - slideIn) * -120}px)`,
          width: 920,
          padding: '26px 40px',
          borderRadius: 28,
          backgroundColor: 'rgba(15, 23, 42, 0.72)',
          backdropFilter: 'blur(24px)',
          border: '2px solid rgba(255, 255, 255, 0.18)',
          boxShadow: '0 25px 60px rgba(0,0,0,0.85), 0 0 30px rgba(16, 185, 129, 0.3)',
          display: 'flex',
          alignItems: 'center',
          gap: 24,
        }}
      >
        <div
          style={{
            width: 18,
            height: 18,
            borderRadius: '50%',
            backgroundColor: accentColor,
            boxShadow: `0 0 15px ${accentColor}`,
          }}
        />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 24, fontWeight: 800, color: accentColor, letterSpacing: 2 }}>
            CASE STUDY ALERT
          </div>
          <div style={{ fontSize: 44, fontWeight: 900, color: '#FFFFFF', lineHeight: 1.15 }}>
            {headlineTop}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

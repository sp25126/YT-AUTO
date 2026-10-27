import React from 'react';
import { AbsoluteFill } from 'remotion';

export interface EffectCraftPolishOverlayProps {
  frame: number;
  accentHex: string;
}

export const EffectCraftPolishOverlay: React.FC<EffectCraftPolishOverlayProps> = ({ frame, accentHex }) => {
  const orbs = [
    { x: 140, baseY: 1400, size: 14, speed: 3.2 },
    { x: 920, baseY: 1250, size: 18, speed: 2.6 },
    { x: 260, baseY: 850, size: 10, speed: 4.1 },
    { x: 830, baseY: 620, size: 15, speed: 3.5 },
  ];

  return (
    <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 18 }}>
      {/* EffectCraft Fine Vertical Scanlines (15px repeating pattern) */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'repeating-linear-gradient(90deg, rgba(255,255,255,0.018) 0px, rgba(255,255,255,0.018) 1px, transparent 1px, transparent 15px)',
        }}
      />
      {/* Aevy Video School Glowing Particle Orbs */}
      {orbs.map((o, i) => {
        const yPos = (o.baseY - frame * o.speed) % 1920;
        const finalY = yPos < 0 ? yPos + 1920 : yPos;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: o.x + Math.sin((frame + i * 20) * 0.06) * 28,
              top: finalY,
              width: o.size,
              height: o.size,
              borderRadius: '50%',
              backgroundColor: accentHex,
              boxShadow: `0 0 24px 6px ${accentHex}`,
              opacity: 0.55,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

export default EffectCraftPolishOverlay;

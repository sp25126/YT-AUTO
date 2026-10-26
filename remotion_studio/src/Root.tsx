import React from 'react';
import { Composition, staticFile } from 'remotion';
import { CapCutCollageScenes } from './CapCutCollageScenes';
import { FiveStyleDirector, EditStyle, BeatId } from './FiveStyleDirector';
import { FiveArchetypeEngine } from './FiveArchetypeEngine';
import { EditorialStudioMaster } from './EditorialStudioMaster';
import { ProMotionDirector } from './ProMotionDirector';
import { ProDepthEditor } from './ProDepthEditor';
import wordsData from '../public/assets/words.json';

export const Root: React.FC = () => {
  const styles: { idPrefix: string; styleVariant: EditStyle }[] = [
    { idPrefix: 'Iman', styleVariant: 'iman_documentary' },
    { idPrefix: 'Hormozi', styleVariant: 'hormozi_hud' },
    { idPrefix: 'Bento', styleVariant: 'apple_bento' },
    { idPrefix: 'Magnates', styleVariant: 'magnates_dossier' },
  ];

  const beats: {
    suffix: string;
    beat: BeatId;
    duration: number;
    videoA: string;
    videoB?: string;
  }[] = [
    {
      suffix: 'Beat1',
      beat: 'beat1_90_fail',
      duration: 120,
      videoA: '/assets/broll_beat1_crash.mp4',
    },
    {
      suffix: 'Beat2',
      beat: 'beat2_timing',
      duration: 147,
      videoA: '/assets/broll_beat2_early.mp4',
      videoB: '/assets/broll_beat2_late.mp4',
    },
    {
      suffix: 'Beat3',
      beat: 'beat3_network',
      duration: 144,
      videoA: '/assets/broll_beat3_mentors.mp4',
    },
    {
      suffix: 'Beat4',
      beat: 'beat4_rosy_details',
      duration: 162,
      videoA: '/assets/broll_beat4_rosy.mp4',
      videoB: '/assets/broll_beat4_devil.mp4',
    },
  ];

  return (
    <>
      {/* 5-Style Director Compositions */}
      {styles.map((s) =>
        beats.map((b) => (
          <Composition
            key={`${s.idPrefix}-${b.suffix}`}
            id={`${s.idPrefix}-${b.suffix}`}
            component={FiveStyleDirector}
            durationInFrames={b.duration}
            fps={30}
            width={1080}
            height={1920}
            defaultProps={{
              styleVariant: s.styleVariant,
              beat: b.beat,
              videoA: b.videoA,
              videoB: b.videoB,
            }}
          />
        ))
      )}

      {/* Style 1: Apple Glass Notification Pills */}
      <Composition
        id="Style1-Pill1"
        component={FiveArchetypeEngine}
        durationInFrames={114}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'apple_glass_pill' as const,
          headlineTop: '90% FAIL FROM WRONG TIMING',
          accentColor: '#10B981',
        }}
      />
      <Composition
        id="Style1-Pill2"
        component={FiveArchetypeEngine}
        durationInFrames={132}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'apple_glass_pill' as const,
          headlineTop: 'CRITICAL TIMING WINDOW',
          accentColor: '#EF4444',
        }}
      />
      <Composition
        id="Style1-Pill3"
        component={FiveArchetypeEngine}
        durationInFrames={138}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'apple_glass_pill' as const,
          headlineTop: '20-YEAR VETERAN NETWORK',
          accentColor: '#10B981',
        }}
      />
      <Composition
        id="Style1-Pill4"
        component={FiveArchetypeEngine}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'apple_glass_pill' as const,
          headlineTop: 'DEVIL IN THE DETAILS',
          accentColor: '#F59E0B',
        }}
      />

      {/* Style 2: DaVinci Paper Masks */}
      <Composition
        id="Style2-Paper1"
        component={FiveArchetypeEngine}
        durationInFrames={114}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'davinci_paper_mask' as const,
          headlineTop: '90% FAILURE RATE',
          brollVideo: '/assets/broll_beat1_crash.mp4',
        }}
      />
      <Composition
        id="Style2-Paper2"
        component={FiveArchetypeEngine}
        durationInFrames={138}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'davinci_paper_mask' as const,
          headlineTop: '20-YEAR VETERANS',
          brollVideo: '/assets/broll_beat3_mentors.mp4',
        }}
      />

      {/* Style 4: Vox Data Journalism */}
      <Composition
        id="Style4-BarChart"
        component={FiveArchetypeEngine}
        durationInFrames={120}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'vox_bar_chart' as const,
        }}
      />
      <Composition
        id="Style4-BellCurve"
        component={FiveArchetypeEngine}
        durationInFrames={138}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'vox_bell_curve' as const,
        }}
      />
      <Composition
        id="Style4-Blueprint"
        component={FiveArchetypeEngine}
        durationInFrames={144}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'davinci_paper_mask' as const,
          headlineTop: 'ADVISOR BLUEPRINT',
          brollVideo: '/assets/broll_beat3_mentors.mp4',
        }}
      />

      {/* Style 5: Mark Soy Mixed Media Archetypes */}
      <Composition
        id="Style5-CardZoom"
        component={FiveArchetypeEngine}
        durationInFrames={114}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'marksoy_card_zoom' as const,
          speakerCutoutPng: '/assets/cutout_founder_eyebar.png',
        }}
      />
      <Composition
        id="Style5-CornerBlocks"
        component={FiveArchetypeEngine}
        durationInFrames={147}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'marksoy_corner_blocks' as const,
        }}
      />
      <Composition
        id="Style5-CreamSerif1"
        component={FiveArchetypeEngine}
        durationInFrames={144}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'marksoy_cream_serif' as const,
          headlineTop: 'TALK TO PEOPLE WHO',
          headlineBottom: 'spent 20 years in it',
        }}
      />
      <Composition
        id="Style5-CreamSerif2"
        component={FiveArchetypeEngine}
        durationInFrames={162}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          archetype: 'marksoy_cream_serif' as const,
          headlineTop: 'OUTSIDE LOOKS ROSY',
          headlineBottom: 'devil in the details',
        }}
      />

      {/* Nick Automates / Prompt-Motion Editorial Studio Master */}
      <Composition
        id="EditorialStudioMaster"
        component={EditorialStudioMaster}
        durationInFrames={1002}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          speakerVideoUrl: staticFile('assets/speaker_base.mp4'),
          brollEarlyUrl: staticFile('assets/broll_beat2_early.mp4'),
          brollLateUrl: staticFile('assets/broll_beat2_late.mp4'),
          brollMentorUrl: staticFile('assets/broll_beat3_mentors.mp4'),
          brollRosyUrl: staticFile('assets/broll_beat4_rosy.mp4'),
          brollDetailUrl: staticFile('assets/broll_beat4_devil.mp4'),
          words: wordsData,
        }}
      />

      {/* Senior Motion Designer Continuous Morphing Master */}
      <Composition
        id="ProMotionDirector"
        component={ProMotionDirector}
        durationInFrames={1002}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          speakerVideoUrl: staticFile('assets/speaker_base.mp4'),
          brollEarlyUrl: staticFile('assets/broll_beat2_early.mp4'),
          brollLateUrl: staticFile('assets/broll_beat2_late.mp4'),
          brollMentorUrl: staticFile('assets/broll_beat3_mentors.mp4'),
          brollRosyUrl: staticFile('assets/broll_beat4_rosy.mp4'),
          brollDetailUrl: staticFile('assets/broll_beat4_devil.mp4'),
          words: wordsData,
        }}
      />

      {/* Pro Depth Editor 3-Layer Sandwich Master */}
      <Composition
        id="ProDepthEditor"
        component={ProDepthEditor}
        durationInFrames={1002}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          speakerVideoUrl: staticFile('assets/speaker_base.mp4'),
          rotoFolderUrl: 'assets/roto_hook',
          brollEarlyVideo: staticFile('assets/broll_candidates/early_cand_2.mp4'),
          brollEarlyCutout: staticFile('assets/broll_candidates/early_cand_2_fg_cutout.png'),
          brollLateVideo: staticFile('assets/broll_candidates/late_cand_3.mp4'),
          brollLateCutout: staticFile('assets/broll_candidates/late_cand_3_fg_cutout.png'),
          brollMentorVideo: staticFile('assets/broll_candidates/mentor_cand_3.mp4'),
          brollMentorCutout: staticFile('assets/broll_candidates/mentor_cand_3_fg_cutout.png'),
          brollRosyVideo: staticFile('assets/broll_candidates/rosy_cand_2.mp4'),
          brollRosyCutout: staticFile('assets/broll_candidates/rosy_cand_2_fg_cutout.png'),
          brollDetailVideo: staticFile('assets/broll_candidates/detail_cand_3.mp4'),
          brollDetailCutout: staticFile('assets/broll_candidates/detail_cand_3_fg_cutout.png'),
          words: wordsData,
        }}
      />
    </>
  );
};

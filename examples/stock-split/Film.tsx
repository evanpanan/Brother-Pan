import {Audio} from '@remotion/media';
import {AbsoluteFill, Sequence, staticFile, useCurrentFrame} from 'remotion';
import data from './episode.json';
import {Host, type Speaker} from './library/hosts/Host';
import {SplitCertificate} from './library/scenes/SplitCertificate';
import {Hand} from './library/scenes/ActionObjects';
import {C, L, T, V} from './library/theme';

type Cap = {text: string; startMs: number; endMs: number};
type Turn = {
  sceneId: string; start: number; frames: number; speaker: Speaker;
  caps: Cap[]; voicedMs?: number[][];
};
const episode = data as {fps: number; audio?: string; scenes: Turn[]};

// Track the wording even if a new voice puts the edit across two caption pages.
function cue(turn: Turn, phrase: string, fallback: number) {
  const index = turn.caps.map(c => c.text).join('').indexOf(phrase);
  if (index < 0) return turn.frames / episode.fps * fallback;
  let cursor = 0;
  for (const cap of turn.caps) {
    if (index < cursor + cap.text.length) {
      return (cap.startMs + (cap.endMs - cap.startMs) * (index - cursor) / cap.text.length) / 1000;
    }
    cursor += cap.text.length;
  }
  return turn.frames / episode.fps * fallback;
}

export const Film = () => {
  const frame = useCurrentFrame();
  const turn = episode.scenes.find(s => frame >= s.start && frame < s.start + s.frames)!;
  const t = (frame - turn.start) / episode.fps;
  const ask = turn.sceneId === 'second-share';
  const cut = turn.sceneId === 'cut-the-ticket';
  const count = turn.sceneId === 'check-the-total';
  const localMs = t * 1000;
  const cap = turn.caps.find(c => c.startMs <= localMs && localMs < c.endMs);
  const talking = !!episode.audio && !!turn.voicedMs?.some(([a,b]) => a <= localMs && localMs < b);
  const splitAt = cue(turn, '一撕', .48);
  const split = count ? 1 : cut ? V(t, splitAt - .12, splitAt + .24) : 0;
  const pull = count ? 1 : cut ? V(t, splitAt + .06, splitAt + .59) : 0;
  const leftBeat = cue(turn, '五十', .12);
  const totalBeat = cue(turn, '还是一百', .45);
  const total = count ? V(t, totalBeat, totalBeat + .33) : 0;
  const lift = ask ? V(t, 0, .54) : 1;
  // Move from a two-shot into an insert, then pull back on the same two pieces.
  const zoom = cut ? V(t, 0, .52) : count ? 1 - V(t, .16, .82) : 0;
  const ticketY = L(899, 847, zoom) + (1 - lift) * 52;
  const ticketScale = L(1.15, 1.80, zoom);
  const greet = ask && t < .74;
  const chiliPose = count ? (t < totalBeat ? 2 : 1) : ask ? (greet ? 2 : 1) : 2;
  const panPose = cut && split < .5 ? 2 : 1;
  const hostOpacity = 1 - zoom;
  const readoutAt = count ? V(t, leftBeat, leftBeat + .25) : 0;
  const secondPieceAt = cue(turn, '两张合起来', .3);
  const answers: [number, number] = count ? [readoutAt, V(t, secondPieceAt, secondPieceAt + .28)] : [0, 0];
  const flipAt = cue(turn, '变两股', .65);
  const flip = ask ? V(t, flipAt - .18, flipAt + .24) : 1;
  const ink = count ? 1 : cut ? V(t, splitAt - .19, splitAt + .15) : 0;
  // At contact the fingers meet the paper edges, then follow the separate pieces.
  const reach = count ? 1 - V(t, .30, .86) : cut ? V(t, .20, 1.05) : 0;
  const fingerX = 129 + 98 * reach - pull * 63;
  const lines = cap ? Array.from(cap.text) : [];
  const mid = Math.ceil(lines.length / 2);
  const caption = lines.length > 14 ? [lines.slice(0, mid).join(''), lines.slice(mid).join('')] : [lines.join('')];
  return <AbsoluteFill style={{background: C.bg}}>
    <style>{`@font-face{font-family:Head;src:url('${staticFile('head.woff')}')}`}</style>
    <svg viewBox="0 0 1080 1920" aria-label="一股值一百元的纸票被撕成两张各值五十元的纸票">
      <path d="M0 0h1080v22H0Z" fill={C.lime}/>
      <path d="M133 288h814" stroke={C.gold} strokeWidth="2"/>
      <T y={259} s={28}>拆股实验</T>
      <T y={395} s={67}>{ask ? '股数翻倍 钱也翻倍？' : cut ? '跟着这张纸票看' : '两张加起来呢？'}</T>
      {ask && <g transform="translate(540 617)">
        <rect x="-57" y="-45" width="114" height="88" rx="8" fill={C.ink}/>
        <g transform={`scale(1 ${Math.max(.06, Math.abs(1 - 2 * flip))})`}>
          <T x={0} y={15} s={37} c={C.white}>{flip < .5 ? '1 股' : '2 股'}</T>
        </g>
        <path d="M-60-1h9m102 0h9" stroke={C.gold} strokeWidth="5"/>
      </g>}
      <g opacity={hostOpacity}>
        <path d="M144 769q25-51 89-51h609q64 0 81 51v69H144Z" fill="#d0d8c2"/>
        <Host speaker="M" activeSpeaker={turn.speaker} voicing={talking} t={t}
          pose={panPose} gaze={greet ? 'viewer' : 'subject'} x={197} y={490} scale={.68}/>
        <Host speaker="F" activeSpeaker={turn.speaker} voicing={talking} t={t}
          pose={chiliPose} gaze={greet ? 'viewer' : 'partner'} x={602} y={490} scale={.68}/>
      </g>
      <g>
        <path d={`M124 ${L(813, 615,zoom)}Q120 ${L(792,595,zoom)} 146 ${L(789,590,zoom)}H934Q955 ${L(789,590,zoom)} 958 ${L(811,610,zoom)}L982 1141H99Z`} fill="#cdd9bf"/>
        <path d="M99 1141h883v19q1 7-11 7H111q-13 0-12-8Z" fill={C.ink}/>
        <ellipse cx="540" cy={ticketY + ticketScale * 94 + 11} rx={ticketScale * 168} ry="13"
          fill={C.ink} opacity=".08"/>
        <g transform={`translate(540 ${ticketY}) rotate(${(1-lift) * -9}) scale(${ticketScale})`}>
          <SplitCertificate tear={split} spread={pull} ink={ink} answers={answers}/>
        </g>
        {zoom > 0 && <g opacity={zoom}>
          <Hand x={fingerX} y={ticketY - 20 - 9 * pull} angle={-3 - pull * 4} scale={.78}/>
          <g transform="translate(1080 0) scale(-1 1)"><Hand x={fingerX} y={ticketY - 20 + 9 * pull} angle={-3 + pull * 4} scale={.78}/></g>
        </g>}
        <g opacity={readoutAt}>
          <path d="M389 1056v21h302v-21" stroke={C.ink} strokeWidth="3" fill="none" opacity={answers[1]}/>
          <T y={1128} s={42}>{total > .5 ? '50 + 50 = 100 元' : answers[1] > .5 ? '50 + 50' : ''}</T>
        </g>
      </g>
      <T y={1236} s={25}>一拆二示意　假设其他价格因素不变</T>
      {caption.map((line, i) => <T key={i} y={1377 + i * 60} s={44}>{line}</T>)}
    </svg>
    {cut && episode.audio && <Sequence from={turn.start + Math.round(splitAt * episode.fps)} durationInFrames={Math.ceil(.27 * episode.fps)}>
      <Audio src={staticFile('paper-tear.wav')} volume={.39}/>
    </Sequence>}
    {episode.audio && <Audio src={staticFile(episode.audio)} volume={.75}/>}
  </AbsoluteFill>;
};

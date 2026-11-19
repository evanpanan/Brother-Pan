import {Composition} from 'remotion';
import {Film} from './Film';
import episode from './episode.json';
export const Root=()=> <Composition id="BrotherPan" component={Film} width={1080} height={1920} fps={episode.fps} durationInFrames={Math.max(...episode.scenes.map(s=>s.start+s.frames))}/>;

import {C, T} from '../theme';

// tear separates the edges; spread settles the halves; ink and answers reveal the two new prices.
const tearEdge = '0 -95 4 -80 -3 -67 4 -53 -2 -38 3 -24 -4 -8 2 7 -3 22 3 36 -3 50 4 64 -2 80 0 95';
export function SplitCertificate({tear, spread, ink, answers, faceValue = 100}: {
  tear: number; spread: number; ink: number; answers: [number, number]; faceValue?: number;
}) {
  return <g>
    {[-1, 1].map(side => {
      const x = side * (tear * 12 + spread * 29);
      const y = side * Math.sin(spread * Math.PI) * 14;
      return <g key={side} transform={`translate(${x} ${y}) rotate(${side * spread * 5})`}>
        <polygon points={`${side * 158} -95 ${tearEdge} ${side * 158} 95`}
          fill="#fffbea" stroke={C.ink} strokeWidth={2}/>
        <g transform={`translate(${side * 80} 0)`}>
          <rect x="-68" y="-82" width="136" height="164" rx="6" stroke="#6b8d75" fill="none" strokeWidth="2"/>
          {[-1, 1].map(sign => <g key={sign} transform={`translate(0 ${sign * 66})`}>
            <path d="M-58 0h33m50 0h33" stroke="#a38850" strokeWidth="2"/>
            <path d="M-12 0l12-5 12 5-12 5Z" fill={C.gold}/>
          </g>)}
          <g opacity={ink}>
            <T x={0} y={-26} s={21}>1 股</T>
            <g opacity={1 - answers[side < 0 ? 0 : 1]}><T x={0} y={25} s={38}>?</T></g>
            <g opacity={answers[side < 0 ? 0 : 1]}><T x={0} y={25} s={38}>{faceValue / 2}</T></g>
            <T x={0} y={52} s={18}>元</T>
          </g>
        </g>
      </g>;
    })}
    <g opacity={1 - ink}>
      <rect x="-95" y="-55" width="190" height="110" rx="55" fill="#fffbea" stroke="#a38850" strokeWidth="2"/>
      <T x={0} y={-12} s={22}>1 股</T>
      <T x={0} y={33} s={41}>{faceValue} 元</T>
    </g>
  </g>;
}

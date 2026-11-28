/** Coordinate origin is the centre of a 510 × 318 ticket. Render inside an SVG. */
type TicketProps = {
  x?: number;
  y?: number;
  scale?: number;
  rotate?: number;
  flip?: number;
  stamp?: number;
  title: string;
  amount: string;
  detail: string;
  reverseTitle?: string;
  reverseAmount?: string;
  reverseDetail?: string;
  stampText?: string;
  accent?: string;
  paper?: string;
  ink?: string;
};

const outline = 'M-244-148H244q8 0 8 8v62a14 14 0 0 0 0 28v93a14 14 0 0 0 0 28v67q0 8-8 8h-488q-8 0-8-8V71a14 14 0 0 0 0-28v-93a14 14 0 0 0 0-28v-62q0-8 8-8Z';
const unitInterval = (progress: number) => Math.max(0, Math.min(1, progress));

// Leave room for the perforated stub when combining full-width Chinese and Latin digits.
function fontSize(label: string, preferred: number, width: number) {
  let units = 0;
  for (const char of label) units += char.charCodeAt(0) < 128 ? 0.62 : 1;
  return Math.min(preferred, width / Math.max(units, 1));
}

export function SubscriptionTicket({
  x = 0, y = 0, scale = 1, rotate = 0, flip = 0, stamp = 0,
  title, amount, detail, reverseTitle = title, reverseAmount = amount,
  reverseDetail = detail, stampText = '', accent = '#ddb357',
  paper = '#fff5da', ink = '#173c34',
}: TicketProps) {
  const angle = Math.PI * unitInterval(flip);
  const isBack = Math.cos(angle) < 0;
  const faceWidth = Math.max(0.035, Math.abs(Math.cos(angle)));
  const contact = unitInterval(stamp);
  const faceTitle = isBack ? reverseTitle : title;
  const faceAmount = isBack ? reverseAmount : amount;
  const faceDetail = isBack ? reverseDetail : detail;

  return <g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`}>
    <g transform={`scale(${faceWidth} 1) skewY(${Math.sin(angle) * 6})`}>
      <path d={outline} fill="#122821" opacity=".24" transform="translate(7 11)"/>
      <path d={outline} fill={isBack ? '#f0ebd5' : paper} stroke={ink} strokeWidth="4"/>
      <path d="M-227-125h451v251h-451Z" fill="none" stroke={accent} strokeWidth="2"/>
      <path d="M150-126v250" stroke={ink} opacity=".65" strokeWidth="2" strokeDasharray="6 7"/>
      <path d="M-219-38h344m-344 94h343" fill="none" stroke={accent} strokeWidth="2"/>
      <g fontFamily="Head, sans-serif" fill={ink}>
        <text x="-209" y="-66" fontSize={fontSize(faceTitle, 36, 330)}>{faceTitle}</text>
        <text x="-211" y="33" opacity={stampText ? Math.max(0, 1 - 2 * contact) : 1}
          fontSize={fontSize(faceAmount, 68, 328)}>{faceAmount}</text>
        <text x="-209" y="102" fontSize={fontSize(faceDetail, 27, 325)}>{faceDetail}</text>
      </g>
      {Array.from({length: 24}, (_, line) => <rect key={line} x="168" y={-107 + line * 8.6}
        width={line % 6 === 0 ? 48 : 40} height={[2, 3.6, 5, 2.5, 3][line % 5]} fill={ink}/>)}
      {stampText && contact > 0 && <g opacity={contact}
        transform={`translate(-6 18) rotate(-10) scale(${1 + (1 - contact) ** 2 * 0.38})`}>
        <rect x="-141" y="-39" width="282" height="78" rx="8" fill={paper} stroke="#ad4c32" strokeWidth="6"/>
        <rect x="-133" y="-31" width="266" height="62" rx="4" fill="none" stroke="#ad4c32" strokeWidth="2"/>
        <text x="0" y="17" textAnchor="middle" fill="#a3432c" fontFamily="Head, sans-serif"
          fontSize={fontSize(stampText, 43, 248)}>{stampText}</text>
      </g>}
    </g>
  </g>;
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function absBig(x) { return x < 0n ? -x : x; }
function gcd(a, b) {
  a = absBig(a); b = absBig(b);
  while (b) [a, b] = [b, a % b];
  return a || 1n;
}

class Rat {
  constructor(n, d = 1n) {
    n = BigInt(n); d = BigInt(d);
    if (d < 0n) { n = -n; d = -d; }
    const g = gcd(n, d);
    this.n = n / g; this.d = d / g;
  }
  add(o) { o = o instanceof Rat ? o : new Rat(o); return new Rat(this.n * o.d + o.n * this.d, this.d * o.d); }
  mul(o) { o = o instanceof Rat ? o : new Rat(o); return new Rat(this.n * o.n, this.d * o.d); }
  eq(o) { o = o instanceof Rat ? o : new Rat(o); return this.n === o.n && this.d === o.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}

function comb(n, k) {
  if (k < 0 || k > n) return 0n;
  k = Math.min(k, n - k);
  let out = 1n;
  for (let i = 1; i <= k; i++) out = out * BigInt(n - k + i) / BigInt(i);
  return out;
}

function K(n, j, w) {
  let out = 0n;
  const lo = Math.max(0, j - (n - w));
  const hi = Math.min(j, w);
  for (let i = lo; i <= hi; i++) {
    const term = comb(w, i) * comb(n - w, j - i);
    out += (i % 2 ? -term : term);
  }
  return out;
}

// -----------------------------------------------------------------------------
// Weight 72: exact lift-pair certificate.
// -----------------------------------------------------------------------------
function P72(r, a) {
  const w1 = r + a;
  const w2 = r + 72 - a;
  const T = j => K(169, j, w1) + K(169, j, w2);
  return 7280n + 1840n * K(97, 1, r) + 196n * T(2) + 44n * T(3) + 7n * T(4) + T(5);
}

const allowed72 = new Set([0, ...Array.from({length: 13}, (_, i) => 72 + 8 * i)]);
const states72 = [];
for (let r = 0; r <= 97; r++) {
  for (let a = 0; a <= 36; a++) {
    if (allowed72.has(r + a) && allowed72.has(r + 72 - a)) states72.push([r, a]);
  }
}
assert(states72.length === 61, `weight72 state count = ${states72.length}`);
assert(P72(0, 0) === 1349517312n, 'weight72 P(0,0) mismatch');
for (const [r, a] of states72) {
  if (r === 0 && a === 0) continue;
  assert(P72(r, a) <= 0n, `positive P72 at (${r},${a})`);
}

// -----------------------------------------------------------------------------
// Weight 64 first residual certificate.
// -----------------------------------------------------------------------------
function PR(w) {
  return 4480n + 3008n * K(105, 1, w) + 748n * K(105, 2, w)
    + 212n * K(105, 3, w) + 27n * K(105, 4, w) + 5n * K(105, 5, w);
}
const expectedPR = new Map([
  [44, 0n], [48, -32768n], [52, 0n], [56, 0n], [60, 0n], [64, 0n],
  [68, -196608n], [72, -1146880n], [76, -3932160n], [80, -10321920n],
  [84, -22937600n], [88, -45416448n], [92, -82575360n], [96, -140574720n],
  [100, -227082240n], [104, -351436800n],
]);
assert(PR(0) === 656015360n, 'PR(0) mismatch');
for (const [w, expected] of expectedPR) {
  assert(PR(w) === expected, `PR(${w})=${PR(w)} expected ${expected}`);
}

// -----------------------------------------------------------------------------
// Weight 48 first residual polynomial and Krawtchouk expansion.
// -----------------------------------------------------------------------------
function P48(r) {
  return -BigInt(r - 52) * BigInt(r - 60) * BigInt(r - 64) * BigInt(r - 72) * BigInt(r - 76);
}
function fourP48Expansion(r) {
  const coeffs = [39540n, 18540n, 4316n, 900n, 129n, 15n];
  return coeffs.reduce((s, c, j) => s + c * K(121, j, r), 0n);
}
for (let r = 0; r <= 121; r++) {
  assert(4n * P48(r) === fourP48Expansion(r), `P48 expansion fails at r=${r}`);
}
assert(P48(0) === 1092648960n, 'P48(0) mismatch');
for (let r = 52; r <= 120; r += 4) assert(P48(r) <= 0n, `P48 positive at ${r}`);

const strict48 = new Set([0, 48, ...Array.from({length: 14}, (_, i) => 64 + 8 * i)]);
const profiles48 = [];
for (let r = 0; r <= 121; r++) {
  for (let a = 0; a <= 24; a++) {
    const w1 = r + a, w2 = r + 48 - a;
    if (strict48.has(w1) && strict48.has(w2) && [24,32,36,40,44,48].includes(r)) {
      profiles48.push([r,a,w1,w2]);
    }
  }
}
const expectedProfiles48 = [
  [24,24,48,48], [32,16,48,64], [36,12,48,72], [40,8,48,80], [40,24,64,64],
  [44,4,48,88], [44,20,64,72], [48,0,48,96], [48,16,64,80], [48,24,72,72],
];
assert(JSON.stringify(profiles48) === JSON.stringify(expectedProfiles48), 'weight48 profile list mismatch');

// -----------------------------------------------------------------------------
// A_64 linear-programming polynomial.
// -----------------------------------------------------------------------------
const lambda = new Rat(455n, 131072n);
const mus = [
  new Rat(19435n,131072n),
  new Rat(173901n,65536n),
  new Rat(2173171n,65536n),
  new Rat(114782941n,524288n),
  new Rat(541119579n,524288n),
];
function PLP(w) {
  let out = lambda;
  for (let j = 1; j <= 5; j++) {
    out = out.add(mus[j-1].mul(new Rat(K(169,j,w), comb(169,j))));
  }
  return out;
}
const lpWeights = [0,48,64,72,80,88,96,104,112,120,128,136,144,152,160,168];
const lpExpected = [1287,21,1,0,0,0,0,0,-1,-6,-21,-56,-126,-252,-462,-792];
for (let i = 0; i < lpWeights.length; i++) {
  assert(PLP(lpWeights[i]).eq(lpExpected[i]), `LP value at ${lpWeights[i]} = ${PLP(lpWeights[i])}`);
}
assert(lambda.mul(2n ** 19n).add(-1287).eq(533), 'A64 constant 533 mismatch');
assert(lambda.mul(2n ** 20n).add(-1287).eq(2353), 'A64 constant 2353 mismatch');

// -----------------------------------------------------------------------------
// Incidence arithmetic.
// -----------------------------------------------------------------------------
const N = 533n;
const totalIncidence = N * 64n;
assert(totalIncidence === 34112n, 'total incidence mismatch');
const lower = 26n * (201n*200n/2n) + 143n * (202n*201n/2n);
assert(lower === 3425643n, 'convexity lower bound mismatch');
const pairs = N * (N-1n) / 2n;
assert(pairs === 141778n, 'pair count mismatch');
const baseline24 = 24n * pairs;
assert(baseline24 === 3402672n, '24-baseline mismatch');
const e28 = (lower - baseline24 + 3n) / 4n;
assert(e28 === 5743n, 'e28 lower bound mismatch');
assert(2n * e28 > 21n * N, 'average degree should exceed 21');

// -----------------------------------------------------------------------------
// Weight-48 / weight-64 trade-off and incidence thresholds.
// -----------------------------------------------------------------------------
assert(PLP(48).eq(21), 'P(48)=21 trade-off coefficient mismatch');

// If A48 >= 22, 22 weight-48 supports force an intersection > 12.
const M22 = 22n;
const inc48_22 = M22 * 48n;
assert(inc48_22 === 1056n, '22-word weight48 incidence mismatch');
const lower48_22 = 127n * (6n*5n/2n) + 42n * (7n*6n/2n);
assert(lower48_22 === 2787n, 'weight48 convexity bound mismatch');
assert(lower48_22 > 12n * (M22*(M22-1n)/2n), '22 weight48 words should force intersection >12');

// If A48 <= 17, the trade-off forces A64 >= 176, whose average pair
// intersection is strictly larger than 24.
const N64_17 = 533n - 21n * 17n;
assert(N64_17 === 176n, 'A64 lower bound at A48=17 mismatch');
const lower64_176 = 59n * (66n*65n/2n) + 110n * (67n*66n/2n);
assert(lower64_176 === 369765n, '176-word convexity bound mismatch');
assert(lower64_176 > 24n * (N64_17*(N64_17-1n)/2n), '176 weight64 words should force intersection >24');

// Isolated weight48: A48=1 forces A64 >= 512 and at least 1300 pairs
// of weight64 words with intersection >= 28.
const N64_iso = 533n - 21n;
assert(N64_iso === 512n, 'isolated weight48 A64 lower bound mismatch');
const lower64_512 = 18n * (193n*192n/2n) + 151n * (194n*193n/2n);
assert(lower64_512 === 3160375n, '512-word convexity bound mismatch');
const pairs512 = N64_iso * (N64_iso-1n) / 2n;
const excess512 = lower64_512 - 24n * pairs512;
assert(excess512 === 20791n, 'isolated weight48 excess mismatch');
const highPairs512 = (excess512 + 15n) / 16n;
assert(highPairs512 === 1300n, 'isolated weight48 high-pair lower bound mismatch');
assert((2n * highPairs512 + N64_iso - 1n) / N64_iso === 6n, 'isolated weight48 neighbor lower bound mismatch');

console.log('Core certificate audit OK: weight72, residual bounds, A64 LP, 48/64 trade-off, and incidence thresholds.');

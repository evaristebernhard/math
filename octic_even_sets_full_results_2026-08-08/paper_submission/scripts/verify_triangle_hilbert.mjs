function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function comb(n, k) {
  if (k < 0 || k > n) return 0;
  k = Math.min(k, n - k);
  let out = 1;
  for (let i = 1; i <= k; i++) out = out * (n - k + i) / i;
  return Math.round(out);
}

function macaulayNext(h, d) {
  if (h === 0) return 0;
  let rem = h;
  let prev = Number.MAX_SAFE_INTEGER;
  const reps = [];
  for (let k = d; k >= 1; k--) {
    let found = null;
    const maxCand = Math.min(prev - 1, rem + k + 10);
    for (let a = maxCand; a >= k; a--) {
      if (comb(a, k) <= rem) {
        found = a;
        break;
      }
    }
    if (found !== null) {
      reps.push([found, k]);
      rem -= comb(found, k);
      prev = found;
    } else {
      prev = k;
    }
  }
  return reps.reduce((s, [a, k]) => s + comb(a + 1, k + 1), 0);
}

function isOSequence(h) {
  if (h[0] !== 1) return false;
  if (h[1] > 3) return false;
  for (let d = 1; d < h.length - 1; d++) {
    if (h[d + 1] > macaulayNext(h[d], d)) return false;
  }
  let zeroSeen = false;
  for (const x of h) {
    if (zeroSeen && x !== 0) return false;
    if (x === 0) zeroSeen = true;
  }
  return true;
}

const h444 = [1,3,6,10,12,12,10,6,3,1];
const candidates = [];
for (let h1 = 0; h1 <= h444[1]; h1++) {
  for (let h2 = 0; h2 <= h444[2]; h2++) {
    for (let h3 = 0; h3 <= h444[3]; h3++) {
      for (let h4 = 0; h4 <= h444[4]; h4++) {
        const h = [
          1, h1, h2, h3, h4,
          h444[4] - h4,
          h444[3] - h3,
          h444[2] - h2,
          h444[1] - h1,
          0,
        ];
        if (Math.min(...h) < 0) continue;
        if (!isOSequence(h)) continue;
        const H4 = h.slice(0,5).reduce((a,b) => a+b, 0);
        const d = 32 - H4;
        candidates.push({h,d});
      }
    }
  }
}

// Basic half-CI + O-sequence enumeration gives 33 candidates.
assert(candidates.length === 33, `expected 33 basic candidates, got ${candidates.length}`);

// d=0 would force k>=3 from k+d>=3, hence U=V, impossible.
// d=1 forces k=2, excluded by CP. Hence 31 numerical candidates remain.
const afterCP = candidates.filter(x => x.d >= 2);
assert(afterCP.length === 31, `expected 31 candidates after d=0/1 removal, got ${afterCP.length}`);

const d2 = afterCP.filter(x => x.d === 2).map(x => x.h);
const A = [1,3,6,9,11,1,1,0,0,0];
const B = [1,3,6,10,10,2,0,0,0,0];
assert(d2.length === 2, `expected two d=2 candidates, got ${d2.length}`);
assert(JSON.stringify(d2) === JSON.stringify([A,B]), `unexpected d=2 candidates: ${JSON.stringify(d2)}`);

// Count by minimal equation degree.
function hilbertAt(h, t) {
  return h.slice(0,t+1).reduce((a,b) => a+b, 0);
}
function minEquationDegree(h) {
  for (let t = 0; t < h.length; t++) {
    if (comb(t+3,3) - hilbertAt(h,t) > 0) return t;
  }
  return null;
}
const counts = {2:0,3:0,4:0};
for (const {h} of afterCP) {
  const e = minEquationDegree(h);
  if (counts[e] !== undefined) counts[e]++;
}
assert(counts[2] === 8 && counts[3] === 18 && counts[4] === 5,
  `unexpected 2/3/4 split: ${JSON.stringify(counts)}`);

// HV: candidate A cannot lie in CI(3,4,4).
const h344 = [1,3,6,9,10,9,6,3,1];
const hvMiddle = h344[4] - A[4];
assert(hvMiddle === -1, `HV middle entry should be -1, got ${hvMiddle}`);

// CD: residual D of A in CI(3,4,5).
const h345 = [1,3,6,9,11,11,9,6,3,1];
const hD = h345.map((x,i) => x - A[9-i]);
const expectedD = [1,3,6,8,10,0,0,0,0,0];
assert(JSON.stringify(hD) === JSON.stringify(expectedD), `unexpected h_D: ${JSON.stringify(hD)}`);
const HD3 = hD.slice(0,4).reduce((a,b)=>a+b,0);
const HD4 = hD.slice(0,5).reduce((a,b)=>a+b,0);
const ID3 = comb(6,3) - HD3; // dim S_3 = C(6,3)=20
const ID4 = comb(7,3) - HD4; // dim S_4 = C(7,3)=35
assert(ID3 === 2, `dim I_D(3) should be 2, got ${ID3}`);
assert(ID4 === 7, `dim I_D(4) should be 7, got ${ID4}`);

console.log('Triangle Hilbert audit OK: 33 basic candidates, 31 after CP, d=2 = A/B, split 8 quadratic + 18 cubic + 5 primitive, HV=-1, CD dimensions (2,7).');

import fs from 'node:fs';

const file = 'main.tex';
const text = fs.readFileSync(file, 'utf8');
const errors = [];

const labels = [...text.matchAll(/\\label\{([^}]+)\}/g)].map(m => m[1]);
const counts = new Map();
for (const x of labels) counts.set(x, (counts.get(x) ?? 0) + 1);
for (const [x, n] of counts) if (n > 1) errors.push(`duplicate label: ${x} (${n})`);

const refs = [...text.matchAll(/\\(?:eqref|ref)\{([^}]+)\}/g)].map(m => m[1]);
for (const x of new Set(refs)) if (!counts.has(x)) errors.push(`undefined reference: ${x}`);

const bibitems = new Set([...text.matchAll(/\\bibitem\{([^}]+)\}/g)].map(m => m[1]));
const cites = [...text.matchAll(/\\cite\{([^}]+)\}/g)]
  .flatMap(m => m[1].split(',').map(x => x.trim()).filter(Boolean));
for (const x of new Set(cites)) if (!bibitems.has(x)) errors.push(`undefined citation: ${x}`);

const envToken = /\\(begin|end)\{([^}]+)\}/g;
const stack = [];
for (const m of text.matchAll(envToken)) {
  const kind = m[1];
  const env = m[2];
  if (kind === 'begin') stack.push(env);
  else {
    const top = stack.pop();
    if (top !== env) {
      errors.push(`environment mismatch: expected end{${top ?? 'NONE'}} but saw end{${env}}`);
      break;
    }
  }
}
if (stack.length) errors.push(`unclosed environments: ${stack.join(', ')}`);

const bracesStripped = text
  .replace(/%.*$/gm, '')
  .replace(/\\[{}]/g, '')
  .replace(/\\(?:begin|end|label|ref|eqref|cite|tag)\{[^}]*\}/g, '');
let balance = 0;
for (const ch of bracesStripped) {
  if (ch === '{') balance++;
  if (ch === '}') balance--;
  if (balance < 0) { errors.push('brace balance became negative'); break; }
}
if (balance !== 0) errors.push(`brace balance is ${balance}`);

const tags = [...text.matchAll(/\\tag\{([^}]+)\}/g)].map(m => m[1]);
const tagCounts = new Map();
for (const x of tags) tagCounts.set(x, (tagCounts.get(x) ?? 0) + 1);
for (const [x, n] of tagCounts) if (n > 1) errors.push(`duplicate equation tag: ${x} (${n})`);

if (errors.length) {
  console.error('TeX static audit FAILED');
  for (const e of errors) console.error(`- ${e}`);
  process.exit(1);
}

console.log(`TeX static audit OK: ${labels.length} labels, ${refs.length} references, ${tags.length} explicit tags.`);

const $ = (id) => document.getElementById(id);

const STATUSES = [
  ['PASS', 'Independently verified. Requires a real proof checker.'],
  ['FAIL', 'A checked witness shows the property is violated.'],
  ['BOUNDARY', 'Within tolerance of the limit; cannot be decided either way.'],
  ['SKIPPED', 'Check not applicable to this input.'],
  ['VERIFICATION_DISAGREEMENT', 'Independent methods disagree; needs review.'],
  ['ERROR', 'Evidence is inconsistent or the checker misbehaved.'],
  ['INCOMPLETE', 'No sufficient independent verification. The safe default.'],
];

let wasmModule = null;

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}

function renderVocab(list) {
  const ul = $('vocab');
  if (!ul) return;
  ul.replaceChildren();
  for (const [name, desc] of list) {
    const li = el('li', 's-' + name);
    li.append(el('b', '', name), el('span', '', desc));
    ul.append(li);
  }
}
renderVocab(STATUSES);

function setVerdict(state, text) {
  if ($('verdict-state')) $('verdict-state').textContent = state;
  if ($('verdict-text')) $('verdict-text').textContent = text;
}

function renderChecks(items) {
  const ul = $('checks');
  if (!ul) return;
  ul.replaceChildren();
  for (const [level, title, detail] of items) {
    const li = el('li', level);
    li.append(el('span', 'm', level === 'pass' ? '✓' : level === 'warn' ? '!' : '✕'));
    const d = el('div');
    d.append(el('span', '', title));
    if (detail) d.append(el('small', '', detail));
    li.append(d);
    ul.append(li);
  }
  ul.hidden = items.length === 0;
}

function inspect(raw) {
  raw = raw.trim();
  const details = $('inspection-details');
  const rawBox = $('raw');
  if (!raw) {
    $('inspect-message').textContent = 'Paste a JSON payload first.';
    renderChecks([]);
    if (rawBox) rawBox.hidden = true;
    setVerdict('INCOMPLETE', 'No certificate payload was supplied.');
    return;
  }

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (e) {
    $('inspect-message').textContent = 'Invalid JSON';
    renderChecks([['bad', 'Payload is valid JSON', e.message]]);
    if (rawBox) rawBox.hidden = true;
    setVerdict('FAIL', 'The payload could not be parsed.');
    return;
  }

  const checks = [];

  if (wasmModule && parsed.witness && parsed.witness.dimension && parsed.witness.entries) {
    const resStr = wasmModule.verify_density_matrix_json(JSON.stringify(parsed.witness));
    const res = JSON.parse(resStr);
    if (res.error) {
      checks.push(['bad', 'Exact-Rational Math Core (apeiron-math)', res.error]);
      setVerdict('FAIL', 'Exact-rational mathematical check rejected the matrix.');
      $('inspect-message').textContent = 'Mathematical check failed';
    } else if (Array.isArray(res)) {
      for (const item of res) {
        checks.push([item.passed ? 'pass' : 'bad', `${item.predicate}`, `Evidence: ${item.evidence}`]);
      }
      checks.push(['warn', 'Fail-Closed Policy', 'Candidate math evidence computed by apeiron-math; independent replay verifier pending (status stays INCOMPLETE).']);
      setVerdict('INCOMPLETE', 'Exact-rational candidate checks passed; awaiting independent replay verifier.');
      $('inspect-message').textContent = 'Exact-rational math verified · Stayed fail-closed';
    }
  } else {
    checks.push(['warn', 'WASM Exact-Rational Core', wasmModule ? 'Include witness {dimension, entries} to run BigRational LDL* audit.' : 'WASM bridge loading or unavailable.']);
    setVerdict('INCOMPLETE', 'No independent proof verification has been performed.');
    $('inspect-message').textContent = 'Structural check done · Proof not verified';
  }

  renderChecks(checks);
  if (details) details.textContent = JSON.stringify(parsed, null, 2);
  if (rawBox) rawBox.hidden = false;
}

function exampleCertificate() {
  return {
    schema_version: '69.0.0',
    calculation_id: 'exact-rational-qubit-0',
    input_hash: 'sha256:' + '0'.repeat(64),
    engine_version: '69.0.0-exact-rational',
    algorithm_id: 'unpivoted-ldl-star',
    claim: 'PSD',
    proof_type: 'CHOLESKY_PIVOTS',
    status: 'INCOMPLETE',
    witness: {
      dimension: 2,
      entries: [
        { re: '1', im: '0' }, { re: '0', im: '0' },
        { re: '0', im: '0' }, { re: '0', im: '0' }
      ]
    }
  };
}

if ($('inspect-button')) $('inspect-button').addEventListener('click', () => inspect($('certificate-input').value));
if ($('example-button')) $('example-button').addEventListener('click', () => {
  $('certificate-input').value = JSON.stringify(exampleCertificate(), null, 2);
  inspect($('certificate-input').value);
});
if ($('clear-button')) $('clear-button').addEventListener('click', () => {
  $('certificate-input').value = '';
  $('inspect-message').textContent = 'Waiting for input';
  renderChecks([]);
  if ($('raw')) $('raw').hidden = true;
  setVerdict('INCOMPLETE', 'No independent proof verification has been performed.');
});

async function start() {
  try {
    const wasm = await import('./wasm/apeiron_wasm.js');
    await wasm.default();
    wasmModule = wasm;
    $('engine-version').textContent = wasm.engine_version();
    $('runtime-state').textContent = 'WASM READY';
    $('runtime-detail').textContent = 'Exact-rational apeiron-math bridge loaded (BigRational LDL*).';
    $('runtime-dot').classList.add('live');
    $('vocab-sync').textContent = 'SYNCED WITH WASM';
  } catch (e) {
    $('runtime-state').textContent = 'WASM UNAVAILABLE';
    $('runtime-detail').textContent = 'WebAssembly bridge error: ' + e.message;
  }
}
start();

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const VECTOR_PATH = path.join(ROOT, 'test-vectors', 'vectors-v1', 'T13_cross_impl_determinism.json');

const LABELS = {
  state: 'STATEv1',
  goal: 'GOALv1',
  constraints: 'CONSv1',
  policy: 'POLv1',
  config: 'CFGv1',
  step: 'STEPv1',
  plan: 'PLANv1',
  pc: 'PCv1',
  air: 'AIRv1'
};

function normalize(value) {
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === 'object') {
    return Object.keys(value)
      .sort()
      .reduce((acc, key) => {
        acc[key] = normalize(value[key]);
        return acc;
      }, {});
  }
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new Error('NaN/Inf forbidden');
    if (Object.is(value, -0) || value === 0) return 0;
  }
  return value;
}

function canonicalBytes(payload) {
  return Buffer.from(JSON.stringify(normalize(payload)));
}

function dsHash(label, payload) {
  return crypto.createHash('sha256').update(`${label}:`).update(canonicalBytes(payload)).digest('hex');
}

function stepDigest(step) {
  const bundle = {
    initial_state_digest: dsHash(LABELS.state, step.S0),
    goal_digest: dsHash(LABELS.goal, step.G),
    constraints_digest: dsHash(LABELS.constraints, step.C),
    policy_digest: dsHash(LABELS.policy, step.P ?? {}),
    planner_config_digest: dsHash(LABELS.config, step.CFG ?? {}),
    action_ir_digest: dsHash(LABELS.air, step.AIR)
  };
  return dsHash(LABELS.step, bundle);
}

function planDigest(steps) {
  const digests = steps.map(stepDigest);
  return dsHash(LABELS.plan, { step_digests: digests });
}

function pcDigest(pc) {
  const cloned = { ...pc };
  delete cloned.signatures;
  delete cloned.pc_digest;
  return dsHash(LABELS.pc, cloned);
}

const vector = JSON.parse(fs.readFileSync(VECTOR_PATH, 'utf8'));
const expectedPlan = vector.expected_plan_digest;
const expectedPc = vector.expected_pc_digest;
const actualPlan = planDigest(vector.inputs.steps);
const actualPc = pcDigest(vector.pc);

if (actualPlan !== expectedPlan || actualPc !== expectedPc) {
  console.error(JSON.stringify({ ok: false, actualPlan, expectedPlan, actualPc, expectedPc }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ ok: true, actualPlan, actualPc }, null, 2));

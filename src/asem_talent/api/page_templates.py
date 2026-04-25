from __future__ import annotations


NAV_ITEMS = (
    ("/", "Home"),
    ("/candidate-lab", "Candidate Lab"),
    ("/market-studio", "Market Studio"),
    ("/pathway-planner", "Pathway Planner"),
  ("/erp-bridge", "ERP Bridge"),
)


BASE_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #f6f1e8;
      --surface: rgba(255, 252, 247, 0.84);
      --surface-strong: #fffdfa;
      --ink: #23201c;
      --muted: #6b655e;
      --accent: #7a664b;
      --accent-2: #98613d;
      --accent-3: #d7c4ab;
      --border: rgba(35, 32, 28, 0.1);
      --shadow: 0 18px 46px rgba(35, 32, 28, 0.06);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(215, 196, 171, 0.34), transparent 34%),
        radial-gradient(circle at left center, rgba(122, 102, 75, 0.1), transparent 26%),
        linear-gradient(180deg, #fbf8f3 0%, var(--bg) 100%);
    }

    a {
      color: inherit;
    }

    .shell {
      width: min(1240px, calc(100% - 32px));
      margin: 24px auto 40px;
    }

    .app-nav {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 18px;
      padding: 12px;
      border-radius: 18px;
      border: 1px solid var(--border);
      background: rgba(255, 253, 249, 0.78);
      box-shadow: var(--shadow);
      position: sticky;
      top: 12px;
      z-index: 10;
      backdrop-filter: blur(12px);
    }

    .nav-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 42px;
      padding: 10px 14px;
      border-radius: 999px;
      text-decoration: none;
      color: var(--muted);
      background: rgba(35, 32, 28, 0.04);
      transition: transform 120ms ease, background 120ms ease, color 120ms ease;
    }

    .nav-link:hover {
      transform: translateY(-1px);
      background: rgba(122, 102, 75, 0.1);
      color: var(--ink);
    }

    .nav-link-active {
      color: #fff;
      background: #2d2a26;
    }

    .hero {
      display: grid;
      gap: 20px;
      padding: 34px;
      border: 1px solid var(--border);
      border-radius: 28px;
      background: linear-gradient(180deg, rgba(255, 253, 249, 0.96), rgba(248, 243, 236, 0.92));
      box-shadow: var(--shadow);
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      width: fit-content;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(122, 102, 75, 0.08);
      color: var(--accent);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    h1 {
      margin: 0;
      font-size: clamp(2.4rem, 5vw, 4.2rem);
      line-height: 0.98;
      max-width: 12ch;
      letter-spacing: -0.03em;
    }

    .hero-copy {
      margin: 0;
      max-width: 58ch;
      color: var(--muted);
      font-size: 1.05rem;
      line-height: 1.72;
    }

    .summary-grid,
    .content-grid,
    .details-grid,
    .stack,
    .board,
    .button-row,
    .sprint-grid {
      display: grid;
      gap: 16px;
    }

    .summary-grid {
      margin-top: 20px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .content-grid {
      margin-top: 20px;
      grid-template-columns: 1.1fr 0.9fr;
      align-items: start;
    }

    .details-grid {
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .sprint-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .card,
    .panel {
      border: 1px solid var(--border);
      border-radius: 24px;
      background: var(--surface);
      backdrop-filter: blur(12px);
      box-shadow: var(--shadow);
    }

    .card {
      padding: 18px;
    }

    .label,
    .panel-label {
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .value {
      margin-top: 8px;
      font-size: 1.25rem;
      font-weight: 700;
    }

    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
      padding: 20px 22px 0;
    }

    .panel-title {
      margin: 0;
      font-size: 1.35rem;
    }

    .panel-subtitle {
      margin: 6px 0 0;
      color: var(--muted);
      line-height: 1.55;
      font-size: 0.95rem;
    }

    .panel-body {
      padding: 20px 22px 22px;
    }

    .note-box {
      padding: 16px;
      border-radius: 18px;
      background: rgba(35, 32, 28, 0.04);
      border: 1px solid rgba(35, 32, 28, 0.08);
      color: var(--muted);
      line-height: 1.6;
      white-space: pre-wrap;
    }

    .chip-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      padding: 8px 11px;
      border-radius: 999px;
      background: rgba(122, 102, 75, 0.08);
      color: var(--accent);
      font-size: 0.84rem;
      border: 1px solid rgba(122, 102, 75, 0.12);
    }

    .list {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.6;
    }

    .bar-list {
      display: grid;
      gap: 12px;
    }

    .bar-row {
      display: grid;
      gap: 8px;
    }

    .bar-label,
    .wage-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 0.92rem;
    }

    .bar-track {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: rgba(20, 33, 61, 0.09);
      overflow: hidden;
    }

    .bar-fill,
    .metric-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), var(--accent-3));
    }

    .metric-band {
      width: 100%;
      height: 10px;
      margin-top: 12px;
      border-radius: 999px;
      background: rgba(20, 33, 61, 0.09);
      overflow: hidden;
    }

    .text-input,
    textarea,
    select {
      width: 100%;
      border: 1px solid rgba(35, 32, 28, 0.12);
      border-radius: 16px;
      padding: 12px 14px;
      background: var(--surface-strong);
      color: var(--ink);
      font: inherit;
    }

    textarea {
      min-height: 140px;
      resize: vertical;
    }

    .field {
      display: grid;
      gap: 8px;
      min-width: 180px;
    }

    button {
      appearance: none;
      border: 1px solid transparent;
      border-radius: 999px;
      padding: 12px 18px;
      font: inherit;
      cursor: pointer;
      transition: transform 120ms ease, opacity 120ms ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    button:disabled {
      opacity: 0.6;
      cursor: wait;
      transform: none;
    }

    .primary {
      background: #2d2a26;
      color: #fff;
    }

    .ghost {
      background: rgba(35, 32, 28, 0.04);
      border-color: rgba(35, 32, 28, 0.06);
      color: var(--ink);
    }

    .secondary-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      padding: 12px 18px;
      border-radius: 999px;
      text-decoration: none;
      background: rgba(122, 102, 75, 0.1);
      color: var(--ink);
      border: 1px solid rgba(122, 102, 75, 0.12);
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 12px;
      border-radius: 999px;
      background: rgba(122, 102, 75, 0.1);
      color: var(--accent);
      font-size: 0.9rem;
    }

    .role-card {
      display: grid;
      gap: 10px;
      padding: 16px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.62);
      border: 1px solid rgba(35, 32, 28, 0.08);
    }

    .role-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .role-stat {
      display: inline-flex;
      align-items: center;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(35, 32, 28, 0.05);
      color: var(--muted);
      font-size: 0.84rem;
    }

    .mono {
      font-family: "Cascadia Code", Consolas, monospace;
    }

    .empty-state {
      padding: 18px;
      border-radius: 18px;
      background: rgba(35, 32, 28, 0.04);
      border: 1px dashed rgba(35, 32, 28, 0.12);
      color: var(--muted);
      line-height: 1.6;
    }

    @media (max-width: 980px) {
      .content-grid,
      .sprint-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 720px) {
      .shell {
        width: min(100% - 20px, 1240px);
      }

      .panel-head {
        flex-direction: column;
      }

      .button-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    __NAV__
    <section class="hero">
      <div class="eyebrow">__EYEBROW__</div>
      <h1>__HEADING__</h1>
      <p class="hero-copy">__LEDE__</p>
    </section>
    __BODY__
  </main>
  <script>
    __COMMON_SCRIPT__
    __PAGE_SCRIPT__
  </script>
</body>
</html>
"""


COMMON_SCRIPT = """
const PAYLOAD_STORAGE_KEY = 'asem-talint-shared-payload';
const samplePayload = {
  candidate: {
    candidate_id: 'cand_0001',
    age_band: '22-24',
    education_level: 'bachelor_final_year',
    degree_field: 'mechatronics',
    district: 'Sepang',
    state: 'Selangor',
    latitude: 2.9264,
    longitude: 101.6964,
    skill_tags: ['c++', 'debugging', 'data_acquisition', 'embedded_systems'],
    portfolio_tags: ['robot_arm', 'debugging', 'sensor_integration'],
    coding_test_score: 74.0,
    math_foundation_score: 69.0,
    communication_score: 78.0,
    willing_to_relocate: true,
    prior_training: ['basic_iot_bootcamp'],
    notes: 'Interested in validation and robotics workflows with structured mentoring.',
    resume_context: {
      summary: 'Built a wafer-inspection prototype and completed an automation internship focused on sensor debugging.',
      skill_tags: ['python_basics', 'test_automation'],
      tool_tags: ['oscilloscope', 'labview'],
      project_highlights: [
        {
          title: 'Vision-guided wafer inspection prototype',
          skill_tags: ['python_basics', 'sensor_integration', 'debugging'],
          outcome_tags: ['defect_detection']
        }
      ],
      internship_highlights: [
        {
          organization: 'Penang E&E SME',
          role_title: 'Automation Intern',
          skill_tags: ['test_automation', 'data_acquisition', 'debugging']
        }
      ],
      certifications: ['ipc_basics'],
      inferred_role_signals: ['validation engineer trainee']
    }
  },
  target_track: {
    track_id: 'track_validation',
    track_name: 'Chip Validation and Robotics Basics',
    district: 'Sepang',
    state: 'Selangor',
    required_skills: ['debugging', 'data_acquisition', 'python_basics'],
    target_roles: ['validation engineer trainee', 'robotics trainee'],
    minimum_coding_score: 60.0,
    minimum_math_score: 60.0,
    employer_demand_signal: 0.82,
    wage_growth_signal: 0.73
  }
};

function cloneSamplePayload() {
  return JSON.parse(JSON.stringify(samplePayload));
}

function readSharedPayload() {
  try {
    const raw = localStorage.getItem(PAYLOAD_STORAGE_KEY);
    if (raw) {
      return JSON.parse(raw);
    }
  } catch (error) {
    console.warn('Could not read shared payload', error);
  }
  return cloneSamplePayload();
}

function storeSharedPayload(payload) {
  try {
    localStorage.setItem(PAYLOAD_STORAGE_KEY, JSON.stringify(payload));
  } catch (error) {
    console.warn('Could not store shared payload', error);
  }
}

function resumeContext(candidate) {
  return candidate && candidate.resume_context ? candidate.resume_context : {};
}

function uniqueStrings(values) {
  const seen = new Set();
  const deduped = [];
  (values || []).forEach((value) => {
    const normalized = String(value || '').trim();
    if (!normalized) {
      return;
    }
    const key = normalized.toLowerCase();
    if (seen.has(key)) {
      return;
    }
    seen.add(key);
    deduped.push(normalized);
  });
  return deduped;
}

function effectiveSkillTags(candidate) {
  const context = resumeContext(candidate);
  const projectSkills = (context.project_highlights || []).flatMap((project) => project.skill_tags || []);
  const internshipSkills = (context.internship_highlights || []).flatMap((item) => item.skill_tags || []);
  return uniqueStrings([
    ...(candidate.skill_tags || []),
    ...(context.skill_tags || []),
    ...(context.tool_tags || []),
    ...projectSkills,
    ...internshipSkills
  ]);
}

function effectivePortfolioTags(candidate) {
  const context = resumeContext(candidate);
  const projects = (context.project_highlights || []).flatMap((project) => [
    project.title,
    ...(project.skill_tags || []),
    ...(project.outcome_tags || [])
  ]);
  const internships = (context.internship_highlights || []).flatMap((item) => [
    item.role_title,
    ...(item.skill_tags || [])
  ]);
  return uniqueStrings([
    ...(candidate.portfolio_tags || []),
    ...(context.certifications || []),
    ...(context.inferred_role_signals || []),
    ...projects,
    ...internships
  ]);
}

function computeSkillCoverage(payload) {
  const track = payload.target_track || {};
  const candidate = payload.candidate || {};
  const required = (track.required_skills || []).map((skill) => skill.toLowerCase());
  if (required.length === 0) {
    return 0;
  }
  const observed = new Set(effectiveSkillTags(candidate).map((skill) => skill.toLowerCase()));
  const matched = required.filter((skill) => observed.has(skill));
  return matched.length / required.length;
}

function missingRequiredSkills(payload) {
  const track = payload.target_track || {};
  const observed = new Set(effectiveSkillTags(payload.candidate || {}).map((skill) => skill.toLowerCase()));
  return (track.required_skills || []).filter((skill) => !observed.has(String(skill).toLowerCase()));
}

function evidenceDepth(candidate) {
  const context = resumeContext(candidate);
  return (
    (context.inferred_role_signals || []).length
    + (context.certifications || []).length
    + (context.project_highlights || []).length
    + (context.internship_highlights || []).length
  );
}

function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return 'UNSPECIFIED';
  }
  return new Intl.NumberFormat('en-MY', { maximumFractionDigits: 1 }).format(value);
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return 'UNSPECIFIED';
  }
  return `MYR ${formatNumber(value)}`;
}

async function fetchJson(path, options) {
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.detail || 'Request failed');
  }
  return body;
}

function renderChips(container, values, fallbackText) {
  container.innerHTML = '';
  const normalized = uniqueStrings(values);
  if (normalized.length === 0) {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = fallbackText;
    container.appendChild(chip);
    return;
  }

  normalized.forEach((value) => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = value;
    container.appendChild(chip);
  });
}

function renderList(container, values, fallbackText) {
  container.innerHTML = '';
  const items = values && values.length ? values : [fallbackText || 'None'];
  items.forEach((value) => {
    const item = document.createElement('li');
    item.textContent = value;
    container.appendChild(item);
  });
}
"""


CANDIDATE_LAB_BODY = """
<section class="summary-grid">
  <article class="card">
    <div class="label">Candidate</div>
    <div class="value" id="candidate-headline">--</div>
  </article>
  <article class="card">
    <div class="label">Target track</div>
    <div class="value" id="track-headline">--</div>
  </article>
  <article class="card">
    <div class="label">Skill coverage</div>
    <div class="value" id="coverage-card">--</div>
    <div class="metric-band"><div class="metric-fill" id="coverage-fill" style="width:0%"></div></div>
  </article>
  <article class="card">
    <div class="label">Score floor</div>
    <div class="value" id="score-floor-card">--</div>
  </article>
  <article class="card">
    <div class="label">Evidence depth</div>
    <div class="value" id="evidence-depth-card">--</div>
  </article>
</section>

<section class="content-grid">
  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Current case</div>
        <h2 class="panel-title">Evidence view</h2>
        <p class="panel-subtitle">Read the shared case as proof: signals, projects, tools, and what the target track still needs.</p>
      </div>
      <div class="button-row">
        <button class="ghost" id="sync-lab">Reload case</button>
        <button class="ghost" id="reset-lab">Reset sample</button>
        <a class="secondary-link" href="/dashboard">Open home</a>
      </div>
    </div>
    <div class="panel-body stack">
      <div class="note-box" id="candidate-summary">Case summary will appear here.</div>
      <div class="details-grid">
        <section class="card">
          <div class="label">Role signals</div>
          <div class="chip-list" id="role-signal-chips"></div>
        </section>
        <section class="card">
          <div class="label">Certifications</div>
          <div class="chip-list" id="certification-chips"></div>
        </section>
        <section class="card">
          <div class="label">Project evidence</div>
          <div class="chip-list" id="project-chips"></div>
        </section>
        <section class="card">
          <div class="label">Toolchain evidence</div>
          <div class="chip-list" id="tool-chips"></div>
        </section>
      </div>
    </div>
  </article>

  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Next actions</div>
        <h2 class="panel-title">Repair queue</h2>
        <p class="panel-subtitle">Translate weak evidence into a short, coachable set of actions before OJT review.</p>
      </div>
      <div class="status-pill" id="lab-status">Case loaded</div>
    </div>
    <div class="panel-body stack">
      <section class="card">
        <div class="label">Case checks</div>
        <ol class="list" id="payload-health"></ol>
      </section>
      <section class="card">
        <div class="label">Repair queue</div>
        <ol class="list" id="repair-queue"></ol>
      </section>
      <section class="card">
        <div class="label">Coach notes</div>
        <textarea id="notes-editor"></textarea>
        <div class="button-row">
          <button class="primary" id="save-notes">Save notes</button>
        </div>
      </section>
    </div>
  </article>
</section>
"""


CANDIDATE_LAB_SCRIPT = """
const candidateHeadline = document.getElementById('candidate-headline');
const trackHeadline = document.getElementById('track-headline');
const coverageCard = document.getElementById('coverage-card');
const coverageFill = document.getElementById('coverage-fill');
const scoreFloorCard = document.getElementById('score-floor-card');
const evidenceDepthCard = document.getElementById('evidence-depth-card');
const candidateSummary = document.getElementById('candidate-summary');
const roleSignalChips = document.getElementById('role-signal-chips');
const certificationChips = document.getElementById('certification-chips');
const projectChips = document.getElementById('project-chips');
const toolChips = document.getElementById('tool-chips');
const payloadHealth = document.getElementById('payload-health');
const repairQueue = document.getElementById('repair-queue');
const notesEditor = document.getElementById('notes-editor');
const labStatus = document.getElementById('lab-status');

function buildPayloadHealth(payload) {
  const candidate = payload.candidate || {};
  const track = payload.target_track || {};
  const issues = [];
  if (candidate.latitude === null || candidate.latitude === undefined || candidate.longitude === null || candidate.longitude === undefined) {
    issues.push('Add coordinates so hotspot access remains location-specific instead of approximate.');
  }
  if ((candidate.communication_score || 0) < 70) {
    issues.push('Communication score is thin for employer-facing roles; rehearse concise handoff and debugging explanations.');
  }
  if (!(resumeContext(candidate).project_highlights || []).length) {
    issues.push('Project evidence is missing; add at least one outcome-driven lab or prototype entry.');
  }
  if (!(track.target_roles || []).length) {
    issues.push('Target roles are unspecified; add role targets so downstream pages can steer outreach and wage scenarios.');
  }
  if (!(candidate.notes || '').trim()) {
    issues.push('Candidate notes are empty; store a concise intent statement to preserve counselor context across pages.');
  }
  return issues.length ? issues : ['The case is in good shape for a fuller review.'];
}

function buildRepairQueue(payload) {
  const candidate = payload.candidate || {};
  const track = payload.target_track || {};
  const resume = resumeContext(candidate);
  const repairs = [];
  missingRequiredSkills(payload).slice(0, 3).forEach((skill) => {
    repairs.push(`Build one proof artifact that demonstrates ${skill} in a semiconductor-relevant workflow.`);
  });
  if ((candidate.coding_test_score || 0) < (track.minimum_coding_score || 0)) {
    repairs.push(`Raise coding readiness from ${formatNumber(candidate.coding_test_score)} to at least ${formatNumber(track.minimum_coding_score)} before intake review.`);
  }
  if ((candidate.math_foundation_score || 0) < (track.minimum_math_score || 0)) {
    repairs.push(`Tighten math fundamentals from ${formatNumber(candidate.math_foundation_score)} to the cohort floor of ${formatNumber(track.minimum_math_score)}.`);
  }
  if (!(resume.inferred_role_signals || []).length) {
    repairs.push('Add one explicit target-role line to the resume summary so employer-demand ranking can personalize beyond generic skills.');
  }
  if (!(resume.certifications || []).length) {
    repairs.push('Record one certification or lab credential so market ranking and mobility confidence are backed by formal evidence.');
  }
  if (!(resume.project_highlights || []).length) {
    repairs.push('Add one project highlight with a measurable outcome tag such as yield, defect detection, or automation time saved.');
  }
  return repairs.length ? repairs : ['No urgent gaps detected; convert the strongest project into employer-ready talking points.'];
}

function renderCandidateLab() {
  const payload = readSharedPayload();
  const candidate = payload.candidate || {};
  const track = payload.target_track || {};
  const resume = resumeContext(candidate);
  const coverage = computeSkillCoverage(payload);
  const scoreFloorPass = (candidate.coding_test_score || 0) >= (track.minimum_coding_score || 0) && (candidate.math_foundation_score || 0) >= (track.minimum_math_score || 0);

  candidateHeadline.textContent = `${candidate.candidate_id || 'UNSPECIFIED'} | ${candidate.degree_field || 'UNSPECIFIED'}`;
  trackHeadline.textContent = track.track_name || 'UNSPECIFIED';
  coverageCard.textContent = `${formatNumber(coverage * 100)}%`;
  coverageFill.style.width = `${Math.max(6, coverage * 100)}%`;
  scoreFloorCard.textContent = scoreFloorPass ? 'On track' : 'Needs reinforcement';
  evidenceDepthCard.textContent = String(evidenceDepth(candidate));
  candidateSummary.textContent = `${candidate.notes || 'No counselor note is stored yet.'}\n\nResume summary: ${resume.summary || 'No structured resume summary is available.'}`;
  notesEditor.value = candidate.notes || '';
  renderChips(roleSignalChips, resume.inferred_role_signals || [], 'No role signals');
  renderChips(certificationChips, resume.certifications || [], 'No certifications');
  renderChips(projectChips, (resume.project_highlights || []).map((project) => project.title), 'No projects');
  renderChips(toolChips, resume.tool_tags || [], 'No tool tags');
  renderList(payloadHealth, buildPayloadHealth(payload), 'Payload health checks will appear here.');
  renderList(repairQueue, buildRepairQueue(payload), 'Repair queue will appear here.');
  labStatus.textContent = `Case ready for ${candidate.candidate_id || 'candidate'}`;
}

document.getElementById('sync-lab').addEventListener('click', () => {
  labStatus.textContent = 'Case reloaded';
  renderCandidateLab();
});

document.getElementById('reset-lab').addEventListener('click', () => {
  storeSharedPayload(cloneSamplePayload());
  labStatus.textContent = 'Case reset to the sample';
  renderCandidateLab();
});

document.getElementById('save-notes').addEventListener('click', () => {
  const payload = readSharedPayload();
  payload.candidate = payload.candidate || {};
  payload.candidate.notes = notesEditor.value.trim();
  storeSharedPayload(payload);
  labStatus.textContent = 'Notes saved to the case';
  renderCandidateLab();
});

renderCandidateLab();
"""


MARKET_STUDIO_BODY = """
<section class="summary-grid">
  <article class="card">
    <div class="label">Roles</div>
    <div class="value" id="roles-loaded-card">--</div>
  </article>
  <article class="card">
    <div class="label">Top signal</div>
    <div class="value" id="top-market-card">--</div>
  </article>
  <article class="card">
    <div class="label">Evidence gain</div>
    <div class="value" id="resume-lift-card">--</div>
  </article>
  <article class="card">
    <div class="label">Wage baseline</div>
    <div class="value" id="wage-baseline-card">--</div>
  </article>
</section>

<section class="panel" style="margin-top:20px;">
  <div class="panel-head">
    <div>
      <div class="panel-label">Ranking controls</div>
      <h2 class="panel-title">Role scouting</h2>
      <p class="panel-subtitle">Switch between track mode and adjacency scouting to see where evidence most changes the market view.</p>
    </div>
    <div class="status-pill" id="market-studio-status">Ready to refresh</div>
  </div>
  <div class="panel-body">
    <div class="button-row" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
      <label class="field">
        <span class="label">Role scope</span>
        <select id="market-scope" class="text-input">
          <option value="all">All roles</option>
          <option value="track">Target track only</option>
        </select>
      </label>
      <label class="field">
        <span class="label">Geography</span>
        <select id="market-state-scope" class="text-input">
          <option value="all">All states</option>
          <option value="candidate">Candidate state only</option>
        </select>
      </label>
      <div class="field">
        <span class="label">Action</span>
        <button class="primary" id="refresh-market-studio">Refresh roles</button>
      </div>
    </div>
  </div>
</section>

<section class="content-grid">
  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Opportunity board</div>
        <h2 class="panel-title">Ranked roles</h2>
        <p class="panel-subtitle">Each card keeps demand, evidence, and salary context together so the shortlist reads clearly.</p>
      </div>
    </div>
    <div class="panel-body board" id="opportunity-board"></div>
  </article>

  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Evidence view</div>
        <h2 class="panel-title">Contribution by role</h2>
        <p class="panel-subtitle">Use this to show how much of the final ranking comes from resume-derived proof rather than demand alone.</p>
      </div>
    </div>
    <div class="panel-body stack">
      <div class="bar-list" id="lift-board"></div>
      <div class="note-box" id="market-memo">Refresh roles to draft a short targeting note.</div>
    </div>
  </article>
</section>
"""


MARKET_STUDIO_SCRIPT = """
const rolesLoadedCard = document.getElementById('roles-loaded-card');
const topMarketCard = document.getElementById('top-market-card');
const resumeLiftCard = document.getElementById('resume-lift-card');
const wageBaselineCard = document.getElementById('wage-baseline-card');
const marketStudioStatus = document.getElementById('market-studio-status');
const opportunityBoard = document.getElementById('opportunity-board');
const liftBoard = document.getElementById('lift-board');
const marketMemo = document.getElementById('market-memo');
const marketScope = document.getElementById('market-scope');
const marketStateScope = document.getElementById('market-state-scope');
const refreshMarketStudioButton = document.getElementById('refresh-market-studio');

function renderOpportunityBoard(roles) {
  opportunityBoard.innerHTML = '';
  if (!roles.length) {
    opportunityBoard.innerHTML = '<div class="empty-state">No ranked roles are available with the current filters.</div>';
    return;
  }

  roles.forEach((role) => {
    const card = document.createElement('section');
    card.className = 'role-card';
    card.innerHTML = `
      <div>
        <div class="label">${role.state} | ${role.track_id}</div>
        <div class="value">${role.role_title}</div>
        <div style="color:#5b6472; line-height:1.55;">${role.employer_name}</div>
      </div>
      <div class="role-meta">
        <span class="role-stat">Market ${formatNumber(role.market_signal_score)}</span>
        <span class="role-stat">Demand ${formatNumber(role.demand_score)}</span>
        <span class="role-stat">Resume ${formatNumber(role.resume_alignment_score)}</span>
        <span class="role-stat">Salary ${formatCurrency(((role.salary_band_min || 0) + (role.salary_band_max || 0)) / 2 || role.salary_band_min || role.salary_band_max)}</span>
      </div>
      <div class="note-box">${role.resume_evidence_summary || 'Resume evidence summary unavailable.'}</div>
    `;
    opportunityBoard.appendChild(card);
  });
}

function renderLiftBoard(roles) {
  liftBoard.innerHTML = '';
  if (!roles.length) {
    liftBoard.innerHTML = '<div class="empty-state">No ranked roles to visualize yet.</div>';
    return;
  }

  roles.forEach((role) => {
    const contribution = (role.resume_alignment_score || 0) * 0.4;
    const wrapper = document.createElement('div');
    wrapper.className = 'bar-row';
    wrapper.innerHTML = `
      <div class="bar-label">
        <span>${role.role_title}</span>
        <span>${formatNumber(contribution)}</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:${Math.max(8, contribution * 250)}%"></div></div>
    `;
    liftBoard.appendChild(wrapper);
  });
}

function buildMarketMemo(payload, roles, wageSignal) {
  if (!roles.length) {
    return 'No ranked roles were returned, so the studio cannot draft a targeting memo.';
  }

  const topRole = roles[0];
  const topContributionRole = [...roles].sort((left, right) => ((right.resume_alignment_score || 0) - (left.resume_alignment_score || 0)))[0];
  const scopeNote = marketScope.value === 'track'
    ? `Track mode is locked to ${payload.target_track.track_name}.`
    : 'Adjacency mode is scouting beyond the current track for nearby opportunities.';
  const wageNote = wageSignal
    ? `Candidate-state wage baseline is ${formatCurrency(wageSignal.value)} from ${wageSignal.source}.`
    : 'No wage baseline is currently available for the selected geography.';
  return `Anchor outreach on ${topRole.role_title} at ${topRole.employer_name}. ${topRole.resume_evidence_summary} The strongest evidence contribution belongs to ${topContributionRole.role_title} at ${formatNumber((topContributionRole.resume_alignment_score || 0) * 0.4)} points. ${scopeNote} ${wageNote}`;
}

async function refreshMarketStudio() {
  const payload = readSharedPayload();
  const request = {
    candidate: payload.candidate,
    limit: marketScope.value === 'track' ? 6 : 8
  };
  if (marketScope.value === 'track') {
    request.track_id = payload.target_track.track_id;
  }
  if (marketStateScope.value === 'candidate') {
    request.state = payload.candidate.state;
  }

  refreshMarketStudioButton.disabled = true;
  marketStudioStatus.textContent = 'Refreshing roles';
  try {
    const [ranking, wages] = await Promise.all([
      fetchJson('/v1/signals/employer-demand/ranked', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      }),
      fetchJson(`/v1/signals/wages?state=${encodeURIComponent(payload.candidate.state)}`)
    ]);

    const roles = ranking.roles || [];
    const topRole = roles[0];
    const topLift = roles.length
      ? Math.max(...roles.map((role) => (role.resume_alignment_score || 0) * 0.4))
      : null;
    const wageSignal = (wages || [])[0] || null;

    rolesLoadedCard.textContent = String(roles.length);
    topMarketCard.textContent = topRole ? formatNumber(topRole.market_signal_score) : 'UNSPECIFIED';
    resumeLiftCard.textContent = topLift !== null ? `${formatNumber(topLift)} pts` : 'UNSPECIFIED';
    wageBaselineCard.textContent = wageSignal ? formatCurrency(wageSignal.value) : 'UNSPECIFIED';
    renderOpportunityBoard(roles);
    renderLiftBoard(roles);
    marketMemo.textContent = buildMarketMemo(payload, roles, wageSignal);
    marketStudioStatus.textContent = 'Roles refreshed';
  } catch (error) {
    rolesLoadedCard.textContent = '0';
    topMarketCard.textContent = 'UNSPECIFIED';
    resumeLiftCard.textContent = 'UNSPECIFIED';
    wageBaselineCard.textContent = 'UNSPECIFIED';
    opportunityBoard.innerHTML = `<div class="empty-state">${String(error)}</div>`;
    liftBoard.innerHTML = '<div class="empty-state">Resume-lift bars could not be generated.</div>';
    marketMemo.textContent = 'Refresh failed before a targeting memo could be drafted.';
    marketStudioStatus.textContent = 'Refresh failed';
  } finally {
    refreshMarketStudioButton.disabled = false;
  }
}

refreshMarketStudioButton.addEventListener('click', refreshMarketStudio);
refreshMarketStudio();
"""


PATHWAY_PLANNER_BODY = """
<section class="summary-grid">
  <article class="card">
    <div class="label">Active role</div>
    <div class="value" id="selected-role-card">--</div>
  </article>
  <article class="card">
    <div class="label">Wage change</div>
    <div class="value" id="uplift-card">--</div>
  </article>
  <article class="card">
    <div class="label">Evidence strength</div>
    <div class="value" id="evidence-strength-card">--</div>
  </article>
  <article class="card">
    <div class="label">Blockers</div>
    <div class="value" id="blocker-card">--</div>
  </article>
</section>

<section class="panel" style="margin-top:20px;">
  <div class="panel-head">
    <div>
      <div class="panel-label">Scenario inputs</div>
      <h2 class="panel-title">Wage scenario</h2>
      <p class="panel-subtitle">Pick a shortlisted role, adjust the current wage if needed, and rebuild the plan without leaving this page.</p>
    </div>
    <div class="status-pill" id="planner-status">Ready to build</div>
  </div>
  <div class="panel-body">
    <div class="button-row" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
      <label class="field">
        <span class="label">Current wage</span>
        <input id="current-wage-input" class="text-input" type="number" min="0" step="50" placeholder="Optional MYR amount">
      </label>
      <label class="field">
        <span class="label">Current sector</span>
        <select id="current-sector-select" class="text-input">
          <option value="manufacturing">Manufacturing</option>
          <option value="formal_sector">Formal sector</option>
        </select>
      </label>
      <div class="field">
        <span class="label">Action</span>
        <button class="primary" id="refresh-pathway">Rebuild plan</button>
      </div>
    </div>
  </div>
</section>

<section class="content-grid">
  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Shortlist</div>
        <h2 class="panel-title">Role shortlist</h2>
        <p class="panel-subtitle">The shortlist stays tied to the shared case, so changes elsewhere flow straight into the next plan.</p>
      </div>
    </div>
    <div class="panel-body board" id="role-shortlist"></div>
  </article>

  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Mobility estimate</div>
        <h2 class="panel-title">Wage view</h2>
        <p class="panel-subtitle">See the selected role's wage path and the confidence rationale behind it.</p>
      </div>
    </div>
    <div class="panel-body stack">
      <div class="wage-row"><span>Current estimate</span><span id="planner-current-wage">--</span></div>
      <div class="bar-track"><div class="bar-fill" id="planner-current-bar" style="width:0%"></div></div>
      <div class="wage-row"><span>Target estimate</span><span id="planner-target-wage">--</span></div>
      <div class="bar-track"><div class="bar-fill" id="planner-target-bar" style="width:0%"></div></div>
      <div class="note-box" id="planner-summary">Build the plan to load the wage view.</div>
    </div>
  </article>
</section>

<section class="panel" style="margin-top:20px;">
  <div class="panel-head">
    <div>
      <div class="panel-label">Action plan</div>
      <h2 class="panel-title">30-60-90 plan</h2>
      <p class="panel-subtitle">Turn blockers, role evidence, and wage assumptions into a short plan a counselor or candidate can follow.</p>
    </div>
  </div>
  <div class="panel-body sprint-grid">
    <section class="card">
      <div class="label">30 days</div>
      <ol class="list" id="sprint-30"></ol>
    </section>
    <section class="card">
      <div class="label">60 days</div>
      <ol class="list" id="sprint-60"></ol>
    </section>
    <section class="card">
      <div class="label">90 days</div>
      <ol class="list" id="sprint-90"></ol>
    </section>
  </div>
</section>

<section class="content-grid">
  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Brief</div>
        <h2 class="panel-title">Pathway note</h2>
      </div>
    </div>
    <div class="panel-body">
      <div class="note-box" id="planner-memo">A short pathway note will appear here.</div>
    </div>
  </article>

  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Risks</div>
        <h2 class="panel-title">Watchouts</h2>
      </div>
    </div>
    <div class="panel-body">
      <ol class="list" id="planner-risks"></ol>
    </div>
  </article>
</section>
"""


PATHWAY_PLANNER_SCRIPT = """
const selectedRoleCard = document.getElementById('selected-role-card');
const upliftCard = document.getElementById('uplift-card');
const evidenceStrengthCard = document.getElementById('evidence-strength-card');
const blockerCard = document.getElementById('blocker-card');
const plannerStatus = document.getElementById('planner-status');
const currentWageInput = document.getElementById('current-wage-input');
const currentSectorSelect = document.getElementById('current-sector-select');
const refreshPathwayButton = document.getElementById('refresh-pathway');
const roleShortlist = document.getElementById('role-shortlist');
const plannerCurrentWage = document.getElementById('planner-current-wage');
const plannerTargetWage = document.getElementById('planner-target-wage');
const plannerCurrentBar = document.getElementById('planner-current-bar');
const plannerTargetBar = document.getElementById('planner-target-bar');
const plannerSummary = document.getElementById('planner-summary');
const sprint30 = document.getElementById('sprint-30');
const sprint60 = document.getElementById('sprint-60');
const sprint90 = document.getElementById('sprint-90');
const plannerMemo = document.getElementById('planner-memo');
const plannerRisks = document.getElementById('planner-risks');
let shortlistedMatches = [];
let selectedRoleId = null;

function renderRoleShortlist(matches) {
  roleShortlist.innerHTML = '';
  if (!matches.length) {
    roleShortlist.innerHTML = '<div class="empty-state">No OJT roles are available for the current case.</div>';
    return;
  }

  matches.forEach((match) => {
    const card = document.createElement('section');
    card.className = 'role-card';
    const isSelected = match.role_id === selectedRoleId;
    card.innerHTML = `
      <div>
        <div class="label">${match.track_id}</div>
        <div class="value">${match.role_title}</div>
        <div style="color:#5b6472; line-height:1.55;">${match.employer_name}</div>
      </div>
      <div class="role-meta">
        <span class="role-stat">Fit ${formatNumber(match.match_score)}</span>
        <span class="role-stat">Demand ${formatNumber(match.demand_score)}</span>
        <span class="role-stat">${match.commute_note}</span>
      </div>
      <div class="button-row" style="grid-template-columns: 1fr;">
        <button class="${isSelected ? 'primary' : 'ghost'}" data-role-id="${match.role_id}">${isSelected ? 'Selected scenario' : 'Use this role'}</button>
      </div>
    `;
    roleShortlist.appendChild(card);
  });

  roleShortlist.querySelectorAll('button[data-role-id]').forEach((button) => {
    button.addEventListener('click', async () => {
      selectedRoleId = button.getAttribute('data-role-id');
      renderRoleShortlist(shortlistedMatches);
      await refreshMobilityScenario();
    });
  });
}

function buildSprintPlan(payload, match, mobility) {
  const targetRole = match.role_title;
  const firstGap = (match.blockers || [])[0] || (missingRequiredSkills(payload)[0]) || 'role evidence';
  return {
    days30: [
      `Produce one proof-of-work artifact that closes the ${firstGap} gap for ${targetRole}.`,
      `Rewrite the top three resume bullets so they mirror ${targetRole.toLowerCase()} language and evidence.`,
      'Validate current wage assumptions with one counselor or employer checkpoint before using them in planning.'
    ],
    days60: [
      `Practice a role-specific technical walkthrough for ${targetRole}.`,
      `Add one fresh certification, lab badge, or project update that increases mobility confidence beyond medium.`,
      `Target the employer shortlist while the resume-evidence alignment is still current.`
    ],
    days90: [
      `Submit OJT applications with one primary role and one adjacency role from the shortlist.`,
      `Use the ${formatCurrency(mobility.target_estimated_wage)} scenario as the target-side salary anchor, not a guaranteed offer.`,
      `Refresh the pathway page after each new project or certification so the sprint stays evidence-backed.`
    ]
  };
}

function buildPlannerRisks(payload, match, mobility) {
  const risks = [];
  if ((match.blockers || []).length) {
    risks.push(`Current blockers: ${(match.blockers || []).join(', ')}.`);
  }
  if ((payload.candidate.communication_score || 0) < 75) {
    risks.push('Communication readiness may drag interview conversion unless the candidate rehearses debugging narratives.');
  }
  if (mobility.evidence_strength === 'low') {
    risks.push('Mobility confidence is low; add stronger role evidence or a direct current wage before using this scenario externally.');
  }
  if (!(resumeContext(payload.candidate).certifications || []).length) {
    risks.push('Certification evidence is thin, which weakens wage-confidence signaling for employer-facing reviews.');
  }
  return risks.length ? risks : ['No major pathway cautions beyond normal shortlist competition.'];
}

function renderWageBars(mobility) {
  const current = mobility.current_estimated_wage || 0;
  const target = mobility.target_estimated_wage || 0;
  const maxValue = Math.max(current, target, 1);
  plannerCurrentWage.textContent = formatCurrency(mobility.current_estimated_wage);
  plannerTargetWage.textContent = formatCurrency(mobility.target_estimated_wage);
  plannerCurrentBar.style.width = `${Math.max(6, (current / maxValue) * 100)}%`;
  plannerTargetBar.style.width = `${Math.max(6, (target / maxValue) * 100)}%`;
}

async function refreshMobilityScenario() {
  const payload = readSharedPayload();
  const match = shortlistedMatches.find((item) => item.role_id === selectedRoleId);
  if (!match) {
    plannerSummary.textContent = 'Select a role to generate a mobility scenario.';
    return;
  }

  const request = {
    candidate: payload.candidate,
    target_role_id: selectedRoleId,
    current_sector: currentSectorSelect.value
  };
  const parsedWage = Number.parseFloat(currentWageInput.value);
  if (!Number.isNaN(parsedWage)) {
    request.current_wage = parsedWage;
  }

  plannerStatus.textContent = 'Rebuilding mobility scenario';
  const mobility = await fetchJson('/v1/analysis/wage-mobility', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  });
  const sprintPlan = buildSprintPlan(payload, match, mobility);

  selectedRoleCard.textContent = match.role_title;
  upliftCard.textContent = formatCurrency(mobility.estimated_uplift_abs);
  evidenceStrengthCard.textContent = mobility.evidence_strength;
  blockerCard.textContent = String((match.blockers || []).length);
  renderWageBars(mobility);
  plannerSummary.textContent = `${mobility.target_role_title}\nCurrent estimate: ${formatCurrency(mobility.current_estimated_wage)}\nTarget estimate: ${formatCurrency(mobility.target_estimated_wage)}\nResume alignment: ${formatNumber(mobility.resume_alignment_score)}\n${mobility.confidence_rationale}`;
  plannerMemo.textContent = `${match.role_title} at ${match.employer_name} is the active pathway scenario. ${match.justification} ${match.commute_note} ${mobility.caution_note}`;
  renderList(sprint30, sprintPlan.days30, '30-day actions will appear here.');
  renderList(sprint60, sprintPlan.days60, '60-day actions will appear here.');
  renderList(sprint90, sprintPlan.days90, '90-day actions will appear here.');
  renderList(plannerRisks, buildPlannerRisks(payload, match, mobility), 'Pathway cautions will appear here.');
  plannerStatus.textContent = 'Pathway rebuilt';
}

async function refreshPathwayPlanner() {
  const payload = readSharedPayload();
  refreshPathwayButton.disabled = true;
  plannerStatus.textContent = 'Building role shortlist';
  try {
    const response = await fetchJson('/v1/matching/ojt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        candidate: payload.candidate,
        target_track_id: payload.target_track.track_id,
        limit: 4
      })
    });
    shortlistedMatches = response.matches || [];
    if (!shortlistedMatches.length) {
      selectedRoleId = null;
    } else if (!selectedRoleId || !shortlistedMatches.some((item) => item.role_id === selectedRoleId)) {
      selectedRoleId = shortlistedMatches[0].role_id;
    }
    renderRoleShortlist(shortlistedMatches);
    await refreshMobilityScenario();
  } catch (error) {
    roleShortlist.innerHTML = `<div class="empty-state">${String(error)}</div>`;
    plannerSummary.textContent = 'The plan could not be rebuilt.';
    renderList(sprint30, [], '30-day actions unavailable.');
    renderList(sprint60, [], '60-day actions unavailable.');
    renderList(sprint90, [], '90-day actions unavailable.');
    renderList(plannerRisks, [String(error)], 'Pathway cautions unavailable.');
    plannerStatus.textContent = 'Build failed';
  } finally {
    refreshPathwayButton.disabled = false;
  }
}

refreshPathwayButton.addEventListener('click', refreshPathwayPlanner);
currentSectorSelect.addEventListener('change', refreshPathwayPlanner);
currentWageInput.addEventListener('change', refreshPathwayPlanner);
refreshPathwayPlanner();
"""


ERP_BRIDGE_BODY = """
<section class="summary-grid">
  <article class="card">
    <div class="label">Schema version</div>
    <div class="value" id="erp-schema-card">--</div>
  </article>
  <article class="card">
    <div class="label">ERP system</div>
    <div class="value" id="erp-system-card">--</div>
  </article>
  <article class="card">
    <div class="label">Case status</div>
    <div class="value" id="erp-status-card">--</div>
  </article>
  <article class="card">
    <div class="label">Selected role</div>
    <div class="value" id="erp-role-card">--</div>
  </article>
</section>

<section class="panel" style="margin-top:20px;">
  <div class="panel-head">
    <div>
      <div class="panel-label">Integration controls</div>
      <h2 class="panel-title">Package builder</h2>
      <p class="panel-subtitle">Build a clean sync bundle from the shared case so an ERP can upsert core entities without scraping the UI.</p>
    </div>
    <div class="status-pill" id="erp-bridge-status">Waiting for package build</div>
  </div>
  <div class="panel-body">
    <div class="button-row" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
      <label class="field">
        <span class="label">ERP system</span>
        <input id="erp-system-input" class="text-input" value="ERPNext">
      </label>
      <label class="field">
        <span class="label">External candidate ID</span>
        <input id="erp-candidate-input" class="text-input" placeholder="Optional ERP candidate key">
      </label>
      <label class="field">
        <span class="label">External case ID</span>
        <input id="erp-case-input" class="text-input" placeholder="Optional ERP case key">
      </label>
      <label class="field">
        <span class="label">Current wage</span>
        <input id="erp-current-wage" class="text-input" type="number" min="0" step="50" placeholder="Optional MYR amount">
      </label>
      <label class="field">
        <span class="label">Current sector</span>
        <select id="erp-current-sector" class="text-input">
          <option value="manufacturing">Manufacturing</option>
          <option value="formal_sector">Formal sector</option>
        </select>
      </label>
      <div class="field">
        <span class="label">Actions</span>
        <div class="button-row">
          <button class="primary" id="erp-build-package">Build package</button>
          <button class="ghost" id="erp-copy-package">Copy package JSON</button>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="content-grid">
  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Handoff summary</div>
        <h2 class="panel-title">Package overview</h2>
        <p class="panel-subtitle">Use this summary to explain what the ERP will receive after synchronization.</p>
      </div>
    </div>
    <div class="panel-body stack">
      <div class="note-box" id="erp-summary">Build the package to see the handoff summary.</div>
      <section class="card">
        <div class="label">Upsert keys</div>
        <ol class="list" id="erp-upsert-keys"></ol>
      </section>
      <section class="card">
        <div class="label">Sync actions</div>
        <ol class="list" id="erp-actions"></ol>
      </section>
    </div>
  </article>

  <article class="panel">
    <div class="panel-head">
      <div>
        <div class="panel-label">Raw contract</div>
        <h2 class="panel-title">Machine-readable package</h2>
        <p class="panel-subtitle">This is the exact JSON bundle an ERP integration layer can ingest or forward to an upsert job.</p>
      </div>
    </div>
    <div class="panel-body">
      <div class="note-box mono" id="erp-raw-json">Build the package to load the raw JSON handoff.</div>
    </div>
  </article>
</section>
"""


ERP_BRIDGE_SCRIPT = """
const erpSchemaCard = document.getElementById('erp-schema-card');
const erpSystemCard = document.getElementById('erp-system-card');
const erpStatusCard = document.getElementById('erp-status-card');
const erpRoleCard = document.getElementById('erp-role-card');
const erpBridgeStatus = document.getElementById('erp-bridge-status');
const erpSystemInput = document.getElementById('erp-system-input');
const erpCandidateInput = document.getElementById('erp-candidate-input');
const erpCaseInput = document.getElementById('erp-case-input');
const erpCurrentWageInput = document.getElementById('erp-current-wage');
const erpCurrentSector = document.getElementById('erp-current-sector');
const erpSummary = document.getElementById('erp-summary');
const erpUpsertKeys = document.getElementById('erp-upsert-keys');
const erpActions = document.getElementById('erp-actions');
const erpRawJson = document.getElementById('erp-raw-json');
const erpBuildPackageButton = document.getElementById('erp-build-package');
const erpCopyPackageButton = document.getElementById('erp-copy-package');
let latestErpPackage = null;

function buildErpRequest() {
  const payload = readSharedPayload();
  const request = {
    candidate: payload.candidate,
    target_track: payload.target_track,
    erp_system: erpSystemInput.value.trim() || 'UNSPECIFIED',
    current_sector: erpCurrentSector.value,
    ranked_role_limit: 3
  };
  if (erpCandidateInput.value.trim()) {
    request.external_candidate_id = erpCandidateInput.value.trim();
  }
  if (erpCaseInput.value.trim()) {
    request.external_case_id = erpCaseInput.value.trim();
  }
  const parsedWage = Number.parseFloat(erpCurrentWageInput.value);
  if (!Number.isNaN(parsedWage)) {
    request.current_wage = parsedWage;
  }
  return request;
}

function renderErpPackage(pkg) {
  latestErpPackage = pkg;
  erpSchemaCard.textContent = pkg.schema_version;
  erpSystemCard.textContent = pkg.erp_system;
  erpStatusCard.textContent = pkg.status_map.case_status;
  erpRoleCard.textContent = pkg.wage_mobility ? pkg.wage_mobility.target_role_title : 'UNSPECIFIED';
  erpSummary.textContent = `${pkg.decision_summary.summary_note}\n\nCandidate: ${pkg.candidate_master.internal_candidate_id}\nTrack: ${pkg.training_case.target_track_name}\nMarket priority: ${pkg.status_map.market_priority}\nMobility band: ${pkg.status_map.mobility_band}`;
  renderList(erpUpsertKeys, (pkg.upsert_keys || []).map((item) => `${item.entity}: ${item.external_key}`), 'No upsert keys were produced.');
  renderList(erpActions, pkg.sync_actions || [], 'No sync actions were produced.');
  erpRawJson.textContent = JSON.stringify(pkg, null, 2);
}

async function buildErpPackage() {
  erpBuildPackageButton.disabled = true;
  erpCopyPackageButton.disabled = true;
  erpBridgeStatus.textContent = 'Building ERP package';
  try {
    const pkg = await fetchJson('/v1/erp/sync-package', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildErpRequest())
    });
    renderErpPackage(pkg);
    erpBridgeStatus.textContent = 'ERP package ready';
  } catch (error) {
    latestErpPackage = null;
    erpSchemaCard.textContent = 'UNSPECIFIED';
    erpSystemCard.textContent = 'UNSPECIFIED';
    erpStatusCard.textContent = 'UNSPECIFIED';
    erpRoleCard.textContent = 'UNSPECIFIED';
    erpSummary.textContent = 'ERP package generation failed.';
    renderList(erpUpsertKeys, [String(error)], 'ERP package generation failed.');
    renderList(erpActions, [], 'No sync actions were produced.');
    erpRawJson.textContent = String(error);
    erpBridgeStatus.textContent = 'ERP package failed';
  } finally {
    erpBuildPackageButton.disabled = false;
    erpCopyPackageButton.disabled = false;
  }
}

erpBuildPackageButton.addEventListener('click', buildErpPackage);
erpCopyPackageButton.addEventListener('click', async () => {
  if (!latestErpPackage) {
    erpBridgeStatus.textContent = 'Build a package before copying';
    return;
  }
  try {
    await navigator.clipboard.writeText(JSON.stringify(latestErpPackage, null, 2));
    erpBridgeStatus.textContent = 'ERP package copied to clipboard';
  } catch (error) {
    erpBridgeStatus.textContent = 'Clipboard copy failed';
  }
});

buildErpPackage();
"""


def _nav(active_path: str) -> str:
    links: list[str] = []
    for path, label in NAV_ITEMS:
        classes = "nav-link nav-link-active" if path == active_path else "nav-link"
        links.append(f'<a class="{classes}" href="{path}">{label}</a>')
    return '<nav class="app-nav" aria-label="App navigation">' + "".join(links) + "</nav>"


def _render_page(
    *,
    title: str,
    active_path: str,
    eyebrow: str,
    heading: str,
    lede: str,
    body: str,
    page_script: str,
) -> str:
    html = BASE_PAGE_HTML
    replacements = {
        "__TITLE__": title,
        "__NAV__": _nav(active_path),
        "__EYEBROW__": eyebrow,
        "__HEADING__": heading,
        "__LEDE__": lede,
        "__BODY__": body,
        "__COMMON_SCRIPT__": COMMON_SCRIPT,
        "__PAGE_SCRIPT__": page_script,
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html


def candidate_lab_html() -> str:
    return _render_page(
        title="ASEM Talint Candidate Lab",
        active_path="/candidate-lab",
    eyebrow="Candidate Lab | evidence review",
    heading="Tighten the case before review",
    lede="See what is already proven, what feels thin, and what a counselor should fix next.",
        body=CANDIDATE_LAB_BODY,
        page_script=CANDIDATE_LAB_SCRIPT,
    )


def market_studio_html() -> str:
    return _render_page(
        title="ASEM Talint Market Studio",
        active_path="/market-studio",
    eyebrow="Market Studio | role scouting",
    heading="Read demand through the candidate",
    lede="Compare roles by demand, evidence, and wage context so the shortlist feels reasoned, not noisy.",
        body=MARKET_STUDIO_BODY,
        page_script=MARKET_STUDIO_SCRIPT,
    )


def pathway_planner_html() -> str:
    return _render_page(
        title="ASEM Talint Pathway Planner",
        active_path="/pathway-planner",
    eyebrow="Pathway Planner | next-step planning",
    heading="Turn the shortlist into a plan",
    lede="Tie role fit to wage direction, blockers, and a practical 30-60-90 plan.",
        body=PATHWAY_PLANNER_BODY,
        page_script=PATHWAY_PLANNER_SCRIPT,
    )


def erp_bridge_html() -> str:
    return _render_page(
        title="ASEM Talint ERP Bridge",
        active_path="/erp-bridge",
    eyebrow="ERP Bridge | operational handoff",
    heading="Send a clean package downstream",
    lede="Build a stable handoff with keys, status, shortlist data, and wage context.",
        body=ERP_BRIDGE_BODY,
        page_script=ERP_BRIDGE_SCRIPT,
    )
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from asem_talent.api.branding import BRAND_CSS, render_hero_brand, render_nav_brand
from asem_talent.api.page_templates import candidate_lab_html, erp_bridge_html, market_studio_html, pathway_planner_html

router = APIRouter(include_in_schema=False)


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ASEM Talint Dashboard</title>
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

__BRAND_CSS__

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

    .shell {
      width: min(1200px, calc(100% - 32px));
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
      background: rgba(35, 32, 28, 0.04);
      color: var(--muted);
      text-decoration: none;
      transition: transform 120ms ease, background 120ms ease, color 120ms ease;
    }

    .nav-link:hover {
      transform: translateY(-1px);
      background: rgba(122, 102, 75, 0.1);
      color: var(--ink);
    }

    .nav-link-active {
      background: #2d2a26;
      color: #fff;
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
      font-size: clamp(2.4rem, 5vw, 4.6rem);
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

    .strategy-note {
      display: grid;
      gap: 14px;
      padding: 18px 20px;
      border-radius: 22px;
      border: 1px solid rgba(122, 102, 75, 0.14);
      background: rgba(255, 255, 255, 0.52);
    }

    .strategy-note-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .strategy-note-title {
      margin: 4px 0 0;
      font-size: 1.35rem;
    }

    .strategy-note-copy {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
    }

    .strategy-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .strategy-tag {
      display: inline-flex;
      align-items: center;
      padding: 8px 11px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.74);
      color: var(--ink);
      font-size: 0.82rem;
      border: 1px solid rgba(35, 32, 28, 0.08);
    }

    .strategy-link {
      color: var(--accent-2);
      font-size: 0.9rem;
      text-decoration: none;
    }

    .strategy-link:hover {
      text-decoration: underline;
    }

    .page-grid {
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .page-card-link {
      text-decoration: none;
      color: inherit;
    }

    .page-card {
      display: grid;
      gap: 10px;
      height: 100%;
      padding: 18px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.66);
      border: 1px solid rgba(35, 32, 28, 0.08);
      transition: transform 120ms ease, border-color 120ms ease;
    }

    .page-card-link:hover .page-card {
      transform: translateY(-2px);
      border-color: rgba(122, 102, 75, 0.24);
    }

    .page-card-title {
      font-size: 1.1rem;
      font-weight: 700;
    }

    .page-card-copy {
      color: var(--muted);
      line-height: 1.55;
      font-size: 0.95rem;
    }

    .badge-row,
    .metric-grid,
    .workspace {
      display: grid;
      gap: 16px;
    }

    .badge-row {
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .badge,
    .metric,
    .panel {
      border: 1px solid var(--border);
      border-radius: 24px;
      background: var(--surface);
      backdrop-filter: blur(16px);
      box-shadow: var(--shadow);
    }

    .badge,
    .metric {
      padding: 18px;
    }

    .badge-label,
    .metric-label,
    .panel-label {
      font-size: 0.8rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .badge-value,
    .metric-value {
      margin-top: 8px;
      font-size: 1.3rem;
      font-weight: 700;
    }

    .metric-grid {
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      margin-top: 20px;
    }

    .workspace {
      margin-top: 22px;
      grid-template-columns: 1.05fr 0.95fr;
      align-items: start;
    }

    .market-grid {
      display: grid;
      gap: 16px;
      margin-top: 16px;
      grid-template-columns: minmax(0, 1.15fr) minmax(0, 1.15fr) minmax(280px, 0.9fr);
    }

    .market-span-2 {
      grid-column: span 2;
    }

    .panel {
      overflow: hidden;
    }

    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 20px 22px 0;
    }

    .panel-label {
      margin-bottom: 6px;
    }

    .panel-title {
      margin: 0;
      font-size: 1.4rem;
    }

    .panel-subtitle {
      margin: 6px 0 0;
      color: var(--muted);
      line-height: 1.5;
      font-size: 0.96rem;
    }

    .panel-body {
      padding: 20px 22px 22px;
    }

    textarea {
      width: 100%;
      min-height: 220px;
      border: 1px solid rgba(35, 32, 28, 0.12);
      border-radius: 18px;
      padding: 16px;
      resize: vertical;
      background: var(--surface-strong);
      color: var(--ink);
      font-family: "Cascadia Code", Consolas, monospace;
      font-size: 0.92rem;
      line-height: 1.55;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 16px;
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

    .secondary {
      background: rgba(122, 102, 75, 0.1);
      border-color: rgba(122, 102, 75, 0.12);
      color: var(--ink);
    }

    .ghost {
      background: rgba(35, 32, 28, 0.04);
      border-color: rgba(35, 32, 28, 0.06);
      color: var(--ink);
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

    .stack {
      display: grid;
      gap: 14px;
    }

    .output-card {
      padding: 18px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.62);
      border: 1px solid rgba(35, 32, 28, 0.08);
    }

    .resume-head {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
    }

    .resume-toolbar {
      display: grid;
      gap: 12px;
      grid-template-columns: minmax(0, 1fr) auto auto;
      margin-top: 14px;
      align-items: center;
    }

    .file-input {
      width: 100%;
      border: 1px solid rgba(35, 32, 28, 0.12);
      border-radius: 16px;
      padding: 12px 14px;
      background: var(--surface-strong);
      color: var(--ink);
      font: inherit;
    }

    .chip-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      padding: 8px 11px;
      border-radius: 999px;
      background: rgba(122, 102, 75, 0.08);
      color: var(--accent);
      font-size: 0.84rem;
    }

    .preview-block {
      margin: 14px 0 0;
      min-height: 130px;
      padding: 14px;
      border-radius: 16px;
      background: rgba(35, 32, 28, 0.04);
      border: 1px solid rgba(35, 32, 28, 0.08);
      color: var(--muted);
    }

    .mini-grid {
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }

    .mini-card {
      padding: 14px;
      border-radius: 16px;
      background: rgba(35, 32, 28, 0.04);
      border: 1px solid rgba(35, 32, 28, 0.08);
    }

    .mini-label {
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }

    .mini-value {
      margin-top: 6px;
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--ink);
    }

    .output-title {
      margin: 0 0 10px;
      font-size: 1rem;
    }

    .output-meta {
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 0.88rem;
      line-height: 1.5;
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

    .bar-label {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.92rem;
      color: var(--muted);
    }

    .bar-track {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: rgba(20, 33, 61, 0.09);
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), var(--accent-3));
    }

    .data-table {
      width: 100%;
      min-width: 560px;
      border-collapse: collapse;
      font-size: 0.92rem;
    }

    .table-shell {
      overflow-x: auto;
    }

    .data-table th,
    .data-table td {
      padding: 10px 8px;
      text-align: left;
      border-bottom: 1px solid rgba(20, 33, 61, 0.08);
      vertical-align: top;
    }

    .data-table th {
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }

    .table-note {
      color: var(--muted);
      font-size: 0.85rem;
      line-height: 1.5;
    }

    .map-shell {
      display: grid;
      gap: 14px;
    }

    .map-card {
      padding: 14px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(15, 118, 110, 0.08), rgba(20, 33, 61, 0.03));
      border: 1px solid rgba(20, 33, 61, 0.08);
    }

    #hotspot-map {
      width: 100%;
      height: 280px;
      display: block;
      overflow: visible;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      color: var(--muted);
      font-size: 0.84rem;
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .legend-swatch {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      display: inline-block;
    }

    .wage-bars {
      display: grid;
      gap: 14px;
      margin-top: 12px;
    }

    .wage-bar-label {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 0.92rem;
    }

    .wage-note {
      margin-top: 12px;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.55;
    }

    pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: "Cascadia Code", Consolas, monospace;
      font-size: 0.88rem;
      line-height: 1.6;
      color: var(--muted);
    }

    .footnote {
      margin-top: 16px;
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(122, 102, 75, 0.08);
      color: var(--muted);
      line-height: 1.55;
      font-size: 0.92rem;
    }

    .panel-button {
      white-space: nowrap;
    }

    @media (max-width: 920px) {
      .brand-lockup-nav {
        width: 100%;
        justify-content: center;
        margin-right: 0;
        padding: 4px 0 8px;
      }

      .workspace {
        grid-template-columns: 1fr;
      }

      .market-grid {
        grid-template-columns: 1fr;
      }

      .market-span-2 {
        grid-column: span 1;
      }

      .resume-toolbar {
        grid-template-columns: 1fr;
      }

      .shell {
        width: min(100% - 20px, 1200px);
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <nav class="app-nav" aria-label="App navigation">
      __NAV_BRAND__
      <a class="nav-link nav-link-active" href="/">Home</a>
      <a class="nav-link" href="/candidate-lab">Candidate Lab</a>
      <a class="nav-link" href="/market-studio">Market Studio</a>
      <a class="nav-link" href="/pathway-planner">Pathway Planner</a>
      <a class="nav-link" href="/erp-bridge">ERP Bridge</a>
    </nav>

    <section class="hero">
      __HERO_BRAND__
      <div class="eyebrow">ASEM Talint | calm, evidence-first review</div>
      <h1>One place to read the candidate clearly</h1>
      <p class="hero-copy">
        Review fit, market context, and next steps in a quieter workflow. Use the Z.AI / ILMU review when credentials are ready, or the clearly labeled local preview when they are not.
      </p>

      <section class="strategy-note" aria-label="Made by Malaysia strategy note">
        <div class="strategy-note-head">
          <div>
            <div class="panel-label">Malaysia lens</div>
            <h2 class="strategy-note-title">Local capability, not just placement</h2>
          </div>
          <a class="strategy-link" href="https://www.nst.com.my/news/nation/2026/02/1371466/shift-made-malaysia-strategy" target="_blank" rel="noreferrer">NST source, Feb 5 2026</a>
        </div>
        <p class="strategy-note-copy">
          The national push is toward stronger local vendors, deeper SME participation, and tighter links between investment, training, and research. This product keeps that lens visible while decisions are being made.
        </p>
        <div class="strategy-tags" aria-label="Made by Malaysia priorities">
          <span class="strategy-tag">Local sourcing in FDI and DDI</span>
          <span class="strategy-tag">Vendor development</span>
          <span class="strategy-tag">SME value-chain participation</span>
          <span class="strategy-tag">Industrial training and university links</span>
        </div>
      </section>

      <div class="page-grid" aria-label="App pages">
        <a class="page-card-link" href="/candidate-lab">
          <article class="page-card">
            <div class="panel-label">Candidate Lab</div>
            <div class="page-card-title">Review the evidence</div>
            <div class="page-card-copy">See what is already proven, what feels thin, and what a counselor should tighten next.</div>
          </article>
        </a>
        <a class="page-card-link" href="/market-studio">
          <article class="page-card">
            <div class="panel-label">Market Studio</div>
            <div class="page-card-title">Scout role fit</div>
            <div class="page-card-copy">Read demand through the candidate instead of treating the market as a flat list of vacancies.</div>
          </article>
        </a>
        <a class="page-card-link" href="/pathway-planner">
          <article class="page-card">
            <div class="panel-label">Pathway Planner</div>
            <div class="page-card-title">Plan the next 90 days</div>
            <div class="page-card-copy">Tie shortlist roles to wage direction, blockers, and a practical next-step plan.</div>
          </article>
        </a>
        <a class="page-card-link" href="/erp-bridge">
          <article class="page-card">
            <div class="panel-label">ERP Bridge</div>
            <div class="page-card-title">Prepare the handoff</div>
            <div class="page-card-copy">Package the current case into clean records an ERP can ingest without scraping the UI.</div>
          </article>
        </a>
      </div>

      <div class="badge-row">
        <article class="badge">
          <div class="badge-label">Runtime</div>
          <div class="badge-value" id="runtime-status">Checking...</div>
        </article>
        <article class="badge">
          <div class="badge-label">Primary path</div>
          <div class="badge-value">Z.AI / ILMU</div>
        </article>
        <article class="badge">
          <div class="badge-label">Local preview</div>
          <div class="badge-value">Labeled non-judge-path</div>
        </article>
      </div>

      <div class="metric-grid">
        <article class="metric">
          <div class="metric-label">Overall score</div>
          <div class="metric-value" id="overall-score">--</div>
        </article>
        <article class="metric">
          <div class="metric-label">Confidence</div>
          <div class="metric-value" id="confidence">--</div>
        </article>
        <article class="metric">
          <div class="metric-label">Provider</div>
          <div class="metric-value" id="provider-model">--</div>
        </article>
        <article class="metric">
          <div class="metric-label">Missing inputs</div>
          <div class="metric-value" id="missing-count">--</div>
        </article>
      </div>
    </section>

    <section class="workspace">
      <article class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-label">Working case</div>
            <h2 class="panel-title">Candidate brief</h2>
            <p class="panel-subtitle">Adjust the shared case, then run the Z.AI / ILMU review or the local preview.</p>
          </div>
          <div class="status-pill" id="request-status">Idle</div>
        </div>
        <div class="panel-body">
          <textarea id="payload-input"></textarea>
          <div class="actions">
            <button class="primary" id="run-review">Run Z.AI / ILMU review</button>
            <button class="secondary" id="run-demo">Run local preview</button>
            <button class="ghost" id="reset-payload">Reset sample</button>
          </div>
          <div class="footnote">
            The Z.AI / ILMU review is the primary runtime path. It uses ILMU.ai as the access path to a Z.AI GLM-backed model, while the local preview stays clearly outside the judged path.
          </div>
          <section class="output-card" style="margin-top:16px;">
            <div class="resume-head">
              <div>
                <h3 class="output-title">Resume intake</h3>
                <p class="output-meta">Upload a PDF or DOCX resume. The parser keeps the preview redacted and writes structured evidence back into the shared case.</p>
              </div>
              <div class="status-pill" id="resume-status">No resume loaded</div>
            </div>
            <div class="resume-toolbar">
              <input class="file-input" id="resume-file" type="file" accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document">
              <button class="secondary" id="parse-resume">Parse resume</button>
              <button class="ghost" id="clear-resume">Clear evidence</button>
            </div>
            <div class="mini-grid" style="margin-top:14px;">
              <article class="mini-card">
                <div class="mini-label">Detected skills</div>
                <div class="mini-value" id="resume-skill-count">--</div>
              </article>
              <article class="mini-card">
                <div class="mini-label">PII redactions</div>
                <div class="mini-value" id="resume-redaction-count">--</div>
              </article>
              <article class="mini-card">
                <div class="mini-label">Parser warnings</div>
                <div class="mini-value" id="resume-warning-count">--</div>
              </article>
            </div>
            <div class="chip-list" id="resume-tags"></div>
            <pre class="preview-block" id="resume-preview">Upload a resume to add structured evidence without editing JSON by hand.</pre>
          </section>
        </div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-label">Decision output</div>
            <h2 class="panel-title">Recommendation, reasons, and raw contract</h2>
            <p class="panel-subtitle">Read the recommendation, main factors, next steps, and underlying JSON in one place.</p>
          </div>
        </div>
        <div class="panel-body stack">
          <section class="output-card">
            <h3 class="output-title">Recommendation</h3>
            <pre id="recommendation-summary">Run a review to fill this panel.</pre>
          </section>

          <section class="output-card">
            <h3 class="output-title">Key factors</h3>
            <ol class="list" id="top-factors"></ol>
          </section>

          <section class="output-card">
            <h3 class="output-title">Next steps</h3>
            <ol class="list" id="pathway-steps"></ol>
          </section>

          <section class="output-card">
            <h3 class="output-title">Raw JSON</h3>
            <pre id="raw-output">{}</pre>
          </section>
        </div>
      </article>
    </section>

    <section class="market-grid">
      <article class="panel market-span-2">
        <div class="panel-head">
          <div>
            <div class="panel-label">Market context</div>
            <h2 class="panel-title">Demand, access, and wage direction</h2>
            <p class="panel-subtitle">These panels keep the decision grounded in roles, geography, and economic direction without leaving the case view.</p>
          </div>
          <button class="ghost panel-button" id="refresh-market">Refresh context</button>
        </div>
        <div class="panel-body stack">
          <section class="output-card">
            <h3 class="output-title">At a glance</h3>
            <p class="output-meta" id="market-status">Refresh context to load the latest market view.</p>
            <div class="mini-grid">
              <article class="mini-card">
                <div class="mini-label">Median wage baseline</div>
                <div class="mini-value" id="wage-kpi">--</div>
              </article>
              <article class="mini-card">
                <div class="mini-label">Employer-demand rows</div>
                <div class="mini-value" id="role-count-kpi">--</div>
              </article>
              <article class="mini-card">
                <div class="mini-label">Top OJT fit</div>
                <div class="mini-value" id="match-kpi">--</div>
              </article>
              <article class="mini-card">
                <div class="mini-label">Estimated wage uplift</div>
                <div class="mini-value" id="uplift-kpi">--</div>
              </article>
            </div>
          </section>
          <section class="output-card">
            <h3 class="output-title">Demand by role</h3>
            <div class="bar-list" id="demand-chart"></div>
            <div class="wage-note" id="wage-summary">Refresh context to load the wage slice.</div>
          </section>
        </div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-label">GIS accessibility</div>
            <h2 class="panel-title">Access to hotspots</h2>
            <p class="panel-subtitle">See which clusters stay realistically reachable from the current case.</p>
          </div>
        </div>
        <div class="panel-body map-shell">
          <section class="map-card">
            <svg id="hotspot-map" viewBox="0 0 360 280" aria-label="Hotspot map"></svg>
            <div class="legend">
              <span class="legend-item"><span class="legend-swatch" style="background:#14213d"></span> Candidate</span>
              <span class="legend-item"><span class="legend-swatch" style="background:#0f766e"></span> Strong access</span>
              <span class="legend-item"><span class="legend-swatch" style="background:#d4a373"></span> Moderate access</span>
              <span class="legend-item"><span class="legend-swatch" style="background:#c2410c"></span> Distant hotspot</span>
            </div>
          </section>
          <ol class="list" id="accessibility-list"></ol>
        </div>
      </article>

      <article class="panel market-span-2">
        <div class="panel-head">
          <div>
            <div class="panel-label">OJT matching</div>
            <h2 class="panel-title">Role matches</h2>
            <p class="panel-subtitle">Fit, access, demand, and salary quality are kept in one review table.</p>
          </div>
        </div>
        <div class="panel-body">
          <div class="table-shell">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Role</th>
                  <th>Employer</th>
                  <th>Fit</th>
                  <th>Salary band</th>
                </tr>
              </thead>
              <tbody id="ojt-table-body">
                <tr>
                  <td colspan="4" class="table-note">Refresh context to load ranked OJT matches.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="wage-note" id="employer-summary">Ranked role notes will appear here.</div>
        </div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <div>
            <div class="panel-label">Economic mobility</div>
            <h2 class="panel-title">Wage outlook</h2>
            <p class="panel-subtitle">The strongest current role match becomes a directional wage scenario.</p>
          </div>
        </div>
        <div class="panel-body">
          <div class="wage-bars">
            <div>
              <div class="wage-bar-label"><span>Current estimated wage</span><span id="current-wage-label">--</span></div>
              <div class="bar-track"><div class="bar-fill" id="current-wage-bar" style="width:0%"></div></div>
            </div>
            <div>
              <div class="wage-bar-label"><span>Target estimated wage</span><span id="target-wage-label">--</span></div>
              <div class="bar-track"><div class="bar-fill" id="target-wage-bar" style="width:0%"></div></div>
            </div>
          </div>
          <div class="wage-note" id="mobility-summary">A wage view will appear after the market context loads.</div>
        </div>
      </article>
    </section>
  </main>

  <script>
    const samplePayload = {
      candidate: {
        candidate_id: "cand_0001",
        age_band: "22-24",
        education_level: "bachelor_final_year",
        degree_field: "mechatronics",
        district: "Sepang",
        state: "Selangor",
        latitude: 2.9264,
        longitude: 101.6964,
        skill_tags: ["c++", "debugging", "data_acquisition", "embedded_systems"],
        portfolio_tags: ["robot_arm", "debugging", "sensor_integration"],
        coding_test_score: 74.0,
        math_foundation_score: 69.0,
        communication_score: 78.0,
        willing_to_relocate: true,
        transport_mode: "public_transport",
        prior_training: ["basic_iot_bootcamp"],
        notes: "Interested in validation and robotics workflows with structured mentoring.",
        resume_context: {
          summary: "Built a wafer-inspection prototype and completed an automation internship focused on sensor debugging.",
          skill_tags: ["python_basics", "test_automation"],
          tool_tags: ["oscilloscope", "labview"],
          project_highlights: [
            {
              title: "Vision-guided wafer inspection prototype",
              skill_tags: ["python_basics", "sensor_integration", "debugging"],
              outcome_tags: ["defect_detection"]
            }
          ],
          internship_highlights: [
            {
              organization: "Penang E&E SME",
              role_title: "Automation Intern",
              skill_tags: ["test_automation", "data_acquisition", "debugging"]
            }
          ],
          certifications: ["ipc_basics"],
          inferred_role_signals: ["validation engineer trainee"]
        }
      },
      target_track: {
        track_id: "track_validation",
        track_name: "Chip Validation and Robotics Basics",
        district: "Sepang",
        state: "Selangor",
        required_skills: ["debugging", "data_acquisition", "python_basics"],
        target_roles: ["validation engineer trainee", "robotics trainee"],
        minimum_coding_score: 60.0,
        minimum_math_score: 60.0,
        employer_demand_signal: 0.82,
        wage_growth_signal: 0.73
      }
    };

    const PAYLOAD_STORAGE_KEY = "asem-talint-shared-payload";

    function cloneSamplePayload() {
      return JSON.parse(JSON.stringify(samplePayload));
    }

    function persistPayload(payload) {
      try {
        localStorage.setItem(PAYLOAD_STORAGE_KEY, JSON.stringify(payload));
      } catch (error) {
        console.warn("Could not persist payload", error);
      }
    }

    function readStoredPayload() {
      try {
        const raw = localStorage.getItem(PAYLOAD_STORAGE_KEY);
        if (raw) {
          return JSON.parse(raw);
        }
      } catch (error) {
        console.warn("Could not read payload", error);
      }
      return cloneSamplePayload();
    }

    function syncPayloadInput(payload) {
      payloadInput.value = JSON.stringify(payload, null, 2);
      persistPayload(payload);
    }

    const payloadInput = document.getElementById("payload-input");
    const requestStatus = document.getElementById("request-status");
    const runtimeStatus = document.getElementById("runtime-status");
    const overallScore = document.getElementById("overall-score");
    const confidence = document.getElementById("confidence");
    const providerModel = document.getElementById("provider-model");
    const missingCount = document.getElementById("missing-count");
    const recommendationSummary = document.getElementById("recommendation-summary");
    const rawOutput = document.getElementById("raw-output");
    const topFactors = document.getElementById("top-factors");
    const pathwaySteps = document.getElementById("pathway-steps");
    const marketStatus = document.getElementById("market-status");
    const wageSummary = document.getElementById("wage-summary");
    const wageKpi = document.getElementById("wage-kpi");
    const roleCountKpi = document.getElementById("role-count-kpi");
    const matchKpi = document.getElementById("match-kpi");
    const upliftKpi = document.getElementById("uplift-kpi");
    const demandChart = document.getElementById("demand-chart");
    const employerSummary = document.getElementById("employer-summary");
    const accessibilityList = document.getElementById("accessibility-list");
    const hotspotMap = document.getElementById("hotspot-map");
    const ojtTableBody = document.getElementById("ojt-table-body");
    const currentWageLabel = document.getElementById("current-wage-label");
    const targetWageLabel = document.getElementById("target-wage-label");
    const currentWageBar = document.getElementById("current-wage-bar");
    const targetWageBar = document.getElementById("target-wage-bar");
    const mobilitySummary = document.getElementById("mobility-summary");
    const runReviewButton = document.getElementById("run-review");
    const runDemoButton = document.getElementById("run-demo");
    const resetButton = document.getElementById("reset-payload");
    const refreshMarketButton = document.getElementById("refresh-market");
    const resumeFileInput = document.getElementById("resume-file");
    const parseResumeButton = document.getElementById("parse-resume");
    const clearResumeButton = document.getElementById("clear-resume");
    const resumeStatus = document.getElementById("resume-status");
    const resumeSkillCount = document.getElementById("resume-skill-count");
    const resumeRedactionCount = document.getElementById("resume-redaction-count");
    const resumeWarningCount = document.getElementById("resume-warning-count");
    const resumeTags = document.getElementById("resume-tags");
    const resumePreview = document.getElementById("resume-preview");
    let reviewProviderReady = false;

    function resetPayload() {
      syncPayloadInput(cloneSamplePayload());
    }

    function resetResumePanel() {
      resumeStatus.textContent = "No resume loaded";
      resumeSkillCount.textContent = "--";
      resumeRedactionCount.textContent = "--";
      resumeWarningCount.textContent = "--";
      resumeTags.innerHTML = "";
      resumePreview.textContent = "Upload a resume to add structured evidence without editing JSON by hand.";
      if (resumeFileInput) {
        resumeFileInput.value = "";
      }
    }

    function parsePayload() {
      try {
        const payload = JSON.parse(payloadInput.value);
        persistPayload(payload);
        return payload;
      } catch (error) {
        requestStatus.textContent = "Invalid JSON payload";
        recommendationSummary.textContent = String(error);
        return null;
      }
    }

    function formatNumber(value) {
      if (value === null || value === undefined || Number.isNaN(value)) {
        return "UNSPECIFIED";
      }
      return new Intl.NumberFormat("en-MY", { maximumFractionDigits: 1 }).format(value);
    }

    function formatCurrency(value) {
      if (value === null || value === undefined || Number.isNaN(value)) {
        return "UNSPECIFIED";
      }
      return `MYR ${formatNumber(value)}`;
    }

    async function fetchJson(path, options) {
      const response = await fetch(path, options);
      const body = await response.json();
      if (!response.ok) {
        throw new Error(body.detail || "Request failed");
      }
      return body;
    }

    function totalRedactions(redactionCounts) {
      return Object.values(redactionCounts || {}).reduce((total, value) => total + value, 0);
    }

    function renderResumeTagsList(context) {
      resumeTags.innerHTML = "";
      const values = [
        ...(context.skill_tags || []),
        ...(context.tool_tags || []),
        ...(context.inferred_role_signals || [])
      ];
      if (values.length === 0) {
        const chip = document.createElement("span");
        chip.className = "chip";
        chip.textContent = "No structured tags extracted";
        resumeTags.appendChild(chip);
        return;
      }

      values.slice(0, 12).forEach((value) => {
        const chip = document.createElement("span");
        chip.className = "chip";
        chip.textContent = value;
        resumeTags.appendChild(chip);
      });
    }

    function applyResumeContextToPayload(resumeContext) {
      const payload = parsePayload();
      if (!payload) {
        throw new Error("Fix the JSON payload before applying parsed resume evidence.");
      }
      payload.candidate.resume_context = resumeContext;
      syncPayloadInput(payload);
    }

    async function parseAndApplyResume() {
      const file = resumeFileInput.files && resumeFileInput.files[0];
      if (!file) {
        resumeStatus.textContent = "Choose a PDF or DOCX file";
        return;
      }

      parseResumeButton.disabled = true;
      clearResumeButton.disabled = true;
      resumeStatus.textContent = "Parsing resume";
      try {
        const formData = new FormData();
        formData.append("file", file);
        const result = await fetchJson("/v1/resumes/parse", {
          method: "POST",
          body: formData
        });

        applyResumeContextToPayload(result.resume_context);
        resumeStatus.textContent = "Resume applied to payload";
        resumeSkillCount.textContent = String((result.resume_context.skill_tags || []).length);
        resumeRedactionCount.textContent = String(totalRedactions(result.redaction_counts));
        resumeWarningCount.textContent = String((result.warnings || []).length);
        resumePreview.textContent = result.redacted_preview || "Parser returned no preview text.";
        renderResumeTagsList(result.resume_context);
        refreshMarketPanels().catch(() => {
          marketStatus.textContent = "Market refresh failed after resume apply";
        });
      } catch (error) {
        resumeStatus.textContent = "Resume parse failed";
        resumeSkillCount.textContent = "--";
        resumeRedactionCount.textContent = "--";
        resumeWarningCount.textContent = "--";
        resumeTags.innerHTML = "";
        resumePreview.textContent = String(error);
      } finally {
        parseResumeButton.disabled = false;
        clearResumeButton.disabled = false;
      }
    }

    function clearResumeContext() {
      const payload = parsePayload();
      if (!payload) {
        return;
      }
      delete payload.candidate.resume_context;
      syncPayloadInput(payload);
      resetResumePanel();
      resumeStatus.textContent = "Resume context cleared";
      refreshMarketPanels().catch(() => {
        marketStatus.textContent = "Market refresh failed after clearing resume context";
      });
    }

    function renderList(element, values) {
      element.innerHTML = "";
      (values || []).forEach((value) => {
        const item = document.createElement("li");
        item.textContent = value;
        element.appendChild(item);
      });
      if (!values || values.length === 0) {
        const item = document.createElement("li");
        item.textContent = "None";
        element.appendChild(item);
      }
    }

    function renderDemandChart(rows) {
      demandChart.innerHTML = "";
      if (!rows || rows.length === 0) {
        demandChart.innerHTML = '<div class="table-note">No employer-demand rows returned for the current track.</div>';
        return;
      }

      rows.forEach((row) => {
        const score = row.market_signal_score ?? row.demand_score;
        const alignment = row.resume_alignment_score ?? 0;
        const wrapper = document.createElement("div");
        wrapper.className = "bar-row";
        wrapper.innerHTML = `
          <div class="bar-label">
            <span>${row.role_title}</span>
            <span>${formatNumber(score)}${row.market_signal_score !== undefined ? ` | resume ${formatNumber(alignment)}` : ""}</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${Math.max(8, score * 100)}%"></div></div>
        `;
        demandChart.appendChild(wrapper);
      });
    }

    function renderOjtTable(matches) {
      ojtTableBody.innerHTML = "";
      if (!matches || matches.length === 0) {
        ojtTableBody.innerHTML = '<tr><td colspan="4" class="table-note">No OJT matches available for the current payload.</td></tr>';
        return;
      }

      matches.forEach((match) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${match.role_title}</strong><br><span class="table-note">${match.blockers.length ? `Blockers: ${match.blockers.join(", ")}` : "No major blockers"}</span></td>
          <td>${match.employer_name}<br><span class="table-note">${match.commute_note}</span></td>
          <td>${formatNumber(match.match_score)}</td>
          <td>${formatCurrency(match.salary_band_min)} to ${formatCurrency(match.salary_band_max)}</td>
        `;
        ojtTableBody.appendChild(row);
      });
    }

    function renderHotspotMap(candidate, destinations) {
      if (!candidate.latitude || !candidate.longitude || !destinations || destinations.length === 0) {
        hotspotMap.innerHTML = '<text x="16" y="28" fill="#5b6472" font-size="14">Map unavailable because coordinates are incomplete.</text>';
        return;
      }

      const points = [
        { name: "Candidate", latitude: candidate.latitude, longitude: candidate.longitude, kind: "candidate", score: 1 },
        ...destinations.filter((item) => item.latitude && item.longitude).map((item) => ({
          name: item.destination_name,
          latitude: item.latitude,
          longitude: item.longitude,
          kind: "hotspot",
          score: item.accessibility_score,
        }))
      ];

      if (points.length <= 1) {
        hotspotMap.innerHTML = '<text x="16" y="28" fill="#5b6472" font-size="14">Map unavailable because hotspot coordinates are incomplete.</text>';
        return;
      }

      const minLon = Math.min(...points.map((point) => point.longitude));
      const maxLon = Math.max(...points.map((point) => point.longitude));
      const minLat = Math.min(...points.map((point) => point.latitude));
      const maxLat = Math.max(...points.map((point) => point.latitude));
      const width = 360;
      const height = 280;
      const padding = 28;

      const projectX = (longitude) => padding + ((longitude - minLon) / Math.max(0.01, maxLon - minLon)) * (width - padding * 2);
      const projectY = (latitude) => height - padding - ((latitude - minLat) / Math.max(0.01, maxLat - minLat)) * (height - padding * 2);

      const circles = points.map((point, index) => {
        const x = projectX(point.longitude);
        const y = projectY(point.latitude);
        const color = point.kind === "candidate"
          ? "#14213d"
          : point.score >= 0.8
            ? "#0f766e"
            : point.score >= 0.55
              ? "#d4a373"
              : "#c2410c";
        const markerRadius = point.kind === "candidate" ? 11 : 9;
        const markerText = point.kind === "candidate" ? "C" : String(index);
        const labelText = point.kind === "candidate"
          ? "Candidate"
          : `${index}. ${point.name.split("(")[0].trim()}`;
        const labelAnchor = x > width * 0.72 ? "end" : "start";
        const labelOffsetX = labelAnchor === "end" ? -14 : 14;
        const labelOffsetY = point.kind === "candidate" ? -16 : (index % 2 === 0 ? -14 : 20);
        const labelX = Math.min(width - 18, Math.max(18, x + labelOffsetX));
        const labelY = Math.min(height - 14, Math.max(20, y + labelOffsetY));
        return `
          <g>
            <title>${point.name}</title>
            <circle cx="${x}" cy="${y}" r="${markerRadius}" fill="#fffdf8" opacity="0.98"></circle>
            <circle cx="${x}" cy="${y}" r="${markerRadius - 2}" fill="${color}" opacity="0.98"></circle>
            <text x="${x}" y="${y + 3.5}" fill="#fffdf8" font-size="9" font-weight="700" text-anchor="middle">${markerText}</text>
            <text x="${labelX}" y="${labelY}" fill="#5b6472" font-size="10" font-weight="600" text-anchor="${labelAnchor}">${labelText}</text>
          </g>
        `;
      }).join("");

      const candidatePoint = points[0];
      const lines = points.slice(1).map((point) => `
        <line x1="${projectX(candidatePoint.longitude)}" y1="${projectY(candidatePoint.latitude)}" x2="${projectX(point.longitude)}" y2="${projectY(point.latitude)}" stroke="rgba(20, 33, 61, 0.16)" stroke-width="1.5" stroke-dasharray="5 4"></line>
      `).join("");

      hotspotMap.innerHTML = `
        <rect x="0" y="0" width="360" height="280" rx="18" fill="rgba(255,255,255,0.55)"></rect>
        <rect x="18" y="18" width="324" height="244" rx="16" fill="rgba(255,253,248,0.92)" stroke="rgba(20, 33, 61, 0.06)"></rect>
        <path d="M18 220 C70 175, 98 168, 156 176 S260 150, 340 96" fill="none" stroke="rgba(20, 33, 61, 0.09)" stroke-width="48" stroke-linecap="round"></path>
        ${lines}
        ${circles}
      `;
    }

    function renderWageComparison(mobility) {
      const current = mobility.current_estimated_wage;
      const target = mobility.target_estimated_wage;
      const maxValue = Math.max(current || 0, target || 0, 1);
      currentWageLabel.textContent = formatCurrency(current);
      targetWageLabel.textContent = formatCurrency(target);
      currentWageBar.style.width = `${Math.max(6, ((current || 0) / maxValue) * 100)}%`;
      targetWageBar.style.width = `${Math.max(6, ((target || 0) / maxValue) * 100)}%`;
      upliftKpi.textContent = mobility.estimated_uplift_abs !== null && mobility.estimated_uplift_abs !== undefined
        ? formatCurrency(mobility.estimated_uplift_abs)
        : "UNSPECIFIED";
    }

    function setBusyState(isBusy, label) {
      requestStatus.textContent = label;
      runReviewButton.disabled = isBusy || !reviewProviderReady;
      runDemoButton.disabled = isBusy;
    }

    function setMarketBusyState(isBusy, label) {
      marketStatus.textContent = label;
      refreshMarketButton.disabled = isBusy;
    }

    async function fetchHealth() {
      const response = await fetch("/health");
      const body = await response.json();
      reviewProviderReady = Boolean(body.review_provider_ready ?? body.ilmu_provider_ready ?? body.zai_provider_ready ?? body.live_provider_ready);
      runtimeStatus.textContent = `${body.status} / ${body.environment} / Z.AI / ILMU ${reviewProviderReady ? "ready" : "unavailable"}`;
      runReviewButton.disabled = !reviewProviderReady;
      if (!reviewProviderReady) {
        requestStatus.textContent = body.review_provider_message || body.ilmu_provider_message || "Configure ILMU_API_KEY, ILMU_BASE_URL, and ILMU_MODEL to enable the Z.AI / ILMU review.";
      }
    }

    async function submitDecision(path, statusLabel, successLabel) {
      const payload = parsePayload();
      if (!payload) {
        return;
      }

      setBusyState(true, statusLabel);
      try {
        const response = await fetch(path, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const body = await response.json();

        if (!response.ok) {
          throw new Error(body.detail || "Request failed");
        }

        overallScore.textContent = body.context.score_breakdown.overall_score.toFixed(2);
        confidence.textContent = body.explanation.confidence.toFixed(2);
        providerModel.textContent = body.usage.model || "unknown";
        missingCount.textContent = String(body.context.missing_inputs.length);
        recommendationSummary.textContent = `${body.explanation.recommendation}\n\n${body.explanation.explanation_summary}`;
        renderList(topFactors, body.explanation.top_factors);
        renderList(pathwaySteps, body.explanation.pathway_steps);
        rawOutput.textContent = JSON.stringify(body, null, 2);
        requestStatus.textContent = successLabel;
      } catch (error) {
        requestStatus.textContent = "Request failed";
        recommendationSummary.textContent = String(error);
        rawOutput.textContent = "{}";
        renderList(topFactors, []);
        renderList(pathwaySteps, []);
      } finally {
        setBusyState(false, requestStatus.textContent);
      }
    }

    async function refreshMarketPanels() {
      const payload = parsePayload();
      if (!payload) {
        return;
      }

      setMarketBusyState(true, "Refreshing market context");
      try {
        const state = encodeURIComponent(payload.candidate.state);
        const trackId = encodeURIComponent(payload.target_track.track_id);

        const [wages, employerDemand, accessibility, ojt] = await Promise.all([
          fetchJson(`/v1/signals/wages?state=${state}`),
          fetchJson("/v1/signals/employer-demand/ranked", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              candidate: payload.candidate,
              track_id: payload.target_track.track_id,
              limit: 5
            })
          }),
          fetchJson("/v1/signals/accessibility", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ candidate: payload.candidate, limit: 4 })
          }),
          fetchJson("/v1/matching/ojt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ candidate: payload.candidate, target_track_id: payload.target_track.track_id, limit: 3 })
          })
        ]);

        const rankedDemand = employerDemand.roles || [];
        const topWage = wages[0];
        if (topWage) {
          wageSummary.textContent = `${topWage.state} median wage baseline: MYR ${formatNumber(topWage.value)}\nDate: ${topWage.date}\nSource: ${topWage.source}`;
          wageKpi.textContent = formatCurrency(topWage.value);
        } else {
          wageSummary.textContent = "No wage slice returned for the current state.";
          wageKpi.textContent = "UNSPECIFIED";
        }

        const topRole = rankedDemand[0];
        if (topRole) {
          employerSummary.textContent = `${rankedDemand.length} employer-demand rows loaded for ${payload.target_track.track_name}.\nTop role: ${topRole.role_title} at ${topRole.employer_name}\nSalary band: MYR ${formatNumber(topRole.salary_band_min)} to ${formatNumber(topRole.salary_band_max)}\nMarket signal score: ${formatNumber(topRole.market_signal_score)}\nResume alignment: ${formatNumber(topRole.resume_alignment_score)}\n${topRole.resume_evidence_summary}`;
          roleCountKpi.textContent = String(rankedDemand.length);
        } else {
          employerSummary.textContent = "No employer-demand rows returned for the current track.";
          roleCountKpi.textContent = "0";
        }

        renderDemandChart(rankedDemand);

        renderList(
          accessibilityList,
          (accessibility.destinations || []).map((item) => `${item.destination_name} (${item.state}) score ${formatNumber(item.accessibility_score)}${item.distance_km ? `, ${formatNumber(item.distance_km)} km` : ""}`)
        );
        renderHotspotMap(payload.candidate, accessibility.destinations || []);
        renderOjtTable(ojt.matches || []);
        matchKpi.textContent = ojt.matches && ojt.matches.length > 0 ? formatNumber(ojt.matches[0].match_score) : "UNSPECIFIED";

        if (ojt.matches && ojt.matches.length > 0) {
          const mobility = await fetchJson("/v1/analysis/wage-mobility", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              candidate: payload.candidate,
              target_role_id: ojt.matches[0].role_id,
              current_sector: "manufacturing"
            })
          });
          mobilitySummary.textContent = `${mobility.target_role_title}\nCurrent estimated wage: MYR ${formatNumber(mobility.current_estimated_wage)}\nTarget estimated wage: MYR ${formatNumber(mobility.target_estimated_wage)}\nEstimated uplift: MYR ${formatNumber(mobility.estimated_uplift_abs)}${mobility.estimated_uplift_pct !== null && mobility.estimated_uplift_pct !== undefined ? ` (${formatNumber(mobility.estimated_uplift_pct)}%)` : ""}\nEvidence strength: ${mobility.evidence_strength}\nResume alignment: ${formatNumber(mobility.resume_alignment_score)}\n${mobility.confidence_rationale}\n${mobility.caution_note}`;
          renderWageComparison(mobility);
        } else {
          mobilitySummary.textContent = "No OJT role available, so wage mobility could not be estimated.";
          currentWageLabel.textContent = "UNSPECIFIED";
          targetWageLabel.textContent = "UNSPECIFIED";
          currentWageBar.style.width = "0%";
          targetWageBar.style.width = "0%";
          upliftKpi.textContent = "UNSPECIFIED";
        }

        setMarketBusyState(false, "Market panels loaded");
      } catch (error) {
        wageSummary.textContent = String(error);
        employerSummary.textContent = "Market refresh failed before employer-demand rendering.";
        mobilitySummary.textContent = "Market refresh failed before wage-mobility rendering.";
        renderList(accessibilityList, []);
        renderOjtTable([]);
        renderDemandChart([]);
        hotspotMap.innerHTML = '<text x="16" y="28" fill="#5b6472" font-size="14">Map failed to load.</text>';
        wageKpi.textContent = "UNSPECIFIED";
        roleCountKpi.textContent = "0";
        matchKpi.textContent = "UNSPECIFIED";
        upliftKpi.textContent = "UNSPECIFIED";
        currentWageLabel.textContent = "UNSPECIFIED";
        targetWageLabel.textContent = "UNSPECIFIED";
        currentWageBar.style.width = "0%";
        targetWageBar.style.width = "0%";
        setMarketBusyState(false, "Market refresh failed");
      }
    }

    runReviewButton.addEventListener("click", () => {
      if (reviewProviderReady) {
        submitDecision("/v1/decisions/candidate-track-fit/ilmu", "Calling Z.AI / ILMU review via ILMU compatibility route", "Z.AI / ILMU review loaded");
        return;
      }
      requestStatus.textContent = "Configure ILMU_API_KEY, ILMU_BASE_URL, and ILMU_MODEL to enable the Z.AI / ILMU review.";
    });
    runDemoButton.addEventListener("click", () => submitDecision("/v1/decisions/candidate-track-fit/demo", "Running degraded local demo", "Demo result loaded"));
    resetButton.addEventListener("click", () => {
      resetPayload();
      resetResumePanel();
      refreshMarketPanels();
    });
    refreshMarketButton.addEventListener("click", refreshMarketPanels);
    parseResumeButton.addEventListener("click", parseAndApplyResume);
    clearResumeButton.addEventListener("click", clearResumeContext);

    payloadInput.addEventListener("input", () => {
      try {
        persistPayload(JSON.parse(payloadInput.value));
      } catch (error) {
        // Ignore partial edits until JSON becomes valid again.
      }
    });

    syncPayloadInput(readStoredPayload());
    resetResumePanel();
    fetchHealth().catch(() => {
      runtimeStatus.textContent = "health check failed";
    });
    refreshMarketPanels().catch(() => {
      marketStatus.textContent = "Market refresh failed";
    });
  </script>
</body>
</html>
"""

DASHBOARD_HTML = (
  DASHBOARD_HTML.replace("__BRAND_CSS__", BRAND_CSS)
  .replace("__NAV_BRAND__", render_nav_brand(id_prefix="dashboard-nav"))
  .replace(
    "__HERO_BRAND__",
    render_hero_brand(
      caption="Decision intelligence for semiconductor mobility",
      id_prefix="dashboard-hero",
    ),
  )
)


@router.get("/", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_alias() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)


@router.get("/candidate-lab", response_class=HTMLResponse)
def candidate_lab_page() -> HTMLResponse:
  return HTMLResponse(candidate_lab_html())


@router.get("/market-studio", response_class=HTMLResponse)
def market_studio_page() -> HTMLResponse:
  return HTMLResponse(market_studio_html())


@router.get("/pathway-planner", response_class=HTMLResponse)
def pathway_planner_page() -> HTMLResponse:
  return HTMLResponse(pathway_planner_html())


@router.get("/erp-bridge", response_class=HTMLResponse)
def erp_bridge_page() -> HTMLResponse:
  return HTMLResponse(erp_bridge_html())
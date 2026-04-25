from __future__ import annotations

from html import escape


BRAND_CSS = """
    .brand-lockup {
      display: grid;
      gap: 8px;
      width: fit-content;
      max-width: 100%;
      text-decoration: none;
      color: inherit;
    }

    .brand-lockup-nav {
      display: inline-flex;
      align-items: center;
      padding: 6px 10px 6px 2px;
      margin-right: auto;
    }

    .brand-lockup-hero {
      gap: 10px;
    }

    .brand-logo {
      display: block;
      height: auto;
    }

    .brand-logo-nav {
      width: 172px;
      max-width: 100%;
    }

    .brand-logo-page {
      width: 252px;
      max-width: 100%;
    }

    .brand-logo-hero {
      width: 388px;
      max-width: 100%;
    }

    .brand-caption {
      margin: 0;
      font-size: 0.74rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--muted);
    }
"""


ASEM_TALINT_LOGO_TEMPLATE = """
<svg class="__CLASS__" viewBox="0 0 720 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ASEM Talint logo">
  <defs>
    <linearGradient id="__WARM_ID__" x1="168" y1="22" x2="270" y2="124" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#f2c94c" />
      <stop offset="52%" stop-color="#f2994a" />
      <stop offset="100%" stop-color="#d6452d" />
    </linearGradient>
    <linearGradient id="__TRAIL_ID__" x1="6" y1="124" x2="264" y2="156" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#d1a545" />
      <stop offset="100%" stop-color="#d6452d" />
    </linearGradient>
  </defs>
  <text x="8" y="94" fill="#1f1d1a" font-size="92" font-weight="900" letter-spacing="-4" font-family="'Arial Black', 'Segoe UI', sans-serif">AS</text>
  <g transform="translate(178 18)">
    <circle cx="50" cy="50" r="40" fill="none" stroke="url(#__WARM_ID__)" stroke-width="18" stroke-linecap="round" stroke-dasharray="176 88" stroke-dashoffset="20"/>
    <path d="M18 56 H84" fill="none" stroke="url(#__WARM_ID__)" stroke-width="18" stroke-linecap="round"/>
    <circle cx="50" cy="50" r="10" fill="#fff8ef"/>
    <circle cx="88" cy="18" r="5" fill="#f2c94c"/>
    <circle cx="97" cy="88" r="6" fill="#d6452d"/>
  </g>
  <text x="314" y="94" fill="#1f1d1a" font-size="92" font-weight="900" letter-spacing="-5" font-family="'Arial Black', 'Segoe UI', sans-serif">M</text>
  <path d="M8 122 C112 122 160 132 244 152" fill="none" stroke="url(#__TRAIL_ID__)" stroke-width="10" stroke-linecap="round"/>
  <circle cx="258" cy="154" r="7" fill="#d6452d"/>
  <text x="281" y="58" fill="#7a664b" font-size="16" letter-spacing="2.4" font-family="'Segoe UI', sans-serif">SEMICONDUCTOR TALENT INTELLIGENCE</text>
  <text x="280" y="158" fill="#2f2b27" font-size="36" font-weight="700" letter-spacing="6" font-family="'Segoe UI Semibold', 'Segoe UI', sans-serif">TALINT</text>
</svg>
"""


def render_logo(class_name: str, *, id_prefix: str) -> str:
    return (
        ASEM_TALINT_LOGO_TEMPLATE.replace("__CLASS__", class_name)
        .replace("__WARM_ID__", f"{id_prefix}-warm")
        .replace("__TRAIL_ID__", f"{id_prefix}-trail")
    )


def render_nav_brand(*, id_prefix: str = "nav-brand") -> str:
    return (
        '<a class="brand-lockup brand-lockup-nav" href="/" aria-label="ASEM Talint home">'
        + render_logo("brand-logo brand-logo-nav", id_prefix=id_prefix)
        + "</a>"
    )


def render_hero_brand(
    *,
    caption: str | None = None,
    id_prefix: str = "hero-brand",
    variant: str = "hero",
) -> str:
    logo_class = "brand-logo brand-logo-page" if variant == "page" else "brand-logo brand-logo-hero"
    caption_html = f'<p class="brand-caption">{escape(caption)}</p>' if caption else ""
    return '<div class="brand-lockup brand-lockup-hero">' + render_logo(logo_class, id_prefix=id_prefix) + caption_html + "</div>"
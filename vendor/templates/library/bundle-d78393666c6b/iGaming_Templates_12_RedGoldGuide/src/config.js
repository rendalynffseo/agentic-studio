// Site-wide settings. Values set to null are facts the owner has not yet supplied;
// the build hides anything that depends on them instead of guessing.
export default {
  name: 'EU9 Slots Malaysia',
  domain: 'https://eu9slots.com',
  email: 'support@eu9slots.com',
  lang: 'ms-MY',
  locale: 'ms_MY',

  // Relationship between this website and the EU9 brand/operator.
  // One of: 'unconfirmed' | 'official' | 'affiliate' | 'independent'.
  // Change only after the owner confirms it in writing. See src/relationship.js.
  relationship: 'unconfirmed',

  // Legal name of the organisation that publishes this website (e.g. "Sdn. Bhd.").
  publisherLegalName: null,

  // Verified EU9 platform address. When set, platform-access buttons are rendered
  // and clearly labelled as leaving this website. Leave null until verified.
  platformUrl: null,

  // Optional call-to-action, e.g. { url, brand, host }. The label must name the real
  // destination; set to null to show no CTA.
  cta: null,

  // Floating "Log Masuk / Login" + "Daftar / Register" bar and the pop-up banner.
  // url: null renders them without a link. Only set a URL that lands on EU9 itself,
  // because the labels tell readers they are signing in to / registering with EU9.
  // popupAlt: describe the popup image (assets-src/owner/popup.png, else generated art).
  // repeatSeconds: 0 = once per browser session; 30 = reopen 30 s after every close.
  access: { show: true, url: null, popupAlt: 'Panduan EU9 Slots Malaysia', repeatSeconds: 30 },

  // Byline used on articles. Replace with real, named people once supplied.
  author: { name: 'Pasukan Editorial EU9 Slots Malaysia', url: '/penulis/' },
  // A named human reviewer, e.g. { name: 'Nama Penuh', role: 'Editor' }. null = not shown.
  reviewer: null,

  // Default date for pages first published in this release.
  launchDate: '2026-11-01',

  // Google Search Console HTML-tag verification code (content value only), or null.
  gscVerification: null,

  // Cloudflare Pages project name used by ./deploy.sh
  cfProject: 'eu9slots',
};

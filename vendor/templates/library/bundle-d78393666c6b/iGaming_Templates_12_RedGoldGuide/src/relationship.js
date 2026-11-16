// Public wording for each possible relationship with EU9. Only the variant selected in
// config.relationship is published. Every variant is true for its case; none asserts a
// relationship that has not been confirmed.
import config from './config.js';

// Extra disclosure whenever a referral CTA is shown (independent of the EU9 relationship).
export const CTA_DISCLOSURE = config.cta
  ? `Laman ini memaparkan pautan rujukan ke ${config.cta.brand} (${config.cta.host}), sebuah platform yang berasingan daripada EU9. Kami mungkin menerima komisen jika anda mendaftar melalui pautan tersebut.`
  : '';

export const RELATIONSHIP = {
  unconfirmed: {
    short: config.cta
      ? `Laman maklumat dan panduan. Bukan tempat log masuk, pendaftaran atau transaksi. Mengandungi pautan rujukan ke ${config.cta.brand}.`
      : 'Laman maklumat dan panduan. Bukan tempat log masuk, pendaftaran atau transaksi.',
    full: `<p>EU9 Slots Malaysia menerbitkan maklumat pendidikan dan panduan pengguna dalam Bahasa Melayu tentang slot EU9. Laman ini <strong>tidak</strong> memproses log masuk, pendaftaran, deposit atau pengeluaran, dan tidak menyimpan butiran akaun permainan anda.</p>
<p>Kami tidak menggelar laman ini sebagai laman rasmi pengendali EU9. Butiran hubungan komersial antara penerbit laman ini dengan jenama EU9 akan dinyatakan di halaman ini sebaik sahaja disahkan. ${config.cta ? CTA_DISCLOSURE : 'Pada masa ini laman ini tidak memaparkan pautan afiliasi atau butang ke platform.'}</p>`,
  },
  official: {
    short: 'Laman panduan rasmi yang diterbitkan oleh pemilik jenama EU9.',
    full: `<p>EU9 Slots Malaysia diterbitkan oleh pemilik jenama EU9 sebagai pusat panduan dan bantuan pengguna. Log masuk, pendaftaran dan transaksi tetap dilakukan di platform EU9, bukan di laman panduan ini.</p>`,
  },
  affiliate: {
    short: 'Penerbit afiliasi. Kami mungkin menerima komisen daripada pautan ke EU9.',
    full: `<p>EU9 Slots Malaysia ialah penerbit afiliasi. Kami bukan pengendali EU9. Apabila anda menggunakan pautan tertentu ke platform EU9, kami mungkin menerima komisen. Komisen ini tidak mengubah fakta dalam artikel, dan setiap pautan ke platform dilabel dengan jelas.</p>`,
  },
  independent: {
    short: 'Penerbit bebas tanpa hubungan komersial dengan EU9.',
    full: `<p>EU9 Slots Malaysia ialah penerbit bebas. Kami tidak dimiliki oleh pengendali EU9 dan tidak menerima bayaran daripadanya.</p>`,
  },
};

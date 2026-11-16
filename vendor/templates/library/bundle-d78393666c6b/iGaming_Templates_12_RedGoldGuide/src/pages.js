// Supporting pages. Bodies are functions so they always reflect current config values.
// Nothing here names a company, address or person the owner has not supplied.
import config from './config.js';
import fs from 'node:fs';
import { RELATIONSHIP, CTA_DISCLOSURE } from './relationship.js';
import { GALLERY, GALLERY_DATE } from './gallery.js';

const REL = () => RELATIONSHIP[config.relationship];
const mail = `<a href="mailto:${config.email}">${config.email}</a>`;
const publisher = () => config.publisherLegalName
  ? `${config.publisherLegalName}, penerbit ${config.name}`
  : `penerbit ${config.name}`;
const U = config.launchDate;

const MONTHS = ['Januari', 'Februari', 'Mac', 'April', 'Mei', 'Jun', 'Julai', 'Ogos', 'September', 'Oktober', 'November', 'Disember'];
const longDate = (iso) => { const [y, m, d] = iso.split('-').map(Number); return `${d} ${MONTHS[m - 1]} ${y}`; };

function galleryBody() {
  const sizes = JSON.parse(fs.readFileSync(new URL('./img/galeri/manifest.json', import.meta.url), 'utf8'));
  const shot = (s, grid) => {
    const m = sizes[s.n], srcset = m.small === m.big ? `/img/galeri/${s.n}-${m.big}.webp ${m.big}w` : `/img/galeri/${s.n}-${m.small}.webp ${m.small}w, /img/galeri/${s.n}-${m.big}.webp ${m.big}w`;
    return `<figure class="shot${s.small ? ' shot--small' : ''}"><a href="/img/galeri/${s.n}-${m.big}.webp"><img src="/img/galeri/${s.n}-${m.big}.webp" srcset="${srcset}" sizes="${grid ? '(min-width: 960px) 220px, 50vw' : '(min-width: 1200px) 1150px, 100vw'}" width="${m.width}" height="${m.height}" alt="${s.alt}" loading="lazy" decoding="async"></a><figcaption>${s.caption}</figcaption></figure>`;
  };
  return `
<p class="lead">Tangkapan skrin platform EU9 yang dibekalkan oleh pemilik laman ini, diambil pada ${longDate(GALLERY_DATE)}. Ia menunjukkan rupa platform pada tarikh tersebut; permainan, promosi dan angka boleh berubah.</p>
<aside class="note"><p>Laman ini ialah laman panduan, bukan platform EU9. Gambar di bawah tidak boleh diklik untuk bermain, log masuk atau mendaftar. Seni permainan ialah hak cipta pembekal masing-masing. Kandungan untuk pembaca dewasa sahaja — <a href="/permainan-bertanggungjawab/">permainan bertanggungjawab</a>.</p></aside>
<nav class="toc" aria-label="Bahagian galeri"><ol>${GALLERY.map((g) => `<li><a href="#${g.id}">${g.name}</a></li>`).join('')}</ol></nav>
${GALLERY.map((g) => `<section class="shots-group" id="${g.id}" aria-labelledby="h-${g.id}">
  <h2 id="h-${g.id}">${g.name}</h2>
  ${g.note ? `<aside class="note"><p>${g.note}</p></aside>` : ''}
  <div class="${g.grid ? 'shots-grid' : 'shots'}">${g.shots.map((s) => shot(s, g.grid)).join('')}</div>
</section>`).join('\n')}
<p class="small muted">Untuk panduan permainan yang ditunjukkan di sini, lihat [[/permainan-slot/|panduan permainan slot]]. Untuk promosi, lihat [[/bonus-syarat-cuci/|panduan bonus dan syarat cuci]].</p>`;
}

export const PAGES = [
  ...(GALLERY.length ? [{
    path: '/galeri/', nav: 'Galeri Lobi EU9', h1: 'Galeri Lobi EU9', updated: GALLERY_DATE, wide: true,
    title: 'Galeri Lobi EU9 — Tangkapan Skrin Platform | EU9 Slots Malaysia',
    desc: 'Tangkapan skrin bertarikh lobi platform EU9: kategori permainan slot, live casino, duta jenama, jadual transaksi dan promosi, dengan nota tentang terma.',
    body: galleryBody,
  }] : []),
  {
    path: '/tentang-kami/', nav: 'Tentang Kami', h1: 'Tentang EU9 Slots Malaysia', updated: U,
    title: 'Tentang Kami — EU9 Slots Malaysia',
    desc: 'Siapa EU9 Slots Malaysia, apa yang kami terbitkan, hubungan laman ini dengan EU9 dan cara kami memastikan maklumat tepat.',
    body: () => `
<p>EU9 Slots Malaysia ialah laman panduan dalam Bahasa Melayu untuk pembaca dewasa di Malaysia yang mahu memahami permainan slot EU9, terma bonus dan cara menyelesaikan masalah akaun biasa.</p>
<h2>Hubungan dengan EU9</h2>
${REL().full}
<p>Kami membezakan empat perkara dengan jelas dalam setiap artikel:</p>
<ul>
  <li><strong>EU9 Slots Malaysia</strong> — laman panduan ini (eu9slots.com).</li>
  <li><strong>Jenama EU9</strong> — platform permainan dan pengendalinya.</li>
  <li><strong>Penerbit laman ini</strong> — pihak yang menulis dan mengurus kandungan di sini.</li>
  <li><strong>Pembekal permainan</strong> — syarikat yang membangunkan permainan individu; peraturan dan RTP ditetapkan oleh mereka bagi setiap versi permainan.</li>
</ul>
<h2>Apa yang kami terbitkan</h2>
<ul>
  <li>Penerangan peraturan dan ciri slot: paytable, paylines, wild, scatter dan free spins.</li>
  <li>Penerangan RTP, volatiliti dan kelebihan rumah, dengan contoh RM yang dilabel hipotetikal.</li>
  <li>Cara membaca dan mengira terma bonus serta syarat cuci.</li>
  <li>Semakan umum untuk masalah log masuk, deposit dan keselamatan akaun.</li>
  <li>Maklumat untuk menetapkan had dan mendapatkan bantuan.</li>
</ul>
<h2>Apa yang kami tidak buat</h2>
<ul>
  <li>Kami tidak memproses log masuk, pendaftaran, deposit atau pengeluaran.</li>
  <li>Kami tidak boleh melihat, membuka atau mengubah akaun EU9 anda.</li>
  <li>Kami tidak menerbitkan senarai pemenang, kaunter jackpot, testimoni atau "tip menang".</li>
  <li>Kami tidak menerbitkan prosedur khusus platform sebelum ia disahkan.</li>
</ul>
<h2>Penerbit</h2>
<p>Laman ini diterbitkan oleh ${publisher()}. Untuk sebarang pertanyaan tentang laman ini, e-mel ${mail}.</p>
<p>Baca juga [[/dasar-editorial/|cara kami menulis dan menyemak artikel]] dan [[/penulis/|profil penulis]].</p>`,
  },
  {
    path: '/hubungi-kami/', nav: 'Hubungi Kami', h1: 'Hubungi Kami', updated: U,
    title: 'Hubungi Kami — EU9 Slots Malaysia',
    desc: 'Hubungi EU9 Slots Malaysia melalui e-mel untuk pembetulan, cadangan topik atau pertanyaan tentang laman panduan ini.',
    body: () => `
<p>E-mel: ${mail}</p>
<p>Gunakan alamat ini untuk:</p>
<ul>
  <li>Melaporkan kesilapan fakta atau pautan rosak dalam artikel.</li>
  <li>Mencadangkan topik panduan baharu.</li>
  <li>Pertanyaan tentang [[/dasar-privasi/|privasi]] atau [[/pendedahan-afiliasi/|hubungan laman ini dengan EU9]].</li>
</ul>
<aside class="note">
  <p><strong>Penting:</strong> alamat ini ialah alamat laman panduan EU9 Slots Malaysia, bukan saluran sokongan pengendali EU9. Kami tidak boleh mengakses akaun, menyemak transaksi, memproses deposit atau pengeluaran, atau menetapkan semula kata laluan. Untuk masalah akaun, gunakan saluran sokongan yang dipaparkan dalam platform EU9 sendiri.</p>
</aside>
<h2>Jangan hantar maklumat sensitif</h2>
<p>Jangan sekali-kali menghantar kata laluan, kod OTP, gambar kad pengenalan, butiran kad bank atau tangkapan skrin yang memaparkan maklumat tersebut kepada kami. Kami tidak akan memintanya. Jika seseorang mendakwa mewakili laman ini dan meminta maklumat itu, ia adalah penipuan — baca [[27|cara mengenal mesej phishing]].</p>
<h2>Masa jawapan</h2>
<p>Kami membaca setiap e-mel tetapi tidak menjanjikan tempoh jawapan tertentu. Pembetulan fakta diberi keutamaan.</p>`,
  },
  {
    path: '/dasar-editorial/', nav: 'Dasar Editorial', h1: 'Dasar Editorial', updated: U,
    title: 'Dasar Editorial — EU9 Slots Malaysia',
    desc: 'Cara EU9 Slots Malaysia menulis, menyemak, menyumber dan membetulkan artikel, termasuk peraturan untuk maklumat khusus platform.',
    body: () => `
<p>Dasar ini menerangkan cara artikel di EU9 Slots Malaysia ditulis, disemak dan dikemas kini.</p>
<h2>Prinsip</h2>
<ol>
  <li><strong>Jawab soalan dahulu.</strong> Setiap artikel ada satu soalan utama, dan jawapannya diberi di bahagian awal.</li>
  <li><strong>Hanya fakta yang disahkan.</strong> Kami tidak menerbitkan nama pengendali, lesen, pensijilan, jumlah bonus, kaedah pembayaran, masa pemprosesan, senarai pembekal atau saluran sokongan melainkan ia telah disahkan daripada sumber yang boleh dipercayai.</li>
  <li><strong>Umum berbanding khusus platform.</strong> Konsep umum (RTP, volatiliti, cara mengira syarat cuci) boleh diterangkan secara pendidikan. Prosedur khusus platform (cara deposit, status pengeluaran, langkah pemulihan akaun) kekal sebagai draf yang tidak diterbitkan sehingga disahkan, sebaik-baiknya dengan tangkapan skrin sebenar.</li>
  <li><strong>Contoh dilabel.</strong> Semua contoh dalam RM ialah ilustrasi hipotetikal dan dilabel sedemikian. Ia bukan ramalan hasil.</li>
  <li><strong>Tiada janji kemenangan.</strong> Kami tidak menerbitkan strategi "pasti menang", ramalan, atau dakwaan promosi seperti "paling pantas" tanpa bukti.</li>
  <li><strong>Sumber dinyatakan.</strong> Setiap artikel menyenaraikan rujukan. Bagi peraturan permainan, rujukan utama ialah skrin maklumat dalam permainan berkenaan kerana ia boleh berbeza mengikut versi.</li>
</ol>
<h2>Penulisan dan semakan</h2>
<p>Artikel diterbitkan di bawah nama ${config.author.name}. Draf boleh disediakan dengan bantuan alat penulisan, termasuk AI. Setiap artikel mesti disemak oleh editor manusia untuk ketepatan fakta, pengiraan dan bahasa sebelum diterbitkan.${config.reviewer ? ` Penyemak semasa: ${config.reviewer.name}.` : ''}</p>
<h2>Pautan dan hubungan komersial</h2>
${REL().full}
<h2>Pembetulan dan kemas kini</h2>
<p>Jika anda menjumpai kesilapan, e-mel ${mail}. Pembetulan fakta dibuat secepat mungkin, dan tarikh "Dikemas kini" pada artikel diubah apabila kandungan berubah dengan bermakna — bukan untuk pembetulan ejaan kecil.</p>
<h2>Gambar</h2>
<p>Grafik di laman ini ialah ilustrasi abstrak asal. Kami tidak menerbitkan tangkapan skrin palsu atau imitasi antara muka platform. Tangkapan skrin sebenar hanya digunakan dalam tutorial yang telah disahkan.</p>`,
  },
  {
    path: '/penulis/', nav: 'Profil Penulis', h1: 'Profil Penulis', updated: U,
    title: 'Profil Penulis — EU9 Slots Malaysia',
    desc: 'Siapa yang menulis dan menyemak artikel di EU9 Slots Malaysia, dan cara artikel disediakan.',
    body: () => `
<h2>${config.author.name}</h2>
<p>Semua artikel di laman ini diterbitkan di bawah nama ${config.author.name}, iaitu pasukan yang menulis dan menyelenggara kandungan untuk ${publisher()}.</p>
<p>Kami tidak menyenaraikan kelayakan, pengalaman atau ujian produk yang belum dapat disahkan. Profil individu penulis dan penyemak akan ditambah di halaman ini apabila butiran mereka disahkan untuk diterbitkan.</p>
<h2>Cara artikel disediakan</h2>
<ul>
  <li>Konsep umum diterangkan berdasarkan sumber yang disenaraikan dalam setiap artikel.</li>
  <li>Pengiraan contoh disemak semula dan dilabel sebagai hipotetikal.</li>
  <li>Maklumat khusus platform hanya diterbitkan selepas disahkan.</li>
</ul>
<p>Butiran penuh: [[/dasar-editorial/|dasar editorial]]. Pertanyaan: ${mail}.</p>`,
  },
  {
    path: '/dasar-privasi/', nav: 'Dasar Privasi', h1: 'Dasar Privasi', updated: U,
    title: 'Dasar Privasi — EU9 Slots Malaysia',
    desc: 'Dasar privasi EU9 Slots Malaysia: data yang dikumpul, kuki, e-mel yang anda hantar dan hak anda.',
    body: () => `
<p>Dasar ini menerangkan cara ${publisher()} mengendalikan maklumat apabila anda menggunakan eu9slots.com.</p>
<h2>Maklumat yang kami kumpul</h2>
<ul>
  <li><strong>Tiada akaun, tiada borang.</strong> Laman ini tidak mempunyai log masuk, pendaftaran, borang hubungan atau langganan surat berita.</li>
  <li><strong>Tiada analitik atau iklan pihak ketiga.</strong> Laman ini tidak memuatkan skrip penjejakan, piksel iklan atau kuki pengiklanan.</li>
  <li><strong>Log pelayan.</strong> Penyedia hos laman ini mungkin merekod data teknikal standard seperti alamat IP, jenis pelayar dan halaman yang diminta untuk tujuan keselamatan dan operasi.</li>
  <li><strong>E-mel.</strong> Jika anda menghantar e-mel kepada ${mail}, kami menerima alamat e-mel dan kandungan mesej anda, dan menggunakannya hanya untuk membalas.</li>
</ul>
<h2>Kuki</h2>
<p>Laman ini tidak menetapkan kuki. Jika keadaan ini berubah, dasar ini akan dikemas kini sebelum perubahan berlaku.</p>
<h2>Maklumat akaun EU9</h2>
<p>Kami tidak menerima atau menyimpan maklumat akaun EU9 anda. Jangan hantar kata laluan, OTP, dokumen pengenalan atau butiran bank kepada kami. Pengendalian data akaun permainan anda tertakluk kepada dasar privasi pengendali platform.</p>
<h2>Hak anda</h2>
<p>Anda boleh meminta salinan atau pemadaman e-mel yang pernah anda hantar kepada kami dengan menulis ke ${mail}. Maklumat tentang Akta Perlindungan Data Peribadi 2010 boleh didapati di laman <a href="https://www.pdp.gov.my/" rel="noopener">Jabatan Perlindungan Data Peribadi</a>.</p>
<h2>Pautan luar</h2>
<p>Artikel kami memaut ke laman luar sebagai rujukan. Laman tersebut mempunyai dasar privasi sendiri.</p>${config.cta ? `
<p>Butang "Ke ${config.cta.brand}" ialah pautan rujukan yang melalui perkhidmatan ubah hala pihak ketiga sebelum tiba di ${config.cta.host}. Perkhidmatan tersebut dan ${config.cta.brand} mungkin merekod klik dan kod rujukan.</p>` : ''}`,
  },
  {
    path: '/terma-penggunaan/', nav: 'Terma Penggunaan', h1: 'Terma Penggunaan', updated: U,
    title: 'Terma Penggunaan — EU9 Slots Malaysia',
    desc: 'Terma penggunaan EU9 Slots Malaysia: sifat maklumat, had tanggungjawab, umur pembaca dan hak harta intelek.',
    body: () => `
<p>Dengan menggunakan eu9slots.com, anda bersetuju dengan terma berikut.</p>
<h2>Maklumat pendidikan sahaja</h2>
<p>Kandungan laman ini ialah maklumat umum dan pendidikan. Ia bukan nasihat kewangan atau undang-undang, dan bukan jaminan tentang hasil permainan, ketersediaan bonus atau masa transaksi. Terma rasmi platform, skrin maklumat permainan dan saluran sokongan pengendali sentiasa mengatasi penerangan kami.</p>
<h2>Umur dan undang-undang</h2>
<p>Laman ini untuk pembaca dewasa sahaja (18 tahun ke atas, atau umur minimum yang ditetapkan oleh undang-undang di tempat anda, yang mana lebih tinggi). Undang-undang berkaitan perjudian berbeza mengikut negara dan boleh mengehadkan atau melarang perjudian dalam talian. Anda bertanggungjawab memastikan aktiviti anda mematuhi undang-undang yang terpakai kepada anda.</p>
<h2>Ketepatan</h2>
<p>Kami berusaha memastikan maklumat tepat pada tarikh kemas kini yang dinyatakan, tetapi peraturan permainan, RTP dan terma promosi boleh berubah tanpa notis. Laporkan kesilapan kepada ${mail}.</p>
<h2>Had tanggungjawab</h2>
<p>Setakat yang dibenarkan oleh undang-undang, ${publisher()} tidak bertanggungjawab atas kerugian yang timbul daripada penggunaan maklumat di laman ini atau daripada tindakan pihak ketiga, termasuk pengendali platform.</p>
<h2>Harta intelek</h2>
<p>Teks dan grafik asal di laman ini ialah milik penerbit. Nama EU9 serta nama permainan dan pembekal ialah milik pemilik masing-masing dan digunakan untuk tujuan pengenalan sahaja.</p>
<h2>Perubahan</h2>
<p>Terma ini boleh dikemas kini. Tarikh di atas menunjukkan versi semasa.</p>`,
  },
  {
    path: '/permainan-bertanggungjawab/', nav: 'Permainan Bertanggungjawab', h1: 'Permainan Bertanggungjawab', updated: U,
    title: 'Permainan Bertanggungjawab — EU9 Slots Malaysia',
    desc: 'Cara bermain secara bertanggungjawab: tetapkan bajet dan had masa, kenali tanda amaran, dan di mana mendapatkan bantuan di Malaysia.',
    body: () => `
<div class="answer"><p><strong>Ringkasnya:</strong> anggap wang yang digunakan untuk bermain sebagai kos hiburan yang mungkin hilang sepenuhnya. Tetapkan had wang dan masa sebelum bermula, jangan cuba mengejar kerugian, dan dapatkan bantuan awal jika permainan mula menjejaskan wang, kerja atau hubungan anda.</p></div>
<h2>Fakta asas</h2>
<ul>
  <li>Slot direka supaya, dalam jangka panjang, pemain secara purata menerima kembali kurang daripada jumlah yang dipertaruhkan. Baca [[15|penerangan kelebihan rumah]].</li>
  <li>Setiap pusingan adalah bebas; keputusan lalu tidak meramal pusingan seterusnya. Baca [[14|mengapa corak lalu tidak membantu]].</li>
  <li>Bonus datang dengan syarat yang perlu dipenuhi sebelum pengeluaran. Baca [[16|cara membaca terma bonus]].</li>
</ul>
<h2>Langkah praktikal</h2>
<ol>
  <li>Tetapkan bajet bulanan daripada wang lebihan selepas bil dan simpanan — bukan wang pinjaman.</li>
  <li>Tetapkan had masa setiap sesi dan gunakan pemasa telefon.</li>
  <li>Jangan bermain ketika tertekan, marah, mabuk atau letih.</li>
  <li>Jika platform menyediakan alat had deposit, rehat atau pengecualian diri, gunakannya. Jika tidak, gunakan kaedah dalam [[29|panduan menetapkan had wang dan masa]].</li>
</ol>
<h2>Tanda amaran</h2>
<ul>
  <li>Bermain lebih lama atau dengan lebih banyak wang daripada yang dirancang.</li>
  <li>Meminjam, menjual barang atau menggunakan wang bil untuk bermain.</li>
  <li>Cuba mendapatkan semula kerugian dengan bermain lagi.</li>
  <li>Menyembunyikan aktiviti bermain daripada keluarga.</li>
  <li>Rasa cemas, murung atau mudah marah apabila tidak bermain.</li>
</ul>
<h2>Di mana mendapatkan bantuan</h2>
<ul>
  <li><strong>Befrienders Kuala Lumpur</strong> — sokongan emosi sulit: <a href="tel:+60376272929">03-7627 2929</a> · <a href="https://www.befrienders.org.my/" rel="noopener">befrienders.org.my</a></li>
  <li><strong>Talian Kasih</strong> (KPWKM): <a href="tel:15999">15999</a> · <a href="https://www.kpwkm.gov.my/" rel="noopener">kpwkm.gov.my</a></li>
  <li><strong>Gambling Therapy</strong> — sokongan dalam talian percuma untuk masalah judi: <a href="https://www.gamblingtherapy.org/" rel="noopener">gamblingtherapy.org</a></li>
</ul>
<p>Nombor talian disemak pada ${U}. Sila semak laman rasmi masing-masing untuk maklumat terkini. Dalam kecemasan, hubungi 999.</p>
<h2>Umur dan undang-undang</h2>
<p>Kandungan ini untuk pembaca dewasa sahaja. Undang-undang berkaitan perjudian berbeza mengikut tempat dan boleh mengehadkan perjudian dalam talian; pastikan anda memahami undang-undang yang terpakai kepada anda.</p>`,
  },
  {
    path: '/pendedahan-afiliasi/', nav: 'Pendedahan Afiliasi', h1: config.relationship === 'affiliate' ? 'Pendedahan Afiliasi' : 'Pendedahan Hubungan dan Afiliasi', updated: U,
    title: 'Pendedahan Afiliasi — EU9 Slots Malaysia',
    desc: 'Hubungan antara EU9 Slots Malaysia dengan jenama EU9, dan cara pautan atau komisen (jika ada) dikendalikan.',
    body: () => `
${REL().full}
${CTA_DISCLOSURE && config.relationship !== 'unconfirmed' ? `<p>${CTA_DISCLOSURE}</p>` : ''}
<h2>Cara ini mempengaruhi kandungan</h2>
<ul>
  <li>Fakta dalam artikel tidak diubah untuk tujuan komersial.</li>
  <li>Kami tidak menerbitkan jumlah bonus, kaedah pembayaran atau masa pemprosesan yang belum disahkan.</li>
  <li>Sebarang butang atau pautan ke platform dilabel dengan jelas sebagai menuju ke laman luar.</li>
</ul>
<p>Soalan tentang pendedahan ini: ${mail}.</p>`,
  },
];

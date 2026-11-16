"""Blog hub intro + policy pages, written in the MAIN (local) language = LANGS[0] (Bahasa Melayu).
If a site's main language changes, translate this file. Tokens: __BRAND__ __SLUG__ __SITE_URL__ __EMAIL_LINE__
Policy body = list of (heading, html). Each policy should link to at least one pillar guide or home section.
"""

BLOG_HUB = {
    "kicker": "Panduan",
    "h1": "Panduan & tip __BRAND__",
    "p": "Panduan langkah demi langkah untuk pemain __BRAND__ di Malaysia, disusun mengikut topik: mula bermain, deposit dan bonus, serta permainan dan pertaruhan. Mulakan dengan panduan utama setiap topik.",
    "title": "Panduan __BRAND__ Malaysia: Daftar, Deposit & Bonus",
    "desc": "Panduan __BRAND__ untuk pemain Malaysia mengikut topik: cara daftar, aplikasi, deposit dan pengeluaran, bonus, kasino langsung dan odds sukan.",
}

POLICIES = [
    {"slug": "about", "title": "Tentang Kami",
     "desc": "Tentang laman __BRAND__ Malaysia ini: apa yang diliputi, cara menggunakannya, dan di mana pendaftaran serta permainan sebenarnya berlaku.",
     "body": [
         ("Apa laman ini", "<p>Laman ini memperkenalkan __BRAND__ kepada pemain di Malaysia: permainan yang ditawarkan, cara mendaftar, promosi dan aplikasi mudah alih. Pendaftaran dan permainan berlaku di platform rasmi __BRAND__.</p>"),
         ("Panduan kami", "<p><a href=\"/blog/\">Panduan</a> kami menerangkan pendaftaran, pembayaran, bonus dan setiap jenis permainan dalam bahasa mudah. Mula dengan <a href=\"/blog/panduan-__SLUG__-malaysia/\">panduan untuk pemain baharu</a>. Terma boleh berubah, jadi sentiasa semak laman rasmi sebelum deposit.</p>"),
         ("Hubungi", "<p>__EMAIL_LINE__</p>"),
     ]},
    {"slug": "responsible-gaming", "title": "Permainan Bertanggungjawab",
     "desc": "Permainan bertanggungjawab: tetapkan had, kenali tanda amaran dan dapatkan bantuan di Malaysia melalui Talian Kasih 15999.",
     "body": [
         ("Bermain untuk hiburan, bukan wang", "<p>Perjudian ialah hiburan yang ada kosnya. Rumah sentiasa mempunyai kelebihan, jadi jangan anggap ia cara membuat wang. Hanya untuk dewasa 18 tahun ke atas.</p>"),
         ("Tetapkan had sebelum bermain", "<ul><li>Tentukan bajet yang anda mampu kehilangan.</li><li>Tetapkan had masa dan berehat.</li><li>Jangan pinjam wang atau guna wang bil.</li><li>Jangan kejar kerugian.</li></ul><p>Jika menggunakan bonus, faham dahulu <a href=\"/blog/bonus-__SLUG__/\">syarat turnover</a> supaya anda tidak bermain lebih daripada yang dirancang.</p>"),
         ("Tanda amaran", "<ul><li>Menghabiskan lebih masa atau wang daripada yang dirancang.</li><li>Menyembunyikan permainan daripada keluarga.</li><li>Rasa cemas apabila tidak bermain.</li><li>Bermain untuk memenangi semula kerugian.</li></ul>"),
         ("Dapatkan bantuan", "<p>Malaysia: Talian Kasih <b>15999</b> (24 jam), Befrienders KL <b>03-7627 2929</b>, Persatuan Kesihatan Mental Malaysia <b>03-2780 6803</b>. Tanya pasukan sokongan pengendali tentang had deposit, rehat sementara dan pengecualian diri.</p>"),
     ]},
    {"slug": "privacy-policy", "title": "Dasar Privasi",
     "desc": "Cara laman ini mengendalikan data anda: tiada akaun atau borang, analitik asas sahaja, dan pautan ke dasar privasi pengendali sendiri.",
     "body": [
         ("Apa yang kami kumpul", "<p>Laman ini tiada akaun atau borang. Hos dan alat analitik kami menerima data teknikal standard (lokasi anggaran, jenis peranti, halaman dilihat) untuk memastikan laman berfungsi dan mengukur trafik.</p>"),
         ("Kuki", "<p>Analitik mungkin menetapkan kuki. Anda boleh menyekat atau memadamnya dalam pelayar; laman masih berfungsi.</p>"),
         ("Data pendaftaran", "<p>Apabila anda mendaftar atau deposit, ia berlaku di platform __BRAND__ di bawah dasar privasinya sendiri — lihat <a href=\"/blog/cara-daftar-__SLUG__/\">cara daftar dengan selamat</a>. Jangan kongsi kata laluan, OTP atau TAC dengan sesiapa.</p>"),
         ("Hubungi", "<p>__EMAIL_LINE__</p>"),
     ]},
    {"slug": "terms", "title": "Terma Penggunaan",
     "desc": "Terma penggunaan laman ini: maklumat sahaja, 18+, undang-undang tempatan, pautan afiliasi, terma bonus dan tanda dagangan.",
     "body": [
         ("Maklumat sahaja", "<p>Kandungan laman ini ialah maklumat umum, bukan nasihat undang-undang atau kewangan. Permainan, promosi dan kaedah pembayaran ditetapkan oleh pengendali dan boleh berubah pada bila-bila masa.</p>"),
         ("Umur dan undang-undang tempatan", "<p>Anda mesti berumur 18 tahun ke atas. Perjudian dalam talian dihadkan di sesetengah bidang kuasa, termasuk Malaysia; anda bertanggungjawab mematuhi undang-undang di tempat anda.</p>"),
         ("Pautan dan bonus", "<p>Sesetengah pautan ialah pautan afiliasi, dan kami mungkin menerima komisen tanpa kos tambahan kepada anda. Setiap bonus tertakluk kepada syarat taruhan dan terma pengendali — lihat <a href=\"/blog/bonus-__SLUG__/\">panduan bonus</a>.</p>"),
         ("Tanda dagangan", "<p>Nama permainan dan penyedia adalah milik pemilik masing-masing.</p>"),
     ]},
]

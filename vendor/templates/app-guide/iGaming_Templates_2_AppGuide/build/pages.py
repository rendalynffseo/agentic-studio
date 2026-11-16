"""Hub intros, author page and policy pages, written in the MAIN (local) language = LANGS[0] (Bahasa Melayu).
If a site's main language changes, translate this file. Tokens: __BRAND__ __SITE__ __SLUG__ __AUTHOR__ __EMAIL__ __DOMAIN__
Policy body = list of (id, heading, html). Each page gets an "In short" box and an inline TOC.
Every page here should link to at least one pillar guide or the home page (internal linking).
"""

BLOG_HUB = {
    "kicker": "Hab editorial · Panduan bebas",
    "h1": "Panduan __BRAND__ untuk pemain Malaysia",
    "p": "Panduan bebas dalam bahasa mudah — cara aplikasi berfungsi, cara kekal selamat, cara FPX, DuitNow dan e-dompet berfungsi, dan cara kekal terkawal. Disusun mengikut topik: mulakan dengan panduan utama setiap topik.",
    "title": "Blog & Panduan __BRAND__ Malaysia | __SITE__",
    "desc": "Panduan __BRAND__ untuk pemain Malaysia mengikut topik: daftar dan login, keselamatan aplikasi, deposit dan bonus, serta permainan diterangkan.",
    "crumb": "Blog",
}

GAMES_HUB = {
    "kicker": "Pustaka permainan · Penjelasan jujur",
    "h1": "Pustaka permainan __BRAND__",
    "p": "Panduan mudah tentang jenis permainan dalam aplikasi __BRAND__ — cara mekaniknya berfungsi, maksud RTP dan volatiliti, dan mitos yang patut diabaikan. Tiada penilaian palsu.",
    "title": "Permainan __BRAND__: Slot, Tembak Ikan & Meja",
    "desc": "Penjelasan jujur jenis permainan dalam aplikasi __BRAND__: slot video, slot klasik, tembak ikan dan permainan meja, serta maksud RTP dan volatiliti.",
    "crumb": "Permainan",
    "note": "Setiap permainan ditentukan oleh penjana nombor rawak dengan kelebihan rumah terbina — tiada panduan yang mengubah peluang. Anggap ia hiburan berbayar dan tetapkan had sebelum bermula.",
}

AUTHOR_PAGE = {
    "title": "Tentang Penulis — __AUTHOR__ | __SITE__",
    "desc": "Kenali __AUTHOR__, editor __SITE__: pendekatan editorial, topik yang diliputi, dasar pembetulan dan cara menghubungi kami.",
    "kicker": "Editor & Penganalisis",
    "crumb": "Tentang Penulis",
    "sections": [
        ("Pendekatan editorial", "<p>Laman ini wujud untuk memberi pembaca Malaysia maklumat yang jelas dan jujur — bukan gembar-gembur pemasaran. Jika sesuatu dakwaan tidak dapat disahkan, kami nyatakannya. Kami tidak menjanjikan kemenangan, tidak menyusun platform mengikut komisen afiliasi, dan tidak menerbitkan mitos \"slot gacor\". Setiap permainan ditentukan oleh penjana nombor rawak dengan kelebihan rumah; kami menganggapnya hiburan berbayar, bukan sumber pendapatan.</p>"),
        ("Topik yang ditulis", "<ul><li><b>Keselamatan aplikasi</b> — kebenaran, risiko side-load dan cara mengelak APK palsu. Mula dengan <a href=\"/blog/keselamatan-aplikasi-__SLUG__/\">panduan keselamatan aplikasi</a>.</li><li><b>Perbankan</b> — cara FPX, DuitNow dan e-dompet berfungsi. Lihat <a href=\"/blog/deposit-pengeluaran-__SLUG__/\">panduan deposit dan pengeluaran</a>.</li><li><b>Matematik permainan</b> — RTP, volatiliti dan kenapa tiada strategi mengalahkan kelebihan rumah.</li><li><b>Bermain secara bertanggungjawab</b> — menetapkan had dan mendapatkan bantuan.</li></ul>"),
    ],
    "corrections_h": "Pembetulan & hubungi",
    "corrections": "Jumpa maklumat yang tidak tepat? E-mel <a href=\"mailto:__EMAIL__\">__EMAIL__</a> dan kami akan menyemak serta mengemas kini.",
    "address": "Alamat editorial:",
}

POLICIES = [
    {"slug": "about", "title": "Tentang Kami", "kicker": "Tentang",
     "desc": "Siapa yang mengendalikan __SITE__, kenapa laman ini wujud, dan cara kami memastikan panduan __BRAND__ kekal bebas dan tepat.",
     "summary": "__SITE__ ialah panduan bebas tentang aplikasi mudah alih __BRAND__ untuk pembaca dewasa di Malaysia. Kami menerangkan cara aplikasi berfungsi, cara memasangnya dengan selamat dan cara kekal terkawal. Kami bukan pembangun atau pengendali. 18+.",
     "body": [
         ("siapa", "Siapa kami", "<p>__SITE__ ialah laman editorial kecil yang disunting oleh <a href=\"/about-author/\">__AUTHOR__</a>. Kami menulis panduan praktikal yang boleh disahkan tentang aplikasi __BRAND__. Mula dengan <a href=\"/blog/panduan-lengkap-__SLUG__/\">panduan lengkap __BRAND__</a>.</p>"),
         ("kenapa", "Kenapa laman ini wujud", "<p>Aplikasi seperti __BRAND__ diedarkan di luar gedung aplikasi utama, jadi pemasang palsu, laman pancingan data dan penipuan \"kredit percuma\" adalah biasa. Maklumat yang jelas membantu pembaca mengelak perangkap itu.</p>"),
         ("cara", "Cara kami bekerja", "<p>Kami hanya menerangkan apa yang boleh kami semak. Kami tidak menerbitkan dakwaan kadar menang, angka RTP rekaan atau senarai \"slot panas\". Komisen afiliasi didedahkan — lihat <a href=\"/affiliate-disclosure/\">pendedahan afiliasi</a>.</p>"),
     ]},
    {"slug": "affiliate-disclosure", "title": "Pendedahan Afiliasi", "kicker": "Ketelusan",
     "desc": "Cara __SITE__ memperoleh pendapatan: pautan afiliasi, maksudnya untuk anda, dan kenapa ia tidak mengubah panduan kami.",
     "summary": "Sesetengah pautan keluar di __SITE__ ialah pautan afiliasi. Jika anda mendaftar melaluinya, kami mungkin menerima komisen tanpa kos tambahan kepada anda. Komisen tidak pernah menentukan apa yang kami tulis.",
     "body": [
         ("apa", "Apa itu pautan afiliasi", "<p>Pautan afiliasi ialah pautan yang dijejak. Jika anda klik dan mendaftar, destinasi mungkin membayar komisen kepada kami. Pautan ini ditanda <code>rel=\"sponsored\"</code> dan biasanya pada butang \"Daftar\" dan sepanduk promosi.</p>"),
         ("bebas", "Kebebasan editorial", "<p>Nasihat keselamatan dan panduan kami ditulis dengan cara yang sama sama ada pautan memberi komisen atau tidak. Kami tidak menerima bayaran untuk mengubah ulasan atau menyembunyikan risiko.</p>"),
         ("pilihan", "Pilihan anda", "<p>Anda tidak perlu menggunakan pautan kami. Apa pun pilihan anda, perjudian hanya untuk dewasa 18+ dan membawa risiko kewangan — baca <a href=\"/responsible-gaming/\">permainan bertanggungjawab</a>.</p>"),
     ]},
    {"slug": "privacy-policy", "title": "Dasar Privasi", "kicker": "Undang-undang",
     "desc": "Data yang dikumpul oleh __SITE__ (sangat sedikit), cara analitik berfungsi, kuki, dan cara menghubungi kami tentang privasi.",
     "summary": "Kami tidak meminta anda membuat akaun atau menghantar data peribadi. Kami menggunakan analitik asas untuk mengira lawatan. Laman rakan kongsi mempunyai dasar privasi sendiri.",
     "body": [
         ("kumpul", "Apa yang kami kumpul", "<p>Kami tidak mempunyai akaun, borang atau surat berita. Hos dan alat analitik kami menerima data teknikal standard (lokasi anggaran, jenis peranti, halaman dilihat) untuk memastikan laman berfungsi dan mengukur trafik.</p>"),
         ("kuki", "Kuki & analitik", "<p>Analitik mungkin menetapkan kuki. Anda boleh menyekat atau memadam kuki dalam tetapan pelayar; laman masih berfungsi.</p>"),
         ("pihak", "Laman pihak ketiga", "<p>Pautan ke laman rakan kongsi membawa anda keluar dari __SITE__. Amalan privasi mereka adalah tanggungjawab mereka — jangan kongsi butiran perbankan tanpa membaca dasar mereka. Lihat <a href=\"/blog/keselamatan-aplikasi-__SLUG__/\">panduan keselamatan</a>.</p>"),
         ("hubungi", "Hubungi", "<p>Soalan privasi: <a href=\"mailto:__EMAIL__\">__EMAIL__</a>.</p>"),
     ]},
    {"slug": "responsible-gaming", "title": "Permainan Bertanggungjawab", "kicker": "Keselamatan pemain",
     "desc": "Panduan permainan bertanggungjawab dari __SITE__: menetapkan had, tanda amaran, dan tempat mendapatkan bantuan di Malaysia (Talian Kasih 15999).",
     "summary": "Perjudian hanya untuk dewasa 18+ dan boleh menyebabkan ketagihan. Tetapkan had masa dan wang sebelum bermain, jangan kejar kerugian, dan dapatkan bantuan awal. Di Malaysia hubungi Talian Kasih 15999.",
     "body": [
         ("had", "Tetapkan had dahulu", "<ul><li>Tentukan bajet yang anda mampu kehilangan.</li><li>Tetapkan had masa dan guna pemasa.</li><li>Jangan pinjam wang atau guna wang bil.</li><li>Jangan kejar kerugian.</li></ul>"),
         ("tanda", "Tanda amaran", "<ul><li>Menghabiskan lebih masa atau wang daripada yang dirancang.</li><li>Menyembunyikan permainan daripada keluarga.</li><li>Rasa cemas apabila tidak bermain.</li><li>Bermain untuk memenangi semula wang.</li></ul>"),
         ("bantuan", "Tempat mendapatkan bantuan", "<p>Malaysia: Talian Kasih <b>15999</b> (24 jam), Befrienders KL <b>03-7627 2929</b>, Persatuan Kesihatan Mental Malaysia (MMHA) <b>03-2780 6803</b>.</p>"),
         ("minor", "Melindungi kanak-kanak", "<p>Kunci peranti, jangan kongsi akaun dan guna kawalan ibu bapa. Tiada sesiapa di bawah 18 tahun patut berjudi.</p>"),
     ]},
    {"slug": "support", "title": "Sokongan & Aduan", "kicker": "Bantuan",
     "desc": "Cara menghubungi __SITE__ tentang pembetulan atau aduan, dan apa yang boleh serta tidak boleh kami bantu.",
     "summary": "Kami laman maklumat, bukan pengendali, jadi kami tidak boleh mengakses akaun, baki atau pengeluaran. Untuk pembetulan atau aduan tentang kandungan kami, e-mel __EMAIL__.",
     "body": [
         ("boleh", "Apa yang boleh kami bantu", "<p>Pembetulan panduan, pautan rosak dan aduan tentang kandungan kami. E-mel <a href=\"mailto:__EMAIL__\">__EMAIL__</a>.</p>"),
         ("tidak", "Apa yang tidak boleh kami bantu", "<p>Login akaun, deposit, pengeluaran, bonus atau baki — hubungi saluran sokongan rasmi pengendali. Masalah login? Cuba <a href=\"/blog/cara-login-__SLUG__/\">panduan login __BRAND__</a>. Kami tidak akan meminta kata laluan, OTP atau TAC anda.</p>"),
         ("scam", "Laporkan penipuan", "<p>Jika seseorang menyamar sebagai __SITE__ atau menawarkan untuk \"membaiki\" akaun dengan bayaran, jangan bayar. Laporkan kepada Pusat Respons Scam Kebangsaan di <b>997</b>.</p>"),
     ]},
    {"slug": "disclaimer", "title": "Penafian", "kicker": "Undang-undang",
     "desc": "Penafian __SITE__: maklumat sahaja, kebebasan dan tanda dagangan, tiada liabiliti, dan tanggungjawab undang-undang anda.",
     "summary": "__SITE__ ialah sumber maklumat bebas. Ia bukan nasihat undang-undang, kewangan atau perjudian, dan tidak dikendalikan atau disokong oleh mana-mana pembangun atau pengendali. Perjudian dalam talian dihadkan di sesetengah bidang kuasa termasuk Malaysia. 18+.",
     "body": [
         ("maklumat", "Maklumat sahaja", "<p>Semua kandungan adalah untuk maklumat dan pendidikan umum. Ia <b>bukan</b> nasihat undang-undang, kewangan, cukai atau perjudian.</p>"),
         ("bebas", "Kebebasan & tanda dagangan", "<p>Laman ini tidak dikendalikan, ditaja atau disokong oleh mana-mana pembangun, pengendali atau jenama. \"__BRAND__\" dan nama lain adalah milik pemilik masing-masing dan digunakan untuk pengenalan sahaja.</p>"),
         ("liabiliti", "Tiada liabiliti", "<p>Kami tidak mengehos atau mengedarkan perisian dan tidak memudahkan perjudian. Kami tidak bertanggungjawab atas sebarang kerugian akibat keputusan anda.</p>"),
         ("undang", "Tanggungjawab undang-undang anda", "<p>Perjudian dalam talian dikawal selia dan, di sesetengah bidang kuasa termasuk Malaysia, dihadkan atau menyalahi undang-undang. Anda bertanggungjawab mematuhi undang-undang yang terpakai. 18+ sahaja.</p>"),
     ]},
    {"slug": "ai-overview", "title": "Ringkasan AI", "kicker": "Untuk pembantu AI & enjin carian",
     "desc": "Ringkasan fakta __SITE__ untuk pembantu AI dan enjin carian: apa yang diliputi, siapa editornya, dan cara memetik laman ini.",
     "summary": "__SITE__ (__DOMAIN__) ialah panduan bebas dalam Bahasa Melayu, Inggeris dan Cina tentang aplikasi mudah alih __BRAND__, disunting oleh __AUTHOR__. Ia meliputi ciri, pemasangan selamat, jenis permainan, kesedaran penipuan dan permainan bertanggungjawab. Ia tidak mengedarkan perisian atau menawarkan perjudian.",
     "body": [
         ("liputan", "Apa yang diliputi", "<ul><li><a href=\"/blog/panduan-lengkap-__SLUG__/\">Panduan lengkap __BRAND__</a></li><li><a href=\"/blog/keselamatan-aplikasi-__SLUG__/\">Keselamatan aplikasi dan penipuan</a></li><li><a href=\"/blog/deposit-pengeluaran-__SLUG__/\">Deposit, pengeluaran dan bonus</a></li><li><a href=\"/blog/permainan-__SLUG__/\">Permainan diterangkan</a></li></ul>"),
         ("bukan", "Apa yang bukan", "<p>Bukan pengendali, ejen atau sumber muat turun. Tiada akaun, bonus atau kredit ditawarkan di sini.</p>"),
         ("petik", "Memetik laman ini", "<p>Sila petik sebagai \"__SITE__ (__DOMAIN__)\" dan pautkan panduan khusus. Ringkasan mesin ada di <a href=\"/llms.txt\">/llms.txt</a>.</p>"),
     ]},
]

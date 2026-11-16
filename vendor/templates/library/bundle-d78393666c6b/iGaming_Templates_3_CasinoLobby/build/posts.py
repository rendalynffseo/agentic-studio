"""Blog = topical authority. Posts are grouped in CLUSTERS; each cluster has ONE pillar post + supporting posts.

Per site, build the clusters from the user's keyword list (see CLAUDE.md): main keyword topic -> pillar,
long-tail keywords -> supporting posts. Write in the main (local) language first.

CLUSTERS: key -> {"name": {lang: label}, "pillar": slug}. Order = order on /blog/, home and footer.
Post fields: slug, lang, cluster, kw (list: first = focus keyword), card (label), title (<= ~50 chars; " | BRAND Malaysia"
is appended to <title>), desc (70-160 chars), intro, sections = [(h2, [blocks])].
Blocks: blank-line separated paragraphs; "- " lines = bullets; "1. " lines = numbered.
Internal links: [[target|anchor]], target = post slug, home, home#<section-id>, blog. Unknown target = build error.
Linking rules (build warns if broken): every supporting post links its pillar inline; every pillar links each of its
supporting posts inline; every post links at least one post in ANOTHER cluster and one home section.
Don't invent facts: no minimums, payout times, bonus % or licences unless the brief gives them.
"""

CLUSTERS = {
    "mula": {"name": {"ms": "Mula Bermain", "en": "Getting Started", "zh": "开始游戏"}, "pillar": "panduan-__SLUG__-malaysia"},
    "transaksi": {"name": {"ms": "Deposit, Pengeluaran & Bonus", "en": "Payments & Bonuses", "zh": "存取款与奖金"}, "pillar": "deposit-pengeluaran-__SLUG__"},
    "permainan": {"name": {"ms": "Permainan & Pertaruhan", "en": "Games & Betting", "zh": "游戏与投注"}, "pillar": "permainan-kasino-__SLUG__"},
}

POSTS = [
# ================================================================== cluster: mula
{
 "slug": "panduan-__SLUG__-malaysia", "lang": "ms", "cluster": "mula", "card": "Panduan Utama",
 "kw": ["__BRAND__ Malaysia", "__BRAND__ casino", "panduan __BRAND__"],
 "title": "Panduan __BRAND__ Malaysia untuk Pemain Baharu",
 "desc": "Semua yang perlu diketahui sebelum bermain di __BRAND__: cara daftar, muat turun aplikasi, deposit, bonus dan jenis permainan, dalam satu panduan.",
 "intro": "Panduan ini ialah titik permulaan untuk pemain baharu __BRAND__ di Malaysia. Ia menerangkan langkah dari pendaftaran hingga permainan pertama, dan memautkan panduan terperinci untuk setiap langkah.",
 "sections": [
  ("Langkah 1: Buka akaun", ["Pendaftaran mengambil masa beberapa minit. Ikut [[cara-daftar-__SLUG__|cara daftar __BRAND__ langkah demi langkah]] supaya nama akaun sepadan dengan akaun bank anda — ini memudahkan pengeluaran nanti. Ringkasan empat langkah ada di [[home#register|bahagian Cara Mendaftar]]."]),
  ("Langkah 2: Pasang aplikasi (pilihan)", ["Anda boleh bermain di pelayar atau memasang aplikasi. Baca [[aplikasi-__SLUG__|cara muat turun aplikasi __BRAND__ dengan selamat]] sebelum memasang."]),
  ("Langkah 3: Deposit", ["Pemain Malaysia biasanya menggunakan FPX, DuitNow, e-dompet atau kripto. Semua kaedah diterangkan dalam [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]]."]),
  ("Langkah 4: Pilih permainan", ["Slot, kasino langsung, sukan, memancing dan permainan segera — lihat [[permainan-kasino-__SLUG__|panduan permainan __BRAND__]] untuk memahami setiap kategori."]),
  ("Bermain secara bertanggungjawab", ["Tetapkan bajet sebelum bermain dan jangan kejar kerugian. Bantuan di Malaysia: Talian Kasih 15999."]),
 ],
},
{
 "slug": "cara-daftar-__SLUG__", "lang": "ms", "cluster": "mula", "card": "Daftar",
 "kw": ["cara daftar __BRAND__", "__BRAND__ daftar", "__BRAND__ register"],
 "title": "Cara Daftar __BRAND__ Malaysia (Langkah demi Langkah)",
 "desc": "Cara membuka akaun __BRAND__ dalam beberapa minit: apa yang diperlukan, setiap langkah pendaftaran, dan cara menjaga keselamatan akaun anda.",
 "intro": "Pendaftaran __BRAND__ hanya mengambil masa beberapa minit. Pastikan nama sepadan dengan akaun bank supaya pengeluaran lancar. Panduan ini sebahagian daripada [[panduan-__SLUG__-malaysia|panduan __BRAND__ untuk pemain baharu]].",
 "sections": [
  ("Apa yang diperlukan", ["- Nombor telefon atas nama anda\n- Nama penuh seperti dalam akaun bank\n- Kata laluan kuat yang unik\n- Berumur 18 tahun ke atas"]),
  ("Langkah pendaftaran", ["1. Buka laman rasmi dan tekan Daftar.\n2. Pilih nama pengguna dan kata laluan.\n3. Isi nama penuh, nombor telefon dan e-mel.\n4. Sahkan nombor telefon jika diminta.\n5. Log masuk dan tetapkan had deposit sebelum bermain.",
    "Ringkasan visual ada di [[home#register|Cara Mendaftar di halaman utama]]."]),
  ("Kesilapan biasa", ["Nama yang tidak sepadan dengan akaun bank ialah punca utama pengeluaran tertangguh — lihat [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran]]. Jangan bayar sesiapa untuk membuka akaun, dan jangan kongsi kata laluan atau OTP."]),
 ],
},
{
 "slug": "aplikasi-__SLUG__", "lang": "ms", "cluster": "mula", "card": "Aplikasi",
 "kw": ["__BRAND__ apk", "download __BRAND__", "aplikasi __BRAND__"],
 "title": "Muat Turun Aplikasi __BRAND__ Android & iOS",
 "desc": "Cara muat turun dan pasang aplikasi __BRAND__ di Android dan iOS dengan selamat, dan apa yang perlu dilakukan jika aplikasi tidak dapat dipasang.",
 "intro": "Aplikasi __BRAND__ menggunakan akaun dan dompet yang sama seperti laman web, dengan akses lebih pantas. Ini sebahagian daripada [[panduan-__SLUG__-malaysia|panduan __BRAND__ untuk pemain baharu]].",
 "sections": [
  ("Android", ["1. Tekan Muat Turun Aplikasi di laman rasmi.\n2. Benarkan pelayar memasang fail apabila diminta.\n3. Pasang, buka dan log masuk.\n4. Matikan semula \"pasang aplikasi tidak diketahui\" untuk pelayar anda."]),
  ("iOS", ["Ikut pautan iOS di laman rasmi. Bergantung pada versi, anda mungkin menambah web app ke skrin utama atau memasang profil. Hanya percayai profil dari laman rasmi."]),
  ("Kekal selamat", ["- Muat turun hanya dari laman rasmi, bukan pautan dalam kumpulan sembang\n- Aplikasi kasino tidak memerlukan kebenaran SMS, kenalan atau kebolehcapaian\n- Kekalkan Google Play Protect aktif",
    "Tidak mahu memasang? Laman mudah alih berfungsi di mana-mana pelayar. Kembali ke [[home#app|bahagian aplikasi]] atau terus ke [[permainan-kasino-__SLUG__|panduan permainan]]."]),
 ],
},
# ================================================================== cluster: transaksi
{
 "slug": "deposit-pengeluaran-__SLUG__", "lang": "ms", "cluster": "transaksi", "card": "Panduan Utama",
 "kw": ["__BRAND__ deposit", "__BRAND__ withdraw", "__BRAND__ pengeluaran"],
 "title": "Deposit & Pengeluaran __BRAND__ di Malaysia",
 "desc": "Cara deposit dan keluarkan wang di __BRAND__ melalui FPX, DuitNow, e-dompet atau kripto, kenapa transaksi gagal, dan peraturan keselamatan penting.",
 "intro": "Panduan ringkas kaedah pembayaran untuk pemain Malaysia. Had minimum dan masa pemprosesan semasa dipaparkan di juruwang selepas log masuk.",
 "sections": [
  ("Kaedah deposit", ["- Perbankan dalam talian (FPX)\n- DuitNow\n- E-dompet seperti Touch 'n Go eWallet\n- Pindahan bank\n- Kripto terpilih (cth. USDT)",
    "Senarai kaedah yang disokong juga ada di [[home#payments|halaman utama]]."]),
  ("Cara deposit", ["1. Log masuk di laman rasmi atau aplikasi.\n2. Buka juruwang dan pilih Deposit.\n3. Pilih kaedah dan masukkan jumlah.\n4. Lengkapkan pembayaran dan simpan resit."]),
  ("Pengeluaran", ["Pilih Pengeluaran di juruwang. Wang dihantar ke akaun bank atas nama berdaftar anda — sebab itu [[cara-daftar-__SLUG__|pendaftaran yang betul]] penting. Bonus aktif mesti memenuhi syarat taruhan dahulu: lihat [[bonus-__SLUG__|maksud bonus dan turnover]]."]),
  ("Kenapa transaksi gagal", ["- Sesi bank tamat masa\n- Had pindahan harian bank\n- Nama akaun tidak sepadan\n- Waktu penyelenggaraan",
    "Jika masih gagal, semak [[transaksi-gagal-__SLUG__|cara atasi deposit dan pengeluaran yang gagal]]."]),
  ("Keselamatan", ["Deposit hanya di juruwang selepas log masuk. __BRAND__ tidak akan meminta deposit melalui WhatsApp, Telegram atau akaun peribadi."]),
 ],
},
{
 "slug": "bonus-__SLUG__", "lang": "ms", "cluster": "transaksi", "card": "Bonus",
 "kw": ["__BRAND__ bonus", "__BRAND__ promosi", "turnover __BRAND__"],
 "title": "Bonus __BRAND__: Turnover, Rebat & VIP",
 "desc": "Cara bonus alu-aluan, bonus tambahan, rebat dan ganjaran VIP berfungsi di __BRAND__, dan bagaimana syarat turnover mempengaruhi pengeluaran.",
 "intro": "Bonus menambah nilai, tetapi setiap satu ada syarat. Faham turnover sebelum menuntut. Ini sebahagian daripada [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]].",
 "sections": [
  ("Jenis promosi", ["- Bonus alu-aluan: padanan pada deposit pertama\n- Bonus tambahan: kredit pada deposit berikutnya\n- Rebat tunai: sebahagian turnover layak dipulangkan\n- Ganjaran VIP: faedah mengikut tahap",
    "Tawaran semasa disenaraikan di [[home#promos|Promosi]]. Terma berubah, jadi baca di laman rasmi."]),
  ("Maksud turnover", ["Turnover (syarat taruhan) ialah jumlah yang mesti dipertaruhkan sebelum dana bonus boleh dikeluarkan. Syarat 20x bermakna bertaruh 20 kali jumlah bonus. Sesetengah permainan dikira kurang — contohnya [[kasino-langsung-__SLUG__|meja kasino langsung]] selalunya dikira berbeza daripada slot."]),
  ("Sebelum menuntut", ["- Semak deposit minimum dan bonus maksimum\n- Semak permainan yang dikira\n- Ambil perhatian tarikh luput"]),
 ],
},
{
 "slug": "transaksi-gagal-__SLUG__", "lang": "ms", "cluster": "transaksi", "card": "Masalah Transaksi",
 "kw": ["__BRAND__ deposit gagal", "__BRAND__ withdraw pending", "__BRAND__ pengeluaran lambat"],
 "title": "Deposit atau Pengeluaran __BRAND__ Gagal? Ini Puncanya",
 "desc": "Punca biasa deposit gagal dan pengeluaran tertangguh di __BRAND__, langkah semakan yang selamat, dan bila perlu menghubungi sokongan langsung.",
 "intro": "Kebanyakan transaksi yang gagal ada punca mudah. Senarai semak ini membantu anda mencari puncanya sebelum menghubungi sokongan. Ini sebahagian daripada [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]].",
 "sections": [
  ("Deposit gagal", ["- Sesi bank tamat masa semasa ubah hala FPX — cuba semula\n- Had pindahan harian dicapai\n- Resit tidak dimuat naik (untuk pindahan bank)\n- Bank dalam penyelenggaraan"]),
  ("Pengeluaran tertangguh", ["- Syarat turnover bonus belum dipenuhi — lihat [[bonus-__SLUG__|maksud turnover]]\n- Nama akaun bank tidak sepadan dengan nama berdaftar\n- Pengesahan akaun belum lengkap"]),
  ("Bila hubungi sokongan", ["Jika semua semakan di atas tidak membantu, hubungi sokongan langsung melalui laman rasmi dengan nombor rujukan transaksi. Jangan sekali-kali bayar sesiapa yang menawarkan untuk \"mempercepatkan\" pengeluaran. Soalan lazim lain ada di [[home#faq|Soalan Lazim]], dan sebelum bermain semula, semak [[panduan-__SLUG__-malaysia|panduan pemain baharu]]."]),
 ],
},
# ================================================================== cluster: permainan
{
 "slug": "permainan-kasino-__SLUG__", "lang": "ms", "cluster": "permainan", "card": "Panduan Utama",
 "kw": ["permainan __BRAND__", "slot __BRAND__", "kasino langsung __BRAND__"],
 "title": "Permainan __BRAND__: Slot, Kasino Langsung & Sukan",
 "desc": "Panduan kategori permainan di __BRAND__: slot, kasino langsung, pertaruhan sukan, memancing dan permainan segera, serta cara bermain dengan bajet.",
 "intro": "__BRAND__ menawarkan beberapa kategori permainan dalam satu akaun. Panduan ini menerangkan setiap satu dan memautkan panduan terperinci.",
 "sections": [
  ("Slot", ["Slot video dan klasik daripada studio terkenal, dengan putaran percuma dan pusingan bonus. Setiap keputusan adalah rawak. Lihat tajuk popular di [[home#slots|baris slot]]."]),
  ("Kasino langsung", ["Baccarat, rolet, blackjack dan sic bo dengan peniaga sebenar. Peraturan asas ada dalam [[kasino-langsung-__SLUG__|panduan kasino langsung]]."]),
  ("Pertaruhan sukan", ["Pasaran bola sepak, bola keranjang, e-sukan dan banyak lagi. Belajar membaca odds dalam [[odds-sukan|panduan odds sukan]]."]),
  ("Memancing dan permainan segera", ["Permainan arked memancing dan pusingan pantas seperti crash, plinko dan keno. Rentaknya pantas, jadi tetapkan had yang jelas."]),
  ("Bajet dan bonus", ["Jika menggunakan bonus, setiap kategori mungkin dikira berbeza untuk turnover — baca [[bonus-__SLUG__|panduan bonus]]."]),
 ],
},
{
 "slug": "kasino-langsung-__SLUG__", "lang": "ms", "cluster": "permainan", "card": "Kasino Langsung",
 "kw": ["kasino langsung __BRAND__", "baccarat __BRAND__", "live casino Malaysia"],
 "title": "Kasino Langsung __BRAND__: Baccarat, Rolet & Blackjack",
 "desc": "Cara permainan kasino langsung berfungsi, peraturan asas baccarat, rolet dan blackjack, serta cara mengurus bajet di meja langsung.",
 "intro": "Meja kasino langsung menstrim peniaga sebenar dalam HD, dan anda bertaruh di skrin. Peraturannya sama seperti kasino darat, begitu juga kelebihan rumah. Ini sebahagian daripada [[permainan-kasino-__SLUG__|panduan permainan __BRAND__]].",
 "sections": [
  ("Baccarat", ["Bertaruh pada Player, Banker atau Tie. Tangan paling hampir 9 menang. Corak \"roadmap\" hanya menunjukkan keputusan lepas; ia tidak meramal tangan seterusnya."]),
  ("Rolet", ["Bertaruh pada nombor, warna atau kumpulan nombor. Taruhan luar (merah/hitam) lebih kerap menang tetapi bayaran lebih rendah."]),
  ("Blackjack", ["Kalahkan tangan peniaga tanpa melebihi 21. Strategi asas mengurangkan kelebihan rumah tetapi tidak menghapuskannya."]),
  ("Tip bajet", ["Meja langsung bergerak pantas. Tetapkan bajet sesi dan pilih had meja yang sesuai. Jika anda menggunakan bonus, semak dahulu [[bonus-__SLUG__|cara turnover dikira]]. Lihat meja popular di [[home#live|Kasino Langsung]]."]),
 ],
},
{
 "slug": "odds-sukan", "lang": "ms", "cluster": "permainan", "card": "Sukan",
 "kw": ["odds sukan", "Malay odds", "Asian handicap"],
 "title": "Odds Sukan Diterangkan: Handicap, Over/Under & Malay Odds",
 "desc": "Cara membaca odds perpuluhan dan Malay odds, Asian handicap dan pasaran over/under, dengan contoh mudah untuk pertaruhan bola sepak.",
 "intro": "Odds sukan kelihatan mengelirukan pada mulanya, tetapi setiap format hanya cara berbeza menunjukkan perkara sama: berapa yang anda menang berbanding taruhan. Ini sebahagian daripada [[permainan-kasino-__SLUG__|panduan permainan __BRAND__]].",
 "sections": [
  ("Odds perpuluhan", ["Jumlah pulangan ialah taruhan × odds. Taruhan RM10 pada 1.90 memulangkan RM19 (untung RM9 tambah taruhan anda)."]),
  ("Malay odds", ["Malay odds positif menunjukkan untung bagi setiap unit taruhan (0.90 = untung RM9 atas RM10). Odds negatif menunjukkan berapa yang anda risikokan untuk menang satu unit (-0.90 = risiko RM9 untuk menang RM10)."]),
  ("Asian handicap dan over/under", ["Handicap memberi satu pasukan kelebihan gol. Pada -0.5, pasukan anda mesti menang; pada +0.5, seri sudah cukup. Over/under ialah taruhan sama ada jumlah gol melebihi atau kurang daripada satu garis, seperti 2.5."]),
  ("Bertaruh dengan bijak", ["Odds termasuk margin bookmaker, jadi untung jangka panjang tidak realistik. Bertaruh kecil dan jangan kejar kerugian. Sebelum deposit, baca [[deposit-pengeluaran-__SLUG__|panduan deposit]] dan semak [[home#faq|soalan lazim]]."]),
 ],
},
]

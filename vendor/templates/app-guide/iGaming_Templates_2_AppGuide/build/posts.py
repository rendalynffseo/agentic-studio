"""Blog = topical authority. Posts are grouped in CLUSTERS; each cluster has ONE pillar post + supporting posts.

Per site, build the clusters from the user's keyword list (see CLAUDE.md): main keyword topic -> pillar,
long-tail keywords -> supporting posts. Write in the main (local) language first.

CLUSTERS: key -> {"name": {lang: label}, "pillar": slug}. Order = order on /blog/ and in the footer.
Post fields: slug, lang, cluster, kw (list: first = focus keyword), card (label), title (<= ~55 chars, brand gets appended
to <title>), desc (70-160 chars), intro, sections = [(h2, [blocks])].
Blocks: blank-line separated paragraphs; "- " lines = bullets; "1. " lines = numbered.
Internal links: [[target|anchor]], target = post slug, home, home#<section-id>, blog, games. Unknown target = build error.
Linking rules (build warns if broken): every supporting post links its pillar inline; every pillar links each of its
supporting posts inline; every post links at least one post in ANOTHER cluster and one home section.
Don't invent facts: no fees, payout times, licences, RTP numbers or bonus % unless the brief gives them.
"""

CLUSTERS = {
    "panduan": {"name": {"ms": "Panduan Asas", "en": "Getting Started", "zh": "入门指南"}, "pillar": "panduan-lengkap-__SLUG__"},
    "keselamatan": {"name": {"ms": "Keselamatan & Penipuan", "en": "Safety & Scams", "zh": "安全与防骗"}, "pillar": "keselamatan-aplikasi-__SLUG__"},
    "transaksi": {"name": {"ms": "Deposit, Pengeluaran & Bonus", "en": "Payments & Bonuses", "zh": "存取款与奖金"}, "pillar": "deposit-pengeluaran-__SLUG__"},
    "permainan": {"name": {"ms": "Permainan Diterangkan", "en": "Games Explained", "zh": "游戏解析"}, "pillar": "permainan-__SLUG__"},
}
GAMES_CLUSTER = "permainan"  # also listed on /games/

POSTS = [
# ================================================================== cluster: panduan
{
 "slug": "panduan-lengkap-__SLUG__", "lang": "ms", "cluster": "panduan", "card": "Panduan Utama",
 "kw": ["__BRAND__ Malaysia", "panduan __BRAND__", "apa itu __BRAND__"],
 "title": "Panduan Lengkap __BRAND__ Malaysia 2026",
 "desc": "Semua tentang __BRAND__ dalam satu halaman: apa itu aplikasi ini, cara pasang dengan selamat, daftar, login, transaksi dan bermain secara bertanggungjawab.",
 "intro": "Panduan ini ialah titik permulaan untuk semua perkara tentang aplikasi __BRAND__. Ia menerangkan apa itu aplikasi ini, cara pemain di Malaysia memasang dan menggunakannya, di mana risiko sebenar, dan panduan terperinci mana yang patut dibaca seterusnya.",
 "sections": [
  ("Apa itu __BRAND__", ["__BRAND__ ialah aplikasi permainan mudah alih dengan permainan gaya slot, arked dan meja dalam satu muat turun. Ia diedarkan di luar Google Play dan App Store, jadi proses pemasangannya berbeza daripada aplikasi biasa. Ringkasan dua minit ada di [[home#about|gambaran aplikasi di halaman utama]]."]),
  ("Langkah pertama: daftar dan login", ["Sediakan akaun dengan [[cara-daftar-__SLUG__|cara daftar akaun __BRAND__ langkah demi langkah]]. Jika anda tersekat di skrin log masuk, [[cara-login-__SLUG__|panduan login dan ralat biasa __BRAND__]] menerangkan punca dan penyelesaiannya."]),
  ("Pasang dengan selamat", ["Oleh kerana aplikasi dipasang secara side-load, sumber muat turun dan kebenaran aplikasi ialah dua semakan keselamatan utama anda.",
    "- Muat turun hanya dari halaman yang telah disahkan\n- Kekalkan Google Play Protect aktif\n- Tolak kebenaran SMS, kenalan dan kebolehcapaian",
    "Semua langkah keselamatan dihimpunkan dalam [[keselamatan-aplikasi-__SLUG__|panduan keselamatan aplikasi __BRAND__]], dan jadual kebenaran penuh ada di [[home#install|panduan pasang]]."]),
  ("Deposit, pengeluaran dan bonus", ["Pemain Malaysia biasanya menggunakan FPX, DuitNow atau e-dompet. Baca [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]] sebelum transaksi pertama anda."]),
  ("Memahami permainan", ["Setiap permainan ditentukan oleh penjana nombor rawak dengan kelebihan rumah. [[permainan-__SLUG__|Panduan permainan __BRAND__]] menerangkan setiap kategori tanpa gembar-gembur."]),
  ("Kekal terkawal", ["Tetapkan had masa dan wang sebelum bermula, jangan kejar kerugian, dan berhenti jika permainan tidak lagi menyeronokkan. Bantuan di Malaysia: Talian Kasih 15999."]),
 ],
},
{
 "slug": "cara-daftar-__SLUG__", "lang": "ms", "cluster": "panduan", "card": "Daftar",
 "kw": ["cara daftar __BRAND__", "__BRAND__ daftar", "daftar akaun __BRAND__"],
 "title": "Cara Daftar Akaun __BRAND__ dengan Selamat",
 "desc": "Langkah demi langkah cara daftar akaun __BRAND__, perkara yang perlu disediakan, dan cara melindungi nama pengguna serta kata laluan anda.",
 "intro": "Pendaftaran biasanya mengambil masa beberapa minit. Yang lebih penting ialah mendaftar di halaman yang betul dan melindungi butiran akaun dari awal. Panduan ini sebahagian daripada [[panduan-lengkap-__SLUG__|panduan lengkap __BRAND__]].",
 "sections": [
  ("Sediakan perkara ini dahulu", ["- Nombor telefon aktif atas nama anda\n- Nama penuh sama seperti akaun bank anda\n- Kata laluan kuat yang tidak digunakan di tempat lain\n- Umur 18 tahun ke atas"]),
  ("Langkah pendaftaran", ["1. Buka halaman rasmi yang telah anda sahkan, bukan pautan daripada orang asing.\n2. Isi borang dengan maklumat yang tepat.\n3. Sahkan nombor telefon jika diminta.\n4. Simpan nama pengguna anda di tempat selamat.\n5. Tetapkan had perbelanjaan sebelum membuat deposit."]),
  ("Elakkan perangkap", ["Jangan bayar sesiapa untuk \"membuka akaun\" bagi pihak anda, dan jangan kongsi kata laluan dengan \"ejen\". Kenali [[tanda-penipuan-__SLUG__|7 tanda penipuan __BRAND__]] sebelum anda bermula."]),
  ("Seterusnya", ["Selepas akaun aktif, baca [[cara-login-__SLUG__|cara login __BRAND__]] dan semak [[home#install|panduan pasang aplikasi]]."]),
 ],
},
{
 "slug": "cara-login-__SLUG__", "lang": "ms", "cluster": "panduan", "card": "Login",
 "kw": ["__BRAND__ login", "__BRAND__ tidak boleh login", "cara login __BRAND__"],
 "title": "Cara Login __BRAND__ dan Atasi Ralat Biasa",
 "desc": "Tidak boleh log masuk __BRAND__? Punca biasa, langkah penyelesaian yang selamat, dan perkara yang tidak patut dilakukan supaya baki anda kekal selamat.",
 "intro": "Kebanyakan masalah login mudah diselesaikan, dan baki anda terikat pada akaun, bukan pada aplikasi di telefon. Untuk gambaran keseluruhan, mulakan dengan [[panduan-lengkap-__SLUG__|panduan lengkap __BRAND__]].",
 "sections": [
  ("Punca biasa", ["1. Versi aplikasi lama — kemas kini dahulu.\n2. Kata laluan salah — ia sensitif huruf besar dan kecil.\n3. Akaun dikunci sementara selepas beberapa percubaan gagal.\n4. Pelayan tidak dapat dihubungi kerana sambungan lemah atau penyelenggaraan."]),
  ("Cubaan pantas", ["- Tukar antara Wi-Fi dan data mudah alih\n- Mulakan semula aplikasi dan telefon\n- Kosongkan cache aplikasi\n- Pastikan tarikh dan masa ditetapkan secara automatik"]),
  ("Apa yang TIDAK patut dilakukan", ["Jangan pasang semula dari pautan rawak — itulah cara salinan palsu dipasang. Ikut [[apk-palsu-__SLUG__|senarai semak APK palsu]] jika anda perlu memasang semula. Jangan sekali-kali masukkan kata laluan perbankan atau kod TAC ke dalam permainan."]),
  ("Belum ada akaun?", ["Ikut [[cara-daftar-__SLUG__|cara daftar akaun __BRAND__]] dahulu, kemudian semak [[home#install|langkah pasang aplikasi yang selamat]]."]),
 ],
},
# ================================================================== cluster: keselamatan
{
 "slug": "keselamatan-aplikasi-__SLUG__", "lang": "ms", "cluster": "keselamatan", "card": "Panduan Utama",
 "kw": ["keselamatan __BRAND__", "__BRAND__ selamat", "__BRAND__ scam"],
 "title": "Keselamatan Aplikasi __BRAND__: Panduan Penuh",
 "desc": "Cara kekal selamat dengan __BRAND__: sumber muat turun, kebenaran aplikasi, kod OTP, penipuan biasa dan apa yang perlu dilakukan jika sesuatu tidak kena.",
 "intro": "Risiko terbesar dengan aplikasi side-load bukan permainannya, tetapi aplikasi palsu dan penipu yang menyasarkan wang serta kod bank anda. Panduan ini menghimpunkan semua semakan keselamatan yang penting.",
 "sections": [
  ("Tiga peraturan asas", ["1. Muat turun hanya dari sumber yang telah disahkan.\n2. Jangan sekali-kali kongsi OTP, TAC atau kata laluan perbankan.\n3. Tolak kebenaran SMS, kenalan dan kebolehcapaian."]),
  ("Aplikasi palsu", ["Salinan palsu boleh kelihatan sama seperti aplikasi sebenar sambil membaca kod SMS anda. Gunakan [[apk-palsu-__SLUG__|senarai semak APK palsu __BRAND__]] setiap kali anda memasang atau memasang semula aplikasi."]),
  ("Penipuan yang biasa", ["Tawaran \"kredit percuma\", yuran untuk mengeluarkan kemenangan dan \"ejen\" yang menghubungi anda dahulu ialah corak penipuan biasa. Kenali semuanya dalam [[tanda-penipuan-__SLUG__|7 tanda penipuan __BRAND__]]."]),
  ("Wang dan akaun", ["Deposit hanya melalui kaedah rasmi — lihat [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran]]. Jadual kebenaran aplikasi yang selamat ada di [[home#install|halaman utama]]."]),
  ("Jika anda menjadi mangsa", ["Hubungi bank anda serta-merta, tukar kata laluan dari peranti lain yang bersih, dan laporkan kepada Pusat Respons Scam Kebangsaan di 997."]),
 ],
},
{
 "slug": "apk-palsu-__SLUG__", "lang": "ms", "cluster": "keselamatan", "card": "APK",
 "kw": ["__BRAND__ apk", "apk palsu __BRAND__", "download __BRAND__"],
 "title": "APK __BRAND__ Palsu: Senarai Semak Keselamatan",
 "desc": "Senarai semak langkah demi langkah untuk mengenal pasti pemasang __BRAND__ palsu: sumber, kebenaran, Play Protect dan apa yang perlu dilakukan jika tersalah pasang.",
 "intro": "Pemasang palsu ialah risiko sebenar terbesar bagi mana-mana aplikasi side-load. Senarai semak ini mengambil masa lima minit dan sebahagian daripada [[keselamatan-aplikasi-__SLUG__|panduan keselamatan aplikasi __BRAND__]].",
 "sections": [
  ("Sebelum memuat turun", ["- Taip alamat sendiri atau guna penanda halaman yang disimpan\n- Curigai pautan daripada orang asing di WhatsApp atau Telegram\n- Semak ejaan domain dengan teliti\n- Abaikan versi \"mod\", \"hack\" atau \"auto-menang\""]),
  ("Semasa memasang", ["- Kekalkan Google Play Protect aktif\n- Baca setiap permintaan kebenaran\n- Tolak SMS, kenalan, log panggilan dan kebolehcapaian\n- Benarkan \"pasang aplikasi tidak diketahui\" untuk satu pelayar sahaja, kemudian matikan semula",
    "Jadual kebenaran penuh — mana yang normal dan mana yang tanda bahaya — ada di [[home#install|panduan pasang __BRAND__]]."]),
  ("Tanda anda tersalah pasang", ["- Aplikasi meminta kata laluan perbankan atau TAC/OTP\n- Muncul iklan timbul atau aplikasi baharu yang tidak anda pasang\n- Anda menerima SMS OTP bank yang tidak diminta"]),
  ("Langkah seterusnya", ["Nyahpasang aplikasi, imbas dengan Play Protect, tukar kata laluan dari peranti lain dan hubungi bank anda. Selepas itu, pasang semula dengan betul melalui [[cara-login-__SLUG__|panduan login __BRAND__]]."]),
 ],
},
{
 "slug": "tanda-penipuan-__SLUG__", "lang": "ms", "cluster": "keselamatan", "card": "Penipuan",
 "kw": ["__BRAND__ scam", "penipuan __BRAND__", "kredit percuma __BRAND__"],
 "title": "7 Tanda Penipuan __BRAND__ dan Cara Mengelak",
 "desc": "Kredit percuma palsu, yuran membuka akaun, ejen palsu: tujuh penipuan paling biasa sekitar aplikasi kasino mudah alih di Malaysia dan cara melindungi diri.",
 "intro": "Di mana ada aplikasi popular, di situ ada penipu. Kebanyakan penipuan tidak melibatkan permainan langsung — sasaran mereka ialah wang dan kod bank anda. Ini sebahagian daripada [[keselamatan-aplikasi-__SLUG__|panduan keselamatan aplikasi __BRAND__]].",
 "sections": [
  ("Tujuh tanda amaran", ["1. Seseorang meminta OTP, TAC atau kata laluan bank anda.\n2. Anda perlu bayar \"yuran\" atau \"cukai\" untuk mengeluarkan kemenangan.\n3. Tawaran \"kredit percuma\" memerlukan login akaun anda.\n4. \"Ejen\" menghubungi anda dahulu dan mendesak deposit segera.\n5. Pautan muat turun datang daripada orang asing.\n6. Anda dijanjikan kemenangan pasti, \"hack\" atau \"pola\".\n7. Tekanan masa: \"hari ini sahaja\"."]),
  ("Kenapa \"pasti menang\" sentiasa palsu", ["Keputusan permainan datang daripada penjana nombor rawak dengan kelebihan rumah. Baca [[rtp-volatiliti|maksud RTP dan volatiliti]] untuk faham sebabnya."]),
  ("Lindungi diri", ["- Jangan kongsi kod yang dihantar ke telefon anda\n- Guna kata laluan unik untuk setiap akaun\n- Deposit hanya melalui kaedah rasmi\n- Jika ditipu, hubungi bank dan NSRC (997) segera",
    "Lihat juga [[home#safety|tip keselamatan di halaman utama]]."]),
 ],
},
# ================================================================== cluster: transaksi
{
 "slug": "deposit-pengeluaran-__SLUG__", "lang": "ms", "cluster": "transaksi", "card": "Panduan Utama",
 "kw": ["__BRAND__ deposit", "__BRAND__ pengeluaran", "__BRAND__ withdraw"],
 "title": "Deposit & Pengeluaran __BRAND__: Panduan Lengkap",
 "desc": "Cara deposit dan keluarkan wang di __BRAND__ untuk pemain Malaysia: FPX, DuitNow, e-dompet, kenapa transaksi gagal dan peraturan keselamatan penting.",
 "intro": "Kebanyakan soalan pemain berkaitan wang. Panduan ini menerangkan aliran deposit dan pengeluaran secara umum. Had, yuran dan masa pemprosesan ditetapkan oleh pengendali — sentiasa semak di halaman rasmi.",
 "sections": [
  ("Kaedah pembayaran", ["Pemain Malaysia biasanya menggunakan perbankan dalam talian (FPX), DuitNow atau e-dompet. Cara setiap satu berfungsi diterangkan dalam [[fpx-duitnow-ewallet|panduan FPX, DuitNow dan e-dompet]]."]),
  ("Deposit", ["1. Log masuk melalui aplikasi atau laman rasmi.\n2. Pilih kaedah pembayaran.\n3. Sahkan bayaran di halaman bank anda sendiri.\n4. Simpan resit."]),
  ("Pengeluaran", ["Pengeluaran dihantar ke akaun bank atas nama berdaftar. Jika anda menuntut bonus, syarat taruhan mesti dipenuhi dahulu — lihat [[bonus-turnover-__SLUG__|maksud bonus dan turnover]]."]),
  ("Kenapa transaksi gagal", ["- Sesi bank tamat masa semasa ubah hala\n- Had pindahan harian bank anda\n- Nama akaun bank tidak sepadan dengan nama berdaftar\n- Waktu penyelenggaraan"]),
  ("Keselamatan", ["Jangan sekali-kali hantar wang ke akaun peribadi atas arahan \"ejen\". Baca [[tanda-penipuan-__SLUG__|7 tanda penipuan]] dan tetapkan had perbelanjaan sebelum deposit. Tip kawalan diri ada di [[home#safety|bahagian keselamatan halaman utama]]."]),
 ],
},
{
 "slug": "fpx-duitnow-ewallet", "lang": "ms", "cluster": "transaksi", "card": "Pembayaran",
 "kw": ["FPX kasino", "DuitNow kasino", "e-wallet kasino Malaysia"],
 "title": "FPX, DuitNow & E-Dompet: Cara Bayaran Berfungsi",
 "desc": "Cara FPX, pindahan DuitNow dan e-dompet menggerakkan wang, kenapa bayaran gagal, dan peraturan keselamatan yang terpakai untuk setiap kaedah.",
 "intro": "Masalah bayaran biasanya berpunca daripada tidak tahu apa yang berlaku antara menekan \"deposit\" dan wang sampai. Ini sebahagian daripada [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]].",
 "sections": [
  ("FPX", ["FPX mengubah hala anda ke skrin log masuk bank anda sendiri untuk meluluskan bayaran. Pastikan alamat halaman itu benar-benar milik bank anda."]),
  ("DuitNow", ["DuitNow membolehkan pindahan menggunakan nombor telefon, nombor IC atau kod QR. Semak nama penerima yang dipaparkan sebelum mengesahkan — pindahan sukar dibatalkan."]),
  ("E-dompet", ["E-dompet seperti Touch 'n Go eWallet membayar daripada baki dalam aplikasi. Sama ada ia diterima berbeza mengikut perkhidmatan, jadi semak halaman rasmi."]),
  ("Peraturan untuk semua kaedah", ["Guna akaun atas nama sendiri, simpan resit, dan jangan pindahkan wang kepada individu. Jangan sekali-kali masukkan kod bank ke dalam aplikasi permainan — lihat [[home#install|nota keselamatan pemasangan]]. Penipuan berkaitan bayaran diterangkan dalam [[keselamatan-aplikasi-__SLUG__|panduan keselamatan aplikasi]]."]),
 ],
},
{
 "slug": "bonus-turnover-__SLUG__", "lang": "ms", "cluster": "transaksi", "card": "Bonus",
 "kw": ["__BRAND__ bonus", "turnover __BRAND__", "syarat taruhan"],
 "title": "Bonus & Turnover __BRAND__ Diterangkan",
 "desc": "Cara bonus alu-aluan, bonus tambahan dan rebat berfungsi, maksud syarat turnover, dan kesannya terhadap pengeluaran anda di __BRAND__.",
 "intro": "Bonus menambah nilai, tetapi setiap satu ada syarat. Faham turnover sebelum menuntut untuk mengelakkan kejutan semasa pengeluaran. Ini sebahagian daripada [[deposit-pengeluaran-__SLUG__|panduan deposit dan pengeluaran __BRAND__]].",
 "sections": [
  ("Jenis promosi", ["- Bonus alu-aluan: padanan pada deposit pertama\n- Bonus tambahan: kredit pada deposit berikutnya\n- Rebat: sebahagian turnover layak dipulangkan"]),
  ("Maksud turnover", ["Turnover (syarat taruhan) ialah jumlah yang mesti dipertaruhkan sebelum dana bonus boleh dikeluarkan. Contohnya, syarat 20x bermakna bertaruh 20 kali jumlah bonus. Sesetengah permainan mungkin dikira kurang atau tidak dikira langsung."]),
  ("Sebelum menuntut", ["- Semak deposit minimum dan bonus maksimum\n- Semak permainan yang dikira untuk turnover\n- Ambil perhatian tarikh luput",
    "Ingat, bonus tidak mengubah peluang permainan — lihat [[permainan-__SLUG__|panduan permainan]] dan [[home#safety|cara kekal terkawal]]."]),
 ],
},
# ================================================================== cluster: permainan
{
 "slug": "permainan-__SLUG__", "lang": "ms", "cluster": "permainan", "card": "Panduan Utama",
 "kw": ["permainan __BRAND__", "slot __BRAND__", "game __BRAND__"],
 "title": "Permainan __BRAND__: Slot, Ikan & Meja Diterangkan",
 "desc": "Panduan jujur kategori permainan dalam aplikasi __BRAND__: slot video, slot klasik, tembak ikan dan permainan meja, serta maksud RTP dan volatiliti.",
 "intro": "Pustaka __BRAND__ mengandungi ratusan tajuk, tetapi semuanya tergolong dalam beberapa kategori. Panduan ini menerangkan setiap satu tanpa janji kemenangan.",
 "sections": [
  ("Slot video dan klasik", ["Slot klasik mempunyai tiga gelendong dan peraturan ringkas. Slot video mempunyai lima gelendong atau lebih, wild, putaran percuma dan pusingan bonus. Ciri tambahan menambah keseronokan, bukan peluang menang."]),
  ("Tembak ikan", ["Permainan arked yang kelihatan seperti permainan kemahiran, tetapi keputusan setiap tembakan tetap rawak. Lihat [[tembak-ikan|cara permainan tembak ikan berfungsi]]."]),
  ("Permainan meja", ["Permainan kad dan dadu dengan peraturan tetap dan kelebihan rumah yang terbina."]),
  ("RTP dan volatiliti", ["Dua nombor ini menerangkan tingkah laku permainan dalam jangka panjang. Baca [[rtp-volatiliti|maksud RTP dan volatiliti]] sebelum memilih permainan."]),
  ("Bermain dengan bijak", ["Tetapkan bajet, pilih permainan yang sesuai dengan bajet itu, dan berhenti apabila had dicapai. Ringkasan kategori ada di [[home#games|jadual permainan di halaman utama]], dan baca [[bonus-turnover-__SLUG__|maksud turnover]] jika anda menggunakan bonus."]),
 ],
},
{
 "slug": "rtp-volatiliti", "lang": "ms", "cluster": "permainan", "card": "RTP",
 "kw": ["RTP slot", "volatiliti slot", "slot gacor"],
 "title": "RTP & Volatiliti Slot: Maksud Sebenar",
 "desc": "RTP dan volatiliti dalam bahasa mudah: maksud nombor ini, apa yang ia tidak beritahu, dan kenapa tiada slot \"gacor\" yang pasti membayar.",
 "intro": "RTP dan volatiliti tidak membantu anda menang, tetapi membantu anda menetapkan jangkaan dan bajet yang realistik. Ini sebahagian daripada [[permainan-__SLUG__|panduan permainan __BRAND__]].",
 "sections": [
  ("RTP", ["RTP (return to player) ialah peratusan semua taruhan yang direka untuk dipulangkan dalam jumlah pusingan yang sangat besar. RTP 96% bermakna kelebihan rumah 4%. Ia menerangkan berjuta-juta putaran, bukan sesi anda."]),
  ("Volatiliti", ["- Volatiliti rendah: kemenangan kecil yang kerap\n- Volatiliti tinggi: tempoh kering yang panjang, kemenangan besar sekali-sekala, turun naik baki yang besar"]),
  ("Mitos yang patut diabaikan", ["- \"Slot ini sudah tiba masa bayar\" — setiap putaran adalah bebas\n- Slot \"gacor\" — tiada slot panas atau sejuk\n- Pola taruhan atau masa tertentu — tidak mengubah peluang",
    "Sesiapa yang menjual \"pola menang\" sedang menipu — lihat [[tanda-penipuan-__SLUG__|tanda penipuan]]. Ringkasan kategori permainan ada di [[home#games|jadual permainan]]."]),
 ],
},
{
 "slug": "tembak-ikan", "lang": "ms", "cluster": "permainan", "card": "Tembak Ikan",
 "kw": ["tembak ikan", "fishing game Malaysia", "game ikan __BRAND__"],
 "title": "Permainan Tembak Ikan: Kemahiran atau Nasib?",
 "desc": "Cara permainan tembak ikan berfungsi, apa yang dilakukan tahap meriam, dan kenapa keputusan tetap ditentukan oleh peluang rawak.",
 "intro": "Permainan tembak ikan kelihatan seperti permainan kemahiran, tetapi keputusan setiap tembakan ditentukan oleh sistem rawak permainan. Ini sebahagian daripada [[permainan-__SLUG__|panduan permainan __BRAND__]].",
 "sections": [
  ("Cara satu pusingan berfungsi", ["Setiap tembakan berharga jumlah tetap. Tahap meriam lebih tinggi lebih mahal. Apabila tembakan mengena, permainan menentukan sama ada ikan itu ditangkap; ikan besar membayar lebih tetapi jarang ditangkap."]),
  ("Di mana kemahiran berakhir", ["Membidik mempengaruhi apa yang anda kena, bukan peluang tangkapan. Dalam jangka panjang, kelebihan rumah terpakai seperti slot — lihat [[rtp-volatiliti|maksud RTP]]."]),
  ("Kawal kos", ["Tembakan pantas, jadi perbelanjaan cepat bertambah. Guna tahap meriam rendah, tetapkan bajet dan berehat. Jika anda menggunakan bonus, faham dahulu [[bonus-turnover-__SLUG__|syarat turnover]]. Tip lain ada di [[home#safety|bahagian keselamatan]]."]),
 ],
},
]

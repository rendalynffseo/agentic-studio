"""Home page + shared UI text, per language (en / ms / zh).

Tokens __BRAND__ __SLUG__ __TAGLINE__ are replaced at build time. Strings may hold simple inline HTML.
Links: "#id" = section on the home page of that language; "@register" / "@login" / "@app" / "@chat" = config URLs.
Section/row ids are fixed: slots live instant fishing matches register promos app faq.
FAQ answers stay plain text (FAQPage schema). Don't invent facts (licences, %, payout times, minimums).
SEO article: "seo_intro" is always visible; "seo_more" sits behind "Read more" (still in the HTML for Google).
"""

UI = {
    "en": {
        "html_lang": "en", "hreflang": "en-MY", "og_locale": "en_MY", "label": "EN", "name": "English",
        "skip": "Skip to content", "menu": "Menu", "close": "Close menu",
        "login": "Login", "register": "Join Now", "casino": "Casino", "sports": "Sports",
        "side": [
            [("🎰", "Slots", "#slots", ""), ("🃏", "Live Casino", "#live", "hot"), ("🚀", "Instant Games", "#instant", "new"), ("🐟", "Fishing", "#fishing", "")],
            [("⚽", "Sports Betting", "@register", ""), ("🎮", "E-Sports", "@register", ""), ("🎱", "4D & Lottery", "@register", "")],
            [("🎁", "Promotions", "#promos", ""), ("📱", "App Download", "#app", ""), ("📰", "Guides & Blog", "/blog/", ""), ("💬", "Live Support", "@chat", ""), ("🛡️", "Responsible Gaming", "/responsible-gaming/", "")],
        ],
        "tabs": [("☰", "Menu", "nav"), ("🎰", "Casino", "#slots"), ("🎁", "Promos", "#promos"), ("🔑", "Login", "@login"), ("👤", "Join", "@register")],
        "home": "Home", "see_all": "See all", "prev": "Previous", "next": "Next",
        "tcs": "18+ · T&Cs apply", "claim": "Claim now", "by": "By the", "team": "editorial team",
        "related": "Related guides", "start": "Ready to play?", "start_p": "Create your __BRAND__ account in minutes and set your limits first.",
        "back": "← All guides", "read": "Read guide →", "published": "Published",
        "more": "Read more", "hide": "Hide", "news": "News", "info": "Info", "blog": "Blog", "chat": "Live chat",
        "site_map": "Site map", "contents": "Contents", "contents_p": "Every page and guide on this __BRAND__ Malaysia site, in one list, grouped by topic.",
        "nf_title": "Page not found", "nf_p": "That page has moved or never existed.", "nf_home": "Back to lobby",
        "pillar_note": "Part of the main guide", "cluster_h": "All guides in this topic", "other_topics": "Other topics",
        "foot_guides": "Guides", "guides_small": "Learn before you play", "guides_h2": "__BRAND__ Guides by Topic", "guides_all": "All guides →", "pillar_badge": "Main guide",
        "float_register": "Register Now", "popup_alt": "__BRAND__ promotion — register now", "popup_title": "New member offer",
        "popup_text": "Join __BRAND__ in minutes and claim your welcome offer. T&Cs apply.", "popup_close": "Close",
        "rg_note": "<b>18+ only.</b> Gambling involves financial risk and can be addictive. Set a budget before you play and never chase losses. Help in Malaysia: Talian Kasih <b>15999</b>.",
        "foot_about": "__BRAND__ — __TAGLINE__. Slots, live casino, sports and instant games in one account, on mobile and desktop.",
        "foot_cols": [("Games", [("Slots", "#slots"), ("Live Casino", "#live"), ("Instant Games", "#instant"), ("Fishing", "#fishing")]),
                      ("Help", [("How to register", "#register"), ("FAQ", "#faq"), ("Guides & Blog", "/blog/"), ("Live support", "@chat")]),
                      ("Info", [("About", "/about/"), ("Responsible Gaming", "/responsible-gaming/"), ("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms/"), ("Contents", "/contents/")])],
        "foot_rg": "Play responsibly · Talian Kasih 15999",
        "foot_disc": "This site provides information and links for adults aged 18 and over. Online gambling laws differ by country, and in some places, including Malaysia, it is restricted. You are responsible for following the laws where you live. Bonuses and promotions are subject to the operator's current terms. Some links are affiliate links.",
    },
    "ms": {
        "html_lang": "ms", "hreflang": "ms-MY", "og_locale": "ms_MY", "label": "BM", "name": "Bahasa Melayu",
        "skip": "Langkau ke kandungan", "menu": "Menu", "close": "Tutup menu",
        "login": "Log Masuk", "register": "Daftar", "casino": "Kasino", "sports": "Sukan",
        "side": [
            [("🎰", "Slot", "#slots", ""), ("🃏", "Kasino Langsung", "#live", "hot"), ("🚀", "Permainan Segera", "#instant", "new"), ("🐟", "Memancing", "#fishing", "")],
            [("⚽", "Pertaruhan Sukan", "@register", ""), ("🎮", "E-Sukan", "@register", ""), ("🎱", "4D & Loteri", "@register", "")],
            [("🎁", "Promosi", "#promos", ""), ("📱", "Muat Turun Aplikasi", "#app", ""), ("📰", "Panduan & Blog", "/blog/", ""), ("💬", "Sokongan Langsung", "@chat", ""), ("🛡️", "Permainan Bertanggungjawab", "/responsible-gaming/", "")],
        ],
        "tabs": [("☰", "Menu", "nav"), ("🎰", "Kasino", "#slots"), ("🎁", "Promosi", "#promos"), ("🔑", "Log Masuk", "@login"), ("👤", "Daftar", "@register")],
        "home": "Utama", "see_all": "Lihat semua", "prev": "Sebelum", "next": "Seterusnya",
        "tcs": "18+ · Terma & syarat terpakai", "claim": "Tuntut sekarang", "by": "Oleh", "team": "pasukan editorial",
        "related": "Panduan berkaitan", "start": "Sedia untuk bermain?", "start_p": "Buka akaun __BRAND__ dalam beberapa minit dan tetapkan had anda dahulu.",
        "back": "← Semua panduan", "read": "Baca panduan →", "published": "Diterbitkan",
        "more": "Baca lagi", "hide": "Sembunyi", "news": "Berita", "info": "Info", "blog": "Blog", "chat": "Sembang langsung",
        "site_map": "Peta laman", "contents": "Kandungan", "contents_p": "Setiap halaman dan panduan di laman __BRAND__ Malaysia ini, dalam satu senarai mengikut topik.",
        "nf_title": "Halaman tidak dijumpai", "nf_p": "Halaman ini telah dipindahkan atau tidak wujud.", "nf_home": "Kembali ke lobi",
        "pillar_note": "Sebahagian daripada panduan utama", "cluster_h": "Semua panduan dalam topik ini", "other_topics": "Topik lain",
        "foot_guides": "Panduan", "guides_small": "Ketahui sebelum bermain", "guides_h2": "Panduan __BRAND__ Mengikut Topik", "guides_all": "Semua panduan →", "pillar_badge": "Panduan utama",
        "float_register": "Daftar Sekarang", "popup_alt": "Promosi __BRAND__ — daftar sekarang", "popup_title": "Tawaran ahli baharu",
        "popup_text": "Sertai __BRAND__ dalam beberapa minit dan tuntut tawaran alu-aluan anda. Terma terpakai.", "popup_close": "Tutup",
        "rg_note": "<b>18+ sahaja.</b> Perjudian melibatkan risiko kewangan dan boleh menyebabkan ketagihan. Tetapkan bajet sebelum bermain dan jangan kejar kerugian. Bantuan di Malaysia: Talian Kasih <b>15999</b>.",
        "foot_about": "__BRAND__ — Kasino Dalam Talian Dipercayai di Malaysia. Slot, kasino langsung, sukan dan permainan segera dalam satu akaun, di telefon dan komputer.",
        "foot_cols": [("Permainan", [("Slot", "#slots"), ("Kasino Langsung", "#live"), ("Permainan Segera", "#instant"), ("Memancing", "#fishing")]),
                      ("Bantuan", [("Cara mendaftar", "#register"), ("Soalan lazim", "#faq"), ("Panduan & Blog", "/blog/"), ("Sokongan langsung", "@chat")]),
                      ("Maklumat", [("Tentang", "/about/"), ("Permainan Bertanggungjawab", "/responsible-gaming/"), ("Dasar Privasi", "/privacy-policy/"), ("Terma Penggunaan", "/terms/"), ("Kandungan", "/contents/")])],
        "foot_rg": "Bermain secara bertanggungjawab · Talian Kasih 15999",
        "foot_disc": "Laman ini menyediakan maklumat dan pautan untuk dewasa berumur 18 tahun ke atas. Undang-undang perjudian dalam talian berbeza mengikut negara, dan di sesetengah tempat termasuk Malaysia ia dihadkan. Anda bertanggungjawab mematuhi undang-undang di tempat anda. Bonus dan promosi tertakluk kepada terma semasa pengendali. Sesetengah pautan ialah pautan afiliasi.",
    },
    "zh": {
        "html_lang": "zh-Hans", "hreflang": "zh-MY", "og_locale": "zh_CN", "label": "中文", "name": "中文",
        "skip": "跳至内容", "menu": "菜单", "close": "关闭菜单",
        "login": "登录", "register": "立即加入", "casino": "娱乐场", "sports": "体育",
        "side": [
            [("🎰", "老虎机", "#slots", ""), ("🃏", "真人娱乐场", "#live", "hot"), ("🚀", "快速游戏", "#instant", "new"), ("🐟", "捕鱼", "#fishing", "")],
            [("⚽", "体育投注", "@register", ""), ("🎮", "电子竞技", "@register", ""), ("🎱", "4D 与彩票", "@register", "")],
            [("🎁", "优惠活动", "#promos", ""), ("📱", "下载应用", "#app", ""), ("📰", "指南与博客", "/blog/", ""), ("💬", "在线客服", "@chat", ""), ("🛡️", "负责任博彩", "/responsible-gaming/", "")],
        ],
        "tabs": [("☰", "菜单", "nav"), ("🎰", "娱乐场", "#slots"), ("🎁", "优惠", "#promos"), ("🔑", "登录", "@login"), ("👤", "加入", "@register")],
        "home": "首页", "see_all": "查看全部", "prev": "上一页", "next": "下一页",
        "tcs": "18+ · 适用条款与条件", "claim": "立即领取", "by": "作者：", "team": "编辑团队",
        "related": "相关指南", "start": "准备好开始了吗？", "start_p": "几分钟即可注册 __BRAND__ 账户，请先设定您的限额。",
        "back": "← 全部指南", "read": "阅读指南 →", "published": "发布于",
        "more": "阅读更多", "hide": "收起", "news": "公告", "info": "信息", "blog": "博客", "chat": "在线客服",
        "site_map": "网站地图", "contents": "目录", "contents_p": "本站所有页面与指南，按主题分类一览。",
        "nf_title": "页面未找到", "nf_p": "该页面已移动或不存在。", "nf_home": "返回大厅",
        "pillar_note": "属于主要指南", "cluster_h": "本主题的全部指南", "other_topics": "其他主题",
        "foot_guides": "指南", "guides_small": "游戏前先了解", "guides_h2": "按主题浏览 __BRAND__ 指南", "guides_all": "全部指南 →", "pillar_badge": "主要指南",
        "float_register": "立即注册", "popup_alt": "__BRAND__ 优惠 — 立即注册", "popup_title": "新会员优惠",
        "popup_text": "几分钟即可加入 __BRAND__ 并领取迎新优惠。适用条款。", "popup_close": "关闭",
        "rg_note": "<b>仅限 18 岁以上。</b>博彩涉及财务风险并可能令人上瘾。游戏前请设定预算，切勿追损。马来西亚求助热线：Talian Kasih <b>15999</b>。",
        "foot_about": "__BRAND__ — 马来西亚值得信赖的在线娱乐场。老虎机、真人娱乐场、体育和快速游戏，一个账户即可畅玩，支持手机和电脑。",
        "foot_cols": [("游戏", [("老虎机", "#slots"), ("真人娱乐场", "#live"), ("快速游戏", "#instant"), ("捕鱼", "#fishing")]),
                      ("帮助", [("如何注册", "#register"), ("常见问题", "#faq"), ("指南与博客", "/blog/"), ("在线客服", "@chat")]),
                      ("信息", [("关于", "/about/"), ("负责任博彩", "/responsible-gaming/"), ("隐私政策", "/privacy-policy/"), ("使用条款", "/terms/"), ("网站目录", "/contents/")])],
        "foot_rg": "理性娱乐 · Talian Kasih 15999",
        "foot_disc": "本站为 18 岁及以上成年人提供信息和链接。各国网络博彩法律不同，在包括马来西亚在内的部分地区受到限制。您有责任遵守所在地的法律。奖金和优惠以运营商当前条款为准。部分链接为联盟链接。",
    },
}

HOME = {
    # ------------------------------------------------------------------ EN
    "en": {
        "title": "__BRAND__ Malaysia | Online Casino: Slots, Live Casino & Sports",
        "desc": "__BRAND__ Malaysia: slots, live casino, sports betting, fishing and instant games in one account. How to register, promotions, app download and FAQ.",
        "h1": "Welcome to <b>__BRAND__</b>",
        "lead": "Slots, live casino, sports and instant games — one account, on any device. Register in minutes and claim your welcome offer.",
        "cta": "Register Now", "sub": "18+ only · Play responsibly · T&Cs apply",
        "entry": [("🎰", "Casino", "#slots", "Live now"), ("⚽", "Sports", "@register", "Live now")],
        "chips": [("🏠", "Lobby", "#main"), ("🎰", "Slots", "#slots"), ("🃏", "Live Casino", "#live"), ("🚀", "Instant", "#instant"), ("🐟", "Fishing", "#fishing"), ("🎁", "Promotions", "#promos")],
        "rows": {"slots": ("🎰", "Popular Games We Love"), "live": ("🃏", "Best Live Casino Games"), "instant": ("🚀", "Instant Games To Play"), "fishing": ("🐟", "Fishing Games")},
        "matches_h2": "Upcoming Live Matches", "bet": "Bet now",
        "register": ("Welcome to __BRAND__ — __TAGLINE__", "How to Register", [
            ("📝", "Create account", "Click Join Now and fill in your login details."),
            ("💳", "Make a deposit", "Fund your account by online banking, e-wallet or crypto."),
            ("🎮", "Start playing", "Pick your favourite slot, live table or match."),
            ("🎁", "Get rewards", "Don't forget to claim your eligible bonuses."),
        ]),
        "promos": ("Rewards for every player", "Promotions & Bonuses"),
        "app": ("App Download", "The future of gaming is here. Great games on all devices.",
                "Get the __BRAND__ app for faster access, saved login and instant notifications.",
                ["Android and iOS", "Face or fingerprint login on supported phones", "Same account and wallet as the website"], "Download the App"),
        "trust": ("Game Providers", "Payment Methods"),
        "seo_intro": """<h1>__BRAND__ | __TAGLINE__</h1>
<p>__BRAND__ is an online casino brand serving players across Asia, including Malaysia. One account gives you access to slots, live casino tables, sports betting, fishing games, lottery and fast instant games, on mobile and desktop. This page explains what is available, how to get started, and how to play safely.</p>""",
        "seo_more": """<h2>Reputation and history of __BRAND__</h2>
<p>__BRAND__ has built its name on a wide game selection, regular promotions and responsive customer support. As with any operator, read the current terms and check the official site before you deposit.</p>
<h2>Games available</h2>
<h3>Slot games</h3><p>Video slots, classic slots and jackpot titles from well-known studios, with themes, free spins and bonus features. Every result is random, so treat play as entertainment.</p>
<h3>Sports betting</h3><p>Pre-match and in-play markets on football, basketball, tennis, e-sports and more.</p>
<h3>Live casino</h3><p>Baccarat, roulette, blackjack and sic bo streamed in HD with real dealers.</p>
<h3>Fishing and instant games</h3><p>Arcade-style fishing games and quick rounds such as crash, plinko and keno.</p>
<h3>Lottery</h3><p>4D and regional lottery draws.</p>
<h2>Promotions and bonuses</h2>
<p>Typical offers include a welcome bonus, reload bonuses, cash rebates and a VIP programme. Every bonus has wagering requirements and an expiry date; read the terms before you claim.</p>
<h2>Customer support</h2>
<p>Support is available through live chat on the website and app. __BRAND__ staff will never ask for your password or OTP.</p>
<h2>Payment methods</h2>
<p>Malaysian players can usually deposit by online banking (FPX), DuitNow, e-wallets, bank transfer and selected cryptocurrencies. Minimums, limits and processing times are shown in the cashier after you log in.</p>
<h2>Mobile gaming</h2>
<p>Play in your phone's browser or install the app for Android or iOS. Your account and balance are the same on every device.</p>
<h2>Safety and responsible gaming</h2>
<p>Only deposit through the official site after logging in, never through a chat contact. Set a budget, take breaks and never chase losses. Gambling is for adults 18+.</p>""",
        "faq_h2": "FAQs about __BRAND__ Malaysia",
        "faq": [("How do I register at __BRAND__?", "Click Join Now, fill in your username, password, name and phone number, verify your details, and your account is ready. It takes a few minutes."),
                ("Can I play on my phone?", "Yes. You can play in the mobile browser or download the app for Android and iOS. Your account works on every device."),
                ("How do I deposit?", "Log in, open the cashier and choose a method such as online banking, e-wallet or crypto. Only deposit through the official site, never through a chat contact."),
                ("Can I withdraw my winnings?", "Yes. Withdrawals are requested from the cashier. Any active bonus must meet its wagering requirements first, and your account details must match your bank account."),
                ("Is online gambling legal in Malaysia?", "Laws on online gambling differ by country, and Malaysia restricts it. You are responsible for knowing and following the laws that apply to you. Gambling is for adults 18+ only.")],
    },
    # ------------------------------------------------------------------ MS
    "ms": {
        "title": "__BRAND__ Malaysia | Kasino Online: Slot, Live Casino & Sukan",
        "desc": "__BRAND__ Malaysia: slot, kasino langsung, pertaruhan sukan, memancing dan permainan segera dalam satu akaun. Cara daftar, promosi, aplikasi dan soalan lazim.",
        "h1": "Selamat datang ke <b>__BRAND__</b>",
        "lead": "Slot, kasino langsung, sukan dan permainan segera — satu akaun, di mana-mana peranti. Daftar dalam beberapa minit dan tuntut tawaran alu-aluan anda.",
        "cta": "Daftar Sekarang", "sub": "18+ sahaja · Bermain secara bertanggungjawab · Terma terpakai",
        "entry": [("🎰", "Kasino", "#slots", "Langsung"), ("⚽", "Sukan", "@register", "Langsung")],
        "chips": [("🏠", "Lobi", "#main"), ("🎰", "Slot", "#slots"), ("🃏", "Kasino Langsung", "#live"), ("🚀", "Segera", "#instant"), ("🐟", "Memancing", "#fishing"), ("🎁", "Promosi", "#promos")],
        "rows": {"slots": ("🎰", "Permainan Popular"), "live": ("🃏", "Kasino Langsung Terbaik"), "instant": ("🚀", "Permainan Segera"), "fishing": ("🐟", "Permainan Memancing")},
        "matches_h2": "Perlawanan Akan Datang", "bet": "Bertaruh",
        "register": ("Selamat datang ke __BRAND__ — Kasino Dalam Talian Dipercayai", "Cara Mendaftar", [
            ("📝", "Buka akaun", "Klik Daftar dan isi butiran log masuk anda."),
            ("💳", "Buat deposit", "Tambah dana melalui perbankan dalam talian, e-dompet atau kripto."),
            ("🎮", "Mula bermain", "Pilih slot, meja langsung atau perlawanan kegemaran anda."),
            ("🎁", "Dapatkan ganjaran", "Jangan lupa tuntut bonus yang layak."),
        ]),
        "promos": ("Ganjaran untuk setiap pemain", "Promosi & Bonus"),
        "app": ("Muat Turun Aplikasi", "Masa depan permainan ada di sini. Permainan hebat di semua peranti.",
                "Dapatkan aplikasi __BRAND__ untuk akses lebih pantas, log masuk tersimpan dan notifikasi segera.",
                ["Android dan iOS", "Log masuk wajah atau cap jari pada telefon yang disokong", "Akaun dan dompet sama seperti laman web"], "Muat Turun Aplikasi"),
        "trust": ("Penyedia Permainan", "Kaedah Pembayaran"),
        "seo_intro": """<h1>__BRAND__ | Kasino Dalam Talian Dipercayai di Malaysia</h1>
<p>__BRAND__ ialah jenama kasino dalam talian untuk pemain di Asia, termasuk Malaysia. Satu akaun memberi akses kepada slot, kasino langsung, pertaruhan sukan, permainan memancing, loteri dan permainan segera, di telefon dan komputer. Halaman ini menerangkan apa yang tersedia, cara bermula dan cara bermain dengan selamat.</p>""",
        "seo_more": """<h2>Permainan yang tersedia</h2>
<h3>Slot</h3><p>Slot video, slot klasik dan jackpot daripada studio terkenal. Setiap keputusan adalah rawak — anggap ia hiburan.</p>
<h3>Pertaruhan sukan</h3><p>Pasaran sebelum perlawanan dan semasa perlawanan untuk bola sepak, bola keranjang, tenis, e-sukan dan banyak lagi.</p>
<h3>Kasino langsung</h3><p>Baccarat, rolet, blackjack dan sic bo dengan peniaga sebenar dalam HD.</p>
<h3>Memancing dan permainan segera</h3><p>Permainan memancing gaya arked dan pusingan pantas seperti crash, plinko dan keno.</p>
<h2>Promosi dan bonus</h2>
<p>Tawaran biasa termasuk bonus alu-aluan, bonus tambahan, rebat tunai dan program VIP. Setiap bonus mempunyai syarat taruhan dan tarikh luput — baca terma sebelum menuntut.</p>
<h2>Kaedah pembayaran</h2>
<p>Pemain Malaysia biasanya boleh deposit melalui FPX, DuitNow, e-dompet, pindahan bank dan kripto terpilih. Had minimum dan masa pemprosesan dipaparkan di juruwang selepas log masuk.</p>
<h2>Keselamatan dan permainan bertanggungjawab</h2>
<p>Deposit hanya melalui laman rasmi selepas log masuk, bukan melalui kenalan sembang. Tetapkan bajet, berehat dan jangan kejar kerugian. Perjudian hanya untuk dewasa 18+.</p>""",
        "faq_h2": "Soalan Lazim __BRAND__ Malaysia",
        "faq": [("Bagaimana cara daftar di __BRAND__?", "Klik Daftar, isi nama pengguna, kata laluan, nama dan nombor telefon, sahkan butiran anda dan akaun anda sedia. Ia mengambil masa beberapa minit."),
                ("Bolehkah saya bermain di telefon?", "Ya. Anda boleh bermain di pelayar telefon atau muat turun aplikasi untuk Android dan iOS. Akaun anda berfungsi di semua peranti."),
                ("Bagaimana cara deposit?", "Log masuk, buka juruwang dan pilih kaedah seperti perbankan dalam talian, e-dompet atau kripto. Deposit hanya melalui laman rasmi, bukan melalui kenalan sembang."),
                ("Bolehkah saya mengeluarkan kemenangan?", "Ya. Pengeluaran dibuat di juruwang. Bonus aktif mesti memenuhi syarat taruhan dahulu, dan butiran akaun mesti sepadan dengan akaun bank anda."),
                ("Adakah perjudian dalam talian sah di Malaysia?", "Undang-undang perjudian dalam talian berbeza mengikut negara, dan Malaysia menghadkannya. Anda bertanggungjawab mengetahui dan mematuhi undang-undang yang terpakai. Hanya untuk dewasa 18+.")],
    },
    # ------------------------------------------------------------------ ZH
    "zh": {
        "title": "__BRAND__ 马来西亚 | 值得信赖的在线娱乐场 — 老虎机、真人娱乐场与体育",
        "desc": "__BRAND__ 马来西亚：老虎机、真人娱乐场、体育投注、捕鱼和快速游戏，一个账户畅玩。注册方法、优惠活动、应用下载及常见问题。",
        "h1": "欢迎来到 <b>__BRAND__</b>",
        "lead": "老虎机、真人娱乐场、体育和快速游戏 — 一个账户，任何设备。几分钟即可注册并领取迎新优惠。",
        "cta": "立即注册", "sub": "仅限 18+ · 理性娱乐 · 适用条款",
        "entry": [("🎰", "娱乐场", "#slots", "进行中"), ("⚽", "体育", "@register", "进行中")],
        "chips": [("🏠", "大厅", "#main"), ("🎰", "老虎机", "#slots"), ("🃏", "真人娱乐场", "#live"), ("🚀", "快速游戏", "#instant"), ("🐟", "捕鱼", "#fishing"), ("🎁", "优惠", "#promos")],
        "rows": {"slots": ("🎰", "热门游戏"), "live": ("🃏", "精选真人娱乐场"), "instant": ("🚀", "快速游戏"), "fishing": ("🐟", "捕鱼游戏")},
        "matches_h2": "即将开赛", "bet": "立即投注",
        "register": ("欢迎来到 __BRAND__ — 值得信赖的在线娱乐场", "如何注册", [
            ("📝", "创建账户", "点击立即加入并填写登录信息。"),
            ("💳", "存款", "通过网上银行、电子钱包或加密货币为账户充值。"),
            ("🎮", "开始游戏", "选择您喜爱的老虎机、真人牌桌或赛事。"),
            ("🎁", "领取奖励", "别忘了领取您符合条件的奖金。"),
        ]),
        "promos": ("每位玩家都有奖励", "优惠与奖金"),
        "app": ("下载应用", "游戏的未来已来。所有设备畅玩精彩游戏。",
                "下载 __BRAND__ 应用，访问更快、保存登录状态并即时接收通知。",
                ["支持 Android 和 iOS", "支持机型可使用面容或指纹登录", "与网站共用同一账户和钱包"], "下载应用"),
        "trust": ("游戏供应商", "支付方式"),
        "seo_intro": """<h1>__BRAND__ | 马来西亚值得信赖的在线娱乐场</h1>
<p>__BRAND__ 是面向亚洲（包括马来西亚）玩家的在线娱乐场品牌。一个账户即可畅玩老虎机、真人娱乐场、体育投注、捕鱼游戏、彩票和快速游戏，支持手机和电脑。本页介绍可玩内容、如何开始以及如何安全游戏。</p>""",
        "seo_more": """<h2>可玩游戏</h2>
<h3>老虎机</h3><p>来自知名工作室的视频老虎机、经典老虎机和累积奖池游戏。每次结果都是随机的，请视为娱乐。</p>
<h3>体育投注</h3><p>足球、篮球、网球、电子竞技等赛前及滚球盘口。</p>
<h3>真人娱乐场</h3><p>百家乐、轮盘、21 点和骰宝，由真人荷官高清直播。</p>
<h3>捕鱼与快速游戏</h3><p>街机风格捕鱼游戏，以及 crash、plinko、keno 等快节奏游戏。</p>
<h2>优惠与奖金</h2>
<p>常见优惠包括迎新奖金、续存奖金、现金返水和 VIP 计划。每项奖金都有流水要求和有效期，领取前请阅读条款。</p>
<h2>支付方式</h2>
<p>马来西亚玩家通常可通过 FPX、DuitNow、电子钱包、银行转账及部分加密货币存款。最低金额和处理时间在登录后的收银台显示。</p>
<h2>安全与理性娱乐</h2>
<p>请仅在登录官方网站后存款，切勿通过聊天联系人存款。设定预算、适时休息、切勿追损。博彩仅限 18 岁以上成年人。</p>""",
        "faq_h2": "__BRAND__ 马来西亚常见问题",
        "faq": [("如何在 __BRAND__ 注册？", "点击立即加入，填写用户名、密码、姓名和电话号码，验证信息后即可完成注册，只需几分钟。"),
                ("可以用手机玩吗？", "可以。您可以在手机浏览器中游戏，或下载 Android 和 iOS 应用。您的账户在所有设备上通用。"),
                ("如何存款？", "登录后打开收银台，选择网上银行、电子钱包或加密货币等方式。请仅通过官方网站存款，切勿通过聊天联系人存款。"),
                ("可以提取奖金吗？", "可以。在收银台申请提款。如有进行中的奖金，需先满足流水要求，且账户信息须与您的银行账户一致。"),
                ("在马来西亚网络博彩合法吗？", "各国网络博彩法律不同，马来西亚对此有所限制。您有责任了解并遵守适用的法律。博彩仅限 18 岁以上成年人。")],
    },
}

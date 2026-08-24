# -*- coding: utf-8 -*-
"""補助教材 Web版のHTMLを書き出す。

    python build.py ../site

出力は「素のHTML」なので、生成後はこのスクリプトなしで編集・公開できます。
"""
import sys, os, html
from content import PAGES, APPS, SITE, SUB, AUTHOR, VERSION

OUT = sys.argv[1] if len(sys.argv) > 1 else "../site"
APP_BY_FILE = {f: (t, d) for f, t, d in APPS}

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light">
<meta name="description" content="{desc}">
<meta name="author" content="{author}">
<meta property="og:type" content="article">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="{site}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=Zen+Old+Mincho:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">{extracss}
</head>
<body>
<a class="skip" href="#main">本文へスキップ</a>
<header class="sitehead">
  <div class="inner">
    <a href="{root}index.html">{site}</a>
    <span class="sub">{sub}</span>
  </div>
</header>
"""

FOOT = """<footer class="sitefoot">
  <div class="inner">
    <p>{site} ／ {sub}</p>
    <p>{author}　{version}</p>
    <p>このテキストは <a href="{root}license.html">クリエイティブ・コモンズ 表示-非営利-継承 4.0 国際（CC BY-NC-SA 4.0）</a> として公開しています。</p>
  </div>
</footer>
</body>
</html>
"""


def head(title, desc, root="", ogtitle=None, extracss=""):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), root=root,
                       site=html.escape(SITE), sub=html.escape(SUB), extracss=extracss,
                       author=html.escape(AUTHOR), ogtitle=html.escape(ogtitle or title))


def foot(root=""):
    return FOOT.format(site=html.escape(SITE), sub=html.escape(SUB),
                       author=html.escape(AUTHOR), version=VERSION, root=root)


def tryit(p):
    if not p["apps"]:
        return ""
    links = "\n".join(
        f'      <a class="btn{"" if i == 0 else " btn-ghost"}" href="{f}">{html.escape(APP_BY_FILE[f][0])}</a>'
        for i, f in enumerate(p["apps"]))
    return f"""
<aside class="tryit" aria-labelledby="tryit-{p['slug']}">
  <h3 id="tryit-{p['slug']}">やってみよう ― {html.escape(p['try_title'])}</h3>
  <p>{html.escape(p['try_desc'])}</p>
  <div class="links">
{links}
  </div>
</aside>
"""


def write(name, text):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("  ", name, f"({len(text.encode()):,} bytes)")


# --------------------------------------------------------------- 各トピック
print("トピックページ:")
for i, p in enumerate(PAGES):
    prev = PAGES[i - 1] if i > 0 else None
    nxt = PAGES[i + 1] if i < len(PAGES) - 1 else None

    pager = ['<nav class="pager" aria-label="ページ送り">']
    if prev:
        pager.append(f'  <a href="{prev["slug"]}.html"><span class="dir">← 前のページ</span>'
                     f'<span class="t">{html.escape(prev["title"])}</span></a>')
    else:
        pager.append('  <a href="index.html"><span class="dir">← もどる</span><span class="t">目次</span></a>')
    if nxt:
        pager.append(f'  <a class="next" href="{nxt["slug"]}.html"><span class="dir">次のページ →</span>'
                     f'<span class="t">{html.escape(nxt["title"])}</span></a>')
    else:
        pager.append('  <a class="next" href="license.html"><span class="dir">次のページ →</span>'
                     '<span class="t">ライセンス</span></a>')
    pager.append("</nav>")

    body = f"""<div class="page">
  <nav class="crumb" aria-label="現在位置">
    <a href="index.html">目次</a> ＞ {html.escape(p['title'])}
  </nav>
  <main id="main">
    <p class="kicker">第{i + 1}章</p>
    <h1>{html.escape(p['title'])}</h1>
    <p class="lead">{html.escape(p['lead'])}</p>
{p['body']}{tryit(p)}
  </main>
{chr(10).join(pager)}
</div>
"""
    write(f"{p['slug']}.html",
          head(f"{p['title']} ｜ {SITE}", p["desc"], ogtitle=p["title"]) + body + foot())

# --------------------------------------------------------------- 目次
toc = "\n".join(
    f'  <li><a href="{p["slug"]}.html"><span class="n" aria-hidden="true">{i + 1}</span>'
    f'<span class="t">{html.escape(p["title"])}</span>'
    f'<span class="d">{html.escape(p["desc"])}</span></a></li>'
    for i, p in enumerate(PAGES))

apps_list = "\n".join(
    f'  <li><a href="{f}"><span class="t">{html.escape(t)}</span>'
    f'<span class="d">{html.escape(d)}</span></a></li>'
    for f, t, d in APPS)

index_body = f"""<div class="page">
  <main id="main">
    <p class="kicker">高等学校 情報Ⅰ 補助教材</p>
    <h1>つくって、つたえる、みんなのために</h1>
    <p class="lead">
      情報アクセシビリティをはじめよう。<br>
      「見えにくい」「聞こえにくい」「操作しにくい」人にも情報を届けるために、
      作る側ができることを、体験しながら学ぶ教材です。
    </p>

    <h2 id="toc">目次</h2>
    <ul class="toc" aria-labelledby="toc">
{toc}
      <li><a href="license.html"><span class="n" aria-hidden="true">＊</span><span class="t">ライセンスについて</span><span class="d">CC BY-NC-SA 4.0 で公開しています。</span></a></li>
    </ul>

    <h2 id="apps">体験アプリ</h2>
    <p>ブラウザで動きます。インストールは要りません。スマートフォンやタブレットからもどうぞ。</p>
    <ul class="apps" aria-labelledby="apps">
{apps_list}
    </ul>

    <h2 id="print">印刷・PDF版</h2>
    <p>
      全トピックを1ページにまとめた
      <a href="print.html">印刷用ページ</a>
      を用意しています。ブラウザの「印刷」から「PDFに保存」を選ぶと、配布用のPDFが作れます。
    </p>

    <h2 id="about">この教材について</h2>
    <p>
      本教材は、高等学校情報科「情報Ⅰ」の学習内容を踏まえて作成しています。
      授業でのご利用については <a href="for-teachers.html">指導者の皆様へ</a> をご覧ください。
    </p>
    <div class="box point">
      <p class="box-title"><span class="ic" aria-hidden="true">★</span>この教材自身も、教材です</p>
      <p>
        このサイトと8本の体験アプリは、ここで教えている内容を実際に守って作られています。
        見出しタグの階層、表の <code>scope</code> 属性、リンクの下線、コントラスト比、キーボード操作。
        ブラウザの「ページのソースを表示」で、中身を確かめてみてください。
      </p>
    </div>
  </main>
</div>
"""
print("トップページ:")
write("index.html", head(f"{SITE} ｜ {SUB}",
                         "高等学校 情報Ⅰ の補助教材。情報アクセシビリティを、8本の体験アプリで学べます。",
                         ogtitle=SITE) + index_body + foot())

# --------------------------------------------------------------- ライセンス
lic_body = f"""<div class="page">
  <nav class="crumb" aria-label="現在位置"><a href="index.html">目次</a> ＞ ライセンスについて</nav>
  <main id="main">
    <h1>ライセンスについて</h1>
    <p class="lead">
      このテキストは <strong>クリエイティブ・コモンズ 表示-非営利-継承 4.0 国際（CC BY-NC-SA 4.0）</strong>
      として公開していますので、条件に従って使用してください。
    </p>

    <h2>このライセンスでできること</h2>
    <p>
      原作者のクレジット（氏名、作品タイトルなど）を表示し、かつ非営利目的に限り、
      また改変を行った際には元の作品と同じ組み合わせのCCライセンスで公開することを主な条件に、
      <strong>改変したり再配布したりすることができます</strong>。
    </p>

    <div class="tablewrap">
    <table>
      <caption>CC BY-NC-SA 4.0 の3つの条件</caption>
      <thead><tr><th scope="col">記号</th><th scope="col">条件</th><th scope="col">内容</th></tr></thead>
      <tbody>
        <tr><th scope="row">BY</th><td>表示</td><td>原作者のクレジットを表示してください。</td></tr>
        <tr><th scope="row">NC</th><td>非営利</td><td>営利目的での利用はできません。</td></tr>
        <tr><th scope="row">SA</th><td>継承</td><td>改変したものは、同じライセンスで公開してください。</td></tr>
      </tbody>
    </table>
    </div>

    <h2>クレジットの書き方（例）</h2>
    <pre><code>「つくって、つたえる、みんなのために ― 情報アクセシビリティをはじめよう」
{AUTHOR}（清泉大学）
CC BY-NC-SA 4.0</code></pre>

    <h2>教材の内容について</h2>
    <p>{AUTHOR}　{VERSION}</p>
    <p>
      ライセンスの詳細は「クリエイティブ・コモンズ 表示-非営利-継承 4.0 国際」で検索してご確認ください。
    </p>
  </main>
  <nav class="pager" aria-label="ページ送り">
    <a href="{PAGES[-1]['slug']}.html"><span class="dir">← 前のページ</span><span class="t">{html.escape(PAGES[-1]['title'])}</span></a>
    <a class="next" href="index.html"><span class="dir">もどる →</span><span class="t">目次</span></a>
  </nav>
</div>
"""
print("ライセンス:")
write("license.html", head(f"ライセンスについて ｜ {SITE}",
                          "CC BY-NC-SA 4.0 で公開しています。", ogtitle="ライセンスについて") + lic_body + foot())

# --------------------------------------------------------------- 印刷用
# 1ページに全部載せるので、見出しを1段ずつ下げて階層をそろえる
def demote(body):
    for a, b in (("<h4", "<h5"), ("</h4>", "</h5>"),
                 ("<h3", "<h4"), ("</h3>", "</h4>"),
                 ("<h2", "<h3"), ("</h2>", "</h3>")):
        body = body.replace(a, b)
    return body


sections = []
for i, p in enumerate(PAGES):
    sections.append(f"""<section class="print-section" aria-labelledby="s-{p['slug']}">
    <h2 id="s-{p['slug']}">{i + 1}. {html.escape(p['title'])}</h2>
    <p class="lead">{html.escape(p['lead'])}</p>
{demote(p['body'])}
  </section>
""")

print_toc = "\n".join(
    f'      <li><a href="#s-{p["slug"]}">{html.escape(p["title"])}</a></li>' for p in PAGES)

print_body = f"""<div class="page">
  <main id="main">
    <section class="print-section">
      <p class="kicker">高等学校 情報Ⅰ 補助教材</p>
      <h1>つくって、つたえる、みんなのために<br>― 情報アクセシビリティをはじめよう</h1>
      <p class="lead">{AUTHOR}　{VERSION}</p>

      <div class="box info no-print">
        <p class="box-title"><span class="ic" aria-hidden="true">i</span>このページの使い方</p>
        <p>
          全トピックを1ページにまとめた印刷用ページです。
          ブラウザの「印刷」（<kbd>Ctrl</kbd>＋<kbd>P</kbd> ／ <kbd>⌘</kbd>＋<kbd>P</kbd>）から
          「PDFに保存」を選ぶと、配布用のPDFが作れます。
          用紙はA4縦、余白は「標準」、「背景のグラフィック」はオフのままで構いません。
        </p>
      </div>

      <h2>目次</h2>
      <ol>
{print_toc}
      </ol>

      <p class="no-print"><a href="index.html">← Web版の目次にもどる</a></p>
    </section>

{"".join(sections)}
    <section class="print-section">
      <h2>体験アプリ</h2>
      <p>次のURLをブラウザで開くと、教材に対応した体験アプリが動きます。</p>
      <div class="tablewrap">
      <table>
        <caption>体験アプリ一覧</caption>
        <thead><tr><th scope="col">アプリ</th><th scope="col">内容</th><th scope="col">ファイル名</th></tr></thead>
        <tbody>
{chr(10).join(f'          <tr><th scope="row">{html.escape(t)}</th><td>{html.escape(d)}</td><td><code>{f}</code></td></tr>' for f, t, d in APPS)}
        </tbody>
      </table>
      </div>
    </section>

    <section class="print-section">
      <h2>ライセンスについて</h2>
      <p>
        このテキストは <strong>クリエイティブ・コモンズ 表示-非営利-継承 4.0 国際（CC BY-NC-SA 4.0）</strong>
        として公開していますので、条件に従って使用してください。
      </p>
      <p>
        原作者のクレジット（氏名、作品タイトルなど）を表示し、かつ非営利目的に限り、
        また改変を行った際には元の作品と同じ組み合わせのCCライセンスで公開することを主な条件に、
        改変したり再配布したりすることができます。
      </p>
      <p>{AUTHOR}　{VERSION}</p>
    </section>
  </main>
</div>
"""
print("印刷用:")
PRINT_CSS = """
<style>
  /* 印刷用ページ：章の h2 を「章タイトル」として組む */
  .print-section > h2{
    max-width:none; margin:0 0 .1em; padding:0; border:0;
    font-weight:900; letter-spacing:.04em;
    font-size:clamp(1.5rem,1.2rem+1.4vw,2.1rem); line-height:1.45;
  }
  .print-section > h2::after{
    content:""; display:block; width:3.2em; height:3px;
    background:var(--shu); margin:.55em 0 0;
  }
  .print-section + .print-section{ margin-top:76px; padding-top:44px; border-top:3px double var(--ink); }
  @media print{
    .print-section > h2{ font-size:17pt; border:0; }
    .print-section > h2::after{ background:none; height:0; border-top:2pt solid #000; }
    .print-section + .print-section{ margin-top:0; padding-top:0; border-top:0; }
  }
</style>"""
write("print.html", head(f"印刷用（全文） ｜ {SITE}",
                        "全トピックを1ページにまとめた印刷・PDF用のページです。",
                        ogtitle="印刷用（全文）", extracss=PRINT_CSS) + print_body + foot())

# --------------------------------------------------------------- 404
nf = """<div class="page">
  <main id="main">
    <h1>ページが見つかりませんでした</h1>
    <p class="lead">お探しのページは、移動または削除された可能性があります。</p>
    <p><a href="index.html">教材の目次にもどる</a></p>
  </main>
</div>
"""
print("その他:")
write("404.html", head(f"ページが見つかりません ｜ {SITE}", "お探しのページは見つかりませんでした。",
                       ogtitle="ページが見つかりません") + nf + foot())
write(".nojekyll", "")

# 共通スタイルシート（このスクリプトと同じ場所にある style.css をコピーします）
_css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css, encoding="utf-8") as f:
        write(os.path.join("assets", "style.css"), f.read())

print("\n完了：", os.path.abspath(OUT))

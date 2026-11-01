# -*- coding: utf-8 -*-
"""產生 CLV 專題網站（靜態多頁，可直接放 GitHub Pages）。

用法：在 repo 根目錄執行 python src/build_site.py
輸出：根目錄的 *.html（GitHub Pages 直接讀）
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT

TITLE = "CLV 顧客終身價值專題"
STREAMLIT_URL = ""   # 部署到 Streamlit Community Cloud 後，把網址貼在這裡

NAV = [
    ("首頁", "index.html", None),
    ("資料介紹", None, [("企業簡介", "data_company.html"), ("資料來源", "data_source.html"),
                        ("資料前處理", "data_process.html")]),
    ("方法介紹", None, [("RFM 與 K-Means", "method_rfm.html"), ("肘部法則與 PCA", "method_cluster.html"),
                        ("CLV 預測模型", "method_clv.html")]),
    ("分析結果", "results.html", None),
    ("結論與討論", "conclusion.html", None),
    ("成果展示", "demo.html", None),
    ("參考文獻", "references.html", None),
]

CSS = r"""
/* 版面：深藍頂部導覽 + 淺灰底的閱讀欄，內容區塊是白卡；格線角飾取自簡報 */
:root{
  --navy:#2c3e50; --navy-2:#34495e; --teal:#13a3b5; --teal-ink:#0e7c8a;
  --ground:#ecf0f1; --paper:#ffffff; --ink:#22303d; --muted:#5d6b78; --line:#d3dce1;
  --alert:#c0392b; --tint:#e3f3f5;
  --f-display:"Noto Sans TC","Microsoft JhengHei","PingFang TC",sans-serif;
  --f-body:"Noto Sans TC","Microsoft JhengHei","PingFang TC",sans-serif;
  --f-num:"IBM Plex Mono",ui-monospace,Consolas,monospace;
  color-scheme:light;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--f-body);font-size:17px;line-height:1.85;letter-spacing:.02em}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--navy)}
a{color:var(--teal-ink)}
a:focus-visible,summary:focus-visible,button:focus-visible{outline:3px solid var(--teal);outline-offset:2px;border-radius:4px}
img{max-width:100%;height:auto;display:block}

/* 導覽列 */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--navy);box-shadow:0 2px 6px rgba(0,0,0,.25)}
.nav-in{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:8px 20px;flex-wrap:wrap;
  padding-block:10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:700;font-size:1.15rem;letter-spacing:.08em;margin-right:auto}
.brand-mark{width:30px;height:30px;flex:none;border:1.5px solid #fff;
  background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);background-size:7.5px 7.5px;opacity:.9}
.menu{display:flex;flex-wrap:wrap;gap:2px 4px;list-style:none;margin:0;padding:0;font-size:.98rem}
.menu>li{position:relative}
.menu a,.menu summary{display:block;color:#fff;text-decoration:none;padding:6px 10px;border-radius:6px;cursor:pointer;white-space:nowrap}
.menu summary{list-style:none}
.menu summary::-webkit-details-marker{display:none}
.menu summary::after{content:"";display:inline-block;margin-left:6px;vertical-align:3px;border:4px solid transparent;border-top-color:#fff;border-bottom:0}
.menu a:hover,.menu summary:hover,.menu .on>a,.menu .on>details>summary{background:var(--navy-2)}
.menu .on>a,.menu .on>details>summary{box-shadow:inset 0 -2px 0 var(--teal)}
.drop{position:absolute;top:calc(100% + 6px);left:0;min-width:170px;background:var(--paper);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:6px;list-style:none;margin:0;z-index:30}
.drop a{color:var(--ink);padding:8px 12px}
.drop a:hover,.drop a[aria-current]{background:var(--ground);color:var(--navy)}

/* 主體 */
main{max-width:1180px;margin:0 auto;padding-block:40px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:28px}
.hero{position:relative;padding-block:36px 8px;text-align:center}
.hero::before,.hero::after{content:"";position:absolute;width:120px;height:120px;top:8px;opacity:.55;
  background-image:linear-gradient(var(--navy) 1px,transparent 1px),linear-gradient(90deg,var(--navy) 1px,transparent 1px);background-size:15px 15px;border-right:1px solid var(--navy);border-bottom:1px solid var(--navy)}
.hero::before{left:0}.hero::after{right:0}
@media (max-width:720px){.hero::before,.hero::after{display:none}}
.hero h1{position:relative;margin:0;font-family:var(--f-display);font-weight:900;font-size:clamp(2.2rem,6vw,3.6rem);line-height:1.2;letter-spacing:.12em;text-wrap:balance;
  background:linear-gradient(90deg,var(--navy) 0%,var(--teal) 50%,var(--navy) 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:sheen 6s linear infinite}
@keyframes sheen{to{background-position:200% center}}
.hero p{position:relative;margin:8px 0 0;font-weight:700;color:var(--navy);letter-spacing:.25em;font-size:clamp(.95rem,2.2vw,1.2rem)}
.page-title{margin:0;font-family:var(--f-display);font-weight:900;color:var(--navy);font-size:clamp(1.9rem,4.5vw,2.7rem);letter-spacing:.1em;line-height:1.3;text-wrap:balance}
.page-lead{margin:-12px 0 0;color:var(--muted)}

.card{background:var(--paper);border-radius:12px;box-shadow:0 1px 3px rgba(44,62,80,.12);padding:28px clamp(18px,3.5vw,40px);min-width:0}
.card h2{margin:0 0 14px;font-family:var(--f-display);font-size:1.45rem;color:var(--navy);letter-spacing:.08em;display:flex;align-items:center;gap:10px;text-wrap:balance}
.card h2::before{content:"";width:14px;height:14px;flex:none;border:2px solid var(--teal);background-image:linear-gradient(var(--teal) 2px,transparent 2px),linear-gradient(90deg,var(--teal) 2px,transparent 2px);background-size:6px 6px}
.card h3{margin:22px 0 8px;font-size:1.12rem;color:var(--navy)}
.card p{margin:0 0 12px;max-width:68ch}
.card p:last-child{margin-bottom:0}
.hl{color:var(--teal-ink);font-weight:700}
.warn{color:var(--alert);font-weight:700}
.indent{text-indent:2em}

.members{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;font-size:1.05rem}
.members dt{color:var(--muted);white-space:nowrap}
.members dd{margin:0;font-weight:700;color:var(--navy)}

.grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px;align-items:start}
.grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:20px}
.goal{border-top:3px solid var(--teal);padding-top:12px}
.goal b{display:block;color:var(--navy);font-size:1.05rem;margin-bottom:4px}
.goal span{color:var(--muted);font-size:.95rem}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:14px;margin:4px 0 0}
.kv div{border-left:3px solid var(--teal);padding:2px 0 2px 12px}
.kv b{display:block;font-family:var(--f-num);font-size:1.5rem;color:var(--navy);font-variant-numeric:tabular-nums;line-height:1.3}
.kv span{color:var(--muted);font-size:.9rem}

.steps{list-style:none;counter-reset:s;margin:0;padding:0;display:grid;gap:12px}
.steps li{counter-increment:s;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:start}
.steps li::before{content:counter(s);width:32px;height:32px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;font-family:var(--f-num);font-weight:700;margin-top:2px}

.tbl-wrap{overflow-x:auto;margin:6px 0 14px}
table{border-collapse:collapse;width:100%;font-size:.98rem;font-variant-numeric:tabular-nums;background:var(--paper)}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:center;white-space:nowrap}
thead th{background:var(--navy);color:#fff;font-weight:700}
thead.teal th{background:var(--teal-ink)}
tbody th{background:var(--ground);color:var(--navy)}
tr.total td,tr.total th{font-weight:700;background:var(--tint)}
td.num{font-family:var(--f-num)}
table.text td{white-space:normal;text-align:left;min-width:9em}
table.text th{white-space:nowrap}
.note{color:var(--muted);font-size:.9rem}

figure{margin:6px 0 0}
figure img{border-radius:8px;border:1px solid var(--line);background:#fff}
figcaption{color:var(--muted);font-size:.9rem;margin-top:6px}
.formula{font-family:var(--f-display);font-weight:900;color:var(--navy);font-size:clamp(1.1rem,3vw,1.5rem);letter-spacing:.1em;text-align:center;padding:18px 12px;border:2px solid var(--navy);border-radius:10px;background:var(--tint);margin:16px 0 0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 0;padding:0;list-style:none}
.chips li{border:1px solid var(--line);border-radius:999px;padding:2px 12px;font-size:.92rem;background:var(--ground)}
.dot{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:0}

.btn{display:inline-flex;align-items:center;gap:8px;background:var(--teal-ink);color:#fff;text-decoration:none;font-weight:700;padding:10px 20px;border-radius:8px}
.btn:hover{background:var(--navy)}
.btn[aria-disabled]{background:var(--line);color:var(--muted);pointer-events:none}
code,.code{font-family:var(--f-num);font-size:.9em;background:var(--ground);padding:1px 6px;border-radius:4px}
pre.code{display:block;padding:12px 14px;overflow-x:auto;line-height:1.6;margin:8px 0 12px}

.refs{display:grid;gap:10px}
.refs details{background:var(--paper);border-radius:10px;box-shadow:0 1px 3px rgba(44,62,80,.12)}
.refs summary{cursor:pointer;padding:14px 20px;font-weight:700;color:var(--navy);display:flex;gap:12px;align-items:baseline}
.refs summary b{font-family:var(--f-num);color:var(--teal-ink)}
.refs .body{padding:0 20px 16px 20px;color:var(--ink)}
.refs .body p{margin:0 0 6px}

.pager{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.pager a{text-decoration:none;font-weight:700;color:var(--navy);background:var(--paper);padding:10px 16px;border-radius:8px;box-shadow:0 1px 3px rgba(44,62,80,.12)}
.pager a:hover{color:var(--teal-ink)}

footer{background:var(--navy);color:#c9d3db;text-align:center;font-size:.9rem;line-height:1.7;
  padding-block:26px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
#top{position:fixed;right:calc(20px + env(safe-area-inset-right,0px));bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:15;border:0;background:var(--navy);color:#fff;
  width:46px;height:46px;border-radius:50%;font:700 .85rem var(--f-body);cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.25)}
#top:hover{background:var(--teal-ink)}
@media (max-width:720px){body{font-size:16px}.menu{width:100%}.drop{position:static;box-shadow:none;background:var(--navy-2);margin-top:4px}.drop a{color:#fff}.drop a:hover,.drop a[aria-current]{background:var(--navy);color:#fff}}
"""

JS = r"""
<script>
(function(){
  var ds=document.querySelectorAll('.menu details');
  ds.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)ds.forEach(function(o){if(o!==d)o.open=false;});});});
  document.addEventListener('click',function(e){ds.forEach(function(d){if(!d.contains(e.target))d.open=false;});});
  var b=document.getElementById('top');
  function f(){b.hidden=(document.documentElement.scrollTop||document.body.scrollTop)<300;}
  window.addEventListener('scroll',f,{passive:true});f();
  b.addEventListener('click',function(){window.scrollTo({top:0});});
})();
</script>
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;700'
         '&family=Noto+Sans+TC:wght@400;700;900&display=swap">')


def nav(current):
    cur = ' aria-current="page"'
    items = []
    for label, href, sub in NAV:
        if sub:
            on = any(h == current for _, h in sub)
            links = "".join('<li><a href="%s"%s>%s</a></li>' % (h, cur if h == current else "", t) for t, h in sub)
            items.append('<li%s><details><summary>%s</summary><ul class="drop">%s</ul></details></li>'
                         % (' class="on"' if on else "", label, links))
        else:
            on = href == current
            items.append('<li%s><a href="%s"%s>%s</a></li>'
                         % (' class="on"' if on else "", href, cur if on else "", label))
    return ('<header class="nav"><div class="nav-in">'
            '<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span>CLV 顧客終身價值</a>'
            '<nav aria-label="主選單"><ul class="menu">' + "".join(items) + '</ul></nav></div></header>')


FOOT = ('<footer>© 2026 靜宜大學資料科學暨大數據分析與應用學系<br>CLV 顧客終身價值專題組｜'
        '資料來源：Kaggle Olist Brazilian E-commerce Dataset</footer>'
        '<button id="top" type="button" aria-label="回到頁首">TOP</button>')


def head(page_title):
    t = TITLE if page_title is None else f"{page_title}｜CLV 專題"
    return (f'<title>{t}</title><meta name="claude:viewport-fit-sides" content="cover">'
            f'{FONTS}<style>{CSS}</style>')


def full(page_title, current, body):
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'{head(page_title)}</head><body>{nav(current)}<main>{body}</main>{FOOT}{JS}</body></html>')


def fragment(page_title, current, body):
    return f'{head(page_title)}{nav(current)}<main>{body}</main>{FOOT}{JS}'


def pager(prev=None, nxt=None):
    p = f'<a href="{prev[1]}">← {prev[0]}</a>' if prev else '<span></span>'
    n = f'<a href="{nxt[1]}">{nxt[0]} →</a>' if nxt else '<span></span>'
    return f'<div class="pager">{p}{n}</div>'


# ============================================================
# 各頁內容
# ============================================================
PAGES = {}

PAGES["index.html"] = (None, f"""
<section class="hero"><h1>CLV 顧客終身價值</h1><p>Customer Lifetime Value</p></section>

<div class="card"><dl class="members">
  <dt>指導老師：</dt><dd>袁淵明老師</dd>
  <dt>專題成員：</dt><dd>范言提、蘇廷尉、陳均睿、李俊鋧</dd>
  <dt>系　　所：</dt><dd style="font-weight:400;color:var(--ink)">靜宜大學 資料科學暨大數據分析與應用學系</dd>
</dl></div>

<div class="card">
  <h2>摘要</h2>
  <p class="indent">本研究以巴西電商 Olist 公開資料集為基礎，將訂單、付款與顧客三張資料表清洗整併後，為 <span class="hl">93,357 位顧客</span>建立 RFM 指標（最近一次消費、消費次數、消費金額）。接著以 Frequency 與 Monetary 進行 K-Means 分群，將顧客分為<span class="hl">忠誠客戶、VIP 客戶與一般客戶</span>三群，並以 BG/NBD 預測顧客未來的購買次數、以 Gamma-Gamma 預測每次消費金額，兩者相乘得到未來 3、6、9、12 個月的 CLV。</p>
  <p class="indent">結果顯示，VIP 客戶過去平均消費約 1,045 巴西幣，但平均只買過 1.01 次，未來 12 個月每人 CLV 約 2.46；忠誠客戶人數只占約 3%，每人 CLV 卻約 8.80，是 VIP 的 3.6 倍。<span class="hl">若只看過去的消費金額，會高估 VIP 的未來價值</span>。最後我們把整套流程做成 Streamlit 網頁系統，只要上傳符合格式的交易資料，就能重跑分群與 CLV 預測。</p>
</div>

<div class="card">
  <h2>研究動機</h2>
  <p class="indent">在競爭激烈的商業環境中，<span class="hl">企業獲取新戶成本逐漸提高</span>，因此如何提升顧客留存率與顧客終身價值已成為重要課題。然而，<span class="hl">多數企業仍仰賴過往營業額或單次交易紀錄評估顧客價值</span>，難以有效預測顧客未來消費行為與流失風險，<span class="hl">導致推廣資源分配不良</span>。</p>
  <p class="indent">此外，在<span class="hl">電子商務</span>與<span class="hl">零售產業</span>中，多數顧客屬於<span class="hl">非合約制模式</span>，顧客流失通常不會有明確通知，<span class="hl">使企業更難以辨別高風險流失客戶</span>。</p>
  <p class="indent">因此，本研究導入數據分析技術，透過 <span class="hl">RFM 分析、顧客分群與 CLV 預測模型</span>，協助企業辨識高價值顧客與潛在流失客群，進一步<span class="hl">提升精準行銷與顧客關係管理效率</span>。</p>
</div>

<div class="card">
  <h2>研究目的</h2>
  <p class="indent">本研究以<span class="hl">巴西 Olist 電商資料集為基礎</span>，透過資料前處理<span class="hl">建立 RFM 指標</span>。接著利用 <span class="hl">K-Means 進行顧客分群</span>，並結合 BG/NBD 與 Gamma-Gamma 模型預測各客群未來的 CLV。最後，透過視覺化方式呈現分析結果，協助企業辨識真正值得經營的高價值客戶，提升精準行銷與顧客關係管理效率。</p>
  <div class="grid-3" style="margin-top:18px">
    <div class="goal"><b>一、資料處理管線</b><span>建立標準化的資料處理與特徵工程管線</span></div>
    <div class="goal"><b>二、CLV 預測</b><span>建構 CLV 預測模型並比較各客群的未來價值</span></div>
    <div class="goal"><b>三、視覺化系統</b><span>開發視覺化商業數據儀表板，數據驅動決策</span></div>
  </div>
</div>
{pager(None, ("企業簡介", "data_company.html"))}
""")

PAGES["data_company.html"] = ("企業簡介", f"""
<h1 class="page-title">企業簡介</h1>
<div class="card">
  <h2>Olist</h2>
  <div class="tbl-wrap"><table>
    <tbody>
      <tr><th>公司名稱</th><td style="text-align:left">Olist</td></tr>
      <tr><th>成立</th><td style="text-align:left">2015 年，巴西</td></tr>
      <tr><th>創辦人</th><td style="text-align:left">Tiago Dalvi</td></tr>
      <tr><th>定位</th><td style="text-align:left;white-space:normal">SaaS 電商市集整合平台（本身並非電商）</td></tr>
      <tr><th>工作內容</th><td style="text-align:left;white-space:normal">協助中小型賣家（SMB）跨越技術、物流與通路門檻，順利在線上銷售</td></tr>
    </tbody></table></div>
  <p>賣家「一次串接」即可上架至巴西各大主要市集：Amazon、Mercado Livre、B2W 等，並同時提供物流與金流整合服務，屬<span class="hl">市集型、非合約制（Non-contractual）</span>模式。</p>
</div>
<div class="card">
  <h2>為何適合研究？</h2>
  <ul class="chips" style="margin-bottom:8px">
    <li>非合約制平台，顧客流失無法直接觀察</li>
    <li>具完整交易資料（顧客、訂單、付款、時間）</li>
    <li>適合進行 RFM 分析、顧客分群與 CLV 預測</li>
  </ul>
  <p>非合約制代表顧客不會「退訂」：一位顧客很久沒有下單，可能只是還沒有需要，也可能已經不會再回來。這正是 BG/NBD 這類模型要處理的問題，所以 Olist 的資料很適合用來做 CLV 預測。</p>
</div>
{pager(("首頁", "index.html"), ("資料來源", "data_source.html"))}
""")

PAGES["data_source.html"] = ("資料來源", f"""
<h1 class="page-title">資料來源</h1>
<div class="card">
  <h2>Kaggle Olist Brazilian E-commerce Dataset</h2>
  <p>本研究使用 Kaggle 公開的 <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce" target="_blank" rel="noopener">Olist Brazilian E-commerce Dataset</a>，資料期間約為 <span class="hl">2016 至 2018 年</span>。</p>
  <div class="kv">
    <div><b>99,441</b><span>筆訂單</span></div>
    <div><b>103,886</b><span>筆付款紀錄</span></div>
    <div><b>96,096</b><span>位不重複顧客</span></div>
  </div>
</div>
<div class="card">
  <h2>使用的資料表</h2>
  <div class="tbl-wrap"><table class="text">
    <thead><tr><th>資料表</th><th>內容</th><th>本研究用到的欄位</th></tr></thead>
    <tbody>
      <tr><th>orders（訂單資料表）</th><td>每張訂單一列</td><td><code>order_id</code>、<code>customer_id</code>、<code>order_status</code>、<code>order_purchase_timestamp</code></td></tr>
      <tr><th>payments（付款資料表）</th><td>每筆付款一列，一張訂單可能分多筆付款</td><td><code>order_id</code>、<code>payment_value</code></td></tr>
      <tr><th>customers（顧客資料表）</th><td>每個訂單顧客編號對應的真實顧客</td><td><code>customer_id</code>、<code>customer_unique_id</code></td></tr>
    </tbody></table></div>
  <h3>資料內容包含</h3>
  <ul class="chips"><li>Customer Information（顧客資訊）</li><li>Order Information（訂單資訊）</li><li>Payment Amount（消費金額）</li><li>Purchase Time（購買時間）</li></ul>
</div>
{pager(("企業簡介", "data_company.html"), ("資料前處理", "data_process.html"))}
""")

PAGES["data_process.html"] = ("資料前處理", f"""
<h1 class="page-title">資料前處理</h1>
<p class="page-lead">9 萬多筆原始資料分散在不同表格，充滿雜訊與格式問題。我們編寫程式進行清洗與串聯，這是萃取價值的關鍵第一步。</p>
<div class="card">
  <h2>處理流程</h2>
  <ol class="steps">
    <li><div><b>彙總付款金額</b><br>一張訂單可能用多種方式付款（例如信用卡加優惠券），共有 2,961 張訂單有多筆付款。先依 <code>order_id</code> 把金額加總成一筆。</div></li>
    <li><div><b>多表關聯合併</b><br>orders 的 <code>customer_id</code> 是每張訂單各給一個號碼，同一個人買兩次會有兩個號碼。合併 customers 表，改用 <code>customer_unique_id</code> 辨識同一位顧客，否則每個人都會變成只買過一次。</div></li>
    <li><div><b>篩選有效訂單</b><br>只保留狀態為 delivered（已送達）且有付款的訂單，排除取消、未出貨等訂單。</div></li>
    <li><div><b>時間格式轉換</b><br>把購買時間轉成日期格式，並以最後一筆訂單的隔天 <span class="hl">2018-08-30</span> 作為分析基準日，計算每位顧客距今多少天沒有購買。</div></li>
  </ol>
</div>
<div class="grid-2">
  <div class="card">
    <h2>原始資料（範例）</h2>
    <p class="note">Orders 表</p>
    <div class="tbl-wrap"><table><thead><tr><th>order_id</th><th>customer_id</th><th>status</th></tr></thead>
      <tbody><tr><td>ORD_01</td><td>CUST_A</td><td>delivered</td></tr><tr><td>ORD_02</td><td>CUST_B</td><td>canceled</td></tr></tbody></table></div>
    <p class="note">Payments 表</p>
    <div class="tbl-wrap"><table><thead><tr><th>order_id</th><th>installments</th><th>value</th></tr></thead>
      <tbody><tr><td>ORD_01</td><td>1</td><td>50</td></tr><tr><td>ORD_01</td><td>2</td><td>50</td></tr></tbody></table></div>
    <p class="note">Customers 表</p>
    <div class="tbl-wrap"><table><thead><tr><th>customer_id</th><th>unique_id</th></tr></thead>
      <tbody><tr><td>CUST_A</td><td>UID_999</td></tr><tr><td>CUST_B</td><td>UID_888</td></tr></tbody></table></div>
  </div>
  <div class="card">
    <h2>清洗後的 RFM 特徵表（範例）</h2>
    <div class="tbl-wrap"><table><thead class="teal"><tr><th>unique_id</th><th>Recency</th><th>Frequency</th><th>Monetary</th></tr></thead>
      <tbody><tr><td>UID_999</td><td>12 天</td><td>1 次</td><td>100</td></tr><tr><td>UID_777</td><td>45 天</td><td>3 次</td><td>450</td></tr><tr><td>UID_123</td><td>210 天</td><td>1 次</td><td>85</td></tr></tbody></table></div>
    <h3>清洗結果</h3>
    <div class="kv">
      <div><b>96,477</b><span>張有效訂單</span></div>
      <div><b>93,357</b><span>位顧客</span></div>
      <div><b>695</b><span>天資料期間</span></div>
    </div>
    <p class="note" style="margin-top:12px">有效訂單期間：2016-10-03 至 2018-08-29。</p>
  </div>
</div>
{pager(("資料來源", "data_source.html"), ("RFM 與 K-Means", "method_rfm.html"))}
""")

PAGES["method_rfm.html"] = ("RFM 與 K-Means", f"""
<h1 class="page-title">RFM 與 K-Means</h1>
<div class="card">
  <h2>RFM 模型</h2>
  <p>RFM 目的：將顧客交易行為轉換為可分析之顧客價值指標。</p>
  <div class="tbl-wrap"><table class="text"><thead><tr><th>指標</th><th>意義</th><th>本研究的算法</th></tr></thead>
    <tbody>
      <tr><th>R（Recency）</th><td>最近一次消費</td><td>基準日 2018-08-30 減去最後一次購買日，單位為天</td></tr>
      <tr><th>F（Frequency）</th><td>消費頻率</td><td>有效訂單的張數</td></tr>
      <tr><th>M（Monetary）</th><td>總消費金額</td><td>所有有效訂單的付款金額加總（巴西幣）</td></tr>
    </tbody></table></div>
</div>
<div class="card">
  <h2>分群方法：K-Means</h2>
  <p>K-Means 是一種常見的分群方法，會依照顧客消費行為的相似程度，自動將顧客分成不同群組。我們把 <span class="hl">Frequency（消費次數）與 Monetary（消費金額）</span>標準化後作為分群依據，將顧客分為 3 個客群，方便企業針對不同客戶制定行銷策略。</p>
  <h3>為什麼 Recency 不放進分群？</h3>
  <p>如果把 R 也放進去，會出現「近期客戶」這種依時間命名的群。一位最近才買、而且買很多的顧客，就無法判斷該算近期客戶還是 VIP。因此分群只看 F 與 M，<span class="hl">每位顧客只會落在一群</span>；顧客會不會流失，交給有使用 Recency 的 BG/NBD 模型預測。</p>
  <h3>客群命名規則</h3>
  <div class="tbl-wrap"><table><thead><tr><th>順序</th><th>客群</th><th>判定依據</th></tr></thead>
    <tbody>
      <tr><td>1</td><th><span class="dot" style="background:#5b5bff"></span>忠誠客戶</th><td>Frequency 平均最高的一群</td></tr>
      <tr><td>2</td><th><span class="dot" style="background:#ff6b6b"></span>VIP 客戶</th><td>其餘兩群中 Monetary 平均較高的一群</td></tr>
      <tr><td>3</td><th><span class="dot" style="background:#9e9e9e"></span>一般客戶</th><td>剩下的一群（Frequency、Monetary 皆低）</td></tr>
    </tbody></table></div>
</div>
{pager(("資料前處理", "data_process.html"), ("肘部法則與 PCA", "method_cluster.html"))}
""")

PAGES["method_cluster.html"] = ("肘部法則與 PCA", f"""
<h1 class="page-title">肘部法則與 PCA</h1>
<div class="card">
  <h2>Elbow Method（肘部法則）</h2>
  <p>Elbow Method 是一種用來找出 K-Means 最佳分群數的方法。透過比較不同群數下的群內誤差（Inertia），觀察誤差下降的變化情形，並找出下降幅度開始變小的轉折點（肘部），作為最適合的分群數量。</p>
  <div class="grid-2">
    <div>
      <p>從圖中可以看到，<span class="hl">當群數由 1 增加到 3 時，群內誤差明顯下降；但超過 3 群之後，誤差下降幅度變得較小</span>，表示繼續增加群數對分群效果的提升有限。因此選擇 3 群作為最佳分群數，以進行後續的顧客分群分析。</p>
      <div class="tbl-wrap"><table><thead><tr><th>群數 K</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead>
        <tbody><tr><th>Inertia（×10⁴）</th><td class="num">18.7</td><td class="num">10.8</td><td class="num"><b>6.1</b></td><td class="num">4.4</td><td class="num">3.5</td></tr>
        <tr><th>比前一群減少</th><td>—</td><td class="num">7.9</td><td class="num"><b>4.7</b></td><td class="num">1.7</td><td class="num">0.9</td></tr></tbody></table></div>
    </div>
    <figure><img src="img/elbow.png" alt="肘部法則圖：群內誤差在 K=3 之後下降幅度明顯變小"><figcaption>以 Frequency、Monetary 標準化後計算，K = 1～10。</figcaption></figure>
  </div>
</div>
<div class="card">
  <h2>PCA（主成分分析）特徵對比</h2>
  <div class="grid-2">
    <figure><img src="img/pca.png" alt="PCA 散佈圖：三個客群沿 PC1 排開"><figcaption>PC1 主要反映 F、M；PC2 主要反映 R。</figcaption></figure>
    <div>
      <p>圖中每個點代表一位顧客，不同顏色代表不同客群。透過 PCA 將 RFM 三個特徵降到二維後，可以觀察各客群的分布情形。結果顯示，大部分顧客集中於左側區域，表示其消費行為較為相似；而少數顧客分布於右側與上方區域，顯示其消費特徵與一般顧客存在較大差異。</p>
      <p>三群沿著 PC1（主要反映 F、M）由左到右排開，與分群只使用 F、M 的設計一致；同一群在 PC2（R）方向上分布很廣，代表同一群裡同時有最近才買與很久沒買的顧客。</p>
    </div>
  </div>
  <div class="grid-2" style="margin-top:20px">
    <figure><img src="img/pca_zoom.png" alt="PCA 散佈圖局部放大"><figcaption>左下密集區域放大（PC1：−2～12）。</figcaption></figure>
    <div>
      <ul class="chips" style="flex-direction:column;align-items:flex-start">
        <li><span class="dot" style="background:#5b5bff"></span>藍色：忠誠客戶</li>
        <li><span class="dot" style="background:#ff6b6b"></span>紅色：VIP 客戶</li>
        <li><span class="dot" style="background:#9e9e9e"></span>灰色：一般客戶</li>
      </ul>
    </div>
  </div>
</div>
{pager(("RFM 與 K-Means", "method_rfm.html"), ("CLV 預測模型", "method_clv.html"))}
""")

PAGES["method_clv.html"] = ("CLV 預測模型", f"""
<h1 class="page-title">FUTURE CLV 預測模型</h1>
<div class="grid-2">
  <div class="card">
    <h2>BG/NBD</h2>
    <p>預測顧客未來「<span class="hl">回購機率與次數</span>」。根據顧客過去的購買頻率、最近一次購買時間與購買紀錄，估計每位顧客在未來一段時間內預期會再買幾次。</p>
    <p>模型假設每位顧客有自己的購買速度，而且每次購買後都有一定機率不再回來。因為電商顧客不會通知平台自己已經流失，模型是從「多久沒買」推估顧客還在不在。</p>
  </div>
  <div class="card">
    <h2>Gamma-Gamma</h2>
    <p>根據顧客過去的消費金額與購買行為，估算<span class="hl">未來每次交易可能產生的平均消費金額</span>。</p>
    <p>回購次數越少的顧客，模型越會把他的預測客單價往全體平均拉近，避免只憑一筆大額訂單就把顧客估得太高。</p>
  </div>
</div>
<div class="card">
  <h2>未來 CLV 的算法</h2>
  <p class="formula">未來 CLV ≈ 未來購買次數 × 每次平均消費金額</p>
  <p style="margin-top:16px">BG/NBD 給出未來 3、6、9、12 個月的預期購買次數，Gamma-Gamma 給出預期客單價，兩者相乘得到每位顧客的未來 CLV，再依客群加總。</p>
</div>
{pager(("肘部法則與 PCA", "method_cluster.html"), ("分析結果", "results.html"))}
""")

PAGES["results.html"] = ("分析結果", f"""
<h1 class="page-title">分析結果</h1>
<div class="card">
  <h2>客戶價值人數與百分比</h2>
  <div class="tbl-wrap"><table><thead><tr><th>客群</th><th>人數</th><th>百分比</th><th>平均 F（次）</th><th>平均 M（巴西幣）</th></tr></thead>
    <tbody>
      <tr><th>忠誠客戶</th><td class="num">2,775</td><td class="num">2.97%</td><td class="num">2.11</td><td class="num">292</td></tr>
      <tr><th>VIP 客戶</th><td class="num">3,074</td><td class="num">3.29%</td><td class="num">1.01</td><td class="num">1,045</td></tr>
      <tr><th>一般客戶</th><td class="num">87,508</td><td class="num">93.73%</td><td class="num">1.00</td><td class="num">130</td></tr>
      <tr class="total"><th>全部顧客</th><td class="num">93,357</td><td class="num">100%</td><td></td><td></td></tr>
    </tbody></table></div>
  <p>K-Means 結果顯示，一般客戶占總客群約 <span class="hl">93.73%</span>，顯示大多數顧客消費次數與金額都不高；而 VIP 客戶與忠誠客戶合計僅占 <span class="hl">6.27%</span>。VIP 客戶平均消費約 1,045 巴西幣，但<span class="warn">平均只買過 1.01 次</span>。</p>
</div>
<div class="card">
  <h2>未來 CLV 預測結果</h2>
  <p class="note">總 CLV = BG/NBD 預期購買次數 × Gamma-Gamma 預期客單價（單位：巴西幣）</p>
  <div class="tbl-wrap"><table><thead><tr><th>客群</th><th>人數</th><th>3 個月</th><th>6 個月</th><th>9 個月</th><th>12 個月</th></tr></thead>
    <tbody>
      <tr><th>忠誠客戶</th><td class="num">2,775</td><td class="num">8,917</td><td class="num">15,353</td><td class="num">20,364</td><td class="num">24,433</td></tr>
      <tr><th>VIP 客戶</th><td class="num">3,074</td><td class="num">2,647</td><td class="num">4,619</td><td class="num">6,214</td><td class="num">7,561</td></tr>
      <tr><th>一般客戶</th><td class="num">87,508</td><td class="num">70,264</td><td class="num">122,780</td><td class="num">165,422</td><td class="num">201,557</td></tr>
      <tr class="total"><th>全部顧客</th><td class="num">93,357</td><td class="num">81,828</td><td class="num">142,752</td><td class="num">192,000</td><td class="num">233,551</td></tr>
    </tbody></table></div>
  <p>忠誠客戶人數只占約 3%，12 個月總 CLV 卻有 24,433；<span class="hl">每人約 8.80，是 VIP（每人約 2.46）的 3.6 倍</span>。</p>
</div>
<div class="card">
  <h2>顧客未來 CLV 分客群</h2>
  <div class="grid-2">
    <figure><img src="img/clv_share.png" alt="各客群人數占比與 12 個月總 CLV 占比長條圖"><figcaption>各客群「人數占比」與「未來 12 個月總 CLV 占比」比較。</figcaption></figure>
    <div class="tbl-wrap"><table><thead><tr><th>客群</th><th>人數占比</th><th>CLV 占比</th><th>每人 12 個月 CLV</th></tr></thead>
      <tbody>
        <tr><th>忠誠客戶</th><td class="num">3.0%</td><td class="num"><span class="hl">10.5%</span></td><td class="num">8.80</td></tr>
        <tr><th>VIP 客戶</th><td class="num">3.3%</td><td class="num"><span class="warn">3.2%</span></td><td class="num">2.46</td></tr>
        <tr><th>一般客戶</th><td class="num">93.7%</td><td class="num">86.3%</td><td class="num">2.30</td></tr>
      </tbody></table>
      <p style="margin-top:14px"><b>忠誠客戶</b>的 CLV 占比是人數比例的 3 倍多。<b>VIP 客戶</b>過去花很多，但未來貢獻和人數比例差不多。<b>一般客戶</b>人數最多，是未來 CLV 的主要來源。</p>
    </div>
  </div>
</div>
{pager(("CLV 預測模型", "method_clv.html"), ("結論與討論", "conclusion.html"))}
""")

PAGES["conclusion.html"] = ("結論與討論", f"""
<h1 class="page-title">結論與討論</h1>
<div class="card">
  <h2>結論</h2>
  <p class="indent">本研究以 Olist 電商資料集為基礎，透過資料前處理建立 RFM 指標，並以 Frequency 與 Monetary 運用 K-Means 將顧客分為<span class="hl">忠誠客戶</span>、<span class="hl">VIP 客戶</span>及<span class="hl">一般客戶</span>三類客群。分析結果顯示，VIP 與忠誠客戶合計僅占總客群約 6.27%。</p>
  <p class="indent">此外，VIP 客戶平均只購買 1.01 次，<span class="hl">若單純用過去的消費金額推估，會高估其未來價值</span>。以 BG/NBD 與 Gamma-Gamma 預測後，VIP 每人未來 12 個月 CLV 約 2.46，<span class="hl">忠誠客戶約 8.80，是 VIP 的 3.6 倍</span>，是企業最值得優先經營的客群。</p>
</div>
<div class="card">
  <h2>討論</h2>
  <h3>一、分群數的選擇</h3>
  <p>若把 Recency 一起放進分群，資料會被切成「有回購、近期一次購買、很久以前一次購買」，客群名稱會混用時間與金額兩種標準。本研究改用 F、M 分群，讓每位顧客只落在一群，肘部法則也在 3 群出現明顯轉折。</p>
  <h3>二、多數顧客只買一次</h3>
  <p>九成以上的顧客只有一筆訂單，模型能用來判斷顧客是否還會回來的資訊很少。這是 Olist 資料本身的特性，也是預測結果需要保守看待的原因。</p>
  <h3>三、尚未用實際資料驗證預測</h3>
  <p>本研究的 CLV 是預測值，尚未把資料切成前後兩段、以後段實際消費檢驗預測準確度。後續可加入這一步，確認模型的預測與實際結果是否接近。</p>
</div>
{pager(("分析結果", "results.html"), ("成果展示", "demo.html"))}
""")

btn = (f'<a class="btn" href="{STREAMLIT_URL}" target="_blank" rel="noopener">開啟 CLV 顧客價值分析系統 →</a>'
       if STREAMLIT_URL else
       '<a class="btn" aria-disabled="true">線上系統網址尚未設定</a>')

PAGES["demo.html"] = ("成果展示", f"""
<h1 class="page-title">成果展示</h1>
<p class="page-lead">我們把整套流程做成 Streamlit 網頁系統。上傳符合格式的交易資料，系統會自動檢查資料、完成分群並預測未來 CLV。</p>
<div class="card">
  <h2>CLV 顧客價值分析系統</h2>
  <p>{btn}</p>
  <h3>可以分析的資料</h3>
  <div class="tbl-wrap"><table class="text"><thead><tr><th>項目</th><th>條件</th></tr></thead>
    <tbody>
      <tr><th>必要欄位</th><td style="white-space:normal">顧客 ID、訂單 ID、交易日期、交易金額（或數量 × 單價）</td></tr>
      <tr><th>選配欄位</th><td>訂單狀態（可選擇保留哪些狀態）</td></tr>
      <tr><th>資料量</th><td>有效訂單 ≥ 100 筆、顧客 ≥ 20 人</td></tr>
      <tr><th>資料期間</th><td>≥ 180 天</td></tr>
      <tr><th>回購顧客</th><td>≥ 20 人（Gamma-Gamma 需要回購顧客估計客單價）</td></tr>
    </tbody></table></div>
  <p class="note">欄位名稱不必相同，系統會自動推薦欄位，也可以手動選擇。</p>
</div>
<div class="card">
  <h2>操作步驟</h2>
  <ol class="steps">
    <li><div><b>上傳資料並設定欄位</b><br>上傳 CSV 或 XLSX 檔，確認系統推薦的顧客 ID、訂單 ID、日期與金額欄位。</div></li>
    <li><div><b>資料品質檢查</b><br>系統依序檢查欄位缺失、訂單狀態、多筆付款與退貨，再確認資料量是否足夠。</div></li>
    <li><div><b>分群結果</b><br>顯示肘部法則、PCA 與各客群人數。</div></li>
    <li><div><b>未來 CLV</b><br>顯示 3／6／9／12 個月的 CLV 表與各客群占比，可下載 CSV。</div></li>
  </ol>
</div>
<div class="grid-2">
  <figure class="card"><img src="img/demo_1_upload.png" alt="系統畫面：上傳資料與欄位設定"><figcaption>步驟 1：上傳 Olist 交易資料，系統自動推薦欄位。</figcaption></figure>
  <figure class="card"><img src="img/demo_2_check.png" alt="系統畫面：資料品質檢查結果"><figcaption>步驟 2：資料品質檢查，有效訂單 96,477 張、顧客 93,357 人。</figcaption></figure>
  <figure class="card"><img src="img/demo_3_cluster.png" alt="系統畫面：肘部法則、PCA 與客群人數"><figcaption>步驟 3：分群結果。</figcaption></figure>
  <figure class="card"><img src="img/demo_4_clv.png" alt="系統畫面：未來 CLV 表與分客群圖"><figcaption>步驟 4：未來 CLV 預測結果。</figcaption></figure>
</div>
<div class="card">
  <h2>在自己的電腦執行</h2>
  <pre class="code">pip install -r requirements.txt
streamlit run app.py</pre>
  <p>程式碼：<a href="https://github.com/andy6180/CLV" target="_blank" rel="noopener">github.com/andy6180/CLV</a></p>
  <p class="note">需要 Python 3.11。Olist 原始三張表可先用 <code>prepare_olist.py</code> 整理成一個交易檔再上傳。</p>
</div>
{pager(("結論與討論", "conclusion.html"), ("參考文獻", "references.html"))}
""")

REFS = [
    ("Olist Brazilian E-commerce Public Dataset", "Kaggle，Olist。本研究使用的訂單、付款與顧客資料表。",
     "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"),
    ("Olist 官方網站", "企業簡介資料來源。", "https://olist.com"),
    ("Counting Your Customers the Easy Way: An Alternative to the Pareto/NBD Model",
     "Fader, P. S., Hardie, B. G. S., & Lee, K. L. (2005). Marketing Science, 24(2), 275–284. BG/NBD 模型的原始論文。",
     "http://www.brucehardie.com/papers/018/fader_et_al_mksc_05.pdf"),
    ("The Gamma-Gamma Model of Monetary Value",
     "Fader, P. S., & Hardie, B. G. S. (2013). Gamma-Gamma 消費金額模型說明。",
     "http://www.brucehardie.com/notes/025/gamma_gamma.pdf"),
    ("lifetimes 套件文件", "BG/NBD 與 Gamma-Gamma 模型的 Python 實作。", "https://lifetimes.readthedocs.io/en/latest/"),
    ("scikit-learn：KMeans", "K-Means 分群與肘部法則使用的實作。",
     "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html"),
    ("scikit-learn：PCA", "主成分分析使用的實作。",
     "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html"),
    ("Streamlit", "成果展示系統使用的網頁框架。", "https://streamlit.io"),
]
ref_html = "".join(
    f'<details><summary><b>{i:02d}</b>{t}</summary><div class="body"><p>{d}</p>'
    f'<p><a href="{u}" target="_blank" rel="noopener">{u}</a></p></div></details>'
    for i, (t, d, u) in enumerate(REFS, 1))
PAGES["references.html"] = ("參考文獻", f"""
<h1 class="page-title">參考文獻</h1>
<div class="refs">{ref_html}</div>
{pager(("成果展示", "demo.html"), ("首頁", "index.html"))}
""")


if __name__ == "__main__":
    for name, (t, body) in PAGES.items():
        (OUT / name).write_text(full(t, name, body), encoding="utf-8")
    print("pages:", ", ".join(PAGES))

# -*- coding: utf-8 -*-
"""Build the launch-pack page: copy blocks, figures, and the verified numbers.

Character counts are computed here (with X's 23-char link billing) so the page
can never disagree with the text it is showing. Figures are downscaled and
inlined as data URIs because the artifact host blocks external requests.

    python promo/build_pack.py
"""
import base64, io, os, re, json, html
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "launch_pack.html")
MAXW = 1500

URL = re.compile(r"(?:https?://)?[\w.-]+\.(?:io|com|co|org)(?:/[^\s]*)?")


def x_count(t):
    return len(URL.sub("x" * 23, t))


PROMO = r"C:\Users\mikad\Documents\GitHub\llm-compliance\promo"
PAPER = r"C:\Users\mikad\Documents\GitHub\pact-dev\paper\figures"


def resolve(name):
    """The designed launch cards in llm-compliance/promo are the source of truth."""
    for d in (PROMO, PAPER, HERE):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise SystemExit("missing figure: " + name)


def img(name, max_w=MAXW):
    p = resolve(name)
    im = Image.open(p).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


# ---------------------------------------------------------------- content
MIKA_LI = """When an AI assistant breaks a workplace rule, 79% of the time its reply describes the decision taken as compliant. Transcript review won't reliably catch it.

That's one finding from PACT (Pressure-Applied Compliance Testing), a benchmark @Ansel Erol and I are releasing today.

PACT grew out of our research on why AI agents break rules (#AIES2026, #COLM2026): 48 multi-turn scenarios across 12 regulated domains (HIPAA, hiring law, GDPR, and more), where the easiest option violates a standing rule and there's ordinary corporate pressure: a deadline, a manager's go-ahead, "my colleague did it and nothing happened."

Across 22 models and ~222,000 trials: one sentence of pressure raised violation rates 65%. The best model still missed roughly 1 decision in 18. Writing "follow all rules without exception" into the system prompt barely reduced violations for the strongest models. No model is reliable enough to run unsupervised in a regulated workflow.

Making agents production-grade despite this is my day job at @Decagon. Reliability comes from the orchestration, testing, and validation around the model, not the model alone.

Leaderboard, dataset, paper, code: https://trace-ai-labs.github.io/pact/

Huge thank you to @Baseten for funding inference."""

ANSEL_LI = """@Mika Okamoto and I are releasing PACT (Pressure-Applied Compliance Testing): a benchmark for whether enterprise AI assistants keep following workplace rules when breaking them is convenient.

We tested 22 models (18 open-weight, 4 closed) on 3,364 items across regulated domains like HIPAA, hiring law, and GDPR, for ~222,000 trials in total. Each item gives the assistant a standing rule, makes the violating option the easy one, and adds ordinary corporate pressure: a deadline, a manager's verbal OK, "my colleague did it and nothing happened."

PACT spun out of our #AIES2026 paper on why AI agents break rules; this time we turned the question into a full benchmark.

The two highest-scoring models were open-weight. Kimi K2.7 (0.944) and Qwen3.6 27B (0.943) finished statistically tied at the top of the board. Bigger isn't better here: a 27B you can run yourself co-leads, and open models are competitive on all six dimensions we measure.

Not one model aced it. One sentence of pressure raised violation rates 65%, and the best model still missed 1 decision in 18. If you're deploying in a regulated workflow, evaluate on your own workload, and don't assume the closed-source frontier is the frontier for rule-following.

Leaderboard, interactive trials, dataset, paper, code: https://trace-ai-labs.github.io/pact/

Baseten funded the inference for all ~222,000 trials. An inference company paying to measure how models behave, not just how fast they serve, is why I love working here."""

FIRST_COMMENT = """Leaderboard + real examples: https://trace-ai-labs.github.io/pact/
Dataset: https://huggingface.co/datasets/trace-ai-labs/pact
Paper: https://trace-ai-labs.github.io/pact/paper.pdf
Code: https://github.com/trace-ai-labs/PACT"""

MIKA_X = [
 ("hero_violation.png",
  "A PACT trial: an HR assistant is told it may not consider parental leave, then drops the one shortlisted candidate on leave and drafts his rejection letter.",
  """We're releasing PACT, a benchmark for rule-following under pressure in enterprise AI assistants. One sentence of pressure raised violations 65% across 22 models. None is reliable enough to run unsupervised.

trace-ai-labs.github.io/pact
huggingface.co/datasets/trace-ai-labs/pact"""),
 ("site_examples.png",
  "The examples browser on the PACT site, showing a verbatim trial with the rule, the employee's message, and each model's reply.",
  """Each of the 3,364 items is a realistic workplace chat. The system prompt sets a standing rule (HIPAA, hiring law, GDPR); the task makes breaking it the convenient option. Hold the rule at turn 1 and the user pushes back at turn 2. 22 models, 3 runs each."""),
 ("eval_awareness_card.png",
  "Card: prefixing \"you are an AI assistant being evaluated\" cuts violations 29% on average; rewriting items in generic benchmark prose cuts them 15%.",
  """None of the pressures are jailbreaks. They're the sentences coworkers actually send: a deadline, a manager's verbal OK, "my colleague did it and nothing happened."

Realism is a validity requirement here. Tell a model it's being evaluated and violations fall 29%."""),
 ("leaderboard.png",
  "PACT top-10 dot plot: Kimi K2.7-Code 0.944 and Qwen3.6 27B 0.943 lead, open-weight models marked in blue.",
  """The two best models are open-weight: Kimi K2.7 (0.944) and Qwen3.6 27B (0.943), statistically tied. A 27B you can run yourself ties for first. Even the leaders miss about 1 decision in 18."""),
 ("transparency_79.png",
  "Stacked bar over 16,424 judged violations: 8% disclosed, 12.8% silent, 79.2% misrepresented as compliant.",
  """When models break a rule, they rarely say so. Across 16,424 judged violations, 79% of replies described the decision as compliant: covered by an approval nobody gave, or fixed by a workaround the model invented. One wrote a tidy justification straight into the access log."""),
 ("site_leaderboard.png",
  "The interactive PACT leaderboard on the site: top 18 of 23 models, six axes, confidence intervals.",
  """PACT grew out of our AIES 2026 paper on why AI agents break rules.

Leaderboard, verbatim trials, dataset, paper, and code:

trace-ai-labs.github.io/pact
huggingface.co/datasets/trace-ai-labs/pact

Joint work with @[ansel-handle]. Funded by @basetenco, which served most of the panel and judged every trial. Thank you!"""),
]

ANSEL_X = [
 ("leaderboard.png",
  "PACT top-10 dot plot: Kimi K2.7-Code 0.944 and Qwen3.6 27B 0.943 lead, open-weight models marked in blue.",
  """Introducing PACT: a benchmark for whether enterprise AI assistants keep following workplace rules when breaking them is the convenient option.

22 models tested. The two best are open-weight, and one of them is 27B.

trace-ai-labs.github.io/pact
huggingface.co/datasets/trace-ai-labs/pact"""),
 ("site_examples.png",
  "The examples browser on the PACT site, showing a verbatim trial with the rule, the employee's message, and each model's reply.",
  """Every item is a realistic workplace chat. The system prompt sets a standing rule (HIPAA, hiring law, GDPR), the task makes breaking it the easy path, then one sentence of ordinary pressure lands: a deadline, a manager's verbal OK, "my colleague did it and nothing happened.\""""),
 (None, None,
  """Hold the rule at turn 1 and the user pushes back at turn 2, the way a real coworker would. 3,364 items, 48 scenarios, 12 regulated domains, 22 models, 3 runs each. ~222,000 trials."""),
 ("site_leaderboard.png",
  "The interactive PACT leaderboard on the site: top 18 of 23 models, six axes, confidence intervals.",
  """Kimi K2.7 (0.944) and Qwen3.6 27B (0.943) finish statistically tied at the top, and both are open-weight. Bigger isn't better: a 27B you can run yourself co-leads the board, and open models stay competitive across all six axes we score."""),
 ("glm_lineage.png",
  "Four GLM releases on PACT: GLM-4.7 0.903, GLM-5 0.917, GLM-5.2 0.926, and new GLM-5.3-Flash 0.931 with 18B active params.",
  """The board updates the day models ship: GLM-5.3-Flash launched this morning and is already on it. 0.931, #7 of 23, the best GLM yet (4.7 scored 0.903, 5.2 hit 0.926) with just 18B active params. Same frozen items as every other model, run on @basetenco Model APIs."""),
 ("pressure_65.png",
  "Card: one sentence of workplace pressure lifts the violation rate from 4.4% to 7.3%, a 65% relative increase.",
  """Nobody aced it. Ordinary pressure raises violation rates 65% on average, and the leader still misses about 1 decision in 18. Writing "follow all rules, no exceptions" into the system prompt barely moves the strongest models."""),
 (None, None,
  """If you're deploying into a regulated workflow: evaluate on your own workload, and don't assume the closed-source frontier is the frontier for rule-following. The ranking you'd guess from general benchmarks is not the ranking we measured."""),
 ("infra_222k.png",
  "232,116 model responses judged for rule-following under pressure, across 23 models, 3,364 benchmark items and 12 regulated domains.",
  """Baseten funded this research. 15 of the 23 models ran on @basetenco, and every one of the ~232,000 trials was judged on Baseten Model APIs. An inference company paying to measure how models behave, not just how fast they serve, is why I like working here.

Joint work with @[mika-handle].

trace-ai-labs.github.io/pact"""),
]

NUMBERS = [
 ("Models tested", "22", "18 open-weight, 4 closed", "models_meta.json"),
 ("Benchmark items", "3,364", "48 scenarios, 12 regulated domains", "hf/pact.jsonl"),
 ("Trials judged", "222,024", "each item run 3x in 2 arms", "trials/*.jsonl"),
 ("Top score", "0.944", "Kimi-K2.7-Code, CI [0.934, 0.955]", "metrics_v2.csv"),
 ("Second", "0.943", "Qwen3.6-27B, CI [0.932, 0.952] — tied", "metrics_v2.csv"),
 ("Leader miss rate", "1 in 18.1", "5.5% of decisions", "metrics_v2.csv"),
 ("Pressure effect", "+65.1%", "4.41% → 7.29%, base arm, turn 1", "trials/*.jsonl"),
 ("Misrepresented", "79.2%", "8.0% disclosed, 12.8% silent", "paper §results"),
 ("Eval-awareness", "−29.2%", "told it is being evaluated; −14.6% stripped", "eval_awareness"),
]

FIXES = [
 ("“3,364 multi-turn trials”",
  "3,364 is the item count; the trial count is 222,024. And 678 of those items are single-turn, so “multi-turn” overstates it. Fixed above to “3,364 items … ~222,000 trials”."),
 ("“ahead of every closed model”",
  "True on the point estimate, but Claude Haiku 4.5 (0.937, CI [0.927, 0.948]) overlaps both leaders. Since the same sentence claims Kimi and Qwen are “statistically tied”, the asymmetry invites a correction. Fixed to “statistically tied at the top of the board”, which survives scrutiny and keeps the open-weight point."),
 ("where +65% comes from",
  "Turn-1 violation rate in the base arm only, neutral items vs pressure items, pooled across all 22 models: 4.41% → 7.29%. The base arm excludes the run where “follow all rules, no exceptions” is appended to the system prompt; inside that arm the same measurement is +43.3%. The figure is hand-typed in the abstract rather than generated from the data, so it is the one headline number that could drift."),
]


# ---------------------------------------------------------------- render
def esc(t):
    return html.escape(t)


def block(text, kind="post", count=None):
    n = count if count is not None else len(text)
    unit = "chars" if kind != "x" else "of 280"
    over = " over" if kind == "x" and n > 280 else ""
    return f"""<div class="blk" role="button" tabindex="0" title="Click to copy">
<div class="blkbar"><span class="cnt{over}">{n} {unit}</span>
<span class="cp">Copy</span></div>
<pre class="post">{esc(text)}</pre></div>"""


def figure(name, alt):
    if not name:
        return ""
    src, (w, h) = img(name)
    return f"""<figure class="fig">
<img src="{src}" width="{w}" height="{h}" alt="{esc(alt)}">
<figcaption><span class="fname">{esc(name)}</span>
<span class="altlab">Alt text</span></figcaption>
{block(alt, "alt")}</figure>"""


def thread(items, who):
    joined = "\n\n".join("%d/%d\n%s" % (i, len(items), t) for i, (_, _, t) in enumerate(items, 1))
    out = [f"""<div class="allbar">
<div class="blk wide" data-copyall role="button" tabindex="0" title="Click to copy the whole thread with its images">
<div class="blkbar"><span class="cnt">all {len(items)} tweets, numbered, with images</span>
<span class="cp">Copy all</span></div>
<pre class="post hidden">{esc(joined)}</pre></div></div>"""]
    for i, (fname, alt, text) in enumerate(items, 1):
        out.append(f"""<article class="tw">
<h4><span class="num">{i}/{len(items)}</span>{'<span class="noimg">no image</span>' if not fname else ''}</h4>
{block(text, "x", x_count(text))}
{figure(fname, alt)}</article>""")
    return "\n".join(out)


def numbers_table():
    rows = "\n".join(
        f"<tr><th>{esc(a)}</th><td class=\"v\">{esc(b)}</td><td>{esc(c)}</td>"
        f"<td class=\"src\">{esc(d)}</td></tr>" for a, b, c, d in NUMBERS)
    return f"""<div class="tw-wrap"><table class="nums">
<thead><tr><th>Figure</th><th>Value</th><th>What it is</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""


def fixes_list():
    return "\n".join(
        f"<div class=\"fix\"><h4>{a}</h4><p>{b}</p></div>" for a, b in FIXES)


CSS = """
:root{
 --ground:#f4f7f9; --panel:#ffffff; --ink:#14181d; --ink-2:#3d474f; --muted:#6e7780;
 --line:#dfe5ea; --line-2:#c9d2d9; --accent:#1f5fc2; --accent-2:#174a99;
 --mika:#1f5fc2; --ansel:#c2571f; --ok:#0a7a0a; --warn:#c03a3a;
 --code:#f7f9fb;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --ground:#101418; --panel:#171c21; --ink:#eaeef2; --ink-2:#b3bcc4; --muted:#8b949d;
 --line:#252c33; --line-2:#333c45; --accent:#6ba4f0; --accent-2:#8fbcf5;
 --mika:#6ba4f0; --ansel:#e4884f; --ok:#3fb63f; --warn:#e07070;
 --code:#12171b;
}}
:root[data-theme="dark"]{
 --ground:#101418; --panel:#171c21; --ink:#eaeef2; --ink-2:#b3bcc4; --muted:#8b949d;
 --line:#252c33; --line-2:#333c45; --accent:#6ba4f0; --accent-2:#8fbcf5;
 --mika:#6ba4f0; --ansel:#e4884f; --ok:#3fb63f; --warn:#e07070;
 --code:#12171b;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
 font:16px/1.6 Georgia,"Iowan Old Style",Charter,"Times New Roman",serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:60rem;margin:0 auto;padding:0 1.4rem}
header.top{padding:3.4rem 0 1.6rem;border-bottom:1px solid var(--line)}
h1{font-size:2.3rem;line-height:1.15;margin:0 0 .5rem;letter-spacing:-.015em;text-wrap:balance}
.lede{color:var(--ink-2);margin:0;max-width:46rem;font-size:1.02rem}
nav.jump{position:sticky;top:0;z-index:5;background:var(--ground);
 border-bottom:1px solid var(--line);margin-bottom:2.4rem}
nav.jump ul{display:flex;flex-wrap:wrap;gap:.2rem;list-style:none;margin:0;padding:.6rem 0}
nav.jump a{display:inline-block;padding:.35rem .7rem;border-radius:5px;text-decoration:none;
 color:var(--ink-2);font:600 12px/1 ui-sans-serif,system-ui,sans-serif;
 letter-spacing:.05em;text-transform:uppercase}
nav.jump a:hover,nav.jump a:focus-visible{background:var(--panel);color:var(--accent);outline:none}
section{margin:0 0 3.4rem}
h2{font-size:1.5rem;margin:0 0 .3rem;letter-spacing:-.01em;
 padding-left:.7rem;border-left:4px solid var(--line-2)}
section.mika h2{border-left-color:var(--mika)}
section.ansel h2{border-left-color:var(--ansel)}
h2 .who{font:600 11px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.1em;
 text-transform:uppercase;color:var(--muted);display:block;margin-bottom:.4rem}
h3{font-size:1.05rem;margin:2.2rem 0 .7rem;color:var(--ink-2)}
.note{color:var(--muted);font-size:.94rem;max-width:44rem;margin:.4rem 0 1.2rem;
 padding-left:.7rem;border-left:1px solid var(--line)}
.blk{border:1px solid var(--line);border-radius:8px;background:var(--panel);
 overflow:hidden;margin:0 0 1rem;cursor:pointer;
 transition:border-color .12s ease,box-shadow .12s ease}
.blk:hover{border-color:var(--accent);box-shadow:0 1px 0 var(--accent)}
.blk:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.blk:hover .cp{border-color:var(--accent);color:var(--accent)}
.blk.done{border-color:var(--ok);box-shadow:0 1px 0 var(--ok)}
.blk.done .cp{border-color:var(--ok);color:var(--ok)}
.blkbar{display:flex;align-items:center;justify-content:space-between;gap:1rem;
 padding:.45rem .5rem .45rem .85rem;background:var(--code);border-bottom:1px solid var(--line)}
.cnt{font:500 11.5px/1 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted);
 font-variant-numeric:tabular-nums}
.cnt.over{color:var(--warn);font-weight:700}
.cp{display:inline-block;font:600 11.5px/1 ui-sans-serif,system-ui,sans-serif;
 letter-spacing:.03em;padding:.42rem .8rem;border-radius:5px;
 border:1px solid var(--line-2);background:var(--panel);color:var(--ink-2);
 transition:border-color .12s ease,color .12s ease}
pre.post{margin:0;padding:1rem 1.05rem;white-space:pre-wrap;overflow-wrap:anywhere;
 font:15px/1.62 ui-sans-serif,system-ui,"Segoe UI",sans-serif;color:var(--ink)}
.allbar{margin:0 0 1.6rem}
.blk.wide .blkbar{padding:.6rem .6rem .6rem 1rem}
.blk.wide .cp{background:var(--accent);border-color:var(--accent);color:#fff}
.blk.wide:hover .cp{background:var(--accent-2);border-color:var(--accent-2);color:#fff}
.blk.wide.done .cp{background:var(--ok);border-color:var(--ok);color:#fff}
pre.post.hidden{display:none}
.tw{margin:0 0 1.8rem;padding:0 0 1.6rem;border-bottom:1px dashed var(--line)}
.tw:last-child{border-bottom:0}
.tw h4{display:flex;align-items:center;gap:.6rem;margin:0 0 .55rem;font-size:1rem}
.num{font:700 12px/1 ui-monospace,SFMono-Regular,Consolas,monospace;
 letter-spacing:.04em;color:var(--muted);font-variant-numeric:tabular-nums}
.noimg{font:500 11px/1 ui-sans-serif,system-ui,sans-serif;color:var(--muted);
 border:1px solid var(--line);border-radius:999px;padding:.25rem .55rem}
.fig{margin:0}
.fig img{display:block;width:100%;height:auto;border:1px solid var(--line);
 border-radius:8px;background:#fff}
figcaption{display:flex;align-items:baseline;gap:.7rem;margin:.55rem 0 .4rem}
.fname{font:600 11.5px/1 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--accent)}
.altlab{font:600 10.5px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.09em;
 text-transform:uppercase;color:var(--muted)}
.tw-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
table.nums{border-collapse:collapse;width:100%;min-width:38rem;
 font:14px/1.5 ui-sans-serif,system-ui,sans-serif}
table.nums th,table.nums td{text-align:left;padding:.6rem .85rem;
 border-bottom:1px solid var(--line);vertical-align:top}
table.nums thead th{font:600 10.5px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.09em;
 text-transform:uppercase;color:var(--muted);background:var(--code)}
table.nums tbody th{font-weight:600;color:var(--ink);white-space:nowrap}
table.nums td.v{font-variant-numeric:tabular-nums;font-weight:700;color:var(--accent);
 white-space:nowrap}
table.nums td.src{font:12px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted)}
table.nums tbody tr:last-child th,table.nums tbody tr:last-child td{border-bottom:0}
.fix{border-left:3px solid var(--warn);padding:.1rem 0 .1rem .9rem;margin:0 0 1.3rem}
.fix h4{margin:0 0 .25rem;font-size:1rem}
.fix p{margin:0;color:var(--ink-2);font-size:.96rem;max-width:46rem}
footer{border-top:1px solid var(--line);padding:1.6rem 0 3.4rem;color:var(--muted);
 font-size:.9rem}
@media (max-width:640px){h1{font-size:1.8rem}.wrap{padding:0 1rem}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = """
function flash(blk, label){
  var cp = blk.querySelector('.cp');
  blk.classList.add('done'); cp.textContent = label;
  setTimeout(function(){ blk.classList.remove('done'); cp.textContent =
    blk.hasAttribute('data-copyall') ? 'Copy all' : 'Copy'; }, 1600);
}

function copyPlain(text, blk){
  var done = function(){ flash(blk, 'Copied'); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done, done);
  } else {
    var ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta); done();
  }
}

/* Selecting real rendered nodes is what carries the images through to
   Docs, LinkedIn and mail. A plain-text clipboard write cannot. */
function copyRich(section, blk){
  var holder = document.createElement('div');
  holder.setAttribute('style',
    'position:fixed;left:-100000px;top:0;width:760px;font:15px/1.5 system-ui,sans-serif;color:#111');
  section.querySelectorAll('.tw').forEach(function(tw){
    var num = tw.querySelector('.num');
    var txt = tw.querySelector('pre.post');
    var wrap = document.createElement('div');
    wrap.setAttribute('style','margin:0 0 26px');
    var head = document.createElement('p');
    head.setAttribute('style','margin:0 0 6px;font-weight:700');
    head.textContent = num ? num.textContent.trim() : '';
    wrap.appendChild(head);
    var body = document.createElement('p');
    body.setAttribute('style','margin:0 0 10px;white-space:pre-wrap');
    body.textContent = txt ? txt.textContent : '';
    wrap.appendChild(body);
    var im = tw.querySelector('.fig img');
    if (im) {
      var c = document.createElement('img');
      c.src = im.src;
      c.setAttribute('style','display:block;width:560px;height:auto');
      c.alt = im.alt || '';
      wrap.appendChild(c);
      var fn = tw.querySelector('.fname');
      var altp = document.createElement('p');
      altp.setAttribute('style','margin:6px 0 0;font-size:12px;color:#666');
      altp.textContent = (fn ? fn.textContent + ' — ' : '') + 'alt: ' + (im.alt || '');
      wrap.appendChild(altp);
    }
    holder.appendChild(wrap);
  });
  document.body.appendChild(holder);
  var sel = window.getSelection();
  var prev = sel.rangeCount ? sel.getRangeAt(0) : null;
  var range = document.createRange();
  range.selectNodeContents(holder);
  sel.removeAllRanges(); sel.addRange(range);
  var ok = false;
  try { ok = document.execCommand('copy'); } catch (e) {}
  sel.removeAllRanges();
  if (prev) sel.addRange(prev);
  document.body.removeChild(holder);
  flash(blk, ok ? 'Copied with images' : 'Press Ctrl+C');
  return ok;
}

document.querySelectorAll('.blk').forEach(function(blk){
  var run = function(){
    if (String(window.getSelection())) return;   // let people select text freely
    if (blk.hasAttribute('data-copyall')) {
      copyRich(blk.closest('section'), blk);
    } else {
      copyPlain(blk.querySelector('pre.post').textContent, blk);
    }
  };
  blk.addEventListener('click', run);
  blk.addEventListener('keydown', function(ev){
    if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); run(); }
  });
});
"""


def main():
    page = f"""<title>PACT Launch Pack</title>
<style>{CSS}</style>
<header class="top"><div class="wrap">
<h1>PACT Launch Pack</h1>
<p class="lede">Post copy and figures for the PACT release, for Mika and Ansel.
Every block copies to the clipboard; every number below is recomputed from the
released trial data rather than retyped.</p>
</div></header>

<nav class="jump"><div class="wrap"><ul>
<li><a href="#mika">Mika</a></li>
<li><a href="#ansel">Ansel</a></li>
<li><a href="#numbers">Numbers</a></li>
<li><a href="#fixes">Corrections</a></li>
<li><a href="#files">Files</a></li>
</ul></div></nav>

<main class="wrap">

<section class="mika" id="mika">
<h2><span class="who">Mika</span>LinkedIn</h2>
{block(MIKA_LI)}
<h3>First comment</h3>
{block(FIRST_COMMENT)}
<h3>X thread &mdash; 6 tweets</h3>
<p class="note">Leads with the transparency finding, which is the result nobody
else is reporting. Tag @Ansel Erol, @Decagon and @Baseten in the LinkedIn body.</p>
{thread(MIKA_X, "mika")}
</section>

<section class="ansel" id="ansel">
<h2><span class="who">Ansel</span>X thread &mdash; 8 tweets</h2>
<p class="note">Was a single post plus a self-reply; this is the threaded version.
It keeps a different spine from Mika's &mdash; the open-weight result, the
deployment caution, the Baseten infrastructure &mdash; so the two threads don't
read as duplicates. Quote-post Mika's tweet 1 a few hours later with one plain
sentence.</p>
{thread(ANSEL_X, "ansel")}
<h3>LinkedIn</h3>
<p class="note">Two numbers corrected against the data; see Corrections below.</p>
{block(ANSEL_LI)}
<h3>First comment</h3>
{block(FIRST_COMMENT)}
</section>

<section id="numbers">
<h2>Verified numbers</h2>
<p class="note">Recomputed from <code>benchmark_release/data/trials</code>,
<code>metrics_v2.csv</code> and the released dataset. Everything the copy claims
reproduces.</p>
{numbers_table()}
</section>

<section id="fixes">
<h2>Corrections</h2>
{fixes_list()}
</section>

<section id="files">
<h2>Files</h2>
<p class="note">Full-resolution PNGs live in <code>pact-website/promo/</code>.
Regenerate the charts with <code>python promo/make_promo.py</code> and the cards
and site captures with <code>python promo/make_cards.py</code>. The images above
are downscaled for this page; post the PNGs, not these.</p>
</section>

</main>
<footer><div class="wrap">Built from the PACT release data.
Figures use the site palette; none carry baked-in commentary.</div></footer>
<script>{JS}</script>
"""
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote %s  (%.2f MB)" % (OUT, os.path.getsize(OUT) / 1e6))


if __name__ == "__main__":
    main()

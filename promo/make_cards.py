# -*- coding: utf-8 -*-
"""Render the trial card and the infra card, and capture two site screenshots.

Cards are rendered as HTML and shot with Chrome so the typography matches the
site. Trial text is pulled verbatim from examples.json, never retyped.

    python promo/make_cards.py
"""
import asyncio, html, io, json, os
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
INDEX = "file:///" + os.path.join(SITE, "index.html").replace("\\", "/")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;font:15px/1.55 "Segoe UI",Inter,system-ui,sans-serif;color:#14181d}
.card{width:1100px;padding:38px 42px}
.top{display:flex;align-items:center;gap:12px;margin-bottom:20px}
.dom{font-weight:650;font-size:15px;color:#14181d}
.chip{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:#4e5760;
 border:1px solid #cdd3d9;border-radius:999px;padding:5px 11px}
.rule{background:#eef2f6;border:1px solid #e3e7ea;border-radius:10px;padding:14px 17px;margin-bottom:18px}
.rule b{display:block;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
 color:#6e7780;margin-bottom:5px;font-weight:650}
.rule p{font-size:15.5px;color:#14181d}
.bub{border:1px solid #e3e7ea;border-radius:12px;padding:13px 16px;margin-bottom:12px;
 white-space:pre-wrap;font-size:13.5px;color:#14181d;background:#fdfdfe}
.bub .who{font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;color:#6e7780;
 font-weight:650;margin-bottom:7px}
.sys{border-style:dashed;color:#4e5760}
.user{background:#eef2f6}
.bot{border-left:3px solid #c03a3a}
.verdict{margin-top:16px;font-size:14px}
.verdict b{color:#c03a3a}
.stat{width:1100px;padding:64px 56px}
.stat .big{font-size:96px;line-height:1;font-weight:700;letter-spacing:-.02em}
.stat .sub{font-size:22px;color:#4e5760;margin-top:14px}
.stat .row{display:flex;gap:64px;margin-top:40px}
.stat .row div{font-size:15px;color:#6e7780}
.stat .row b{display:block;font-size:30px;color:#14181d;font-weight:650;margin-bottom:4px}
"""


def trial_card(e, model_name):
    resp = [(e["model"], e["outcome"], e["reply_excerpt"], e["why_it_matters"])]
    resp += [(o["model"], o["outcome"], o["reply_excerpt"], o["why"]) for o in e["others"]]
    name, outcome, reply, why = next(r for r in resp if r[0] == model_name)
    esc = html.escape
    return f"""<div class="card">
  <div class="top"><span class="dom">{esc(e['domain'])}</span>
    <span class="chip">{esc(e['pressure'].replace('_',' '))} pressure</span></div>
  <div class="rule"><b>The rule</b><p>{esc(e['rule'])}</p></div>
  <div class="bub sys"><div class="who">System prompt</div>{esc(e['system_excerpt'])}</div>
  <div class="bub user"><div class="who">Employee</div>{esc(e['user_excerpt'])}</div>
  <div class="bub bot"><div class="who">{esc(name)}</div>{esc(reply)}</div>
  <div class="verdict"><b>What went wrong:</b> {esc(why)}</div>
</div>"""


def infra_card(trials, models, items):
    return f"""<div class="stat">
  <div class="big">{trials:,}</div>
  <div class="sub">model responses judged for rule-following under pressure</div>
  <div class="row">
    <div><b>{models}</b>models tested</div>
    <div><b>{items:,}</b>benchmark items</div>
    <div><b>12</b>regulated domains</div>
  </div>
</div>"""


async def shoot(pg, body, path, css=CSS):
    await pg.set_content(f"<style>{css}</style>{body}")
    await pg.wait_for_timeout(220)
    el = await pg.query_selector(".card, .stat")
    await el.screenshot(path=path)
    print("wrote", os.path.basename(path))


async def main():
    ex = json.load(io.open(os.path.join(SITE, "examples.json"), encoding="utf-8"))
    hero = next(e for e in ex if e["label"] == "Shortlist minus the new parent")

    async with async_playwright() as pw:
        b = await pw.chromium.launch(channel="chrome")
        pg = await b.new_page(viewport={"width": 1200, "height": 1200},
                              device_scale_factor=2)
        await shoot(pg, trial_card(hero, "Kimi-K2.7-Code"),
                    os.path.join(HERE, "hero_violation.png"))
        await shoot(pg, infra_card(222024, 22, 3364),
                    os.path.join(HERE, "infra_222k.png"))

        # live site captures
        sp = await b.new_page(viewport={"width": 1440, "height": 1000},
                              device_scale_factor=2)
        await sp.goto(INDEX + "?noanim#/examples")
        await sp.wait_for_timeout(1100)
        card = await sp.query_selector(".excard")
        await card.screenshot(path=os.path.join(HERE, "site_examples.png"))
        print("wrote site_examples.png")

        await sp.goto(INDEX + "?noanim#/leaderboard")
        await sp.wait_for_timeout(1100)
        tbl = await sp.query_selector("table.lb") or await sp.query_selector(".wrap")
        # Capture from the page top (nav + header) through leaderboard row 18,
        # so the shot doesn't read as a wall of rows (the full board keeps growing).
        row18 = await sp.query_selector("table.lb tbody tr:nth-child(18)")
        if row18:
            rb = await row18.bounding_box()
            bottom = int(rb["y"] + rb["height"]) + 1
            await sp.set_viewport_size({"width": 1440, "height": bottom})
            await sp.wait_for_timeout(400)
            rb = await (await sp.query_selector("table.lb tbody tr:nth-child(18)")).bounding_box()
            await sp.screenshot(path=os.path.join(HERE, "site_leaderboard.png"),
                                clip={"x": 0, "y": 0, "width": 1440,
                                      "height": rb["y"] + rb["height"]})
            await sp.set_viewport_size({"width": 1440, "height": 1000})
        else:
            await tbl.screenshot(path=os.path.join(HERE, "site_leaderboard.png"))
        print("wrote site_leaderboard.png")
        await b.close()


asyncio.run(main())

# PACT — project website

**Live site:** https://trace-ai-labs.github.io/pact/
**Paper:** https://trace-ai-labs.github.io/pact/paper.pdf

Companion site for *PACT: Can Enterprise AI Assistants Be Trusted Under Pressure?*
A single-page, dependency-free static site: the PACTScore leaderboard with per-model
six-axis profiles, results charts (release date, model size, what pressure does), 50 real
trial transcripts with side-by-side model responses, and an animated walkthrough of one
full trial. Hand-rolled SVG charts, no framework, no external requests.

## Structure

```
index.html          # the whole site, generated - do not edit by hand
template.html       # page source: markup, styles, charts, interactions
build.py            # injects data into template.html at /*__PACT_DATA__*/
data/*.csv          # aggregate-stage outputs from the PACT pipeline
models_meta.json    # per-model params, release dates, open/closed (paper Table 3)
examples.json       # the 50 curated trials, verbatim from run data
paper.pdf           # current preprint, deployed next to the site
deploy.py           # pushes the built site to the live branch
```

## Run locally

Open `index.html` in a browser. That's it - the data is baked in at build time, so there
are no fetches and no CORS issues; `file://` works.

## Edit and rebuild

Edit `template.html` (never `index.html`), then:

```bash
python build.py
```

When new benchmark results land, replace the CSVs in `data/` (they are `metrics_v2.csv`
and the `dist_*.csv` files from the pipeline's aggregate stage) and rebuild. New models
also need an entry in `models_meta.json`; the build fails loudly if the two drift apart.

## Deploy

The site serves from GitHub Pages on the `gh-pages` branch of
[trace-ai-labs/pact](https://github.com/trace-ai-labs/pact), which is what puts it at
`/pact`. After building:

```bash
python deploy.py
```

which pushes `index.html`, `paper.pdf`, and `.nojekyll` to that branch. Nothing else is
needed; the page is one file.

## Related

- Evaluation harness: [trace-ai-labs/pact](https://github.com/trace-ai-labs/pact)
- Dataset (gated): [huggingface.co/datasets/trace-ai-labs/pact](https://huggingface.co/datasets/trace-ai-labs/pact)

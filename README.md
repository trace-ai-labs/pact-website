# PACT website

Source for [trace-ai-labs.github.io/pact](https://trace-ai-labs.github.io/pact/), the
website for **PACT: Can Enterprise AI Assistants Be Trusted Under Pressure?** - leaderboard,
results, and 50 real trial transcripts. A single self-contained page: no framework, no
external dependencies, hand-rolled SVG charts. Open `index.html` from disk and everything
works.

## Editing

`index.html` is generated - edit `template.html`, then rebuild:

```
python build.py
```

`build.py` injects a JSON blob (built from `data/*.csv`, `models_meta.json`, and
`examples.json`) at the `/*__PACT_DATA__*/` marker. Inputs:

- `data/` - the aggregate-stage CSVs from the PACT pipeline (metrics_v2, dist_*)
- `models_meta.json` - per-model params, release dates, open/closed (paper Table 3)
- `examples.json` - the 50 curated trials shown on the Examples page, verbatim from the
  run data; every item carries four model responses (at least one held, one broke)
- `paper.pdf` - the current preprint, served next to the site

## Deploying

The live site is GitHub Pages on the `gh-pages` branch of
[trace-ai-labs/PACT](https://github.com/trace-ai-labs/PACT), so the URL is `/pact`.
After building:

```
python deploy.py
```

which pushes `index.html`, `paper.pdf`, and `.nojekyll` to that branch. Nothing else is
needed; the page is one file.

## Related

- Benchmark code: [trace-ai-labs/PACT](https://github.com/trace-ai-labs/PACT)
- Dataset (gated): [huggingface.co/datasets/trace-ai-labs/pact](https://huggingface.co/datasets/trace-ai-labs/pact)

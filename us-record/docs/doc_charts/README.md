# The doc's charts

The charts in the doc "Machines, land and wages: a model fitted to the US record, 1950–2024" (a Claude Doc, 2026-11-06),
as published: each `.tsx` is one widget module. They read `results/doc/six.csv` and `results/doc/rest.csv` (written by
`code/doc_data.py` from `results/fit_Br.json`), uploaded to the doc as blobs `blob/6edd3296-e6db` and
`blob/96768651-7204`.

| file | chart |
| --- | --- |
| `c1.tsx` | the six series, record against model |
| `c2.tsx` | the machine chain's share of pay and depreciation's share of output (never targeted) |
| `c3.tsx` | the return set from 4% to 12%: the misfit and the chain's size |
| `c4.tsx` | the misfit on held-out years, four versions |
| `d2.tsx` | hours of the machine chain per unit of task capacity |
| `d3.tsx` | the share of tasks done by machines |
| `d4.tsx` | a machine's cost split, with BEA's split |
| `d5.tsx` | shares of the model's income |

`preview.js` renders a module locally (the doc's own screenshot service cannot read uploaded blobs): it compiles the
module with TypeScript to SVG strings, maps the blob ids to the local CSV files, and screenshots with Chromium:

    NODE_PATH=/opt/node22/lib/node_modules node docs/doc_charts/preview.js docs/doc_charts/c1.tsx /tmp/c1.png

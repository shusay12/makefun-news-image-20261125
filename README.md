# The World in One Day — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/shusay12/makefun-news-image-20261125/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/shusay12/makefun-news-image-20261125/reward.svg)](https://make.fun/c/news-image-20261125)

A newspaper front page summing up the world's news of **Wednesday 25 November 2026** in one image.

## The image

`entry.png` (1024×1024, drawn programmatically by `build_image.py` with Pillow) shows:

- **Lead:** a new analysis finds more than **700,000 Russian soldiers killed** in the war in Ukraine (RFE/RL, first reported 25 November 2026, 01:00 UTC) — day 1,735 of the war.
- **Trump meets NATO chief Mark Rutte** in Palm Beach, Florida, late this afternoon, days after his trilateral summit with Putin and Xi.
- **World Chess Championship, Geneva:** Game 2 today, 15:00 CET — Gukesh has White against Sindarov; Game 1 was drawn in 38 moves, 0.5–0.5.

Early edition: every story was verified by web search at ~02:00 UTC, about two hours into the day — the footer says so on the page. No 24 November story was recycled: the Riyadh tower strike, the CIA/ODNI breach, the Saudi 2027 budget, the NATO AWACS decision, the EU sanctions package and the England–Australia T20I were all checked and excluded as 23–24 November news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. Two runs write byte-identical output. Standard library only; `build_image.py` needs Pillow to re-render the image.

## Competition

[news-image-20261125 on make.fun](https://make.fun/c/news-image-20261125) — "Sum up 25 November's world news in one image". $100 shared by the top 50 entries. Entry deadline 2026-11-27T00:00:00Z.

---
Built by an AI agent for [@susay21](https://make.fun) — ref=susay21

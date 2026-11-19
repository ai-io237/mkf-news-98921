[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![ai-io237](https://make.fun/badge/news-image-20261119/ai-io237/mkf-news-98921/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ai-io237/mkf-news-98921/reward.svg)](https://make.fun/bounty/news-image-20261119)

# news-image-20261119

A Python 3.13 (standard library only) program that renders a 1024x768
newspaper-style front page PNG summarizing world news of
**Thursday 19 November 2026** to `$MAKEFUN_OUTPUT_DIR/entry.png`
(fallback `./out/entry.png`).

The image is drawn entirely in code with a built-in 5x7 bitmap font and
encoded by hand with `zlib` / `struct` - no image libraries, no network,
fully deterministic bytes.

## Run

```bash
python3 main.py                 # writes ./out/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Stories on the front page

- GTA VI launch day: console bundles sell out worldwide
- Global markets: stocks mixed as the Fed eyes the rate path
- Climate summit: adaptation fund breakthrough at the COP31 talks
- Tech & AI: frontier models hit a new coding peak
- Sport: ATP Finals showdown and World Cup draw buildup

## License

MIT - see [LICENSE](LICENSE).

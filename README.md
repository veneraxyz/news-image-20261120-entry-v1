# news-image-20261120-entry-v1

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/veneraxyz/news-image-20261120-entry-v1/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/veneraxyz/news-image-20261120-entry-v1/reward.svg)](https://make.fun/c/news-image-20261120)

One image summing up world news of **Friday 20 November 2026**, for the
[make.fun](https://make.fun) `news-image-20261120` competition.

## The image

A 1024×1024 news front page, built to stay readable when viewed small:

- **Date band** — "20 NOVEMBER 2026", large, alone at the top.
- **Lead: Cyclone Akvan** — landfall in Odisha near Gopalpur, 300,000+
  evacuated, winds 70–80 km/h with gusts to 90, no major damage or loss of
  life reported. A restrained coastal map marks Gopalpur; nothing in it
  implies catastrophe.
- **Trump / Iran** — the strike decision comes after 1 January 2027.
- **Voyager 1** — radio signals now take 24 hours one way.
- **Hayabusa2** — drops its asteroid landing plan after engine trouble;
  the approach line in the image terminates before the asteroid.
- **Han Duck-soo** — conviction overturned by South Korea's Supreme Court.

## How it is built

`generate.py` draws `entry.png` with Pillow (fixed geometry, fixed fonts,
no randomness, no network, no timestamps), so re-rendering produces
identical bytes. `main.ts` (Node 22, standard library only) copies the
committed `entry.png` to the output directory — that is the whole graded
program, and it is deterministic by construction.

```sh
python3 generate.py                       # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).

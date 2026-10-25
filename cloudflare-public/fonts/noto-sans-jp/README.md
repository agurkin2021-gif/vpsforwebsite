# Japanese typography assets

Noto Sans JP variable font, under the SIL Open Font License in `OFL.txt`.
Upstream: https://github.com/google/fonts/tree/main/ofl/notosansjp
Source: https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf
Retrieved 2026-10-25. Source SHA-256:
`c2f3b4d463500a2ddcd3849cded1fceeb9fd6d1c32e6cbecd568453ba50fc68f`.

`NotoSansJP-site.woff2` retains the variable weight range and every character used
in the Japanese content, menus, shared translations, 404 and CTA. It is served
locally; page rendering does not depend on a font CDN.

To regenerate after a Japanese text change, install `fonttools[woff]`, download
the pinned upstream source outside the tracked tree, then run:

```console
python scripts/build-japanese-font.py /path/to/NotoSansJP-variable.ttf
```

The script verifies the upstream hash and both source/subset character coverage.
It also creates `static/images/home/vps-cta-ja.svg` from the unchanged English CTA
shapes, outlining translated text so external SVG rendering does not require a
system Japanese font. Accessible Japanese labels are retained. The owner's
homepage hero artwork is unchanged.

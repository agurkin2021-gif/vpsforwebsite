Turkish pages use local Inter (400–700) and Fraunces (600–700), the same design families as the original site. These subsets retain the existing Latin characters and add all Turkish letters, including `İ`, `ı`, `Ğ`, `ğ`, `Ş`, `ş`. Other locales keep their original font files.

Pinned upstream sources, retrieved 2026-10-25:

- [Inter](https://raw.githubusercontent.com/google/fonts/0b58fb370093f9a9f4ff785d94405710b79de67c/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf), SHA-256 `29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031`.
- [Fraunces](https://raw.githubusercontent.com/google/fonts/4024282d9b0cffcdb8e3024560862746178d741f/ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf), SHA-256 `177ff6c0f14e5550a3c624247cd1189611d4eb65d000b14944c63d967958abbb`.

Both families are licensed under SIL OFL 1.1. The corresponding upstream licenses are `inter-turkish-OFL.txt` and `fraunces-turkish-OFL.txt` in this directory.

With `fonttools[woff]` installed and both source TTF files in a directory, run `python scripts/build-turkish-fonts.py PATH_TO_SOURCE_DIRECTORY`. The builder validates the upstream hashes, pins non-weight axes, subsets the required characters, verifies Turkish letter coverage and writes the two WOFF2 files. It also generates the Turkish CTA SVG with outlined Inter labels; its shapes, numbers and colors remain the same. The owner homepage hero is unchanged.

`local-fonts.html` selects these faces only for Turkish. Its partial cache varies by language to prevent fonts from another locale being reused. Fingerprinted URLs, preloading and `font-display: optional` retain the existing loading policy.

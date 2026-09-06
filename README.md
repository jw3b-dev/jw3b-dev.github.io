# jw3b-dev.github.io

GitHub profile site for **John Wellard** (JW3B / AgileGypsy), published at
https://jw3b-dev.github.io/. It mirrors the positioning of the operable portfolio at
[jw3b.dev](https://jw3b.dev) and shares its exact design system with
[crosshair15-cooling](https://jw3b-dev.github.io/crosshair15-cooling/).

- Content lives in [profile.md](profile.md); `tools/build.py` renders it to `site/index.html`.
- `brand/jw3b-banner.svg` is the animated mark used on the GitHub profile README.
- The Pages workflow builds and deploys on every push to `main`.

```bash
python3 tools/build.py && (cd site && python3 -m http.server 8765)
```

## License

**Code:** MIT, see [LICENSE](LICENSE).
**Brand assets:** © 2026 John Wellard (jw3b.dev), all rights reserved. The `JW3B.` mark,
prompt treatment, `// STAY WEIRD 👽` tagline, banner and header/footer components in
[brand/](brand/) are excluded from the MIT grant. See [brand/LICENSE-BRAND.md](brand/LICENSE-BRAND.md).

`~❯ JW3B._` · `// STAY WEIRD 👽`

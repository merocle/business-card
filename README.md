# business-card

Source of [merocle.com](https://merocle.com/) — a single static page served by GitHub Pages straight from `main`. No build step, no dependencies.

## Edit

- **Links:** in `index.html`, copy or edit an `<li>` inside the `<ul>`.
- **Avatar:** replace `img/avatar.jpg` (square, 240×240).
- **Contact card / QR:** edit the data at the top of `tools/contact.py`, then run `pip install segno && python3 tools/contact.py` — it regenerates `contact.vcf` (Save contact button) and `img/qr.svg`.
- **Colors:** the `:root` variables at the top of the `<style>` block (`--accent` is the orange).

Push to `main` and the site updates in about a minute.

Analytics: [GoatCounter](https://www.goatcounter.com/) (no cookies).

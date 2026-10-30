# Quizs documentation

Open `index.html` in a browser. No server is required to read or download the packaged guide. The default reader shows all 91 pages of the official PDF continuously, with sidebar navigation to each chapter. The optional text view provides selectable HTML content.

The guide contains 35 chapters in English for the Laravel admin and Flutter app. It explains field validation, data sources, customization locations, app impact, and verification steps. The Settings overview and Environment variables & editing chapter cover exact variable names, current defaults, administrator/database precedence, manual .env editing, configuration caching, worker refresh, and historical effects. Full PDF downloads the complete continuous manual; Chapter PDF downloads only the current chapter. Both are prebuilt PDFs with selectable text, repeated table headers, annotated screenshots, bookmarks where appropriate, and page counts.

## Official format

The supplied PLAY GAMES.docx is the visual format reference. Only its two Arknox branding images were extracted; none of its unrelated project screenshots, URLs, accounts, feature claims, or support-response commitments were imported. The guide follows its A4 margins, 11 pt justified body text, purple subheadings, blue section titles and conclusion, company header, faint logo watermark, and Page X of Y footer. Publisher contact details retain the reference's exact spelling.

All 36 PDFs are inside `pdfs/`. The browser's page previews are generated from the complete PDF and kept inside `assets/pdf-pages/`, so the document view matches the downloaded file and works from a local folder. The sidebar and download controls are web-only.

## Editing

- `assets/js/guide-content.js`: English walkthrough content.
- `assets/js/guide-actions.js`: Detailed dropdown choices, action sequences, analytics controls, and confirmation messages verified against the administrator source.
- `assets/js/guide.js`: chapter metadata, rendering, groups, and screenshot captions.
- `assets/js/screenshots.js`: screenshot dimensions and arrow targets.
- `assets/css/guide.css`: guide layout and responsive presentation.
- `assets/js/app.js`: navigation, search, theme, and printing.
- `assets/js/pdf-reader.js`: continuous official document reader and page navigation.
- `assets/js/pdf-manifest.js`: generated chapter-to-page map and download paths.
- `assets/css/pdf-reader.css`: reader shell and fallback print rules.
- `tools/build_pdfs.py`: generates the full PDF, 35 chapter PDFs, page previews, and manifest from the same guide sources.
- `tools/export_content.cjs`: loads chapter metadata and English content for the PDF builder.
- `tools/check_pdfs.py`: verifies page counts, page bounds, chapter positions, and core configuration references.
- `index.html`: shell and retained deployment/build chapters.

## Screenshot provenance

31 referenced screenshots in `assets/images/walkthrough/` were captured on 4 October 2026 from this folder's Laravel admin and Flutter application, running locally with an isolated SQLite database and demo records. The Flutter web preview used a temporary copy with a local API URL. The original Flutter API configuration was preserved. Numbered SVG arrows are rendered over screenshots and remain visible in enlarged views and printing.

Screenshots show demo content, not production records. Push delivery, SMTP delivery, native Google sign-in, native ads, and provider offerwall callbacks were not validated on a real device or live provider account. Their configuration paths and current source behavior are distinguished in the guide. The cPanel setup map is an illustrative local SVG, not a live hosting screenshot. Hosting steps explain database setup, private application files, the public document root, environment settings, migrations, assets, and queue processing. All guide files and visual assets are inside Documentation. Legacy images from earlier projects have been removed; the Quizs logo and current captures are retained.

## Verification

The PDF builder uses Python with reportlab, beautifulsoup4, svglib, Pillow, and pymupdf, plus Node.js for loading the existing content files. On this Windows workspace it embeds the installed Calibri, Bell MT, and Times New Roman fonts. After editing content or changing screenshots, run `python tools/build_pdfs.py --node PATH_TO_NODE` and `python tools/check_pdfs.py` from Documentation, using your configured runtimes. This refreshes the PDF files and their matching browser previews together.

Checked desktop/mobile layouts, chapter navigation, section links, search, dark theme, screenshots, and JavaScript syntax. The full PDF and all chapter PDFs passed blank-page, footer, page-boundary, and chapter-location checks. Representative cover, screenshot, table, contents, and conclusion pages were visually inspected. Both browser download buttons were tested against actual downloaded PDF files.

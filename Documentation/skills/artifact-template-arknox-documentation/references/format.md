# Approved Arknox document format

All measurements are PDF points (72 pt = 1 inch). The official Word reference established the layout; the approved Quizs PDF established the shipped implementation. The user's later name and email corrections supersede older references.

## Fixed identity and assets

| Item | Value |
| --- | --- |
| Publisher, author metadata, byline, closing name | Arknox |
| Email and mailto destination | info@arknox.in |
| Website | www.arknox.in |
| Contact / Support Center | +91-8787388949 |
| Header logo | assets/branding/arknox-header.png |
| Watermark | assets/branding/arknox-watermark.png |
| Cover reference | assets/reference.png |
| Approved full layout | assets/approved-reference.pdf |

The transparent orange logos were extracted from `word/media/image136.png` (header) and `word/media/image135.png` (watermark) in PLAY GAMES.docx. Use these originals unchanged, preserving aspect ratio. Do not create a new logo, recolor it, or substitute unrelated project artwork. The original DOCX is not needed at runtime. Historic client identities, accounts, tax identifiers, legal claims, domains, and unrelated screenshots are not reusable content.

## Geometry and decoration

| Property | Value |
| --- | --- |
| Page | A4 portrait: 595.276 × 841.890 pt, 210 × 297 mm |
| Left margin | 56.7 pt, approximately 20.0 mm |
| Right margin | 63.7 pt, approximately 22.47 mm |
| Top / bottom margins | 72 pt each, 25.4 mm |
| Body width | Page width minus side margins, approximately 474.876 pt |
| Frame padding | 0 on all sides |
| Chapter opening | New page |
| Paper / body text | White / black |

Cover: no publisher header, but watermark and footer remain. Other pages: header logo 24 × 24 pt at x = left margin, y = page height − 57; publisher right-aligned at x = page width − right margin, y = page height − 40; website right-aligned at the same x, y = page height − 54. Header font Bell MT 11 pt, black.

Watermark: 474.6 × 474.6 pt, x = left margin, y = (page height − 474.6) / 2, alpha 0.065. Preserve its subtle appearance behind text on every page.

Footer: centered at page width / 2, y = 39 pt from bottom, Times New Roman Bold 12 pt, black. Text `Page N of TOTAL`; calculate totals separately for the complete document and each chapter PDF after pagination. Never hardcode the reference's totals.

## Typography and spacing

Embed installed fonts. Body font files: calibri.ttf, calibrib.ttf, calibrii.ttf, calibriz.ttf. Header: BELL.TTF. Footer: timesbd.ttf. Do not bundle these proprietary font files. Courier is the built-in code font.

| Role | Font, size / leading | Alignment, color, spacing |
| --- | --- | --- |
| Body | Calibri 11 / 14.5 pt | Justified, black, 8 pt after; no widow/orphan lines |
| Cover title | Calibri Bold 22 / 27 pt | Left, black, 9 after, keep with next |
| Cover subtitle | Calibri 14 / 18 pt | Left, black, 20 after, keep with next |
| Chapter, Contents, Conclusion Section | Calibri Bold 22 / 27 pt | Center, blue #259CF1, 14 after, keep with next |
| Section / subsection heading | Calibri Bold 12 / 16 pt | Left, purple #6059F7, 12 before, 6 after, keep with next |
| Small / technical source | Calibri 9 / 12 pt | Left, #404040 |
| Caption | Calibri Italic 9 / 12 pt | Center, 5 after |
| Table cell | Calibri 9.5 / 12.5 pt | Left, top vertical alignment |
| Table header | Calibri Bold 9.5 / 12 pt | Left, white |
| Code block | Courier 8 / 11 pt | Left, #F3F3F7 background, #D9D9D9 border 0.5 pt, padding 8, 8 before / 12 after |
| Inline code | Courier 9 pt | Preserve identifiers exactly |
| Note | Body | #F5F3FF background, padding 9, 9 before / 13 after |
| Contents entry | Calibri 10 / 13.5 pt | Left, 3 before, dynamic page number |

Use bold for buttons, exact popup wording, and important field names. Use explicit numbered steps with separate paragraphs; do not flatten ordered lists. Keep headings with following content. Use readable paragraph highlights and code blocks, not decorative cards in the PDF. Natural end-of-chapter whitespace is acceptable.

## Cover, sequence, and common text

Cover order:

1. Actual project name, replacing Quizs.
2. `Administrator and Application Documentation`, adapted to actual scope.
3. Left-aligned `By: Arknox` with publisher bold, then `Email: info@arknox.in`, then `Contact: +91-8787388949`, and 14 pt space.
4. Project-specific introduction describing the system and manual scope.
5. Purple `Administrator Features` and `Application Features` where applicable; actual project descriptions, not copied Quizs features.
6. `How to use this document`: continuous PDF, contents/bookmarks, sidebar reader, full and chapter downloads.
7. `Screenshot provenance`: real capture environment, synthetic data, illustrative diagrams, and unverified integrations.

Then Contents, which may span pages, and chapters in useful task order: prerequisites/setup, authentication/dashboard, modules, daily operations, settings/environment, app flows, customization, troubleshooting, deployment as applicable. Do not add irrelevant empty sections.

End on a new page with centered blue `Conclusion Section`, project-specific closing guidance, actual access instructions when relevant, `Release verification`, then `Contact for support`, email/support center, and small `Arknox`. Do not create legal agreements or SLA promises from the old reference.

Standalone chapter PDFs contain chapter title, common byline/contact, complete chapter content, and closing section, with their own page totals. Overview PDF contains the cover. Full PDF contains dynamic contents, bookmarks, chapters, conclusion.

## Tables and screenshot parameters

Default table headers: `Field / Feature`, `Definition and source`, `Effect of changes`. Width proportions 0.23 / 0.35 / 0.42. Header #6059F7; alternating rows white / #FAF9FF; borders #D9D9D9 at 0.5 pt; padding 7 pt all sides. Repeat header on page continuation. Use splitByRow=1 and splitInRow=0: split between rows only. Restructure any row too tall for a page instead of shrinking the whole guide.

Screenshots: preserve aspect ratio; fit content width and max 355 pt height; center; 8 pt before; caption then marker legends; 7 pt after. Original captures used 1200 px desktop width and 412 × 915 px mobile size. These are useful defaults, not requirements for unrelated projects.

Vector annotations: orange #AC3500 arrows/circles, white numbers/outlines. Circle radius in source coordinates: 21 px desktop, 11 px mobile. Points are source-image pixel positions with top-left origin. Scale coordinates with the image. A marker must have a matching numbered explanation. Keep controls readable. Actual screenshots must not be modified to invent data. Illustrations must be identified as illustrative.

## Browser reader

Exact PDF-page JPGs at 1.6 pixels per PDF point, quality 85. Page display max 794 CSS px, A4 aspect ratio. Continuous page flow, sidebar chapter navigation, page input/Go, scrolling active-chapter state, and real Full PDF / Chapter PDF links. The local JS manifest avoids file:// fetch restrictions. Local assets only; no CDN or hosted viewer dependency.

Sidebar and toolbars belong to the browser, never the exported PDF. Use orange #AC3500 navigation, keyboard-accessible controls, responsive layout. Browser UI may use system sans-serif; PDF fonts remain embedded. Raster previews do not provide selectable text: downloads do, and an optional HTML text view can use the same source content.

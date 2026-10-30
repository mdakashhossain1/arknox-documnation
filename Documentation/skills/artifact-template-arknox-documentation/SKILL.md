---
name: artifact-template-arknox-documentation
description: "Create English project manuals in the approved Arknox documentation format with branded A4 PDFs, chapter downloads, annotated screenshots, and an offline sidebar reader. Use for Arknox-format documentation or reuse of this format across projects."
---

# Arknox Documentation

Produce a source-verified manual, not a picture of a document. The retained PNG is a visual reference; do not invoke image generation to typeset documentation. Use the approved PDF and deterministic renderer for the document format.

## Workflow

For the package's file map, every content option, command-line options, output paths, defaults, and troubleshooting, read [options-and-files.md](references/options-and-files.md). This project-local folder is the complete portable skill; it does not depend on a globally installed copy.

1. Read [format.md](references/format.md) for every measurement, font, branding asset, fixed text, and content position. Read [workflow.md](references/workflow.md) for feature coverage and verification. Read [content-schema.md](references/content-schema.md) before authoring content JSON.
2. Inspect `assets/reference.png` and representative pages of `assets/approved-reference.pdf`. Quizs is only the reference project: reuse formatting, never its features, customer information, credentials, or deployment details.
3. Inspect the target project's source and safe local UI. Write English documentation with complete field, dropdown, create/edit/delete, popup, analytics, settings/environment, notification, deployment, and app flows as applicable. Collect real annotated screenshots. Distinguish verified behavior from unverified native/provider behavior.
4. Keep all outputs within the target project's `Documentation/`: content JSON, local images, index.html, page previews, full PDF, and separate chapter PDFs. Resolve the skill path dynamically; never assume the original Quizs workspace exists.
5. Load the available workspace dependency runtime. The builder needs Python with reportlab, beautifulsoup4, svglib, pymupdf, and Pillow. Run `<python> <skill-directory>/scripts/build_documentation.py --content <project>/Documentation/content.json --output <project>/Documentation`.
6. Run `<python> <skill-directory>/scripts/verify_documentation.py --output <project>/Documentation`. Visually inspect cover, contents, tables, screenshots, lists, and conclusion. Test sidebar, page navigation, responsive view, and actual full/chapter downloads. Fix defects before delivery.

## Fidelity

Publisher is **Arknox**, email **info@arknox.in**, website **www.arknox.in**, contact **+91-8787388949**. Use the bundled transparent orange logos unchanged. Never restore historic company names or email addresses. User-requested changes override defaults.

Preserve the A4 geometry, Calibri body, Bell MT header, Times New Roman Bold footer, purple subheadings, blue chapter titles, watermark, byline, and conclusion treatment. Use installed properly licensed fonts; do not redistribute Windows fonts. On non-Windows machines, set ARKNOX_FONT_DIR to a directory containing the approved font filenames. Do not silently substitute fonts.

The reader shows a continuous PDF with browser-only sidebar and controls. It works offline using local previews and JS manifest; PDF downloads contain no sidebar. Chapter count and page totals come from the new project, never the 91-page reference. For separately requested DOCX output, apply the same measurements and verify an actual DOCX render.

## Install and invoke

Extract the ZIP's `artifact-template-arknox-documentation` folder into the destination machine's personal Codex `skills` directory, preserving all nested files. Reload skill discovery if needed. No original Word reference, Quizs source, or temporary preview environment is required.

Example: `$artifact-template-arknox-documentation Create complete English documentation for this project in the Arknox format, with verified workflows, annotated screenshots, an offline index, and full and chapter PDF downloads.`

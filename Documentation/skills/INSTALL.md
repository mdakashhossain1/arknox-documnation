# Arknox documentation skill

The complete portable source is included in this project at:

`Documentation/skills/artifact-template-arknox-documentation/`

Start with its SKILL.md. Read references/options-and-files.md for every file, content option, command, default, and output location; references/format.md contains the exact fonts, margins, positions, colors, common text, and logo details. This local copy works independently of the globally installed copy.

To use it on another machine, extract `arknox-documentation-skill.zip` into that machine's personal Codex skills directory, normally `~/.codex/skills` or the configured CODEX_HOME/skills. The resulting structure must be `skills/artifact-template-arknox-documentation/SKILL.md`, with its assets, references, scripts, and agents folders beside it. Avoid an extra nested copy of the same folder. Reload skill discovery or restart Codex if it is not listed immediately.

In the target project, invoke:

```text
$artifact-template-arknox-documentation Create complete English documentation for this project in the Arknox format. Verify the actual source and UI, explain all dropdowns, settings, environment variables, analytics, and confirmation popups, include annotated screenshots, and generate an offline index with complete and chapter PDF downloads.
```

The retained PNG is a visual reference for the document format. The skill builds real PDFs and HTML, rather than generating a raster image of the manual.

The package includes original transparent Arknox logos, the approved PDF reference, all formatting values and common text, a content schema, reusable Python renderer and verifier, offline reader assets, and a smoke test. Publisher is Arknox; email is info@arknox.in. Project facts and screenshots must be collected anew.

Python dependencies: reportlab, beautifulsoup4, svglib, pymupdf, Pillow. Use the dependency runtime available in the destination environment. Fonts must be installed and properly licensed: Calibri variants, Bell MT, Times New Roman Bold. On non-Windows systems set ARKNOX_FONT_DIR to the font directory containing the filenames listed in references/format.md. The ZIP does not redistribute system fonts.

The source project, original Word file, temporary preview server, old .documentation-preview folder, and internet-hosted reader are not required. Fonts/runtime packages remain destination-machine prerequisites.

# Package files and every supported option

This is the complete project-local Arknox documentation skill. Keep the entire folder together when copying it to another project or computer. All paths below are relative to this folder unless stated otherwise.

## Where each file belongs

| File or folder | Purpose | When to change it |
| --- | --- | --- |
| SKILL.md | Entry point used by the assistant; links all detailed references | Change the reusable workflow only when requested |
| agents/openai.yaml | Display name, invocation prompt, automatic-discovery setting | Change skill UI metadata, not document content |
| artifact-template.json | Retained visual-reference registration; image kind refers to the cover PNG | Not a document-content configuration file; do not use image generation to typeset the manual |
| assets/reference.png | Approved cover reference | Preserve; the new project's title is supplied through content JSON |
| assets/preview.png | Skill/template preview thumbnail | Preserve unless updating the reusable reference |
| assets/approved-reference.pdf | Approved full Quizs manual showing layout examples | Read for layout; do not copy project facts into another project |
| assets/branding/arknox-header.png | Original orange transparent header logo | Preserve unchanged |
| assets/branding/arknox-watermark.png | Original transparent watermark logo | Preserve unchanged |
| assets/reader/index.html | Offline reader shell and its controls | Change only browser layout or labels, not PDF typography |
| assets/reader/reader.css | Browser sidebar, toolbar, page width, responsive and print rules | Change browser presentation if requested |
| assets/reader/reader.js | Sidebar, search, page navigation, current chapter and download links | Change reader behavior if requested |
| references/format.md | Exact margins, fonts, colors, positions, logo provenance and fixed text | Authoritative formatting specification |
| references/workflow.md | Source verification, feature coverage, screenshots, QA | Read when collecting and writing project content |
| references/content-schema.md | JSON examples and screenshot annotation schema | Read before authoring a new project manual |
| references/options-and-files.md | This file: options, locations, output behavior and troubleshooting | Read when choosing what to edit |
| scripts/build_documentation.py | Project-independent PDF, chapter, preview and reader builder | Run with the new project's content JSON |
| scripts/layout_engine.py | Reusable geometry, embedded fonts, tables, screenshot arrows, watermark, header/footer and pagination | Changes affect PDF formatting; preserve approved defaults |
| scripts/verify_documentation.py | Structural checks on generated output | Run after every build |
| scripts/smoke_test.py | Synthetic multi-page test independent of Quizs | Run after changing builder/layout logic; it writes to the operating system's temporary directory |
| scripts/package_skill.py | Creates a portable ZIP with one top-level skill folder | Run after changing this skill; excludes bytecode caches and ZIPs |

## Fixed brand versus variable project content

Fixed defaults: publisher and PDF author Arknox; email info@arknox.in; website www.arknox.in; contact +91-8787388949; original logos; approved page geometry, fonts and colors. These are not per-project JSON options. Explicit user changes to branding take precedence and require changing the corresponding builder/layout text and format reference consistently.

Variable: project name, subtitle, introduction, feature summaries, chapter order/content, screenshots, captions, annotations, technical sources, access instructions, release checks and conclusion. Supply these in the target project's Documentation/content.json. Read the target project's actual implementation; never reuse Quizs-specific behavior simply because it appears in the reference PDF.

## Top-level JSON options

| Key | Type / requirement | Position and effect |
| --- | --- | --- |
| project | Nonempty string, required | Cover title, PDF title metadata, reader heading and tab title |
| subtitle | String, optional | Cover subtitle; defaults to Administrator and Application Documentation |
| intro | Nonempty string, required | Cover introduction after publisher/contact block |
| overview | Array of [heading, text] pairs, optional | Cover feature summaries in supplied order; omitted if absent |
| provenance | String, optional | Cover Screenshot provenance paragraph; default asks readers to consult captions for environment and verification limits |
| access | String, optional | Administrator access paragraph in closing section; omitted if absent |
| conclusion | String, optional | Closing paragraph; default names the current project and asks readers to verify workflows |
| release_checks | Array of strings, optional | Numbered Release verification list in closing section; omitted if absent |
| chapters | Nonempty array of chapter objects, required | Manual order, contents/bookmarks, sidebar and standalone chapter exports |

## Chapter JSON options

| Key | Type / requirement | Position and effect |
| --- | --- | --- |
| id | Unique lowercase-hyphen identifier, required | Hash navigation, manifest key and chapter PDF filename; overview and conclusion are reserved |
| title | Nonempty string, required | Centered blue chapter title, contents entry, bookmark and reader current-chapter label |
| label | String, optional | Short sidebar label; defaults to title |
| group | String, optional | Sidebar group heading; defaults to Guide; keep related chapters adjacent |
| intro | Nonempty string, required | First chapter paragraph |
| path | String, optional | Small Screen / location line below introduction |
| steps | Nonempty array of strings, required | Numbered Step by step paragraphs |
| fields | Nonempty array of three-cell rows, required | Field / Feature, Definition and source, Effect of changes table |
| note | String, optional | Highlighted Current implementation limit box after the field table |
| details | Array of [heading, HTML] pairs, optional | Detailed topics after table/note, preserving the supplied order |
| verify | Nonempty string, required | Verification after saving paragraph |
| sources | Nonempty array of strings, required | Technical sources list; use source paths and relevant symbols from the target project |
| imageFile and annotation properties | Optional, described below | Main chapter screenshot after introduction/location and before steps |
| gallery | Array of screenshot objects, optional | Additional titled screenshots after verification and before technical sources |

Each gallery object needs title and imageFile; intro is optional. Screenshot properties below apply to both the main image and gallery objects. A chapter with no available screenshot may omit imageFile; do not invent a screenshot to fill the space. Explain any important missing verification in the chapter.

## Screenshot options

| Key | Type / default | Effect |
| --- | --- | --- |
| imageFile | Relative local file path | Resolves inside the output Documentation folder; outside paths and missing files are rejected |
| caption | String, optional | Caption below the screenshot; overrides the generated default |
| illustrative | Boolean, default false | Uses an illustrative-diagram caption when caption is omitted; does not transform a screenshot into a diagram |
| mobile | Boolean, default false | Uses 11 px rather than 21 px source-coordinate marker-circle radius |
| marks | Array of strings, default empty | Numbered legends below the caption |
| points | Array of four-number arrays, default empty | [circleX, circleY, arrowTargetX, arrowTargetY] in source-image pixels from top left |

Use one point per legend. Coordinates must stay within raster image dimensions. The renderer scales positions and image together. Keep labels clear of controls. PNG/JPG are preferred; SVG is supported for illustrative diagrams, with coordinates checked manually against its dimensions. Screenshot fitting remains proportional within content width and 355 pt maximum height.

## Text and HTML support

Ordinary prose is a string. Bold and italic use b/strong and i/em. Inline code uses code. Use br for deliberate line breaks. In details HTML, p creates separate paragraphs, ol/ul create separate numbered/bulleted steps, and pre creates a code block with real newline characters. Do not put an entire procedure into one paragraph or use HTML to simulate an unsupported form widget. Field tables are supplied through fields, not arbitrary HTML tables inside details.

## Commands and environment

Run scripts with an available Python runtime; do not hardcode another computer's user directory.

```text
<python> <skill-folder>/scripts/build_documentation.py --content <project>/Documentation/content.json --output <project>/Documentation
<python> <skill-folder>/scripts/verify_documentation.py --output <project>/Documentation
<python> <skill-folder>/scripts/smoke_test.py
<python> <skill-folder>/scripts/package_skill.py --output <destination>/arknox-documentation-skill.zip
```

| Option | Meaning |
| --- | --- |
| build --content | Required path to UTF-8 JSON source; UTF-8 BOM is accepted |
| build --output | Required output directory; screenshots referenced by imageFile must already exist beneath it |
| verify --output | Required generated documentation directory containing manifest.json |
| package --output | Required ZIP destination outside the skill folder; rebuilding replaces that destination ZIP |
| ARKNOX_FONT_DIR | Optional environment variable naming a directory with the approved font files; default C:/Windows/Fonts |

Required Python packages: reportlab, beautifulsoup4, svglib, pymupdf, Pillow. Fonts: calibri.ttf, calibrib.ttf, calibrii.ttf, calibriz.ttf, BELL.TTF, timesbd.ttf. Use installed properly licensed fonts. Fonts are not redistributed in the package. No original Word file, old temporary environment, Node runtime, hosting account or internet-based reader is required.

## Generated output map

| Path under target Documentation/ | Contents |
| --- | --- |
| content.json | Normalized source content retained for later edits |
| index.html | Offline entry point; browser sidebar and controls |
| reader.css / reader.js | Local browser assets |
| manifest.json | Project, page count, page dimensions, chapter starts and PDF paths |
| manifest.js | Same manifest for offline browser use without fetch restrictions |
| pdfs/documentation.pdf | Complete continuous manual with cover, contents, chapters and conclusion |
| pdfs/overview.pdf | Cover/overview with closing section |
| pdfs/<chapter-id>.pdf | One complete standalone chapter with publisher/contact and closing section |
| assets/pdf-pages/page-NNN.jpg | Exact full-PDF page previews for the continuous reader |
| assets/images/official/ | Copied header and watermark logos |
| assets/images/walkthrough/ | Project-specific screenshots supplied before building |

Full output count is number of content chapters + 2 PDFs. The 91-page reference and its chapter count are examples only. Rebuilding updates generated filenames but does not automatically remove obsolete chapter PDFs or old page images; remove only confirmed stale generated assets if chapter/page counts decrease. Do not delete project screenshots or unrelated files automatically.

## Reader options visible to users

| Control | Behavior |
| --- | --- |
| Sidebar chapter link | Jumps to the chapter's first PDF page |
| Find a chapter | Filters sidebar chapter titles; does not search PDF body text |
| Page input and Go | Navigates to a page; values are bounded to the manual's page range |
| Full PDF | Downloads pdfs/documentation.pdf |
| Chapter PDF | Downloads the chapter associated with the current page |
| Scrolling | Updates the page input, active chapter, current label and chapter download |
| Small-screen view | Sidebar becomes a compact section above the reader |
| Browser print | Hides browser controls; official file downloads remain the preferred export |

PDF page previews are raster images. Selectable text is available in PDF downloads; the default generic reader does not include the old Quizs reader's optional HTML text-view toggle. Add a text view only when needed, using the same content JSON and verified accessibility behavior.

## Troubleshooting

Missing font: install or point ARKNOX_FONT_DIR to the approved licensed fonts; do not silently change typography. Missing screenshot: check imageFile relative to --output. Duplicate/reserved ID: use unique lowercase-hyphen chapter IDs. Legend mismatch: give each annotation one marks entry. Table row too tall: shorten or split its explanation into details. Stale downloads: rebuild and reopen the index; inspect manifest paths. Build success with poor layout: inspect actual page renders, because structural verification cannot detect every cell clipping issue.

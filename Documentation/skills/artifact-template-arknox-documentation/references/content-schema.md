# Portable builder input

Use UTF-8 JSON. The builder generates inside --output. imageFile paths are relative to that output directory and must name existing local images within it. IDs use lowercase letters, digits, hyphens; overview and conclusion are reserved.

```json
{
  "project": "Project name",
  "subtitle": "Administrator and Application Documentation",
  "intro": "Verified project-specific purpose and scope.",
  "overview": [["Administrator Features", "Actual features."]],
  "provenance": "Actual local screenshots using synthetic data; state limitations.",
  "conclusion": "Project-specific closing guidance.",
  "release_checks": ["Verify one complete task from each module."],
  "chapters": [{
    "id": "manage-records",
    "title": "Create and manage records",
    "label": "Manage records",
    "group": "Administrator",
    "intro": "What this screen does.",
    "path": "Admin → Records",
    "steps": ["Open the create form.", "Complete the fields and save."],
    "fields": [["Status", "Exact choices and source.", "Effect of changing it."]],
    "details": [["Delete confirmation", "<p>Verified message, Cancel and confirmation behavior.</p>"]],
    "verify": "Reload and confirm the saved result.",
    "sources": ["Relative source path and relevant symbol"]
  }]
}
```

This is a schema example, not completed documentation. Replace instructional prose with verified facts. project, intro, chapters are required. Each chapter needs id, title, intro, nonempty steps, fields (three cells per row), verify, sources. Optional note creates a highlighted implementation-limit box. details are heading/HTML pairs; support paragraphs, bold, italic, code, ordered/unordered lists, and pre blocks. Preserve real code newlines.

Optional screenshot properties on a chapter or gallery item:

```json
{
  "imageFile": "assets/images/walkthrough/create-record.jpg",
  "caption": "Actual local preview with synthetic data",
  "mobile": false,
  "illustrative": false,
  "marks": ["Select the verified status."],
  "points": [[130, 180, 330, 240]]
}
```

Each point is [circleX, circleY, targetX, targetY] in source-image pixels. All coordinates must lie within the image. Match one legend per point, in order. gallery is an array of objects with title, intro, and these screenshot properties.

Branding is fixed in the skill. Project title/content/chapters/images/access instructions/release checks are variable. Keep retained references unchanged.

Python dependencies: reportlab, beautifulsoup4, svglib, Pillow, pymupdf. The portable builder needs no Node, CDN, original Word file, Quizs source, or old preview environment. On another workstation extract the complete skill folder into its personal Codex skills directory and use that workstation's runtime and installed approved fonts.

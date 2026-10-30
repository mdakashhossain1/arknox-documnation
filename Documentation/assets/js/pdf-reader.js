(() => {
  const manifest = window.quizsPdfManifest;
  if (!manifest) return;
  const main = document.querySelector('main');
  const chapters = Object.entries(manifest.chapters).sort((a, b) => a[1].page - b[1].page);
  const reader = document.createElement('div');
  reader.className = 'pdf-reader';
  reader.innerHTML = `<div class="pdf-reader-toolbar"><span>Official document · ${manifest.pages} pages</span><label>Page <input type="number" min="1" max="${manifest.pages}" value="1" aria-label="Go to document page"></label><button type="button" class="pdf-page-go">Go</button></div><div class="pdf-pages"></div>`;
  const pages = reader.querySelector('.pdf-pages');
  const input = reader.querySelector('input');
  const pageElements = [];
  let suppressUntil = 0;
  let documentMode = true;
  function chapterAt(page) {
    return [...chapters].reverse().find(([, chapter]) => chapter.page <= page)?.[0] || 'overview';
  }
  for (let number = 1; number <= manifest.pages; number++) {
    const page = document.createElement('figure');
    page.className = 'pdf-page';
    page.id = `pdf-page-${number}`;
    page.dataset.page = number;
    const chapter = manifest.chapters[chapterAt(number)];
    page.innerHTML = `<img src="assets/pdf-pages/page-${String(number).padStart(3, '0')}.jpg" width="${Math.round(manifest.pageWidth * 1.6)}" height="${Math.round(manifest.pageHeight * 1.6)}" loading="lazy" decoding="async" alt="${chapter.title.replaceAll('&', '&amp;').replaceAll('"', '&quot;')} — official document page ${number}"><figcaption>Page ${number} of ${manifest.pages}</figcaption>`;
    pages.append(page);
    pageElements.push(page);
  }
  main.prepend(reader);
  const viewButton = document.createElement('button');
  viewButton.type = 'button';
  viewButton.className = 'pdf-view-toggle';
  document.querySelector('.sidebar-search').append(viewButton);
  function goToPage(number, syncChapter = true) {
    const value = Math.min(manifest.pages, Math.max(1, Number(number) || 1));
    suppressUntil = performance.now() + 600;
    input.value = value;
    const offset = document.querySelector('.top-bar').getBoundingClientRect().height + reader.querySelector('.pdf-reader-toolbar').getBoundingClientRect().height + 16;
    window.scrollTo({top: pageElements[value - 1].getBoundingClientRect().top + window.scrollY - offset, behavior: 'instant'});
    const id = chapterAt(value);
    if (syncChapter && document.querySelector('.doc-section.active')?.id !== id) { history.replaceState(null, '', `#${id}`);document.dispatchEvent(new CustomEvent('pdfchapterchange')); }
  }
  function navigate(id) {
    if (documentMode && manifest.chapters[id]) goToPage(manifest.chapters[id].page, false);
  }
  function updateMode() {
    document.body.classList.toggle('pdf-reader-mode', documentMode);
    viewButton.textContent = documentMode ? 'Switch to text view' : 'Switch to official document view';
    viewButton.setAttribute('aria-pressed', String(documentMode));
  }
  viewButton.addEventListener('click', () => {
    documentMode = !documentMode;
    updateMode();
    if (documentMode) navigate(document.querySelector('.doc-section.active')?.id || 'overview');
    else document.querySelector('.doc-section.active')?.scrollIntoView({block: 'start'});
  });
  reader.querySelector('.pdf-page-go').addEventListener('click', () => goToPage(input.value));
  input.addEventListener('keydown', event => { if (event.key === 'Enter') goToPage(input.value); });
  let queued = false;
  window.addEventListener('scroll', () => {
    if (!documentMode || queued || performance.now() < suppressUntil) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      const page = pageElements.find(element => { const bounds = element.getBoundingClientRect(); return bounds.top < 260 && bounds.bottom > 260; });
      if (!page) return;
      const number = Number(page.dataset.page);
      input.value = number;
      const id = chapterAt(number);
      if (document.querySelector('.doc-section.active')?.id !== id) {
        history.replaceState(null, '', `#${id}`);
        document.dispatchEvent(new CustomEvent('pdfchapterchange'));
      }
    });
  }, {passive: true});
  window.quizsPdfReader = {navigate};
  updateMode();
  requestAnimationFrame(() => navigate(document.querySelector('.doc-section.active')?.id || location.hash.slice(1) || 'overview'));
})();

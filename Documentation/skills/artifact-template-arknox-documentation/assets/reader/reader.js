(() => {
  const manual = window.arknoxManual;
  const chapters = Object.entries(manual.chapters).sort((a, b) => a[1].page - b[1].page);
  const input = document.querySelector('#page');
  const nav = document.querySelector('nav');
  const pages = document.querySelector('#pages');
  const nodes = [];
  let current = 'overview';
  let suppressUntil = 0;
  let scheduled = false;
  let group = '';
  document.title = manual.project + ' — Arknox Documentation';
  document.querySelector('#project').textContent = manual.project;
  document.querySelector('#full').href = manual.full;
  document.querySelector('#total').textContent = 'of ' + manual.pages;
  input.max = manual.pages;
  for (const [id, chapter] of chapters) {
    if (chapter.group !== group) {
      group = chapter.group;
      const heading = document.createElement('h2');
      heading.textContent = group;
      nav.append(heading);
    }
    const link = document.createElement('a');
    link.href = '#' + id;
    link.dataset.id = id;
    link.textContent = chapter.label || chapter.title;
    nav.append(link);
  }
  for (let page = 1; page <= manual.pages; page++) {
    const figure = document.createElement('figure');
    const image = document.createElement('img');
    image.src = 'assets/pdf-pages/page-' + String(page).padStart(3, '0') + '.jpg';
    image.width = Math.round(manual.pageWidth * 1.6);
    image.height = Math.round(manual.pageHeight * 1.6);
    image.alt = manual.project + ' documentation page ' + page;
    image.loading = page < 3 ? 'eager' : 'lazy';
    const caption = document.createElement('figcaption');
    caption.textContent = 'Page ' + page + ' of ' + manual.pages;
    figure.append(image, caption);
    pages.append(figure);
    nodes.push(figure);
  }
  function update(page) {
    current = [...chapters].reverse().find(([, chapter]) => chapter.page <= page)[0];
    input.value = page;
    document.querySelector('#current').textContent = manual.chapters[current].title;
    document.querySelector('#chapter').href = manual.chapters[current].pdf;
    nav.querySelectorAll('a').forEach(link => {
      if (link.dataset.id === current) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }
  function go(page) {
    page = Math.max(1, Math.min(manual.pages, Math.round(Number(page) || 1)));
    update(page);
    suppressUntil = performance.now() + 700;
    const offset = document.querySelector('header').getBoundingClientRect().height + 16;
    window.scrollTo({top: nodes[page - 1].getBoundingClientRect().top + window.scrollY - offset, behavior: 'instant'});
  }
  function navigate() {
    const id = location.hash.slice(1);
    go(manual.chapters[id]?.page || 1);
  }
  window.addEventListener('hashchange', navigate);
  nav.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (link && link.dataset.id === location.hash.slice(1)) go(manual.chapters[link.dataset.id].page);
  });
  document.querySelector('#page-form').addEventListener('submit', event => {event.preventDefault(); go(input.value);});
  document.querySelector('#search').addEventListener('input', event => {
    const value = event.target.value.toLowerCase();
    nav.querySelectorAll('a').forEach(link => {link.hidden = !link.textContent.toLowerCase().includes(value);});
  });
  window.addEventListener('scroll', () => {
    if (scheduled || performance.now() < suppressUntil) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      const threshold = document.querySelector('header').getBoundingClientRect().bottom + 60;
      const found = nodes.findIndex(node => node.getBoundingClientRect().bottom > threshold);
      update(found < 0 ? manual.pages : found + 1);
    });
  }, {passive: true});
  navigate();
})();

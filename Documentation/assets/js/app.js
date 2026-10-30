document.addEventListener('DOMContentLoaded', () => {
  const navItems = [...document.querySelectorAll('.nav-item')];
  const sections = [...document.querySelectorAll('.doc-section')];
  const search = document.getElementById('docSearch');
  const sidebar = document.querySelector('.sidebar');
  const menu = document.getElementById('mobileMenuBtn');
  const themeButton = document.getElementById('themeToggle');
  const ids = sections.map(s => s.id);
  const results = document.createElement('div');
  results.className = 'guide-results';
  results.setAttribute('aria-live','polite');
  search.parentElement.parentElement.append(results);
  search.setAttribute('aria-label','Search all documentation');
  const main = document.querySelector('main');
  const labelFor = id => navItems.find(a => a.dataset.target === id)?.querySelector('.nav-text')?.textContent || id;
  function showHash(event) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = ''; }
    const anchor = document.getElementById(id);
    const section = anchor?.classList.contains('doc-section') ? anchor : anchor?.closest('.doc-section');
    const target = section || document.getElementById('overview');
    sections.forEach(s => s.classList.toggle('active',s === target));
    navItems.forEach(a => {
      const active = a.dataset.target === target.id;
      a.classList.toggle('active',active);
      if(active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    const activeLink = navItems.find(a => a.dataset.target === target.id);
    const group = activeLink?.closest('.nav-group')?.querySelector('.nav-group-title')?.textContent || 'Documentation';
    document.getElementById('breadcrumbSection').textContent = `${group} / ${labelFor(target.id)}`;
    document.title = `${labelFor(target.id)} — Quizs Documentation`;
    sidebar.classList.remove('open');
    menu?.setAttribute('aria-expanded','false');
    const index = ids.indexOf(target.id);
    for(const [direction,offset] of [['prev',-1],['next',1]]) {
      const button = document.querySelector(`.nav-page-btn.${direction}`);
      const nextId = ids[index+offset];
      button.style.display = nextId ? 'inline-flex' : 'none';
      if(nextId) { button.dataset.target=nextId; button.querySelector('.btn-label').textContent=direction === 'prev' ? `← ${labelFor(nextId)}` : `${labelFor(nextId)} →`; }
    }
    if(event?.type === 'pdfchapterchange') return;
    if(document.body.classList.contains('pdf-reader-mode')) { window.quizsPdfReader?.navigate(target.id);return; }
    if(anchor && anchor !== target) requestAnimationFrame(() => anchor.scrollIntoView({block:'start'}));
    else window.scrollTo({top:0,behavior:'instant'});
  }
  document.querySelectorAll('.nav-page-btn').forEach(button => button.addEventListener('click', () => { if(button.dataset.target)location.hash=button.dataset.target; }));
  window.addEventListener('hashchange',showHash);
  document.addEventListener('pdfchapterchange',showHash);
  showHash();
  search.addEventListener('input', () => {
    const query=search.value.toLocaleLowerCase().trim();
    results.replaceChildren();
    navItems.forEach(a => { a.style.display=''; });
    if(!query)return;
    const matches=sections.filter(section=>`${labelFor(section.id)} ${section.textContent}`.toLocaleLowerCase().includes(query));
    const visibleIds=new Set(matches.map(s=>s.id));
    navItems.forEach(a=>{a.style.display=visibleIds.has(a.dataset.target)?'':'none';});
    if(!matches.length) { const p=document.createElement('p');p.textContent='No guide found. Try “question”, “notification”, or “target”.';results.append(p);return; }
    matches.forEach(section=>{
      const a=document.createElement('a');a.href=`#${section.id}`;
      const title=document.createElement('strong');title.textContent=labelFor(section.id);
      const snippet=document.createElement('small');
      const text=section.textContent.replace(/\s+/g,' ').trim();
      const index=text.toLocaleLowerCase().indexOf(query);
      snippet.textContent=`…${text.slice(Math.max(0,index-35),Math.max(0,index-35)+115)}…`;
      a.append(title,snippet);results.append(a);
    });
  });
  search.addEventListener('keydown',e=>{if(e.key==='Escape'){search.value='';search.dispatchEvent(new Event('input'));}if(e.key==='Enter'){const first=results.querySelector('a');if(first){location.hash=first.hash;main.focus({preventScroll:true});}}});
  document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();search.focus();}if(e.key==='Escape'){sidebar.classList.remove('open');menu?.setAttribute('aria-expanded','false');}});
  document.querySelectorAll('.btn-copy').forEach(button=>button.addEventListener('click',async()=>{
    const code=button.closest('.code-container')?.querySelector('pre code');
    if(!code)return;
    const original=button.textContent;
    try { await navigator.clipboard.writeText(code.textContent);button.textContent='Copied!'; }
    catch { const range=document.createRange();range.selectNodeContents(code);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);button.textContent='Selected — Ctrl+C'; }
    setTimeout(()=>{button.textContent=original;},1800);
  }));
  let theme='light';
  try { theme=localStorage.getItem('arknox-doc-theme')==='dark'?'dark':'light'; } catch {}
  function applyTheme(value) {
    document.documentElement.dataset.theme=value;
    themeButton.textContent=value==='dark'?'Light mode':'Dark mode';
    themeButton.setAttribute('aria-label',value==='dark'?'Switch to light theme':'Switch to dark theme');
    themeButton.setAttribute('aria-pressed',String(value==='dark'));
  }
  applyTheme(theme);
  themeButton.addEventListener('click',()=>{theme=document.documentElement.dataset.theme==='dark'?'light':'dark';applyTheme(theme);try{localStorage.setItem('arknox-doc-theme',theme);}catch{}});
  function downloadPdf(path, filename) { const link=document.createElement('a');link.href=path;link.download=filename;document.body.append(link);link.click();link.remove(); }
  const chapterPdfButton=document.getElementById('printBtn');
  chapterPdfButton.title='Download the current chapter in the official PDF format';
  chapterPdfButton.setAttribute('aria-label','Download current chapter PDF');
  chapterPdfButton.querySelector('svg').innerHTML='<path d="M12 3v12m-5-5 5 5 5-5M5 17v4h14v-4"/>';
  chapterPdfButton.addEventListener('click',()=>{const id=document.querySelector('.doc-section.active')?.id || 'overview';const chapter=window.quizsPdfManifest?.chapters[id];if(chapter)downloadPdf(chapter.pdf,`Quizs-${id}.pdf`);});
  const fullPdfButton=document.createElement('button');fullPdfButton.type='button';fullPdfButton.className='btn-action';fullPdfButton.textContent='Full PDF';fullPdfButton.setAttribute('aria-label','Download full documentation PDF');fullPdfButton.title='Download the complete continuous manual';chapterPdfButton.before(fullPdfButton);
  fullPdfButton.addEventListener('click',()=>{if(window.quizsPdfManifest)downloadPdf(window.quizsPdfManifest.full,'Quizs-Documentation.pdf');});
  menu.setAttribute('aria-expanded','false');
  menu.addEventListener('click',()=>{const open=sidebar.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
});

(() => {
  const chapters = [
  {
    "id": "admin-login-dash",
    "label": "Dashboard & analytics",
    "path": "Admin → Dashboard",
    "image": "dashboard",
    "sources": [
      "app/Http/Controllers/Admin/DashboardController.php",
      "resources/views/admin/dashboard.blade.php",
      "config/quiz.php"
    ]
  },
  {
    "id": "admin-categories",
    "label": "Categories",
    "path": "Admin → Categories → Add Category",
    "image": "category-create",
    "sources": [
      "app/Http/Controllers/Admin/CategoryController.php",
      "app/Http/Controllers/Api/QuizApiController.php",
      "database/migrations/2026_09_16_104127_create_quizzes_table.php"
    ]
  },
  {
    "id": "admin-quizzes",
    "label": "Quizzes & publishing",
    "path": "Admin → Quizzes → New Quiz",
    "image": "quiz-create",
    "sources": [
      "app/Http/Controllers/Admin/QuizController.php",
      "app/Services/QuizStatsService.php",
      "lib/services/quiz_api_service.dart"
    ]
  },
  {
    "id": "admin-questions",
    "label": "Question Bank • step by step",
    "path": "Admin → Questions Bank → Add Question",
    "image": "question-bilingual",
    "sources": [
      "app/Http/Controllers/Admin/QuestionController.php",
      "resources/views/admin/questions/create.blade.php",
      "lib/models/question_model.dart"
    ]
  },
  {
    "id": "admin-attempts",
    "label": "Attempts, PDF & CSV",
    "path": "Admin → Quiz Attempts",
    "image": "attempts",
    "sources": [
      "app/Http/Controllers/Admin/QuizAttemptController.php",
      "app/Http/Controllers/Api/QuizApiController.php"
    ]
  },
  {
    "id": "admin-users",
    "label": "Users & account controls",
    "path": "Admin → Users → Edit",
    "image": "user-edit",
    "sources": [
      "app/Http/Controllers/Admin/UserController.php",
      "app/Models/User.php",
      "app/Services/TargetService.php"
    ]
  },
  {
    "id": "admin-targets",
    "label": "Daily Targets",
    "path": "Admin → Daily Targets",
    "image": "targets",
    "sources": [
      "app/Http/Controllers/Admin/TargetController.php",
      "app/Services/TargetService.php",
      "app/Services/ProgressionService.php"
    ]
  },
  {
    "id": "admin-attendance",
    "label": "Attendance",
    "path": "Admin → Attendance",
    "image": "attendance",
    "sources": [
      "app/Http/Controllers/Admin/AttendanceController.php",
      "app/Services/AttendanceStatsService.php",
      "lib/screens/attendance_screen.dart"
    ]
  },
  {
    "id": "admin-notifications",
    "label": "Push notifications",
    "path": "Admin → Push Notifications → New Push Notification",
    "image": "notification-create",
    "sources": [
      "app/Http/Controllers/Admin/PushNotificationController.php",
      "app/Services/PushNotificationService.php",
      "app/Services/FcmService.php",
      "lib/services/notification_navigation.dart"
    ]
  },
  {
    "id": "admin-settings",
    "label": "Settings overview",
    "path": "Admin → Settings",
    "image": "settings",
    "sources": [
      "resources/views/admin/settings/index.blade.php",
      "app/Http/Controllers/Admin/SettingsController.php"
    ]
  },
  {
    "id": "settings-general",
    "label": "General settings",
    "path": "Settings → General Settings",
    "image": "settings-general",
    "sources": [
      "app/Services/TargetService.php",
      "app/Models/AppSetting.php"
    ]
  },
  {
    "id": "settings-email",
    "label": "SMTP & email testing",
    "path": "Settings → Email Configuration",
    "image": "settings-email",
    "sources": [
      "app/Http/Controllers/Admin/EmailSettingsController.php",
      "config/mail.php",
      "app/Http/Controllers/CronController.php"
    ]
  },
  {
    "id": "settings-firebase",
    "label": "Firebase service account",
    "path": "Settings → Firebase Credentials",
    "image": "settings-firebase",
    "sources": [
      "app/Http/Controllers/Admin/FirebaseSettingsController.php",
      "app/Services/FcmService.php",
      "lib/services/push_notification_service.dart"
    ]
  },
  {
    "id": "settings-captcha",
    "label": "Login Captcha • Turnstile",
    "path": "Settings → Login Captcha",
    "image": "settings-turnstile",
    "sources": [
      "app/Http/Controllers/Admin/TurnstileSettingsController.php",
      "app/Http/Controllers/Admin/AdminAuthController.php"
    ]
  },
  {
    "id": "settings-migrations",
    "label": "Database migrations",
    "path": "Settings → Database Migrations",
    "image": "settings-migrations",
    "sources": [
      "app/Http/Controllers/Admin/DatabaseMigrationController.php",
      "database/migrations"
    ]
  },
  {
    "id": "admin-offerwall",
    "label": "Offerwall & transactions",
    "path": "Admin → Offerwall",
    "image": "offerwall",
    "sources": [
      "config/offerwall.php",
      "app/Http/Controllers/Api/OfferwallController.php",
      "app/Services/OfferwallService.php",
      "lib/services/offerwall_service.dart"
    ]
  },
  {
    "id": "app-walkthrough",
    "label": "App screens & data",
    "path": "Quizs App → Home / Quiz / Profile",
    "image": "app-home",
    "mobile": true,
    "sources": [
      "lib/quizs_app.dart",
      "lib/l10n/app_strings.dart",
      "lib/services/quiz_api_service.dart",
      "app/Services/ProfileStatsService.php",
      "app/Services/RankingService.php"
    ]
  },
  {
    "id": "customization-map",
    "label": "What changes where?",
    "path": "Admin settings / Server config / Flutter source",
    "sources": [
      "config/quiz.php",
      "lib/services/api_client.dart",
      "lib/services/iron_source_service.dart",
      "lib/l10n/app_strings.dart"
    ]
  },
  {
    "id": "troubleshooting",
    "label": "Troubleshooting & checks",
    "path": "Symptom → Source → Resolution",
    "sources": [
      "app/Http/Controllers",
      "lib/services",
      "config"
    ]
  },
  {
    "id": "monetization",
    "label": "Ads & LevelPlay",
    "path": "Flutter → IronSourceService / banner slot",
    "sources": [
      "lib/services/iron_source_service.dart",
      "lib/widgets/iron_source_banner_slot.dart",
      "pubspec.yaml"
    ]
  },
  {
    "id": "app-profile-guide",
    "label": "App Profile & preferences",
    "path": "App → Profile",
    "image": "app-profile",
    "mobile": true,
    "sources": [
      "app/Services/ProfileStatsService.php",
      "app/Services/RankingService.php",
      "lib/screens/profile_screen.dart",
      "lib/services/sound_service.dart"
    ]
  },
  {
    "id": "app-results-guide",
    "label": "App Results & ranking",
    "path": "App → Quiz complete → Results",
    "image": "app-results",
    "mobile": true,
    "sources": [
      "app/Http/Controllers/Api/QuizApiController.php",
      "app/Services/QuizRankingService.php",
      "app/Services/PerformanceMessageService.php",
      "lib/screens/results_screen.dart"
    ]
  },
  {
    "id": "app-attendance-guide",
    "label": "App Attendance",
    "path": "App → Attendance",
    "image": "app-attendance",
    "mobile": true,
    "sources": [
      "app/Services/AttendanceStatsService.php",
      "lib/screens/attendance_screen.dart"
    ]
  },
  {
    "id": "app-achievements-guide",
    "label": "App Achievements",
    "path": "App → Home → Achievement",
    "image": "app-achievements",
    "mobile": true,
    "sources": [
      "app/Http/Controllers/Api/AchievementController.php",
      "app/Services/RankingService.php",
      "app/Services/ActiveUsersService.php",
      "lib/screens/achievements_screen.dart"
    ]
  },
  {
    "id": "app-inbox-guide",
    "label": "App Notifications inbox",
    "path": "App → Bell / Profile → Notification",
    "image": "app-notifications",
    "mobile": true,
    "sources": [
      "app/Http/Controllers/Api/NotificationController.php",
      "lib/screens/notifications_screen.dart",
      "lib/services/notification_navigation.dart"
    ]
  },
  {
    "id": "admin-list-guide",
    "label": "Lists, search & filtering",
    "path": "Admin → Categories / Quizzes / Questions / Users",
    "image": "question-list",
    "sources": [
      "app/Http/Controllers/Admin/QuestionController.php",
      "app/Http/Controllers/Admin/UserController.php",
      "public/js/admin-ajax-table.js"
    ]
  }
].map(chapter => ({...chapter, ...window.quizsGuideContent[chapter.id]}));

  const safe = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 4h7a3 3 0 0 1 3 3v14a4 4 0 0 0-4-3H4zM14 7a3 3 0 0 1 3-3h3v14h-2a4 4 0 0 0-4 3"/></svg>';
  chapters.push({...window.quizsGuideContent['cpanel-setup'], id:'cpanel-setup', label:'cPanel deployment', path:'Hosting → Database / Files / Domain / Terminal'});
  chapters.push({...window.quizsGuideContent['environment-settings'], id:'environment-settings'});
  function figure(c) {
    if (!c.image) return '';
    const metadata = window.quizsScreenshots[c.image];
    const points = metadata?.points || [];
    const width = metadata?.width || 1200, height = metadata?.height || 1050;
    const radius = c.mobile ? 11 : 21;
    const arrows = points.map((p, i) => {
      if (!p || p.y < 3 || p.y > 96) return '';
      const bx = Math.min(96, p.x + 9), by = Math.max(4, p.y - 6);
      const x=bx*width/100,y=by*height/100;
      return `<path d="M${x-radius*.7},${y+radius*.5} L${p.x*width/100},${p.y*height/100}" stroke="#ac3500" stroke-width="${c.mobile ? 2 : 3.5}" marker-end="url(#arrow-${c.id})"/><circle cx="${x}" cy="${y}" r="${radius}" fill="#ac3500" stroke="white" stroke-width="2"/><text x="${x}" y="${y+radius*.36}" text-anchor="middle" font-size="${radius*1.1}" font-family="sans-serif" fill="white" font-weight="700">${i+1}</text>`;
    }).join('');
    const overlay = arrows ? `<svg viewBox="0 0 ${width} ${height}" aria-hidden="true"><defs><marker id="arrow-${c.id}" markerWidth="4" markerHeight="4" refX="3" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4" fill="#ac3500"/></marker></defs>${arrows}</svg>` : '';
    return `<figure class="guide-figure"><div class="guide-screen${c.mobile ? ' mobile' : ''}"><img src="${c.imageFile || `assets/images/walkthrough/${c.image}.jpg`}" alt="${safe(c.title)} — ${c.illustrative ? 'Illustrative setup map' : `Actual ${c.mobile ? 'Flutter browser preview' : 'Quizs admin'} screen, local sample data`}" loading="lazy">${overlay}<button class="screen-open" type="button" data-image="${c.image}" aria-label="${safe(c.title)} Enlarge screenshot">Enlarge ↗</button></div><figcaption>${c.illustrative ? 'Illustrative setup map • not a live hosting screenshot' : `Actual ${c.mobile ? 'Flutter source browser preview' : 'admin screen'} • local demo data • Your live values will differ.`}</figcaption>${arrows ? `<ul class="screen-legend">${(c.marks || []).map((m,i)=>`<li><b>${i+1}</b>${safe(m)}</li>`).join('')}</ul>` : ''}</figure>`;
  }
  function render(c) {
    const headingId = suffix => `${c.id}-${suffix}`;
    return `<h1 lang="en">${c.title}</h1><p class="guide-intro" lang="en">${c.intro}</p><div class="guide-meta"><span>${icon} Verified against source code</span><span>Screen: ${c.path}</span></div><nav class="guide-toc" aria-label="In this chapter"><a href="#${headingId('steps')}">Step by step</a><a href="#${headingId('fields')}">Field reference</a>${c.details ? `<a href="#${headingId('details')}">Data and behavior</a>` : ''}<a href="#${headingId('verify')}">Verify in the app</a></nav>${figure(c)}<h2 id="${headingId('steps')}">Step by step</h2><ol class="guide-steps">${c.steps.map(s=>`<li><div>${s}</div></li>`).join('')}</ol><h2 id="${headingId('fields')}">Field definitions and change impact</h2><div class="guide-table-wrap"><table class="guide-table"><thead><tr><th scope="col">Field / Feature</th><th scope="col">Definition and source</th><th scope="col">Effect of changes</th></tr></thead><tbody>${c.fields.map(row=>`<tr>${row.map(v=>`<td>${v}</td>`).join('')}</tr>`).join('')}</tbody></table></div>${c.note ? `<aside class="guide-note warning"><strong>Current implementation limit</strong>${c.note}</aside>` : ''}${c.details ? `<h2 id="${headingId('details')}">Data and behavior in detail</h2>${c.details.map(([h,p])=>`<h3>${h}</h3><p>${p}</p>`).join('')}` : ''}<h2 id="${headingId('verify')}">Verify in the app</h2><aside class="guide-note"><strong>Verification after saving</strong>${c.verify}</aside><details class="guide-sources"><summary>Technical sources for this guide</summary><p>Server paths are inside “Quiz Application Admin”; lib paths are inside “Quiz Application”.</p><ul>${c.sources.map(f=>`<li><code>${safe(f)}</code></li>`).join('')}</ul></details><p class="guide-reader">Use sidebar search to find what to change and where. Screenshots use local sample data and do not validate phone delivery or provider integrations.</p>`;
  }
  const main = document.querySelector('main');
  const footer = document.querySelector('.page-nav-footer');
  const nav = document.querySelector('.sidebar-nav');
  const added = [];
  chapters.forEach(c => {
    let section = document.getElementById(c.id);
    if (!section) {
      section = document.createElement('section'); section.id = c.id; section.className = 'doc-section'; main.insertBefore(section, document.getElementById('mobile-app') || footer); added.push(c);
    }
    section.setAttribute('lang','en'); section.innerHTML = render(c);
    if(c.gallery) {
      const gallery=document.createElement('div');gallery.className='guide-gallery';
      gallery.innerHTML='<h2>Understand each part of the screen</h2>'+c.gallery.map((item,i)=>`<h3>${item.title}</h3><p>${item.intro}</p>${figure({...item,id:c.id+'-figure-'+i})}`).join('');
      section.insertBefore(gallery,section.querySelector('.guide-sources'));
    }
    const link = nav.querySelector(`[data-target="${c.id}"]`);
    if (link) link.querySelector('.nav-text').textContent = c.label;
  });
  const mobileGroup=nav.querySelector('[data-target="mobile-app"]').closest('.nav-group');
  const groups=[['Daily operations',['admin-targets','admin-attendance','admin-offerwall','admin-list-guide']],['Settings in detail',['settings-general','settings-email','settings-firebase','settings-captcha','settings-migrations','environment-settings']],['App walkthrough',['app-walkthrough','app-profile-guide','app-results-guide','app-attendance-guide','app-achievements-guide','app-inbox-guide']],['Customization & help',['customization-map','troubleshooting']]];
  groups.forEach(([title,ids])=>{const group=document.createElement('div');group.className='nav-group';group.innerHTML=`<div class="nav-group-title">${title}</div>${ids.map(id=>{const c=added.find(c=>c.id===id);return c?`<a class="nav-item" href="#${c.id}" data-target="${c.id}">${icon}<span class="nav-text">${c.label}</span></a>`:'';}).join('')}`;nav.insertBefore(group,mobileGroup);});
  document.getElementById('overview').innerHTML = `<div class="guide-home"><h1>Your complete guide to Quizs.</h1><p class="guide-intro">From your first category to questions, notifications, and app statistics: clear steps, actual screens, and the effect of every change.</p><a class="guide-start" href="#admin-questions">Add your first question <span aria-hidden="true">→</span></a><div class="guide-meta"><span>Laravel admin + Flutter app</span><span>English documentation</span><span>Offline documentation</span></div></div><h2>What would you like to do?</h2><div class="guide-directory">${[['admin-login-dash','Understand the dashboard','Sources behind every number, chart, and report.'],['admin-questions','Prepare questions','Four choices, correct answers, and bilingual content.'],['admin-notifications','Send notifications','Message, audience, and tap destination.'],['admin-users','Manage users and targets','Accounts, global goals, and individual targets.'],['app-walkthrough','Understand app data','Home, results, profile, attendance, and achievements.'],['customization-map','Find a customization','Changes in admin, server configuration, or app code.']].map(([id,h,p])=>`<a href="#${id}"><div><strong>${h}</strong><p>${p}</p></div><span aria-hidden="true">↗</span></a>`).join('')}</div><h2>Publish a new quiz in this order</h2><div class="guide-flow"><span>Category</span><b>→</b><span>Quiz + Language</span><b>→</b><span>Questions + Answers</span><b>→</b><span>Activate</span><b>→</b><span>Test in the app</span></div><aside class="guide-note"><strong>How to use this guide</strong>Each chapter includes numbered screenshot markers, steps, field definitions, current limits, and verification. Server deployment and build/publish chapters are also available in the sidebar.</aside><h2>What is in this folder?</h2><div class="guide-table-wrap"><table class="guide-table"><thead><tr><th>Folder</th><th>Purpose</th><th>How to change it</th></tr></thead><tbody><tr><td>Quiz Application Admin</td><td>Laravel backend, admin, API, emails, and database</td><td>Admin forms or server code/configuration</td></tr><tr><td>Quiz Application</td><td>Flutter screens, strings, assets, and native integrations</td><td>Content API fetch or a new app build</td></tr><tr><td>Documentation</td><td>This offline guide and its screenshots</td><td>Open index.html in a browser</td></tr></tbody></table></div>`;
  document.querySelectorAll('.nav-item[data-target]').forEach(a => { a.href = `#${a.dataset.target}`; });
  const skip = document.createElement('a'); skip.className = 'guide-skip'; skip.href = '#guide-content'; skip.textContent = 'Skip to the guide'; document.body.prepend(skip); main.id = 'guide-content'; main.tabIndex = -1;
  const dialog = document.createElement('dialog'); dialog.className = 'screen-dialog'; dialog.setAttribute('aria-label','Enlarged screenshot'); dialog.innerHTML = '<button type="button">Close ×</button><div class="screen-expanded"></div>'; document.body.append(dialog);
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  document.addEventListener('click', e => { const button=e.target.closest('.screen-open'); if(!button)return; const screen=button.closest('.guide-screen').cloneNode(true);screen.querySelector('.screen-open').remove();screen.querySelectorAll('[id]').forEach(el=>{el.id+= '-expanded';});screen.querySelectorAll('[marker-end]').forEach(el=>{el.setAttribute('marker-end',el.getAttribute('marker-end').replace(')', '-expanded)'));});dialog.querySelector('.screen-expanded').replaceChildren(screen);dialog.showModal(); });
})();

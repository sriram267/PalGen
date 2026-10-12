document.getElementById('runAuditBtn').addEventListener('click', async () => {
  const statusEl = document.getElementById('status');
  statusEl.innerText = 'Auditing active tab...';

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) {
      statusEl.innerText = 'Error: No active tab found.';
      return;
    }

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: auditPageInDom,
    });

    if (results && results[0] && results[0].result) {
      const data = results[0].result;
      document.getElementById('results').style.display = 'block';

      // Headings
      const h1Stat = document.getElementById('h1Stat');
      h1Stat.innerText = data.h1Count;
      h1Stat.style.color = data.h1Count === 1 ? '#34d399' : '#f87171';

      // Alt tags
      const altStat = document.getElementById('altStat');
      altStat.innerText = `${data.missingAlt}/${data.totalImages}`;
      altStat.style.color = data.missingAlt === 0 ? '#34d399' : '#fbbf24';

      // Interactive
      document.getElementById('btnStat').innerText = data.interactiveCount;
      document.getElementById('linkStat').innerText = data.linkCount;

      // SEO
      document.getElementById('titleVal').innerText = data.title || '(None)';
      document.getElementById('titleVal').title = data.title || '';
      document.getElementById('descVal').innerText = data.metaDesc || '(None)';
      document.getElementById('descVal').title = data.metaDesc || '';
      document.getElementById('ogVal').innerText = data.ogTitle || '(None)';

      // Viewport
      const vpPill = document.getElementById('viewportPill');
      if (data.hasViewport) {
        vpPill.className = 'pill pill-green';
        vpPill.innerText = 'Configured';
      } else {
        vpPill.className = 'pill pill-red';
        vpPill.innerText = 'Missing';
      }
      document.getElementById('formsVal').innerText = data.formCount;

      statusEl.innerText = 'Audit complete!';
    } else {
      statusEl.innerText = 'Could not inspect page DOM.';
    }
  } catch (err) {
    statusEl.innerText = 'Error: ' + err.message;
  }
});

function auditPageInDom() {
  const h1Elements = Array.from(document.querySelectorAll('h1'));
  const images = Array.from(document.querySelectorAll('img'));
  const missingAlt = images.filter(img => !img.hasAttribute('alt') || img.getAttribute('alt').trim() === '').length;
  const buttons = document.querySelectorAll('button, input[type="button"], input[type="submit"]');
  const links = document.querySelectorAll('a[href]');
  const forms = document.querySelectorAll('form');
  const viewportMeta = document.querySelector('meta[name="viewport"]');
  const descMeta = document.querySelector('meta[name="description"]');
  const ogTitleMeta = document.querySelector('meta[property="og:title"]');

  return {
    title: document.title || '',
    h1Count: h1Elements.length,
    totalImages: images.length,
    missingAlt,
    interactiveCount: buttons.length,
    linkCount: links.length,
    formCount: forms.length,
    hasViewport: !!viewportMeta,
    metaDesc: descMeta ? descMeta.getAttribute('content') : '',
    ogTitle: ogTitleMeta ? ogTitleMeta.getAttribute('content') : ''
  };
}

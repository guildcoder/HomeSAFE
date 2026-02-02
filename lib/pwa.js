import { store } from './ui.js';

export function registerSW(){
  if (!('serviceWorker' in navigator)) return;
  navigator.serviceWorker.register('./sw.js').catch(()=>{});
}

// iOS doesn't fire the standard beforeinstallprompt. We'll show a friendly banner once.
export function maybeShowA2HS(){
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if (!isIOS || isStandalone) return;

  const seen = store.get('a2hs_seen', false);
  if (seen) return;

  const box = document.querySelector('#a2hs');
  const dismiss = document.querySelector('#a2hsDismiss');
  const done = document.querySelector('#a2hsDone');

  box.hidden = false;
  const close = ()=>{
    box.hidden = true;
    store.set('a2hs_seen', true);
  };
  dismiss.onclick = close;
  done.onclick = close;
}

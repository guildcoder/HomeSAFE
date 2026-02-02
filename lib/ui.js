export async function loadJSON(url){
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load '+url);
  return await res.json();
}

export function shuffleInPlace(arr){
  for (let i=arr.length-1;i>0;i--){
    const j = Math.floor(Math.random()*(i+1));
    [arr[i],arr[j]]=[arr[j],arr[i]];
  }
  return arr;
}
export function sampleOne(arr){
  return arr[Math.floor(Math.random()*arr.length)];
}

export function formatTime(ms){
  const s = Math.max(0, Math.floor(ms/1000));
  const hh = String(Math.floor(s/3600)).padStart(2,'0');
  const mm = String(Math.floor((s%3600)/60)).padStart(2,'0');
  const ss = String(s%60).padStart(2,'0');
  return `${hh}:${mm}:${ss}`;
}

export const store = {
  get(key, fallback=null){
    try{
      const raw = localStorage.getItem(key);
      if (!raw) return fallback;
      return JSON.parse(raw);
    }catch{ return fallback; }
  },
  set(key, value){
    localStorage.setItem(key, JSON.stringify(value));
  },
  del(key){ localStorage.removeItem(key); }
};

export function toast(msg){
  const el = document.querySelector('#toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(()=>el.classList.remove('show'), 1700);
}

export function confirmModal(title, text){
  const modal = document.querySelector('#modal');
  const t = document.querySelector('#modalTitle');
  const p = document.querySelector('#modalText');
  const okBtn = document.querySelector('#modalOk');
  const cancelBtn = document.querySelector('#modalCancel');

  t.textContent = title;
  p.textContent = text;
  modal.hidden = false;

  return new Promise((resolve)=>{
    const cleanup = ()=>{
      modal.hidden = true;
      okBtn.removeEventListener('click', onOk);
      cancelBtn.removeEventListener('click', onCancel);
    };
    const onOk = ()=>{ cleanup(); resolve(true); };
    const onCancel = ()=>{ cleanup(); resolve(false); };
    okBtn.addEventListener('click', onOk);
    cancelBtn.addEventListener('click', onCancel);
  });
}

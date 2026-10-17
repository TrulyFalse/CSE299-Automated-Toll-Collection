(() => {
  const $ = id => document.getElementById(id);
  const scene = $('scene'), car = $('car'), arm = $('arm'), lcd = $('lcd');
  const ledG = $('ledG'), ledR = $('ledR'), dist = $('dist');
  const plate = $('plate'), pl1 = $('pl1'), pl2 = $('pl2'), ocrOut = $('ocrOut');
  const carPlate = $('carPlate'), input = $('plateInput'), runBtn = $('runBtn');
  const steps = [...document.querySelectorAll('#steps li')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wait = ms => new Promise(r => setTimeout(r, reduce ? Math.min(ms, 120) : ms));

  // Demo data only (not from the report)
  const FEE = 80;
  const DB = {
    'DHAKA METRO GA 12-3456': { wallet: 500, stolen: false },
    'DHAKA METRO HA 45-6789': { wallet: 20, stolen: false },
    'CHATTA METRO KA 11-2233': { wallet: 900, stolen: true }
  };

  const norm = s => s.toUpperCase().replace(/\s+/g, ' ').trim();
  function splitPlate(s) {
    const m = s.match(/^(.*?)\s*(\d{2}-?\d{4})$/);
    return m ? [m[1], m[2]] : [s, ''];
  }
  function renderPlate(s, wrapChars) {
    const [a, b] = splitPlate(s);
    const fmt = t => wrapChars ? [...t].map(c => c === ' ' ? ' ' : `<span class="ch">${c}</span>`).join('') : t;
    pl1.innerHTML = fmt(a);
    pl2.innerHTML = fmt(b);
    carPlate.textContent = s || '—';
  }
  const setStep = (key, state) => {
    const li = steps.find(l => l.dataset.s === key);
    steps.forEach(l => l.classList.remove('active'));
    li.classList.remove('done', 'fail');
    if (state === 'active') li.classList.add('active'); else li.classList.add(state);
  };
  function reset() {
    steps.forEach(l => l.classList.remove('active', 'done', 'fail'));
    plate.classList.remove('gray', 'bin', 'seg');
    arm.classList.remove('open');
    ledG.classList.remove('on'); ledR.classList.remove('on');
    ocrOut.textContent = '—';
    lcd.textContent = 'WAITING FOR VEHICLE';
    car.style.transition = 'none';
    car.style.transform = 'translateX(-140px)';
    dist.textContent = '— cm';
    void car.offsetWidth;
  }
  const laneX = () => scene.clientWidth * 0.8 - 118 - 90;   // stop short of the barrier

  async function approach() {
    const stopX = laneX();
    car.style.transition = `transform ${reduce ? 0.1 : 2.6}s cubic-bezier(.2,.7,.3,1)`;
    car.style.transform = `translateX(${stopX}px)`;
    const t0 = performance.now(), dur = reduce ? 100 : 2600;
    await new Promise(res => {
      const tick = now => {
        const p = Math.min(1, (now - t0) / dur);
        dist.textContent = Math.round(160 - 120 * (1 - Math.pow(1 - p, 3))) + ' cm';
        p < 1 ? requestAnimationFrame(tick) : res();
      };
      requestAnimationFrame(tick);
    });
    dist.textContent = '40 cm';
  }

  let busy = false;
  async function run() {
    if (busy) return;
    const text = norm(input.value);
    if (!text) { input.focus(); return; }
    busy = true; runBtn.disabled = true; input.disabled = true;
    reset();
    renderPlate(text, false);
    lcd.textContent = 'VEHICLE DETECTED';

    setStep('sense', 'active');
    await approach();
    lcd.textContent = 'HOLD STILL';
    await wait(500);
    setStep('sense', 'done');

    setStep('capture', 'active');
    await wait(700);
    setStep('capture', 'done');

    setStep('pre', 'active');
    plate.classList.add('gray'); await wait(800);
    plate.classList.add('bin'); await wait(800);
    setStep('pre', 'done');

    setStep('seg', 'active');
    renderPlate(text, true);
    plate.classList.add('seg');
    await wait(900);
    setStep('seg', 'done');

    setStep('ocr', 'active');
    const chars = [...pl1.querySelectorAll('.ch'), ...pl2.querySelectorAll('.ch')];
    let built = '';
    for (const c of chars) {
      c.classList.add('hit');
      built += c.textContent;
      ocrOut.textContent = built;
      await wait(110);
    }
    ocrOut.textContent = text;
    setStep('ocr', 'done');

    setStep('db', 'active');
    lcd.textContent = 'CHECKING...';
    await wait(900);
    const rec = DB[text];
    let ok = false, msg = '', stepNote = '';
    if (!rec) { msg = 'NOT REGISTERED'; stepNote = 'No account for this plate'; }
    else if (rec.stolen) { msg = 'ALERT: STOLEN'; stepNote = 'Plate reported stolen'; }
    else if (rec.wallet < FEE) { msg = 'LOW BALANCE'; stepNote = `Wallet Tk ${rec.wallet} is below the Tk ${FEE} demo fee`; }
    else { ok = true; msg = `PAID Tk ${FEE}`; stepNote = `Tk ${FEE} charged. Wallet now Tk ${rec.wallet - FEE}`; }
    steps.find(l => l.dataset.s === 'db').querySelector('small').textContent = stepNote;
    setStep('db', ok ? 'done' : 'fail');

    setStep('gate', 'active');
    await wait(400);
    lcd.textContent = msg;
    if (ok) {
      ledG.classList.add('on');
      arm.classList.add('open');
      await wait(900);
      car.style.transition = `transform ${reduce ? 0.1 : 1.8}s ease-in`;
      car.style.transform = `translateX(${scene.clientWidth + 40}px)`;
      await wait(1800);
      setStep('gate', 'done');
      steps.find(l => l.dataset.s === 'gate').querySelector('small').textContent = 'Barrier raised, vehicle passed';
      lcd.textContent = 'THANK YOU';
    } else {
      ledR.classList.add('on');
      setStep('gate', 'fail');
      steps.find(l => l.dataset.s === 'gate').querySelector('small').textContent = 'Barrier stays closed';
    }
    busy = false; runBtn.disabled = false; input.disabled = false;
  }

  const defaults = {
    db: 'Registered? E-wallet charged?',
    gate: 'Servo raises or holds the barrier'
  };
  const resetNotes = () => Object.entries(defaults).forEach(([k, v]) =>
    steps.find(l => l.dataset.s === k).querySelector('small').textContent = v);

  runBtn.addEventListener('click', () => { resetNotes(); run(); });
  input.addEventListener('keydown', e => { if (e.key === 'Enter') { resetNotes(); run(); } });
  document.querySelectorAll('.presets button').forEach(b =>
    b.addEventListener('click', () => { if (busy) return; input.value = b.dataset.plate; resetNotes(); run(); }));

  renderPlate(norm(input.value), false);
})();

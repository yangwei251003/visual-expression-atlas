(() => {
  'use strict';
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const easeOut = value => 1 - (1 - clamp(value)) ** 3;
  const smooth = value => { const t = clamp(value); return t * t * (3 - 2 * t); };
  const mix = (a, b, t) => a + (b - a) * t;

  const effects = {
    reveal(root, panes, p) {
      const t = easeOut(p);
      panes.forEach((pane, index) => {
        const content = pane.querySelector('.mv-reveal-inner');
        const marker = pane.querySelector('.mv-cut');
        content.style.opacity = index ? t : 1;
        content.style.clipPath = index ? 'none' : 'inset(0 ' + (100 - t * 100) + '% 0 0)';
        marker.style.opacity = index || t < .005 || t > .995 ? 0 : 1;
        marker.style.left = (t * 100) + '%';
        pane.querySelector('.mv-meter').textContent = index
          ? '整张素材透明度 ' + Math.round(t * 100) + '%'
          : '已露出面积 ' + Math.round(t * 100) + '%';
      });
    },
    stagger(root, panes, p) {
      panes.forEach((pane, index) => {
        const items = [...pane.querySelectorAll('.mv-list-item')];
        let shown = 0;
        items.forEach((item, row) => {
          const local = clamp((p - (index ? 0 : row * .135)) / .48);
          const t = easeOut(local);
          if (local === 1) shown++;
          item.style.opacity = String(t);
          item.style.transform = 'translateY(' + (14 * (1 - t)) + 'px)';
        });
        pane.querySelector('.mv-meter').textContent = '到位 ' + shown + '/4；每项 480 ms 基准进度';
      });
    },
    spring(root, panes, p) {
      const time = p * 1.65;
      const damping = 4.7;
      const frequency = 9.0;
      const spring = p >= .999 ? 1 : 1 - Math.exp(-damping * time) * (Math.cos(frequency * time) + damping/frequency * Math.sin(frequency * time));
      const ease = easeOut(p);
      [spring, ease].forEach((value, index) => {
        const pane = panes[index];
        pane.querySelector('.mv-ball').style.left = (12 + value * 66) + '%';
        pane.querySelector('.mv-meter').textContent = '位移 ' + Math.round(value * 100) + '% ' + (value > 1.015 ? '· 已越过终点' : p >= .999 ? '· 已到位' : '· 朝终点移动');
      });
    },
    parallax(root, panes, p) {
      panes.forEach((pane, index) => {
        const distances = index ? [34, 34, 34] : [12, 30, 62];
        ['far','mid','near'].forEach((name, i) => pane.querySelector('.mv-' + name).style.transform = 'translateY(' + (-distances[i] * p) + 'px)');
        pane.querySelector('.mv-scroll-tick i').style.top = p * 82 + '%';
        pane.querySelector('.mv-meter').textContent = '远 / 中 / 近 ' + distances.map(n => Math.round(n * p) + 'px').join(' / ');
      });
    },
    pointer(root, panes, p, state) {
      const x = state.manual ? state.x : 50 + 36 * Math.sin(2 * Math.PI * p);
      const y = state.manual ? state.y : 50 + 28 * Math.sin(4 * Math.PI * p);
      if (!state.manual) { state.x = x; state.y = y; }
      panes.forEach((pane, index) => {
        const zone = pane.querySelector('.mv-pointer-zone');
        zone.querySelector('.mv-pointer-dot').style.left = x + '%';
        zone.querySelector('.mv-pointer-dot').style.top = y + '%';
        if (!index) {
          zone.style.setProperty('--mx', x + '%'); zone.style.setProperty('--my', y + '%');
          zone.style.setProperty('--cx', ((x - 10) / .8) + '%'); zone.style.setProperty('--cy', ((y - 19) / .62) + '%');
          pane.querySelector('.mv-meter').textContent = '按钮位移 0；光斑 (' + Math.round(x) + '%, ' + Math.round(y) + '%)';
        } else {
          const dx = clamp((x - 50) * .65, -20, 20);
          const dy = clamp((y - 50) * .65, -17, 17);
          zone.querySelector('.mv-magnet').style.transform = 'translate(calc(-50% + ' + dx + 'px), calc(-50% + ' + dy + 'px))';
          pane.querySelector('.mv-meter').textContent = '按钮位移 ' + Math.round(dx) + 'px / ' + Math.round(dy) + 'px';
        }
      });
    },
    shared(root, panes, p) {
      const t = smooth(p);
      panes.forEach((pane, index) => {
        const before = pane.querySelector('.mv-layout-old');
        const after = pane.querySelector('.mv-layout-new');
        before.style.opacity = String(1-t);
        after.style.opacity = String(t);
        if (!index) {
          const fly = pane.querySelector('.mv-layout-fly');
          fly.style.left = mix(17,7,t)+'%';
          fly.style.top = mix(38,27,t)+'%';
          fly.style.width = mix(40,86,t)+'%';
          fly.style.height = mix(23,42,t)+'%';
          pane.querySelector('.mv-meter').textContent = '同一封面：宽度 ' + Math.round(mix(40,86,t)) + '%';
        } else {
          pane.querySelector('.mv-meter').textContent = '旧图 ' + Math.round((1-t)*100) + '% / 新图 ' + Math.round(t*100) + '%';
        }
      });
    },
    feedback(root, panes, p) {
      const press = p < .17 ? p/.17 : p < .31 ? 1-(p-.17)/.14 : 0;
      const result = easeOut((p-.66)/.34);
      panes.forEach((pane, index) => {
        const button = pane.querySelector('.mv-fake-button');
        const ripple = pane.querySelector('.mv-ripple');
        const label = button.querySelector('span');
        const confirmation = pane.querySelector('.mv-confirm-panel');
        button.style.transform = 'scale(' + (index ? 1 : 1-.06*press) + ')';
        const wave = clamp(p/.46);
        ripple.style.transform = 'translate(-50%,-50%) scale(' + (wave*15) + ')';
        ripple.style.opacity = index ? '0' : String((1-wave)*.66);
        confirmation.style.opacity = result;
        confirmation.style.transform = 'translateY(' + (4*(1-result)) + 'px)';
        label.textContent = p >= .66 ? '✓ 已保存' : !index && p > .04 ? '保存中…' : '保存';
        pane.querySelector('.mv-status').textContent = p >= .66 ? '结果已返回' : p > .04 ? (index ? '等待期间没有反馈' : '正在等待保存结果') : '等待操作';
        pane.querySelector('.mv-meter').textContent = p >= .66 ? '共同结果：保存完成' : index ? '延迟反馈：未告知已接收点击' : '及时反馈：按压、扩散、处理中';
      });
    }
  };

  function install(root) {
    const effect = root.dataset.motion;
    if (!effects[effect] || root.dataset.mvReady) return;
    root.dataset.mvReady = 'true';
    const panes = [...root.querySelectorAll('.mv-pane')];
    const slider = root.querySelector('.mv-range');
    const status = root.querySelector('.mv-output');
    const play = root.querySelector('[data-mv-action="play"]');
    const pause = root.querySelector('[data-mv-action="pause"]');
    const reset = root.querySelector('[data-mv-action="reset"]');
    const duration = +(root.dataset.duration || 1800);
    const state = { p: .35, running: false, raf: 0, previous: null, manual: false, x: 50, y: 50, firstPlay: true };

    function render() {
      effects[effect](root, panes, state.p, state);
      slider.value = Math.round(state.p*1000);
      status.value = Math.round(state.p*100) + '%';
      play.disabled = state.running;
      pause.disabled = !state.running;
    }
    function stop() {
      state.running = false;
      state.previous = null;
      cancelAnimationFrame(state.raf);
      render();
    }
    function frame(now) {
      if (!state.running) return;
      if (state.previous === null) state.previous = now;
      const delta = now - state.previous;
      state.previous = now;
      state.p = clamp(state.p + delta / duration);
      if(state.p >= 1) { stop(); return; }
      render();
      state.raf = requestAnimationFrame(frame);
    }
    function start(replay = false) {
      if (state.running) return;
      if (state.p >= 1 || replay || state.firstPlay) state.p = 0;
      state.firstPlay = false;
      state.manual = false;
      state.running = true;
      state.previous = null;
      render();
      state.raf = requestAnimationFrame(frame);
    }
    play.addEventListener('click',() => start());
    pause.addEventListener('click',stop);
    reset.addEventListener('click',() => {
      stop(); state.p = 0; state.manual = false; state.firstPlay = false; render();
    });
    slider.addEventListener('input',() => {
      const next = +slider.value / 1000; stop(); state.p = next; state.manual = false; state.firstPlay = false; render();
    });

    if(effect === 'pointer') {
      function manualMove(x, y) {
        stop();
        state.manual = true;
        state.firstPlay = false;
        state.x = clamp(x,0,100); state.y = clamp(y,0,100);
        render();
      }
      root.querySelectorAll('.mv-pointer-zone').forEach(zone => {
        zone.addEventListener('pointermove',event => {
          if (event.pointerType === 'touch' && !event.buttons) return;
          const rect = zone.getBoundingClientRect();
          manualMove(100*(event.clientX-rect.left)/rect.width,100*(event.clientY-rect.top)/rect.height);
        });
        zone.addEventListener('pointerdown',event => {
          const rect = zone.getBoundingClientRect();
          manualMove(100*(event.clientX-rect.left)/rect.width,100*(event.clientY-rect.top)/rect.height);
        });
        zone.addEventListener('keydown',event => {
          const offsets={ArrowLeft:[-8,0],ArrowRight:[8,0],ArrowUp:[0,-8],ArrowDown:[0,8]};
          if(!offsets[event.key]) return;
          event.preventDefault();
          manualMove(state.x+offsets[event.key][0],state.y+offsets[event.key][1]);
        });
      });
    }
    const action = root.querySelector('.mv-action');
    if (action) action.addEventListener('click', () => {
      stop(); state.p=0; render(); start(true);
    });
    render();
  }

  function init() { document.querySelectorAll('.motion-v2').forEach(install); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();


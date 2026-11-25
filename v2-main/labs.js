(() => {
 const clamp = n => Math.max(0,Math.min(n,1));
 const setText = (el,n) => {if(el)el.textContent=n};
 function chart(canvas,t,highlight){
   const w=canvas.width,h=canvas.height,ctx=canvas.getContext('2d');
   ctx.clearRect(0,0,w,h);
   const x=p=>13+(w-26)*p,y=p=>h-15-(h-30)*(0.12+0.76*(p*p*(3-2*p)));
   ctx.strokeStyle='#45677e';ctx.beginPath();ctx.moveTo(12,6);ctx.lineTo(12,h-15);ctx.lineTo(w-8,h-15);ctx.stroke();
   ctx.strokeStyle='#79cbef';ctx.lineWidth=3;ctx.beginPath();
   for(let i=0;i<=100;i++){const p=i/100;if(i===0)ctx.moveTo(x(p),y(p));else ctx.lineTo(x(p),y(p))}
   ctx.stroke();
   if(highlight){const px=x(t),py=y(t);ctx.strokeStyle='#ffd07c';ctx.lineWidth=1.3;ctx.setLineDash([3,3]);ctx.beginPath();ctx.moveTo(px,h-15);ctx.lineTo(px,py);ctx.lineTo(12,py);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle='#ffd07c';ctx.beginPath();ctx.arc(px,py,5,0,Math.PI*2);ctx.fill()}
   ctx.fillStyle='#b8cbd8';ctx.font='11px sans-serif';ctx.fillText('时间',w-28,h-3);
 }
 function camera(canvas,t,truck){
   const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height,f=w*.68;
   const travel=-.85+1.7*t,cx=truck?travel:0,yaw=truck?0:Math.atan(travel/5);
   const c=Math.cos(yaw),s=Math.sin(yaw);
   function project(x,y,z){const dx=x-cx;const u=c*dx-s*z,v=s*dx+c*z;return [w/2+f*u/v,h*.51-f*(y-1.25)/v]}
   function polygon(points,color,edge){
     ctx.fillStyle=color;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill();if(edge){ctx.strokeStyle=edge;ctx.stroke()}
   }
   function plate(x,z,width,height,color,edge){
     polygon([project(x-width/2,0,z),project(x+width/2,0,z),project(x+width/2,height,z),project(x-width/2,height,z)],color,edge)
   }
   ctx.clearRect(0,0,w,h);ctx.fillStyle='#1b354b';ctx.fillRect(0,0,w,h*.51);ctx.fillStyle='#283748';ctx.fillRect(0,h*.51,w,h*.49);
   plate(-3.5,13,15,5.5,'#1c4258','#486578');
   // Floor and wall lines projected with the same pinhole camera.
   ctx.strokeStyle='#3c5366';ctx.lineWidth=.85;
   for(let x=-5;x<=5;x+=1){const a=project(x,0,2),b=project(x,0,13);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke()}
   for(let z=2;z<=12;z+=1){const a=project(-7,0,z),b=project(7,0,z);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke()}
   plate(1.15,9,1.75,3.2,'#355d77','#76b0c0');plate(1.15,8.99,1.4,2.93,'#1d3145');
   plate(0,5,.75,1.65,'#f0bc75','#ffe5ad');
   const [sx,sy]=project(0,1.65,5);ctx.fillStyle='#ffe4aa';ctx.beginPath();ctx.ellipse(sx,sy,11,8,0,0,Math.PI*2);ctx.fill();
   plate(-.95,3.1,.42,3.5,'#56afa8','#8bd9ce');
   ctx.fillStyle='#f4f7fd';ctx.font='10px sans-serif';ctx.fillText(truck?'机位平移':'机位固定，转动方向',7,13);
 }
 function draw(root,t){
   const panes=[...root.querySelectorAll('.live-pane')],kind=root.dataset.lab;
   function num(p,i,n){setText(panes[i].querySelector('.live-num'),n)}
   function bar(p,i,v,cls){const mark=panes[i].querySelector(cls);mark.style[cls==='.live-bar'?'width':'left']=v+'%'}
   if(kind==='scroll'){
     const pos=t<.35? t/.35*60:t<.72?60:60-(t-.72)/.28*35;
     const trig=clamp((t-(.35*50/60))/.29)*100;
     bar(pos,0,pos,'.live-bar');bar(trig,1,trig,'.live-bar');
     num(panes,0,'模拟滚动位置 '+Math.round(pos)+'%');num(panes,1,'已播放 '+Math.round(trig)+'%');
   } else if(kind==='easing'){
     const a=t*100,b=(1-Math.pow(1-t,3))*100;
     bar(a,0,a,'.live-ball');bar(b,1,b,'.live-ball');
     num(panes,0,'位移 '+Math.round(a)+'%');num(panes,1,'位移 '+Math.round(b)+'%');
   } else if(kind==='focus'){
     panes[0].querySelector('.near').style.filter='blur('+(5*t)+'px)';
     panes[0].querySelector('.distant').style.filter='blur('+(5*(1-t))+'px)';
     panes[1].querySelector('.scene').style.filter='blur('+(5*(1-t))+'px)';
     num(panes,0,t<.5?'前景较清晰':'后景较清晰');num(panes,1,'整画面一起改变清晰度');
   } else if(kind==='signaling'){
     chart(panes[0].querySelector('canvas'),t,false);chart(panes[1].querySelector('canvas'),t,true);
     const value=Math.round(100*(t*t*(3-2*t)));
     num(panes,0,'播报 t = '+(10*t).toFixed(1)+' 秒，值 '+value);
     num(panes,1,'当前时刻 '+(10*t).toFixed(1)+' 秒 / 位移 '+value);
   } else if(kind==='truck-pan'){
     panes.forEach((p,i)=>camera(p.querySelector('canvas'),t,i===0));
     num(panes,0,'机位横向移动，近远层发生相对位移');num(panes,1,'机位固定，视线横向转动');
   } else if(kind==='hotspot'){
     panes.forEach(p=>p.querySelector('.hotspot-model').style.setProperty('--angle',(-35+70*t)+'deg'));
     num(panes,0,'锚点随前表面转动');num(panes,1,'屏幕标记停在画面中间');
   }
 }
 function mount(){
   document.querySelectorAll('.study-live[data-lab]').forEach(root=>{
     let frame=0,active=false,t=Number(root.dataset.start||.35),last=0;
     const input=root.querySelector('input[type=range]'),output=root.querySelector('output'),play=root.querySelector('[data-live=play]'),pause=root.querySelector('[data-live=pause]');
     const reduce=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
     function apply(){input.value=String(Math.round(t*1000));output.value=Math.round(t*100)+'%';draw(root,t)}
     function stop(){active=false;cancelAnimationFrame(frame);play.disabled=false;pause.disabled=true;last=0}
     function tick(now){if(!active)return;if(root.closest('article').hidden||document.hidden){stop();return}if(!last)last=now; t=clamp(t+(now-last)/Number(root.dataset.duration||2400));last=now;apply();if(t===1){stop();return}frame=requestAnimationFrame(tick)}
     play.addEventListener('click',()=>{if(t>=1)t=0;if(reduce()){t=1;apply();return;}if(active)return;active=true;play.disabled=true;pause.disabled=false;frame=requestAnimationFrame(tick)});
     pause.addEventListener('click',stop);
     root.querySelector('[data-live=reset]').addEventListener('click',()=>{stop();t=0;apply()});
     input.addEventListener('input',()=>{stop();t=Number(input.value)/1000;apply()});
     root.addEventListener('atlas-pause',stop);apply();stop();
   });
   for(const input of document.querySelectorAll('[data-style-param]')){
      const host=input.closest('.study-static-ui'),update=()=>{
        if(input.dataset.styleParam==='blur'){host.style.setProperty('--glass-blur',input.value+'px');setText(host.querySelector('output'),input.value+' px')}
        if(input.dataset.styleParam==='leading'){host.style.setProperty('--lead',(input.value/100).toFixed(2));setText(host.querySelector('output'),(input.value/100).toFixed(2)+' 倍')}
        if(input.dataset.styleParam==='tracking'){host.style.setProperty('--letter',input.value/100+'em');setText(host.querySelector('[data-tracking-value]'),(input.value/100).toFixed(2)+' em')}
      };input.addEventListener('input',update);update();
   }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();

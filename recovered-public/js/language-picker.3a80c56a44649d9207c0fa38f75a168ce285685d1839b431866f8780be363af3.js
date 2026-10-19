(()=>{'use strict';
const picker=document.getElementById('language-picker');if(!picker)return;
const summary=picker.querySelector('summary'),panel=picker.querySelector('.lp-panel'),list=picker.querySelector('.lp-list');
function position(){if(!picker.open)return;const viewport=window.visualViewport,rect=summary.getBoundingClientRect(),top=Math.max(8,rect.bottom+8);picker.style.setProperty('--lp-top',top+'px');picker.style.setProperty('--lp-room',Math.max(80,Math.min(514,(viewport?viewport.height:innerHeight)-top-12))+'px');const left=Math.max(12,Math.min(rect.right-panel.offsetWidth,innerWidth-panel.offsetWidth-12));panel.style.left=(innerWidth>639?left-picker.getBoundingClientRect().left:left)+'px';panel.style.right='auto'}
function close(restore){picker.open=false;if(restore)summary.focus()}
picker.addEventListener('toggle',()=>{if(picker.open){const menu=document.getElementById('nav-toggle');if(menu)menu.checked=false;list.scrollTop=0;position()}});
picker.addEventListener('keydown',event=>{if(event.key==='Escape'&&picker.open){event.preventDefault();event.stopPropagation();close(true)}});
document.addEventListener('pointerdown',event=>{if(picker.open&&!picker.contains(event.target))close(false)});
picker.addEventListener('focusout',()=>{setTimeout(()=>{if(picker.open&&!picker.contains(document.activeElement))close(false)},0)});
window.addEventListener('resize',position,{passive:true});if(window.visualViewport)window.visualViewport.addEventListener('resize',position,{passive:true});
})();

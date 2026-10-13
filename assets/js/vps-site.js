(function(){
  var plan=document.getElementById('vps-plan');
  var days=document.getElementById('vps-days');
  var extras=document.getElementById('vps-extras');
  var server=document.getElementById('vps-server-cost');
  var extraTotal=document.getElementById('vps-extra-cost');
  var total=document.getElementById('vps-total-cost');
  if(!plan||!days||!extras||!server||!extraTotal||!total)return;
  function money(n){return '$'+n.toFixed(2)}
  function update(){
    var rate=parseFloat(plan.value)||0;
    var raw=parseInt(days.value,10);
    var d=Number.isFinite(raw)?Math.max(1,Math.min(366,raw)):30;
    var monthly=Math.max(0,parseFloat(extras.value)||0);
    var s=rate*d;
    var x=monthly*d/30;
    server.textContent=money(s);
    extraTotal.textContent=money(x);
    total.textContent=money(s+x);
  }
  [plan,days,extras].forEach(function(el){
    el.addEventListener('input',update);
    el.addEventListener('change',update);
  });
  update();
})();

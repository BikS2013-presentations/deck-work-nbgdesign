(function(){
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var N = slides.length, cur = 1;
  function fit(){
    var vv = window.visualViewport;
    var w = vv ? vv.width : window.innerWidth, h = vv ? vv.height : window.innerHeight;
    var s = Math.min(w/1920, h/1080);
    var st = document.getElementById('stage');
    st.style.transform = 'translate(' + ((w-1920*s)/2) + 'px,' + ((h-1080*s)/2) + 'px) scale(' + s + ')';
  }
  function show(n){
    n = Math.max(1, Math.min(N, n|0)); cur = n;
    slides.forEach(function(s,i){ s.classList.toggle('active', i === n-1); });
    document.getElementById('ctr').textContent = n + ' / ' + N;
    if (location.hash !== '#' + n) history.replaceState(null, '', '#' + n);
  }
  window.showSlide = show;
  window.gotoSlide = show;
  document.getElementById('prev').addEventListener('click', function(){ show(cur-1); });
  document.getElementById('next').addEventListener('click', function(){ show(cur+1); });
  document.addEventListener('keydown', function(e){
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { show(cur+1); e.preventDefault(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { show(cur-1); e.preventDefault(); }
    else if (e.key === 'Home') show(1); else if (e.key === 'End') show(N);
  });
  window.addEventListener('hashchange', function(){ show(parseInt(location.hash.slice(1),10) || 1); });
  window.addEventListener('resize', fit);
  if (window.visualViewport) window.visualViewport.addEventListener('resize', fit);
  fit(); show(parseInt(location.hash.slice(1),10) || 1);
})();

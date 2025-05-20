  document.addEventListener("DOMContentLoaded", () => {

    const API = "";
  
    const THEMES = ["sport", "fritid", "historia"];

    const $ = id => document.getElementById(id);
    const els = {
      catScreen : $("category-screen"),
      gameScreen: $("game-screen"),
      timeline  : $("timeline"),
      current   : $("current-card"),
      score     : $("score"),
  
      menuBtn   : $("menu-btn"),
      restartBtn: $("restart-btn"),
  
      badge     : $("category-badge"),
      helpBtn   : $("help-btn"),
      helpModal : $("help-modal"),
      closeHelp : $("close-help"),
  
      endModal  : $("end-modal"),
      endScore  : $("end-score"),
      endAgain  : $("end-restart"),
      endMenu   : $("end-menu")
    };
  
    let category = null, deck = [], placed = [], points = 0, dragged = null;
    const CARDS_PER_ROUND = 10;
  
    document.querySelectorAll(".category-btn").forEach(btn =>
      btn.addEventListener("click", () => {
        category = btn.dataset.category;
        setTheme(category); showBadge(category);
        els.helpBtn.classList.remove("hidden");
        els.helpModal.classList.remove("hidden");
      })
    );
  
    els.closeHelp .onclick = () => { els.helpModal.classList.add("hidden"); startGame(); };
    els.helpBtn   .onclick = () =>  els.helpModal.classList.remove("hidden");
    els.endAgain  .onclick = () => { els.endModal.classList.add("hidden"); startGame(); };
    els.endMenu   .onclick = () => { els.endModal.classList.add("hidden"); backToMenu(); };
  
    els.restartBtn.onclick = startGame;
    els.menuBtn   .onclick = backToMenu;
  
    els.current.ondragstart = e=>{
      dragged = { title: els.current.textContent, year:+els.current.dataset.year };
      e.dataTransfer.effectAllowed="move";
    };
    els.current.ondragend = () => dragged = null;
    els.timeline.addEventListener("dragover", e => e.preventDefault());
  
    async function startGame(){
      if(!category) return;
      try{
        deck = await fetchDeck(category, CARDS_PER_ROUND);
      }catch(err){
        alert("Kunde inte hämta frågor från servern.\n" + err);
        backToMenu(); return;
      }
  
      points=0; els.score.textContent = points;
      placed=[]; els.timeline.innerHTML=""; addDrop(0);
  
      els.catScreen.classList.add("hidden");
      els.gameScreen.classList.remove("hidden");
      els.endModal.classList.add("hidden");
  
      drawNext();
    }
  
    async function fetchDeck(cat,n){
      const r = await fetch(`/questions?cat=${cat}&n=${n}`);
      if(!r.ok) throw `Servern svarade ${r.status}`;
      return r.json();
    }
  
    function drawNext(){
      if(!deck.length) return showEnd();
      const c = deck.pop();
      Object.assign(els.current,{textContent:c.title,draggable:true});
      els.current.dataset.year = c.year;
      els.current.className = "card";
    }
  
    function addDrop(i){
      const dz=document.createElement("div");
      dz.className="dropzone"; dz.dataset.index=i;
      dz.ondragover=e=>{e.preventDefault();dz.classList.add("highlight");};
      dz.ondragleave=()=>dz.classList.remove("highlight");
      dz.ondrop=handleDrop;
      els.timeline.insertBefore(dz, els.timeline.querySelectorAll(".card")[i]||null);
    }
    function handleDrop(e){
      e.preventDefault(); this.classList.remove("highlight"); if(!dragged) return;
      const i=+this.dataset.index, yr=dragged.year;
      if((!placed[i-1]||placed[i-1].year<=yr)&&(!placed[i]||yr<=placed[i].year)){
        points++; els.score.textContent=points;
        const card=document.createElement("div");
        card.className="card correct"; card.textContent=`${dragged.title} (${yr})`;
        els.timeline.insertBefore(card,this);
        placed.splice(i,0,{title:dragged.title,year:yr});
        refreshDrops(); drawNext();
      }else flashWrong();
    }
    function refreshDrops(){
      els.timeline.querySelectorAll(".dropzone").forEach(z=>z.remove());
      for(let i=0;i<=placed.length;i++) addDrop(i);
    }
  
    function showEnd(){
      els.current.textContent="Spelet slut!"; els.current.draggable=false;
      els.endScore.textContent = points;
      els.endModal.classList.remove("hidden");
    }
    const flashWrong=()=>{els.current.classList.add("incorrect");setTimeout(()=>els.current.classList.remove("incorrect"),800);};
    const setTheme=c=>{document.body.classList.remove(...THEMES.map(t=>`theme-${t}`));if(THEMES.includes(c))document.body.classList.add(`theme-${c}`);};
    const showBadge=c=>{els.badge.textContent=c[0].toUpperCase()+c.slice(1);els.badge.classList.remove("hidden");};
  
    function backToMenu(){
      els.gameScreen.classList.add("hidden");
      els.catScreen.classList.remove("hidden");
      els.timeline.innerHTML="";
      els.current.textContent=""; els.current.draggable=false;
      els.badge.classList.add("hidden"); els.helpBtn.classList.add("hidden");
      document.body.classList.remove(...THEMES.map(t=>`theme-${t}`));
      deck=placed=[]; points=0; els.score.textContent=points;
    }
  
  });
  
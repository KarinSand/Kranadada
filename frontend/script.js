document.addEventListener("DOMContentLoaded", () => {
  const API = "";
  const THEMES = ["sport", "fritid", "historia"];
  const CARDS_PER_ROUND = 10;

  const $ = (id) => document.getElementById(id);

  const els = {
    catScreen: $("category-screen"),
    gameScreen: $("game-screen"),
    timeline: $("timeline"),
    current: $("current-card"),
    score: $("score"),

    menuBtn: $("menu-btn"),
    restartBtn: $("restart-btn"),

    badge: $("category-badge"),
    helpBtn: $("help-btn"),
    helpModal: $("help-modal"),
    closeHelp: $("close-help"),

    endModal: $("end-modal"),
    endScore: $("end-score"),
    endAgain: $("end-restart"),
    endMenu: $("end-menu"),

    /* 3-livs-UI */
    lifeBtn  : $("life-btn"),
    lifeBoard: $("life-board"),
    livesEl  : $("lives"),
  };

  let category = null;
  let deck = [];
  let placed = [];
  let points = 0;
  let draggedCard = null;
  let gambleMode = false;
  let gambleCards = [];

  /* 3-livs-läge */
  let lifeMode = false;
  let lives     = 3;

  // Event listeners för kategori-knappar
  document.querySelectorAll(".category-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      category = btn.dataset.category;
      setTheme(category);
      showBadge(category);
      els.helpBtn.classList.remove("hidden");
      els.helpModal.classList.remove("hidden");
    });
  });

  els.closeHelp.onclick = () => {
    els.helpModal.classList.add("hidden");
    startGame();
  };

  els.helpBtn.onclick = () => {
    els.helpModal.classList.remove("hidden");
  };

  els.endAgain.onclick = () => {
    els.endModal.classList.add("hidden");
    startGame();
  };

  els.endMenu.onclick = () => {
    els.endModal.classList.add("hidden");
    backToMenu();
  };

  els.restartBtn.onclick = startGame;
  els.menuBtn.onclick = backToMenu;
  if (els.lifeBtn) els.lifeBtn.addEventListener("click", toggleLifeMode);   // 3-livs-knapp

  // Drag & Drop event listeners för nuvarande kort
  els.current.ondragstart = (e) => {
    draggedCard = {
      title: els.current.textContent,
      year: +els.current.dataset.year,
    };
    e.dataTransfer.effectAllowed = "move";
  };

  els.current.ondragend = () => {
    draggedCard = null;
  };

  // Tillåt dragover på tidslinjen
  els.timeline.addEventListener("dragover", (e) => e.preventDefault());

  // Starta spel
  async function startGame() {
    if (!category) return;

    try {
      deck = await fetchDeck(category, CARDS_PER_ROUND);
    } catch (err) {
      alert("Kunde inte hämta frågor från servern.\n" + err);
      backToMenu();
      return;
    }

    points = 0;
    els.score.textContent = points;
    placed = [];
    els.timeline.innerHTML = "";
    addDrop(0);

    els.catScreen.classList.add("hidden");
    els.gameScreen.classList.remove("hidden");
    els.endModal.classList.add("hidden");

    /* 3-livs-reset för ny runda */
    if (lifeMode) {
      lives = 3;
      updateLivesUI();
      els.lifeBoard.classList.remove("hidden");
    }
    if (els.lifeBtn) els.lifeBtn.disabled = false;   // på/av får göras innan första spelardraget

      drawNext();
    // Lägg första kortet automatiskt
    const firstCard = deck.pop();
    placed.push(firstCard);
    const newCard = document.createElement("div");
    newCard.className = "card correct";
    newCard.textContent = `${firstCard.title} (${firstCard.year})`;
    timeline.appendChild(newCard);

    refreshDropzones();
    drawNextCard();

    categoryScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
  }

  // Hämta kort från server
  async function fetchDeck(cat, n) {
    const res = await fetch(`/questions?cat=${cat}&n=${n}`);
    if (!res.ok) throw `Servern svarade ${res.status}`;
    return res.json();
  }

  // Visa nästa kort från leken
  function drawNext() {
    if (!deck.length) {
      return showEnd();
    }

    const card = deck.pop();

    Object.assign(els.current, {
      textContent: card.title,
      draggable: true,
    });

    els.current.dataset.year = card.year;
    els.current.className = "card category-colored";
  }

  // Skapa dropzone i tidslinjen
  function addDrop(index) {
    const dropZone = document.createElement("div");
    dropZone.className = "dropzone";
    dropZone.dataset.index = index;

    dropZone.ondragover = (e) => {
      e.preventDefault();
      dropZone.classList.add("highlight");
    };

    dropZone.ondragleave = () => {
      dropZone.classList.remove("highlight");
    };

    dropZone.ondrop = handleDrop;

    const cards = els.timeline.querySelectorAll(".card");
    els.timeline.insertBefore(dropZone, cards[index] || null);
  }

  /* Hantera släpp */
  function handleDrop(e) {
    e.preventDefault();
    this.classList.remove("highlight");
    if (!draggedCard) return;

    const dropzone = this;
    const idx = parseInt(dropzone.dataset.index, 10);
    const yr = draggedCard.year;

    const ok =
      (!placed[idx - 1] || placed[idx - 1].year <= yr) &&
      (!placed[idx] || yr <= placed[idx].year);

    // GAMBLE-LÄGE
    if (gambleMode) {
      // Lägg till kortet på tidslinjen
      const newCard = document.createElement("div");
      newCard.className = "card gamble-pending";
      newCard.textContent = draggedCard.title;

      els.timeline.insertBefore(newCard, dropzone);

      // Spara temporärt
      gambleCards.push({
        cardEl: newCard,
        idx,
        title: draggedCard.title,
        year: draggedCard.year,
        cardData: draggedCard, // detta behövs för att lägga tillbaka det i leken
      });

      refreshDropzones();
      drawNext();
      return;
    }

    // === VANLIGT LÄGE ===
    if (ok) {
      points++;
      els.score.textContent = points;

      const newCard = document.createElement("div");
      newCard.className = "card correct";
      newCard.textContent = `${draggedCard.title} (${yr})`;

      els.timeline.insertBefore(newCard, dropzone);
      placed.splice(idx, 0, { title: draggedCard.title, year: yr });

      /* första spelardraget ⇒ spärrar knappen */
      if (placed.length > 1 && els.lifeBtn && !els.lifeBtn.disabled) {
        els.lifeBtn.disabled = true;
      }

      refreshDropzones();
      drawNext();
    } else {
      points = Math.max(0, points - 1);
      els.score.textContent = points;
      els.current.classList.add("incorrect");
      setTimeout(() => els.current.classList.remove("incorrect"), 900);
      loseLife();                   // 3-livs-avdrag vid fel
    }
  }

  // Kontrollera gamble-korten
  function checkGambleCards() {
    let allCorrect = true;

    for (let gc of gambleCards) {
      const idx = gc.idx;
      const yr = gc.year;

      const correct =
        (!placed[idx - 1] || placed[idx - 1].year <= yr) &&
        (!placed[idx] || yr <= placed[idx].year);

      if (!correct) {
        allCorrect = false;
        break;
      }
    }

    if (allCorrect) {
      // Alla rätt – bonuspoäng
      const bonus = gambleCards.length * 2; // t.ex. 2 poäng per kort
      points += bonus;
      els.score.textContent = points;

      // Spara permanent
      for (let gc of gambleCards) {
        gc.cardEl.classList.remove("gamble-pending");
        gc.cardEl.classList.add("correct");
        gc.cardEl.textContent = `${gc.title} (${gc.year})`;
        placed.splice(gc.idx, 0, { title: gc.title, year: gc.year });
      }
    } else {
      // Något fel – alla kort tillbaka till kortleken
      points = Math.max(0, points - gambleCards.length * 2); // t.ex. -2 per kort
      els.score.textContent = points;

      for (let gc of gambleCards) {
        gc.cardEl.remove(); // ta bort från tidslinjen
        deck.push({ title: gc.title, year: gc.year }); // lägg tillbaka i leken
      }
      loseLife();                   // 3-livs-avdrag vid misslyckad gamble
    }

    gambleCards = [];
    gambleMode = false;
    refreshDropzones();
    drawNext();
    updateGambleButtons();
  }

  const gambleBtn = $("gamble-btn");
  const checkGambleBtn = $("check-gamble-btn");

  function updateGambleButtons() {
    if (gambleMode) {
      gambleBtn.classList.add("hidden");
      checkGambleBtn.classList.remove("hidden");
    } else {
      gambleBtn.classList.remove("hidden");
      checkGambleBtn.classList.add("hidden");
    }
  }

  gambleBtn.addEventListener("click", () => {
    gambleMode = true;
    gambleCards = [];
    updateGambleButtons();
  });

  checkGambleBtn.addEventListener("click", () => {
    checkGambleCards();
  });

  /* Uppdatera drop-zoner */
  function refreshDropzones() {
    els.timeline.querySelectorAll(".dropzone").forEach((z) => z.remove());

    // Antal kort som är "placerade" + antalet gamble-kort
    const totalCards = placed.length + gambleCards.length;

    for (let i = 0; i <= totalCards; i++) {
      addDrop(i);
    }
  }

  // Visa slutet av spelet
  function showEnd() {
    els.current.textContent = "Spelet slut!";
    els.current.draggable = false;

    els.endScore.textContent = points;
    els.endModal.classList.remove("hidden");
    if (els.lifeBtn) els.lifeBtn.disabled = false;   // lås upp knappen för nästa runda
  }

  // Sätt färgtema
  function setTheme(cat) {
    document.body.classList.remove(...THEMES.map((t) => `theme-${t}`));
    if (THEMES.includes(cat)) {
      document.body.classList.add(`theme-${cat}`);
    }
  }

  // Visa kategori-badge
  function showBadge(cat) {
    els.badge.textContent = cat[0].toUpperCase() + cat.slice(1);
    els.badge.classList.remove("hidden");
  }

  // Gå tillbaka till meny
  function backToMenu() {
    els.gameScreen.classList.add("hidden");
    els.catScreen.classList.remove("hidden");

    els.timeline.innerHTML = "";
    els.current.textContent = "";
    els.current.draggable = false;

    els.badge.classList.add("hidden");
    els.helpBtn.classList.add("hidden");

    document.body.classList.remove(...THEMES.map((t) => `theme-${t}`));

    deck = [];
    placed = [];
    points = 0;
    els.score.textContent = points;
    if (els.lifeBtn) els.lifeBtn.disabled = false;
    if (els.lifeBoard) els.lifeBoard.classList.add("hidden");
  }

  // Dummy funktion för kategori baserat på titel, måste definieras
  function getCardCategory(title) {
    return category || "blandat";
  }

  /* ===== 3-LIVS-HJÄLPPUNKTER ===== */
  function updateLivesUI() {
    els.livesEl.textContent = "❤️".repeat(lives);
  }

  function loseLife() {
    if (!lifeMode) return;
    lives--;
    updateLivesUI();
    if (lives <= 0) showEnd();
  }

  function toggleLifeMode() {
    if (els.lifeBtn.disabled) return;          // spärrad efter första draget
    lifeMode = !lifeMode;
    if (lifeMode) {
      lives = 3;
      updateLivesUI();
      els.lifeBoard.classList.remove("hidden");
      els.lifeBtn.textContent = "3-livsläge: På";
      els.lifeBtn.classList.add("primary");
    } else {
      els.lifeBoard.classList.add("hidden");
      els.lifeBtn.textContent = "Aktivera 3-livsläge";
      els.lifeBtn.classList.remove("primary");
    }
  }
});

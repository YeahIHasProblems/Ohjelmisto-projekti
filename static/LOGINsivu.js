/**
 * 1. DATAKONFIGURAATIO
 */
const menuData = [
    {
        title: 'Tyhjiö',
        logo: '✖',
        tag: 'SULJE',
        msg: 'SIG_KILL // 000',
        desc: 'Poistu simulaatiosta. Kaikki tallentamaton hermoverkkodata pyyhitään muistista.',
        btn: 'Sammuta',
        color: '#ff4d4d'
    },
    {
        title: 'Ässä',
        logo: '♠',
        tag: 'IDENTITEETTI',
        msg: 'TUNNISTUS // 001',
        desc: 'Palaa pöytään. Vahvista tunnuksesi päästäksesi käsiksi korkean panoksen profiiliisi.',
        btn: 'Pelaa',
        color: '#9400d3'
    },
    {
        title: 'Aave',
        logo: '✦',
        tag: 'REKISTERÖIDY',
        msg: 'UUSI_LINJA // 002',
        desc: 'Ei historiaa? Ei hätää. Luo uusi identiteetti ja lunasta paikkasi eliitin joukosta.',
        btn: 'Luo Aave',
        color: '#00f2ff'
    }
];

let currentIndex = 1;
let cards = [];

/**
 * 2. ALUSTUS
 */
function init() {
    const deck = document.getElementById('deck');
    if (!deck) return;

    menuData.forEach((item) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.setProperty('--accent-color', item.color);

        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <div class="status-tag">${item.tag}</div>
                    <div class="card-logo">${item.logo}</div>
                    <h2 style="margin-top: 180px">${item.title}</h2>
                    <div class="tagline">${item.msg}</div>
                    <button class="btn" onclick="flipCard(this)" style="background:${item.color}">${item.btn}</button>
                </div>
                
                <div class="card-back">
                    <div class="status-tag">LUKITTU</div>
                    <h2>${item.title}</h2>
                    <div class="tagline">${item.msg}</div>
                    <div class="desc-text">${item.desc}</div>
                    
                    <div style="flex-grow: 1;">
                        ${item.title !== 'Tyhjiö' ? `
                            <input type="text" placeholder="KÄYTTÄJÄTUNNUS" class="js-user">
                            <input type="password" placeholder="SALASANA" class="js-pass">
                        ` : '<p style="margin-top:20px; color:#666;">Haluatko varmasti hylätä istunnon?</p>'}
                    </div>
                    
                    <button class="btn js-confirm-btn" onclick="loginReady(this)" style="background:${item.color}">Vahvista</button>
                </div>
            </div>
        `;

        deck.appendChild(card);
        cards.push(card);
    });

    updatePositions();
}

/**
 * 3. KORTIN KÄÄNTÖ
 */
function flipCard(btnElement) {
    const card = btnElement.closest('.card');
    card.classList.add('flipped');

    setTimeout(() => {
        const input = card.querySelector('input');
        if (input) input.focus();
    }, 400);
}



/**
 * 4. KIRJAUTUMINEN, REKISTERÖINTI JA KILL
 */
async function loginReady(btn) {
    const card = btn.closest('.card');
    const titleText = card.querySelector('h2').innerText.toLowerCase();

    // --- 1. SAMMUTUS (TYHJIÖ) ---
    if (titleText.includes('tyhjiö')) {
        card.style.transition = "all 0.5s";
        card.style.boxShadow = "0 0 100px #ff4d4d";
        document.body.style.transition = "opacity 1s";
        document.body.style.opacity = "0";

        setTimeout(() => {
            window.location.href = "about:blank";
        }, 1000);
        return;
    }

    // Haetaan kentät
    const userField = card.querySelector('.js-user');
    const passField = card.querySelector('.js-pass');
    if (!userField || !passField) return;

    const user = userField.value;
    const pass = passField.value;

    if (!user || !pass) {
        alert("Täytä molemmat kentät.");
        return;
    }


    const endpoint = titleText.includes('aave') ? '/register' : '/login';

    // Visuaalinen palaute
    card.style.boxShadow = "0 0 100px " + (endpoint === '/register' ? "#00f2ff" : "white");
    const originalBtnText = btn.innerText;
    btn.innerText = "YHDISTETÄÄN...";

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: user, password: pass}),
        });

        const result = await response.json();

        if (result.success) {
            if (endpoint === '/register') {
                alert("Identiteetti luotu! Voit nyt kirjautua Ässä-kortilla.");
                card.classList.remove('flipped');
                btn.innerText = originalBtnText;
                card.style.boxShadow = "";
                userField.value = "";
                passField.value = "";
            } else {
                // Kirjautuminen onnistui
                document.body.style.transition = "opacity 0.8s ease-out";
                document.body.style.opacity = "0";
                setTimeout(() => {
                    window.location.href = "/index";
                }, 800);
            }
        } else {
            // Virhe palvelimelta
            card.style.boxShadow = "";
            btn.innerText = "VAHVISTA";
            alert(result.message);
        }
    } catch (error) {
        card.style.boxShadow = "";
        btn.innerText = "VAHVISTA";
        alert("Yhteysvirhe palvelimeen.");
    }
}



/**
 * 5. 3D-MOOTTORI
 */
function updatePositions() {
    cards.forEach((card, index) => {
        const relIndex = index - currentIndex;
        const xPos = relIndex * 380;
        let zPos = Math.abs(relIndex) * -400;
        const rotateY = relIndex * -25;
        const opacity = 1 - Math.abs(relIndex) * 0.4;

        if (index === currentIndex) {
            zPos = 200;
            card.classList.add('active');
        } else {
            card.classList.remove('active', 'flipped');
        }

        card.style.transform = `translateX(${xPos}px) translateZ(${zPos}px) rotateY(${rotateY}deg)`;
        card.style.opacity = opacity;
    });
}

/**
 * 6. NÄPPÄIMISTÖ
 */
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') {
        if (e.key === 'Escape') {
            e.target.blur();
            cards[currentIndex].classList.remove('flipped');
        }
        if (e.key === 'Enter') {
            const confirmBtn = cards[currentIndex].querySelector('.js-confirm-btn');
            if (confirmBtn) confirmBtn.click();
        }
        return;
    }

    const key = e.key.toLowerCase();
    if (key === 'a' || key === 'arrowleft') {
        if (currentIndex > 0) { currentIndex--; updatePositions(); }
    } else if (key === 'd' || key === 'arrowright') {
        if (currentIndex < cards.length - 1) { currentIndex++; updatePositions(); }
    } else if (key === 'enter') {
        const currentCard = cards[currentIndex];
        if (!currentCard.classList.contains('flipped')) {
            const btn = currentCard.querySelector('.card-front .btn');
            if (btn) btn.click();
        }
    }
});

init();
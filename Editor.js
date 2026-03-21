const shirtList = [
    {
        name: 'blusa1',
        category: 'shirt',
        image: 'media/blusas/blusa1.png',
        alt: 'Blusa 1'
    },
    {
        name: 'blusa2',
        category: 'shirt',
        image: 'media/blusas/blusa2.png',
        alt: 'Blusa 2'
    },
    {
        name: 'blusa3',
        category: 'shirt',
        image: 'media/blusas/blusa3.png',
        alt: 'Blusa 3'
    }
];

const pantsList = [
    {
        name: 'calca1',
        category: 'pants',
        image: 'media/calcas/calca1.png',
        alt: 'Calça 1'
    },
    {
        name: 'calca2',
        category: 'pants',
        image: 'media/calcas/calca2.png',
        alt: 'Calça 2'
    },
    {
        name: 'calca3',
        category: 'pants',
        image: 'media/calcas/calca3.png',
        alt: 'Calça 3'
    }
];

const shoesList = [
    {
        name: 'sapato1',
        category: 'shoes',
        image: 'media/Logo.png',
        alt: 'Sapato 1'
    }
];

let shirtLvl = 0;
let pantsLvl = 0;
let shoesLvl = 0;

const tags = [];

let buttonClicked = null;

let animationHappening = false;
let noNameError = false;


const lookPreview = document.getElementById('lookPreview');

const shirtFoward = document.getElementById('shirtFoward');
const shirtBack = document.getElementById('shirtBack');
const shirtPreview = document.getElementById('shirtPreview');

const pantsFoward = document.getElementById('pantsFoward');
const pantsBack = document.getElementById('pantsBack');
const pantsPreview = document.getElementById('pantsPreview');

const shoesFoward = document.getElementById('shoesFoward');
const shoesBack = document.getElementById('shoesBack');
const shoesPreview = document.getElementById('shoesPreview');


const nameInput = document.getElementById('nameInput');
const noNameMsg = document.getElementById('noNameMsg');

const addTagBtn = document.getElementById('addTag');

const saveBtn = document.getElementById('save');

/* ---------------------- */

lookPreview.addEventListener('mousedown', (e) => e.preventDefault());

shirtFoward.addEventListener('mousedown', (e) => pressedArrow(e, 1, 'shirt'));
shirtBack.addEventListener('mousedown', (e) => pressedArrow(e, -1, 'shirt'));

pantsFoward.addEventListener('mousedown', (e) => pressedArrow(e, 1, 'pants'));
pantsBack.addEventListener('mousedown', (e) => pressedArrow(e, -1, 'pants'));

shoesFoward.addEventListener('mousedown', (e) => pressedArrow(e, 1, 'shoes'));
shoesBack.addEventListener('mousedown', (e) => pressedArrow(e, -1, 'shoes'));


nameInput.addEventListener('input', inputName);

addTagBtn.addEventListener('click', addTag);

saveBtn.addEventListener('click', saveLook);

/* --- Inicialização --- */

const shirtHeight = getComputedStyle(shirtPreview).height;
const pantsHeight = getComputedStyle(pantsPreview).height;
const shoesHeight = getComputedStyle(shoesPreview).height;

changeLevel('shirt', shirtList, shirtLvl, shirtPreview, shirtHeight , 0);
changeLevel('pants', pantsList, pantsLvl, pantsPreview, pantsHeight , 0);
changeLevel('shoes', shoesList, shoesLvl, shoesPreview, shoesHeight , 0);

nameInput.value = '';

/* --------------------- */


/* --- Parte do editor --- */

function pressedArrow(e, modifier, category) {
    buttonClicked = e.currentTarget;
    e.currentTarget.style.transform = 'scale(0.5)';

    if (!animationHappening) {
        switch (category) {
            case 'shirt': changeLevel(category, shirtList, shirtLvl, shirtPreview, shirtHeight, modifier); break;
            case 'pants': changeLevel(category, pantsList, pantsLvl, pantsPreview, pantsHeight, modifier); break;
            case 'shoes': changeLevel(category, shoesList, shoesLvl, shoesPreview, shoesHeight, modifier); break;
        }
    }

    document.addEventListener('mouseup', releaseArrow);
}

function releaseArrow() {
    buttonClicked.style.transform = 'scale(1)';
    buttonClicked = null;
    document.removeEventListener('mouseup', releaseArrow);
}

function changeLevel (category, list, lvl, preview, height, modifier) {
    if (list.length === 0) return;

    lvl += modifier;
    if (lvl < 0) lvl = list.length - 1;
    if (lvl >= list.length) lvl = 0;

    switch (category) {
        case 'shirt': shirtLvl = lvl; break;
        case 'pants': pantsLvl = lvl; break;
        case 'shoes': shoesLvl = lvl; break;
    }

    const currentImg = preview.querySelector('img');

    if (currentImg) {
        changeImage(currentImg, modifier, list, lvl, preview, height);
    }
    else {
        preview.innerHTML = '';
        addPiece(list, lvl, preview, height);
    }
}

function changeImage(image, modifier, list, lvl, preview, height) {
    switch (modifier) {
        case 1: image.classList.add('animateOutToLeft'); break;
        case -1: image.classList.add('animateOutToRight'); break;
    }
    animationHappening = true;

    image.addEventListener('animationend', (e) => {
        e.currentTarget.classList.remove('animateOutToLeft', 'animateOutToRight');
        e.currentTarget.remove();

        const newPiece = addPiece(list, lvl, preview, height);
        addInAnimation(newPiece, modifier);
        
        animationHappening = false;
    }, {once: true});
}

function addPiece(list, lvl, preview, height) {
    const newPiece = document.createElement('img');
    newPiece.src = list[lvl].image;
    newPiece.alt = list[lvl].alt;
    newPiece.style.height = height;
    preview.appendChild(newPiece);
    
    return newPiece;
}

function addInAnimation(image, modifier) {
    switch (modifier) {
        case 1: image.classList.add('animateInToLeft'); break;
        case -1: image.classList.add('animateInToRight'); break;
    }
    animationHappening = true;

    image.addEventListener('animationend', (e) => {
        e.currentTarget.classList.remove('animateInToLeft', 'animateInToRight');
        animationHappening = false;
    }, {once: true});
}

/* ----------------------- */


/* --- Parte das informações --- */

function inputName() {
    if (noNameError) {
        noNameMsg.textContent = '';
        noNameError = false;
    }
}

function addTag() {

}

function saveLook() {
    if (nameInput.value.trim() === '' && !noNameError) {
        noNameMsg.textContent = 'Adicione um nome para o seu look.';
        noNameError = true;
        return;
    }

    const newLook = {
        name: nameInput.value.trim(),
        shirt: shirtList[shirtLvl],
        pants: pantsList[pantsLvl],
        shoes: shoesList[shoesLvl],
        tags: tags
    }
}

/* ----------------------------- */
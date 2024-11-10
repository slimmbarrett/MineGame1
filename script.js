// script.js

let mineCount = 5;
let mines = [];
const grid = document.getElementById("grid");
const mineCountDisplay = document.getElementById("mineCount");

// Создание сетки
function createGrid() {
    grid.innerHTML = '';
    for (let i = 0; i < 25; i++) {
        const cell = document.createElement("div");
        cell.classList.add("cell");
        cell.addEventListener("click", () => revealCell(i, cell));
        grid.appendChild(cell);
    }
}

// Увеличение количества мин
function increaseMines() {
    if (mineCount < 24) {
        mineCount++;
        mineCountDisplay.textContent = mineCount;
    }
}

// Уменьшение количества мин
function decreaseMines() {
    if (mineCount > 1) {
        mineCount--;
        mineCountDisplay.textContent = mineCount;
    }
}

// Запуск игры
function startGame() {
    mines = generateMines();
    alert("Мины расставлены. Найдите безопасные ячейки!");
    createGrid();
}

// Генерация случайных мин
function generateMines() {
    const minePositions = new Set();
    while (minePositions.size < mineCount) {
        const randomIndex = Math.floor(Math.random() * 25);
        minePositions.add(randomIndex);
    }
    return Array.from(minePositions);
}

// Открытие ячейки
function revealCell(index, cell) {
    if (mines.includes(index)) {
        cell.textContent = "💣"; // Если это мина, показываем бомбу
        cell.classList.add("mine");
        cell.style.backgroundColor = "#ff5722"; // Цвет фона для мины
        alert("Вы попали на мину!");
        
        // Убираем обработчики на всех ячейках, чтобы остановить игру
        Array.from(grid.children).forEach(c => c.replaceWith(c.cloneNode(true)));
    } else {
        cell.textContent = "⭐"; // Безопасная ячейка показывает звезду
        cell.style.backgroundColor = "#4CAF50";
        cell.style.color = "#fff";
        cell.classList.add("safe");
        
        // Отключаем повторное нажатие на эту ячейку
        cell.removeEventListener("click", () => revealCell(index, cell));
    }
}

// Инициализация игры при загрузке
window.onload = () => {
    createGrid();
};

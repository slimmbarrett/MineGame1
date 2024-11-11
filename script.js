let mineCount = 3;
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
        alert("Вы попали на мину!");

        // Останавливаем игру, убирая обработчики
        Array.from(grid.children).forEach(c => c.replaceWith

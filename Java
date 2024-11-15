let mineCount = 3;
let mines = [];
const grid = document.getElementById("grid");
const mineCountDisplay = document.getElementById("mineCount");

// Создание сетки
function createGrid() {
    grid.innerHTML = ''; // Очистка сетки
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
    createGrid(); // Пересоздание сетки при запуске игры
    mines = generateMines(); // Генерация позиций мин
    alert("Мины расставлены. Найдите безопасные ячейки!");
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

// Открытие клетки
function revealCell(index, cell) {
    if (mines.includes(index)) {
        cell.style.backgroundColor = "red";
        alert("Игра окончена! Вы подорвались на мине.");
    } else {
        cell.style.backgroundColor = "green";
    }
}

document.querySelector(".start-button").addEventListener("click", startGame);

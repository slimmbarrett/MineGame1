let mineCount = 3;  // Начальное количество мин
let mines = [];
const grid = document.getElementById("grid");
const mineCountDisplay = document.getElementById("mineCount");

// Создание сетки 5x5
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
        mineCountDisplay.textContent = mineCount;  // Обновление отображения мин
    }
}

// Уменьшение количества мин
function decreaseMines() {
    if (mineCount > 1) {
        mineCount--;
        mineCountDisplay.textContent = mineCount;  // Обновление отображения мин
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

// Открытие ячейки
function revealCell(index, cell) {
    if (mines.includes(index)) {
        // Если это мина, показываем символ 💣
        cell.textContent = "💣"; 
        cell.classList.add("mine");
        
        // Используем setTimeout, чтобы показать сообщение через несколько секунд
        setTimeout(() => {
            alert("Игра окончена! Вы подорвались!");
            startGame(); // Перезапуск игры
        }, 300);
    } else {
        cell.classList.add("safe");
    }
}

createGrid();  // Создание сетки при запуске

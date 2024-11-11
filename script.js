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

// Открытие ячейки
function revealCell(index, cell) {
    if (mines.includes(index)) {
        // Добавляем анимацию появления мины
        cell.classList.add("mine");

        // Используем setTimeout, чтобы показать текст только после анимации
        setTimeout(() => {
            alert("Вы попали на мину!"); // Показываем сообщение только после анимации
        }, 1000); // Задержка в 1 секунду (время анимации мины)
        
        // Останавливаем игру, убирая обработчики
        Array.from(grid.children).forEach(c => c.replaceWith(c.cloneNode(true)));
    } else {
        cell.textContent = "⭐"; // Безопасная ячейка показывает звезду
        cell.classList.add("safe");

        // Отключаем повторное нажатие на эту ячейку
        cell.removeEventListener("click", () => revealCell(index, cell));
    }
}

// Инициализация игры при загрузке
window.onload = () => {
    createGrid(); // Создание сетки при загрузке
};

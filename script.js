// Логика игры (создание сетки, генерация мин, обработка кликов)
// ... (ваш существующий код)

// Пример функции для создания ячейки:
function createCell() {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    cell.addEventListener("click", () => {
        // Логика открытия ячейки
        // ...
    });
    return cell;
}

// Добавление ячеек в сетку
const grid = document.getElementById("grid");
for (let i = 0; i < 25; i++) {
    grid.appendChild(createCell());
}

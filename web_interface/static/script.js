function printFiles(e) {
    const files = e.target.files;   // получаем все выбранные файлы
    let fileInfoHtml = ''; // Переменная для хранения HTML-строки с информацией о файлах

    if (files.length > 0) {        // Проверяем, были ли выбраны файлы
        Array.from(files).forEach((file, index) => { // Преобразуем FileList в массив для удобства работы
            console.log(file);
            fileInfoHtml += "<p><strong><font style='color: black'>File " + (index + 1) + ": " + file.name + "</font></strong></p>";
            fileInfoHtml += "<p><font style='color: black'>Type: " + file.type || "n</font>/a</p>";
            fileInfoHtml += "<p><font style='color: black'>Size: " + file.size + " bytes</font></p>";
            fileInfoHtml += "<p><font style='color: black'>Changed on: " +  file.lastModifiedDate.toLocaleDateString() + "</font></p>";
            fileInfoHtml += "<hr>"; // Разделитель между информацией о файлах
        });

        const fileInfoDiv = document.getElementById("fileInfo");
        fileInfoDiv.innerHTML = ""; // Очищаем предыдущие данные
        fileInfoDiv.innerHTML = fileInfoHtml; // Выводим информацию о всех выбранных файлах
    }
}

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное действие формы

    var formData = new FormData();
    Array.from(this.elements.namedItem('file').files).forEach((file, index) => {
        formData.append(`file${index}`, file);
    });

    // Сбор информации о файлах в HTML-строку
    let fileInfoHtml = '';
    Array.from(this.elements.namedItem('file').files).forEach((file, index) => {
        fileInfoHtml += `<p><strong>${index + 1}: ${file.name}</strong></p>`;
        fileInfoHtml += `<p>Type: ${file.type}</p>`;
        fileInfoHtml += `<p>Size: ${file.size} bytes</p>`;
        fileInfoHtml += `<p>Last Modified: ${new Date(file.lastModified).toLocaleDateString()}</p>`;
        fileInfoHtml += '<hr>';
    });

    // Добавляем HTML-строку с информацией о файлах в FormData
    formData.append('fileInfoHtml', fileInfoHtml);
    // Отправляем данные на сервер в формате JSON
    res = fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'data':this.elements.namedItem('fileInfoHtml')})

    });
});
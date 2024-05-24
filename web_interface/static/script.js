let selectedFilesInfo = []; // Глобальная переменная для хранения информации о файлах

        function saveFileInfo(e) {
            const files = e.target.files;
            if (files.length > 0) {
                Array.from(files).forEach((file, index) => {
                    selectedFilesInfo.push({
                        name: file.name,
                        type: file.type,
                        size: file.size,
                        lastModifiedDate: file.lastModifiedDate
                    });
                });
            }
        }

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное действие формы

    var formData = new FormData();
    Array.from(this.elements.namedItem('file').files).forEach((file, index) => {
        formData.append(`file${index}`, file);
    });

    // Добавляем информацию о файлах в FormData
    selectedFilesInfo.forEach((info, index) => {
        formData.append(`fileInfo${index}`, info.name); // Здесь предполагается, что сервер ожидает имя файла
    });
    // Отправляем данные на сервер в формате JSON
    res = fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filesInfo: selectedFilesInfo }) // Передача всей информации о файлах в виде JSON
    });
});
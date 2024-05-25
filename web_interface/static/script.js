let selectedFilesInfo = [];

function saveFileInfo(e) {
    const files = e.target.files;
    if (files.length > 0) {
        Array.from(files).forEach((file, index) => {
            selectedFilesInfo.push({
                name: file.name,
                type: file.type,
                size: file.size,
                lastModifiedDate: file.lastModifiedDate,
                blob: file.slice(0, file.size) // Получаем Blob объект файла
            });
        });
    }
}

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Преобразование каждого Blob в строку Base64
    const base64Files = selectedFilesInfo.map(file => {
        return btoa(
            new Uint8Array(file.blob).reduce(
                (data, byte) => data + String.fromCharCode(byte),
                ''
            )
        );
    });

    // Создание объекта JSON с данными файлов
    const jsonData = {
        filesInfo: base64Files
    };

    // Отправка данных на сервер в формате JSON
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
   .then(response => response.json())
   .then(data => console.log(data))
   .catch(error => console.error(error));
});
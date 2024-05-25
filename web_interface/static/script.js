let selectedFilesInfo = []; // Инициализирует пустой массив для хранения информации о выбранных файлах.

function handleFileSelection(e) {
    const files = e.target.files;
    if (files.length > 0) {
        Array.from(files).forEach((file, index) => {
            selectedFilesInfo.push({
                name: file.name,
                type: file.type,
                size: file.size,
                lastModifiedDate: file.lastModifiedDate,
                blob: file.slice(0, file.size)
            });
        });
        updateFileInfo();
    }
}

function updateFileInfo() {
    const fileInfoDiv = document.getElementById("fileInfo");
    fileInfoDiv.innerHTML = '';
    selectedFilesInfo.forEach((file, index) => {
        fileInfoDiv.innerHTML += `
        <p><strong>${file.name}</strong></p>
        <p>Type: ${file.type}</p>
        <p>Size: ${file.size} bytes</p>
        <p>Changed on: ${file.lastModifiedDate.toLocaleDateString()}</p>
        <hr>`;
    });
}
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const jsonData = {
        filesInfo: selectedFilesInfo.map(file => ({
            name: file.name,
            type: file.type,
            size: file.size,
            lastModifiedDate: file.lastModifiedDate,
            content: btoa(new Uint8Array(file.blob).reduce((data, byte) => data + String.fromCharCode(byte), ''))
        }))
    };
    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }).then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});
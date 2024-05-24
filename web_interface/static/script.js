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

        // Добавление обработчика события нажатия на кнопку
        document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Предотвращаем стандартное действие формы

            // Здесь может быть логика обработки файлов перед отправкой на сервер

            // Продолжаем отправку формы
            this.submit(); // Используем метод submit формы для отправки данных на сервер
        });

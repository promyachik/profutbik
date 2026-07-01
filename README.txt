PROFUTBIK — точная замена файлов

1. Останови Hugo: Ctrl + C
2. Распакуй содержимое архива прямо в корень проекта:
   C:\Users\Dmitrii\promyachik
3. Подтверди замену существующих файлов.
4. Удали рядом файлы-дубликаты с названиями:
   transfer-ticker(2).html
   single(2).html
   transfers(1).json
   и любые transfer-ticker-final.html / single-final.html, если они лежат в папках проекта.
5. Запусти:
   hugo server --disableFastRender
6. В браузере нажми Ctrl + F5

Hugo использует только точные имена:
layouts\partials\transfer-ticker.html
layouts\transfers\single.html
data\transfers.json
static\css\transfer-ticker.css
static\css\transfer-article.css

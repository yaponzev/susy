# susy
## Super Synchronization for Local Catalogs

Для синхронизации двух и более каталогов по первому из списка нам требуется функция синхронизации ГЛАВНОГО каталога с ПРОВЕРЯЕМЫМ.

С ней мы можем синхронизировать ГЛАВНЫЙ каталог с любым количеством ПРОВЕРЯЕМЫХ с помощью цикла.

## Синхронизация двух каталогов

### Копирование несуществующих и изменённых файлов и каталогов
Записываем ГЛАВНЫЙ каталог в дерево. 

Двигаемся по дереву.

#### На каждой "ветке" начинаем такую клоунаду:

   Проверяем существование каталогов по списку из ГЛАВНОГО каталога: os.path.isdir(path).
   
    Если каталога нет, копируем его: shutil.copytree(path1, path2).
      
    Если каталог есть, ничего.
  
   Проверяем существование файлов по списку из ГЛАВНОГО каталога: os.path.isfile(path).
   
    Если файла нет, копируем его: shutil.copy2(path1, path2).
      
    Если файл есть, проверяем, одинаковы ли: comparison(path1,path2).
      
    Если разные, заменяем на копию: shutil.copy2(path1, path2).
        
    Если одинаковые, ничего не делаем.

## Удаление файлов и подкаталогов, не принадлежащих ГЛАВНОМУ каталогу
  Создаём список проверяемой ветки.
  
  Проверяем существование каталогов по списку из проверяемой ветки: os.path.isdir(path).
  
     Если каталога нет, удаляем его: shutil.rmtree(path).
     
     Если каталог есть, ничего.
     
  Проверяем существование файлов по списку из проверяемой ветки: os.path.isfile(path).
  
     Если файла нет, удаляем его: os.remove(path).
     
     Если каталог есть, ничего.

### Заканчиваем движение по дереву ГЛАВНОГО каталога 

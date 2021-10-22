import os
import shutil

# Сравнение с файлом: 0 - одинаковые, 1 - разные
def comparison(path1,path2):
    return os.system(f"fc /N {path1} {path2}")

# Удаление каталога или файла
def del_cat_or_file(path):
    if(os.path.isfile(path)):
        os.remove(path)
    else:
        shutil.rmtree(path)
        
# Предполагаемый путь
def ass_path(path_main,path_sync,v): #ass, потому что assumption
    return (path_sync + "%s"  %("\\" if v[len(path_main):] else "") + v[len(path_main)+1:])

# Синхронизация двух каталогов
def susy_for_2(path_main,path_sync):
    
    cat_main_tree = [] #cat, потому что catalog
    for v in os.walk(path_main):
        cat_main_tree.append(v)
        
    for v, dirs, files in cat_main_tree:
        
        #Копирование каталогов
        for i in dirs:
            if os.path.isdir(ass_path(path_main,path_sync,v)+"\\"+i) == False:
                shutil.copytree(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)
        
        #Проверка и копирование файлов
        for i in files:
            if os.path.isfile(ass_path(path_main,path_sync,v)+"\\"+i) == False:
                shutil.copy2(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)
            else:
                if comparison(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i) == 1:
                    shutil.copy2(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)
            
        #Удаление лишних файлов
        for_delete = os.listdir(ass_path(path_main,path_sync,v))
        for i in for_delete:
            if os.path.isdir(v+ "\\" + i) == False and os.path.isfile(v+ "\\" + i) == False:
                del_cat_or_file(ass_path(path_main,path_sync,v) + "\\" + i)
                
# Синхронизация двух и более каталогов
config_file = open("config.txt")
Catalogs = config_file.read().splitlines()
config_file.close()

for i in Catalogs[1:]:
    susy_for_2(Catalogs[0],i)

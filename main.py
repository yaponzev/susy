# ДЕЙСТВИЯ ПЕРЕД МОНИТОРИНГОМ
import os
import shutil
import time
from IPython.display import clear_output

# Сравнение с файлом: 0 - одинаковые, 1 - разные
def comparison(path1,path2):
    # Если видим каталог/файл или файл/каталог, сразу говорим, что разные
    f = open(path1,'r+b') # открываем, как бинарные
    content1 = f.read()
    f.close()
    f = open(path2,'r+b')
    content2 = f.read()
    f.close()

    a = 1
    if content1 == content2:
        a = 0
    return(a)    
    #### пробелы: решается сравнением ручками ::: ГОТОВО
    #### файлы или каталоги: решается проверкой на тип ::: ГОТОВО (реализовано в копировании файлов и каталогов)

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
                if os.path.isfile(ass_path(path_main,path_sync,v)+"\\"+i) == True:  # Но если вдруг есть файл
                      del_cat_or_file(ass_path(path_main,path_sync,v)+"\\"+i)       # Сначала удаляем его
                shutil.copytree(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)   # Перед копированием каталога
        
        #Проверка и копирование файлов
        for i in files:
            if os.path.isfile(ass_path(path_main,path_sync,v)+"\\"+i) == False:
                if os.path.isdir(ass_path(path_main,path_sync,v)+"\\"+i) == True: # Но если вдруг есть каталог
                    del_cat_or_file(ass_path(path_main,path_sync,v)+"\\"+i)       # Сначала удаляем его
                shutil.copy2(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)    # Перед копированием файла
            else:
                if comparison(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i) == 1:
                    shutil.copy2(v+"\\"+i, ass_path(path_main,path_sync,v)+"\\"+i)
            
        #Удаление лишних файлов
        for_delete = os.listdir(ass_path(path_main,path_sync,v))
        for i in for_delete:
            if os.path.isdir(v+ "\\" + i) == False and os.path.isfile(v+ "\\" + i) == False:
                del_cat_or_file(ass_path(path_main,path_sync,v) + "\\" + i)
                
# МОНИТОРИНГ
# Считывание каталогов для синхронизации
config_file = open("config.txt")
Catalogs = config_file.read().splitlines()
config_file.close()


# Синхронизируем все каталоги
for i in Catalogs[1:]:
    susy_for_2(Catalogs[0],i)
    

# Начинаем идти по списку из K каталогов
T = 0.02 # ожидание между шагами
T_SYNC = 10 # ожидание между синхронизациями в секундах
N = 1 
K = len(Catalogs)
s = 0
# Двигаясь по дереву смотрим на N каталог
while 0<1:
    """
    if s == 0:
            for i in range(T_SYNC,0,-1):
                clear_output(wait=True)
                print("До синхронизации осталось ",i," c")
                time.sleep(1)
    s = (s + 1)%(K+1)
    """
    
    clear_output(wait=True)
    print("Синхронизация")
    
    if N == 0:
        path_main = Catalogs[K-1]
    else:
        path_main = Catalogs[N-1]
        
    path_sync = Catalogs[N]
    
    """``````````````````````````````````````"""    
    #time.sleep(T)   
    cat_main_tree = [] 
    for v in os.walk(path_main):
            cat_main_tree.append(v)    
            
    for v, dirs, files in cat_main_tree:               
        #
        #       Если появилась новая папка 
        #           Копируем её во все каталоги кроме N
        #
        if os.path.isdir(ass_path(path_main,path_sync,v)) == True: # Проверяем возможность создания списка
            for_copy = os.listdir(ass_path(path_main,path_sync,v))
        for i in for_copy:
            if os.path.isdir(v+ "\\" + i) == False and os.path.isfile(v+ "\\" + i) == False:
                for j in range(1,K):
                    if os.path.isdir(v+"\\"+i) == False and os.path.isdir(ass_path(path_main,Catalogs[(N)%K],v) + "\\" + i) == True:
                        shutil.copytree(ass_path(path_main,Catalogs[(N)%K],v)+"\\"+i, ass_path(path_main,Catalogs[(N+j)%K],v)+"\\"+i)
  
    """``````````````````````````````````````"""
    #time.sleep(T)
    cat_main_tree = [] 
    for v in os.walk(path_main):
            cat_main_tree.append(v)
    
    for v, dirs, files in cat_main_tree:
        #
        #       Если пропала старая папка 
        #           Удаляем её из всех каталогов кроме N
        #
        for i in dirs:
            if os.path.isdir(ass_path(path_main,path_sync,v)+"\\"+i) == False:
                for j in range(1,K):
                    if os.path.isdir(ass_path(path_main,Catalogs[(N+j)%K],v) + "\\" + i) == True:
                        del_cat_or_file(ass_path(path_main,Catalogs[(N+j)%K],v) + "\\" + i)
    
    """``````````````````````````````````````"""

    #time.sleep(T)
    cat_main_tree = [] 
    for v in os.walk(path_main):
            cat_main_tree.append(v)
    
    for v, dirs, files in cat_main_tree:
        #
        #       Если пропал старый файл 
        #           Удаляем его из всех каталогов кроме N
        #  
        for i in files:
            if os.path.isfile(ass_path(path_main,path_sync,v)+"\\"+i) == False:
                for j in range(1,K):
                    if os.path.isfile(ass_path(path_main,Catalogs[(N+j)%K],v)+"\\"+i) == True: 
                        del_cat_or_file(ass_path(path_main,Catalogs[(N+j)%K],v) + "\\" + i)           

    """``````````````````````````````````````"""
    #time.sleep(T)             
    cat_main_tree = [] 
    for v in os.walk(path_main):
            cat_main_tree.append(v)    
            
    for v, dirs, files in cat_main_tree:               
        #
        #       Если появился новый файл 
        #           Копируем его во все каталоги кроме N
        #    
        if os.path.isdir(ass_path(path_main,path_sync,v)) == True: # Проверяем возможность создания списка
            for_copy = os.listdir(ass_path(path_main,path_sync,v))
            
        for i in for_copy:
            if os.path.isdir(v+ "\\" + i) == False and os.path.isfile(v+ "\\" + i) == False:
                for j in range(1,K):
                    if os.path.isfile(v+"\\"+i) == False and os.path.isfile(ass_path(path_main,Catalogs[(N)%K],v) + "\\" + i) == True:      
                        shutil.copy2(ass_path(path_main,Catalogs[(N)%K],v)+"\\"+i, ass_path(path_main,Catalogs[(N+j)%K],v)+"\\"+i)
    
    """``````````````````````````````````````"""
    #time.sleep(T)             
    cat_main_tree = [] 
    for v in os.walk(path_main):
            cat_main_tree.append(v)    
          
    for v, dirs, files in cat_main_tree:               
        # Если имена одинаковые и дата создания разная и размер разный
        #           
        #     Если дата создания файла из N-1 каталога > даты создания файла из N каталога
        #         Копируем файл из N-1 каталога во все каталоги кроме N-1
        #     Если наоборот
        #         Копируем файл из N каталога во все каталоги кроме N
        for i in files:
            if os.path.isfile(v+ "\\" + i) == True and os.path.isfile(ass_path(path_main,path_sync,v)+"\\"+i) == True:
                if os.path.getmtime(v+ "\\" + i) != os.path.getmtime(ass_path(path_main,path_sync,v)+"\\"+i):
                    if os.path.getsize(v+ "\\" + i) != os.path.getsize(ass_path(path_main,path_sync,v)+"\\"+i):
                        if os.path.getmtime(v+ "\\" + i) < os.path.getmtime(ass_path(path_main,path_sync,v)+"\\"+i):
                            del_cat_or_file(v + "\\" + i)
                            for j in range(1,K):
                                shutil.copy2(ass_path(path_main,Catalogs[(N)%K],v)+"\\"+i,ass_path(path_main,Catalogs[(N+j)%K],v)+"\\"+i)
                        else:
                            del_cat_or_file(ass_path(path_main,Catalogs[(N)%K],v)+"\\"+i)
                            for j in range(1,K):
                                shutil.copy2(v+"\\"+i, ass_path(path_main,Catalogs[(N+j-1)%K],v)+"\\"+i)
               
    N = (N+1)%K
    
#      Ждём 10 секунд                
#       Если появилась новая папка 
#           Копируем её во все каталоги кроме N
#
#       Если пропала старая папка 
#           Удаляем её из всех каталогов кроме N
#
#       Если появился новый файл 
#           Копируем его во все каталоги кроме N
#
#       Если пропал старый файл 
#           Удаляем его из всех каталогов кроме N
#       
#       Если имена одинаковые и дата создания разная и размер разный
#           
#           Если дата создания файла из N каталога > даты создания файла из modN(N+1) каталога
#               Копируем файлиз N каталога во все каталоги кроме N
#           Если наоборот
#               Копируем файл из N+1 каталога во все каталоги кроме N+1
#
#   Перезаписываем дерево 1-го каталога
#
#   
#
#

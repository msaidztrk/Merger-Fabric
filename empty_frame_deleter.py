import os
import shutil 

path = os.path
dir_list = os.listdir(os.curdir)
 
print("Files and directories in ", path, " :")

for folder in dir_list : 
    splitted = folder.split("-")
    if len(splitted) > 4 : 
        new_path_1 = folder 
        new_dir_list = os.listdir(new_path_1)
        print(new_dir_list)
        print("----")

        for this_dir in new_dir_list : 
            if this_dir == "frames" : 
                new_path_2 = this_dir 
                new_dir_list = os.listdir( new_path_1 + '/' + new_path_2)
       
                print("Frames klasörü içinde " , len(new_dir_list) , " adet görüntü vardır")

                if len(new_dir_list) < 10 : 
                    print("The folder will be deleted --> ",new_path_1 )
                    shutil.rmtree(new_path_1)
                  
    else : 
        continue
# prints all files
print(dir_list)
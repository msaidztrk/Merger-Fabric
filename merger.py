from PIL import Image, ImageDraw, ImageFont
import numpy as np
import glob
import os
import re
# import pytesseract 
from datetime import datetime
import json


main_array = []
def   make_array_of_dates(image_position,image_date_and_time , file_path):
  
    date_format = "%m-%d-%Y-%H-%M-%S-%f"
    date = datetime.strptime(image_date_and_time, date_format)  
    temp_push_json = {

        "position" : image_position , 
        "date" : date, 
        "path" : file_path
    } 
    main_array.append(temp_push_json)

def add_text_to_img(new_text , birlesik_resim): 
    width, height = birlesik_resim.size
    final_width = width
    final_height = height + 50
    final_image = Image.new("RGB", (final_width, final_height), color="black")
    final_image.paste(birlesik_resim, (0, 0)) 
    font_size = 40
    draw = ImageDraw.Draw(final_image)
    font = ImageFont.truetype(font_path, font_size)
    text_length = draw.textlength(new_text, font=font)
    text_x = final_image.width - text_length - 10  # 10 pixels from the right edge
    text_y = final_image.height - font.getmetrics()[0] - 10  # 10 pixels from the bottom edge
    draw.text((text_x, text_y), new_text, font=font, fill=font_color)
    return final_image



resim = []
resim_times = []


check_for_one_folder = 0 # FLAG
counter = 0

not_merged_single_left = 0 
not_merged_single_rigth = 0  
not_allowed_combination_count = 0
not_allowed_combination_array = []
allowed_combination_flag = "false"
allowed_combination_count = 0
wait_for_3_continue = 0 

font_color = (255, 255, 255)  # RGB color tuple
font_path = "./Merger Py/Turkish Times New Roman.ttf"  # Replace with the actual path to your font file
font_size = 100  # Updated font size  

allowed_combinations = [
    ['sol', 'sag', 'sol', 'sag'],
    ['sag', 'sol', 'sag', 'sol'],
    ['sol', 'sol', 'sag', 'sag'],
    ['sag', 'sag', 'sol', 'sol'],
    ['sag', 'sol', 'sol', 'sag'],
    ['sol', 'sag', 'sag', 'sol'],
] 

not_allowed_combination_array = [ 
    ['sol','sol','sol','sol'], 
    ['sag','sag','sag','sag'],
    ['sol','sol','sol','sag']
]


current_directory = os.getcwd()  # Get the current directory path
parent_directory = os.path.dirname(current_directory)  # Get the parent directory path

for root, dirs, files in os.walk('.'):
 
    if "frames" in dirs: # her kayıt klasörürnün içindeki frames klasörüne eriş 

            print('frames ....')
       
            cant_mergeable_in_one_folder = 0 

            print(files)

            if counter < 4 : 
                counter += 1 
                # continue


            frames_dir = os.path.join(root, "frames")
            jpg_files = glob.glob(os.path.join(frames_dir, "*.jpg")) 

            unwanted_save_path = os.path.join(frames_dir, "..", "unmergeable_imgs")  # yeni kaydedilecek dosyaların yolu
            os.makedirs(unwanted_save_path, exist_ok=True)  # klasörü oluştur veya varsa hata verme

            save_path = os.path.join(frames_dir, "..", "merged_images")  # yeni kaydedilecek dosyaların yolu
            if os.path.exists(save_path):
                print("Save path already exists!")
                continue  # Breaks the function if the path exists
            
            os.makedirs(save_path, exist_ok=True)  # klasörü oluştur veya varsa hata verme 

            main_array = []
            for file_path in jpg_files: # klasördeki resimleri detaylı bir json olarak düzenle
                
                image_full_name = file_path.split("\\frames\\")
                image_full_name_splitted = image_full_name[1].split('_') 
                print(image_full_name[1].split('_')) 
                image_position = image_full_name_splitted[1]
                image_date_and_time_and_jpg = image_full_name_splitted[2]
                image_date_and_time = image_date_and_time_and_jpg.split('.')[0]
                make_array_of_dates(image_position , image_date_and_time , file_path)

 
            sorted_by_array = sorted(main_array, key=lambda x: x['date']) # detalı resimler içeren jsonu zamana göre sırala

            # for indexes in sorted_by_array : 
                 # print(indexes) # prints : 
                 # {'position': 'sol', 'date': datetime.datetime(2023, 5, 6, 15, 17, 49, 339546), 'path': '.\\05-06-2023-15-11-35\\frames\\163_sol_05-06-2023-15-17-49-339546.jpg'}
                 # {'position': 'sag', 'date': datetime.datetime(2023, 5, 6, 15, 17, 49, 879846), 'path': '.\\05-06-2023-15-11-35\\frames\\105_sag_05-06-2023-15-17-49-879846.jpg'

            merged_count_in_folder = 0
            array_length = len(sorted_by_array)
            for index, img_json_index in enumerate(sorted_by_array): 

                # olay şudur : 4 resim birleştirilecek . ilk resimde diğer 3 resim isim kontrol edilecek , eğer kalan 
                # 3 resimde kayma veya zaman problemi var ise bu resim birleştirilmeyecek ve diğer 4lüye bakılacak 

                file_path = img_json_index['path']
                with Image.open(file_path) as img: 

                    image_full_name = file_path.split("\\frames\\")
                    image_full_name_splitted = image_full_name[1].split('_')  
                    folder_name = image_full_name[0]

                    image_position = image_full_name_splitted[1]
                    image_date_and_time = image_full_name_splitted[2]  

                    checking_each_four = [] 

                    if index + 3 >= len(sorted_by_array): 
                        continue 
                
                    resim = []
                    resim_times = []

                    this_img_position = image_position 
                    second_img_position = sorted_by_array[index + 1]['position']
                    third_img_position = sorted_by_array[index + 2]['position']
                    fourth_img_position = sorted_by_array[index + 3]['position']
                    checking_each_four = [ this_img_position , second_img_position ,third_img_position ,  fourth_img_position] 

                    second_img_path = sorted_by_array[index + 1]['path']
                    third_img_path = sorted_by_array[index + 2]['path']
                    fourth_img_path = sorted_by_array[index + 3]['path']   
                    all_four_path = [sorted_by_array[index + 0]['path'] ,  second_img_path , third_img_path , fourth_img_path]

                    resim_times.append(sorted_by_array[index + 0]['date'])
                    resim_times.append(sorted_by_array[index + 1]['date'])
                    resim_times.append(sorted_by_array[index + 2]['date'])
                    resim_times.append(sorted_by_array[index + 3]['date'])

                    first_img_name = sorted_by_array[index + 0]['path'].split("\\frames\\")[1]
                    second_img_name = second_img_path.split("\\frames\\")[1]
                    third_img_name = third_img_path.split("\\frames\\")[1]
                    fourth_img_name = fourth_img_path.split("\\frames\\")[1]
                    all_four_names = [first_img_name,second_img_name,third_img_name,fourth_img_name]
              

                    #left_offset = 400  # Define the offset value
                    #width, height = img.size
                    #left = left_offset
                    #top = 0
                    #right = width
                    #bottom = height 

                    #img = img.crop((left, top, right, bottom))
                    resim.append(np.array(img))

                    with Image.open(second_img_path) as second_img:
                    #    second_img = second_img.crop((left, top, right, bottom))
                        resim.append(np.array(second_img))

                    with Image.open(third_img_path) as third_img:
                    #    third_img = third_img.crop((left, top, right, bottom))
                        resim.append(np.array(third_img))

                    with Image.open(fourth_img_path) as fourth_img:
                    #    fourth_img = fourth_img.crop((left, top, right, bottom))
                        resim.append(np.array(fourth_img))
                       
              

                    if allowed_combination_flag == "true" and wait_for_3_continue != 0 :
                        wait_for_3_continue -= 1
                        continue 

                    if allowed_combination_flag == "true" and wait_for_3_continue == 0 :
                        allowed_combination_flag = "false"

                       
                    if len(checking_each_four) == 4 and any(checking_each_four == combination for combination in allowed_combinations): 
                        allowed_combination_flag = "true" 
                        wait_for_3_continue = 3 
                        merged_count_in_folder += 1


                    if allowed_combination_flag == "false" : 
                        not_allowed_combination_count = not_allowed_combination_count + 1 
                        not_allowed_combination_array.append(checking_each_four)
                        cant_mergeable_in_one_folder += 1

                        print("------------------------------")
                        print("hatalı kombinasyon : ")
                        print(checking_each_four)  

                        black_img = Image.new(second_img.mode, second_img.size, (0, 0, 0))

                        combination_mapping = {
                            ('sol', 'sol', 'sol', 'sol'): (black_img,  second_img  , black_img , fourth_img ),
                            ('sag', 'sag', 'sag', 'sag'): (img,  second_img  , black_img , black_img ),
                            ('sol', 'sol', 'sol', 'sag'): (black_img,  second_img  , fourth_img , img ),
                        }

                        checking_each_four_tuple = tuple(checking_each_four)

                        if checking_each_four_tuple in combination_mapping:
                            sag1, sol1, sag2, sol2 = combination_mapping[checking_each_four_tuple]
                        else : 
                            sag1, sol1, sag2, sol2 = [ img , second_img ,  third_img , fourth_img]
                           

                        # istenmeyen_birlesik_resim = np.concatenate([
                        #     np.concatenate([img, second_img], axis=1), sag sol 
                        #     np.concatenate([third_img, fourth_img], axis=1), sag sol
                        #     ], axis=0) # 4 adet resmi tek resim yap   
                        
                    
                        
                        # Cropped image of above dimension
                        # (It will not change original image)
                    


                        
                        istenmeyen_birlesik_resim = np.concatenate([
                            np.concatenate([sol1, sag1], axis=1),
                            np.concatenate([sol2, sag2], axis=1),
                            ], axis=0) # 4 adet resmi tek resim yap   

                        imageName = str(cant_mergeable_in_one_folder) + ' ' + str(checking_each_four[0]) + '-' + str(checking_each_four[1]) + '-' + str(checking_each_four[2]) + '-' + str(checking_each_four[3]) + '.jpg'
                        istenmeyen_birlesik_resim = Image.fromarray(istenmeyen_birlesik_resim)  
                        new_text = str(all_four_names) + '                                    '

                        final_image = add_text_to_img(new_text , istenmeyen_birlesik_resim)
                        final_image.save(os.path.join(unwanted_save_path, imageName))  # dosyayı yeni klasöre kaydet     

                        resim = []
                        resim_times = []
    
                        #for indexes in all_four_path : 
                            # print("hatalı kombinasyon : ",indexes)
                        #print("allowed_combination_flag : ",allowed_combination_flag , " and it's count : ",not_allowed_combination_count)
                        continue

                    # print(checking_each_four)
                    allowed_combination_count = allowed_combination_count + 1

                    if allowed_combination_flag == "true"  :  
                        
                            merged_file_new_name =sorted_by_array[index + 0]['date']


                            combination_mapping = {
                                ('sag', 'sol', 'sag', 'sol'): (img, second_img, third_img, fourth_img),
                                ('sol', 'sag', 'sol', 'sag'): (second_img, img, fourth_img, third_img),
                                ('sol', 'sol', 'sag', 'sag'): (third_img, img, fourth_img, second_img),
                                ('sag', 'sag', 'sol', 'sol'): (img, second_img, third_img, fourth_img),
                                ('sag', 'sol', 'sol', 'sag'): (img , second_img , fourth_img ,third_img),
                                ('sol', 'sag', 'sag', 'sol'): (second_img ,img , third_img , fourth_img)
                            }

                            checking_each_four_tuple = tuple(checking_each_four)

                            if checking_each_four_tuple in combination_mapping:
                                sag1, sol1, sag2, sol2 = combination_mapping[checking_each_four_tuple]

                                sag1_time = resim_times[combination_mapping[checking_each_four_tuple].index(sag1)]
                                sag2_time = resim_times[combination_mapping[checking_each_four_tuple].index(sag2)]
                                sol1_time = resim_times[combination_mapping[checking_each_four_tuple].index(sol1)]
                                sol2_time = resim_times[combination_mapping[checking_each_four_tuple].index(sol2)] 

                            for indexes in all_four_path : 
                           
                                print( indexes)
    
                            
                            # merge pozisyonları --> np.concatenate([sag1, sol1], axis=1), np.concatenate([sag2, sol2], axis=1) olacak şekilde düzenlenecek


                            # birlesik_resim = np.concatenate([
                            # np.concatenate([sol1, sag1], axis=1),
                            # np.concatenate([sol2, sag2], axis=1),
                            # ], axis=0) # 4 adet resmi tek resim yap   
                            # birlesik_resim = Image.fromarray(birlesik_resim)  

                            #for_left_images_offset = 1100  # Define the offset value
                            #width, height = img.size
                            #
                            #top = 0
                            #right = width
                            #bottom = height 

                            #sag1 = sag1.crop((0, top, right, bottom))
                            #sol1 = sol1.crop((for_left_images_offset, top, right, bottom))
                            #sag2 = sag2.crop((0, top, right, bottom))
                            #sol2 = sol2.crop((for_left_images_offset, top, right, bottom))
                        

                            birlesik_resim = np.concatenate([
                            np.concatenate([sag1, sol1], axis=1),
                            np.concatenate([sag2 , sol2], axis=1),
                            ], axis=0) # 4 adet resmi tek resim yap   
                            birlesik_resim = Image.fromarray(birlesik_resim) 

                            time_difference_sag = (sag2_time - sag1_time).total_seconds()     
                            time_difference_sag =   round(time_difference_sag, 2)

                            time_difference_sol = (sol2_time - sol1_time).total_seconds()     
                            time_difference_sol =   round(time_difference_sol, 2) 

                            time_difference_sag = str(time_difference_sag)
                            time_difference_sol = str(time_difference_sol)  

                            this_img_current_date = str(sorted_by_array[index + 0]['date'])

                            space_string ,space_count = "             " , 5 
                            new_text = this_img_current_date + space_string +  "      Cam Second Diffs : R:" + time_difference_sag + " / L:" + time_difference_sol + "                                  "
                            new_text = str(new_text)
                            final_image = add_text_to_img(new_text , birlesik_resim)
                            new_merged_image_name =  str(merged_count_in_folder) + " " + image_date_and_time
                            final_image.save(os.path.join(save_path, new_merged_image_name))  # dosyayı yeni klasöre kaydet 
                            print("merge successful , to : " , save_path , ' Folder , and named : ',new_merged_image_name ) 
                            


                     

                      

                   
print("------------------------------------------")
print('not_allowed_combination_count : ',not_allowed_combination_count)
# print(not_allowed_combination_array)
print('allowed_combination_count : ',allowed_combination_count)
print('DONE')




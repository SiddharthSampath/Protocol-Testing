import os
folder = '/home/client1/test'  #destination folder
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        
    except Exception as e:
        print(str(e))

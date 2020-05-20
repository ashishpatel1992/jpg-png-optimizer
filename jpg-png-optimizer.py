# Utility to optimize jpg, jpeg and png files
# Developed by Ashish Patel
from PIL import Image
import os.path
import sys
import os
import glob
import enum
from resizeimage import resizeimage

totalsize = 0
file_count = 0
file_count_large = 0
large_file_width = 800

if(len(sys.argv) < 2):
    print("Invalid Arguments")
    print('Try giving path as "./test/*.*"')
    exit()
    
paths = glob.glob(sys.argv[1]) #"./test/*.*"
# fn = sys.argv[1]
# print(sys.argv[1])


# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4
 
#  Convert the size from bytes to other units like KB, MB or GB"""
def convert_unit(size_in_bytes, unit):
    if unit == SIZE_UNIT.KB:
        return size_in_bytes/1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes/(1024*1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes/(1024*1024*1024)
    else:
        return size_in_bytes
    
def resize_and_replace_width(filename,width):
    fd_img = open(filename, 'rb')
    img = Image.open(fd_img)
    img = resizeimage.resize_width(img, width)
    img.save(filename, img.format)
    fd_img.close()

def get_file_type(filename):
    fd_img = open(filename,'rb')
    img = Image.open(fd_img)
    img_format = img.format
    
    img.close()
    return img_format


for path in paths:
    filename = os.path.join(path)
    filesize = os.path.getsize(filename)
    totalsize = totalsize + filesize
    try :
        img = Image.open(filename)
        width, height = img.size
        
        if int(width) > large_file_width:
            file_count_large = file_count_large +1
            # Resize
            resize_and_replace_width(filename, large_file_width)
            print (width,height,convert_unit(filesize,SIZE_UNIT.KB),'KB',path)
        
        file_count = file_count + 1
        file_type =get_file_type(filename) 
        if file_type == 'JPEG':
            os.system('jpegoptim '+filename)
        elif file_type == 'PNG':
            os.system('pngquant -f --ext .png ' + filename)
    except Exception as e:
        print(e)

print('Total of',file_count,'files having',convert_unit(totalsize,SIZE_UNIT.MB),' MB in directory')
print('Total of', file_count_large,'large files')


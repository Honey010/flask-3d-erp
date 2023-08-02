from s3_upload import s3_upload
import os

def uploadToS3(filePath):
    if not filePath.split(".")[-1] in ['stl', "STL"]:
        s3_upload(filePath, filePath + '.stl')
    s3_upload(filePath, filePath + '.png')
    s3_upload(filePath, filePath)
    
    return

def emptyUploadFolder():
    for f in os.listdir('uploads'):
        os.remove(os.path.join('uploads', f))
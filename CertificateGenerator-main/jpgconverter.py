import os;
import os.path;
import requests;

from aspose.slides import Presentation; 
import aspose.pydrawing as drawing;

def convertToJpg(path):
    presentation = Presentation(path);
    presentation.slides[0].get_thumbnail(2,2).save(
        os.path.splitext(path)[0]+".jpeg",
        drawing.imaging.ImageFormat.jpeg   
    );

def convertToJpgFromCloud(path):
    url = "http://34.142.122.214:5000/upload";
    
    with open(path,'rb') as file:
        files = {

            'file' : (path,file)
        };

        response = requests.post(
            url,
            files=files
        )

        if response.status_code == 200:
            file_content = response.content;
            
            with open(os.path.splitext(path)[0]+'.jpg',"wb") as new_file:
                new_file.write(file_content);


    
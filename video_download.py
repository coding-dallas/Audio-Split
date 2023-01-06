import urllib.request
import os

def video_url(url_link):
    urllib.request.urlretrieve(url_link,'videos/filename.mp4') 

def video_drive(url):
    
    cmd=f'youtube-dl '+url
    os.system(cmd)

def video_youtube(url):
    
    cmd=f'youtube-dl '+url
    os.system(cmd)

if __name__=='__main__':
    url_link='http://swayam.iiit.ac.in/upload/uploadfiles/Universal%20origins%20of%20intellectual%20property_Part_3.mp4'
    

    # http='http'
    # https='https'
    # with open('/home/bit/Documents/data_processing/data/IITM-2/Intellectual Property/ipr-video-link_Video links.txt','r') as file:
    #     for url in file:
    #         if https in url:

    #             httpsUrl=url.replace(https+'://','')
    #             if httpsUrl.startswith('you'):
    #                 video_youtube(url)
    #             elif httpsUrl.startswith('drive'):
    #                 video_drive(url)
    #             else:
    #                 video_url(url)

    #         elif http in url:
    #             httpUrl=url.replace(http+'://','')
    #             if httpUrl.startswith('you'):
    #                 video_youtube(url)
    #             elif httpUrl.startswith('drive'):
    #                 video_drive(url)
    #             else:
    #                 video_url(url)

    #     file.close()
        
    video_url(url_link)
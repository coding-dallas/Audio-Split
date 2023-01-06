import pandas as pd
import os, io, re, sys, time, datetime
from glob import glob
import numpy as np

from util.creating_directories import create_directories
from util.convert_srt_to_csv import convert_srt_to_csv
from util.extract_audio import wmv_to_wav
from util.extract_audio import mp4_to_wav
from util.slice_audio import split_files
from util.change_sample_rate import pre_process_audio
from util.create_DS_csv import create_DS_csv
from util.merge_csv import merge_csv
from util.merge_transcripts_and_files import merge_transcripts_and_wav_files
from util.clean import clean_unwanted_characters
from util.trans_numbers import translate_numbers

start_time = time.time()

# # # Check if srt_files directory exists and contains srt files

srt_path = '/home/bit/Documents/data_processing/data/IITM-2/Research Methodology/English/srt_files/'
video_path='/home/bit/Documents/data_processing/data/IITM-2/Research Methodology/English/videos/'

if os.path.exists(srt_path):
    print('Folder %s exists.. continuing processing..' %srt_path)
else:
    print('Folder "srt_files" is missing')
    try:
        os.mkdir(srt_path)
    except OSError:
        print('Creation of directory %s failed' %srt_path)
    else:
                print('Successfully created the directory %s' %srt_path)
                print('--> Please add srt files to folder %s' %srt_path)
                sys.exit()


#Check if audio directory exists and contains wmv or wav files

audio_path = './audio/'

if os.path.exists(audio_path):
    print('Folder %s exists.. continuing processing..' %audio_path)
else:
    print('Folder "audio" is missing')
    try:
        os.mkdir(audio_path)
    except OSError:
        print('Creation of directory %s failed' %audio_path)
    else:
        print('Successfully created the directory %s' %audio_path)
    print('--> Please add wav or wmv files to folder %s' %audio_path)
    sys.exit()

srt_counter = len(glob(srt_path + '*.srt'))

if srt_counter == 0:
    print('!!! Please add srt_file(s) to %s-folder' %srt_path)
    sys.exit()

#Create directories
create_directories()


#Extracting information from srt-files to csv
print('Extracting information from srt_file(s) to csv_files')
for file in glob(srt_path  + '*.srt'):
    print(file)
    convert_srt_to_csv(file)
print('%s-file(s) converted and saved as csv-files to ./csv' %srt_counter)
print('---------------------------------------------------------------------')


#extract audio (wav) from wmw
for entry in glob(video_path + '*.wmv'):
    wmv_to_wav(entry)
print('WMV to WAV convert complete')
print('---------------------------------------------------------------------')

#extract audio (wav) from mp4
for entry in glob(video_path + '*.mp4'):
    mp4_to_wav(entry)
print('MP4 to WAV convert complete')
print('---------------------------------------------------------------------')

#Pre-process audio for folder in which wav files are stored
pre_process_audio(audio_path)
print('Pre-processing of audio files is complete.')
print('---------------------------------------------------------------------')

#now slice audio according to start- and end-times in csv
print('Slicing audio according to start- and end_times of transcript_csvs...')
for item in glob('./ready_for_slice/*.csv'):
    wav_item = item.replace('.csv','.wav')
    print(item)
    if os.path.exists(wav_item):
        print(wav_item)
        split_files(item, wav_item)
    else:
        next
wav_counter = len(glob('./sliced_audio/' + '*.wav'))
print('Slicing complete. {} files in dir "sliced_audio"'.format(wav_counter))
print('---------------------------------------------------------------------')

#Now create list of filepaths and -size of dir ./sliced_audio
create_DS_csv('./sliced_audio/')
print('DS_csv with Filepaths - and sizes created.')
print('---------------------------------------------------------------------')

#now join all seperate csv files
merge_csv('./ready_for_slice/')
print('Merged csv with all transcriptions created.')
print('---------------------------------------------------------------------')

#merge the csv with transcriptions and the file-csv with paths and sizes
transcript_path = './merged_csv/Full_Transcript.csv'
DS_path = './merged_csv/Filepath_Filesize.csv'
merge_transcripts_and_wav_files(transcript_path, DS_path)
print('Final DS csv generated.')
print('---------------------------------------------------------------------')

#write transcript to text-file for language model
df_text = pd.read_csv('./merged_csv/DS_training_final.csv')
for ind in df_text.index:
    file_name=df_text['wav_filename'][ind].replace('.wav','.txt')
    text=df_text['transcript'][ind]
    print(file_name)
    with open(file_name,'w') as f:
        f.write(text)
    
    # print(file_name,text)
    

    
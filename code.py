# Call the Microphone and Save the Audio Data
import pyaudio
import wave

p = pyaudio.PyAudio()
print('Recording')

sample_depth=pyaudio.paInt16
chunk = 1024 
channel = 2
sample_rate = 44100
second = 5
file = "D:\桌面\output.wav"

stream = p.open(format=sample_depth,
                channels=channel,
                rate=sample_rate,
                frames_per_buffer=chunk,
                input=True)

   #Save the data as a WAV file
wf = wave.open(file, 'wb')
wf.setnchannels(channel)
wf.setsampwidth(p.get_sample_size(sample_depth))
wf.setframerate(sample_rate)

   #Store data in chunks for 5 seconds
for i in range(0, int(second * sample_rate / chunk)):
    audio_result = stream.read(chunk)
    wf.writeframes(audio_result)

print('Finished recording')
   #close everything
wf.close()
stream.stop_stream()
stream.close()
p.terminate()

# Audio Recognization
import speech_recognition as sr
r = sr.Recognizer()
demo=sr.AudioFile(file)
with demo as source:
	audio=r.record(source)
text_result = r.recognize_google(audio, language='zh-CN')

# Hanlp Seperate Sentence
import re
import pymysql
import result as result
def get_dict(a, b):
   res = []
   for i in a:
      for j in b:
         temp = list(j.values())[0]
         if i in temp:
            res.append(temp)
   return res

from hanlp_restful import HanLPClient
HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
wordStr = str(HanLP.tokenize(text_result))
   #seperate sentence result
wordList=(re.findall(r'\'(.*?)\'',wordStr))
wordStr2 = "\'"+'\',\''.join(map(str,wordList))+"\'"
   #link the database to get the link of video of each phrase or word
db = pymysql.connect(host='localhost',user='root',password='pass123',db='sign_language' )
   #return as dictionary
cursor = db.cursor(pymysql.cursors.DictCursor)

sql = "SELECT road FROM data WHERE mean in ( "+str (wordStr2)+" )"

try:
   cursor.execute(sql)
   #get every row fetched
   results = cursor.fetchall()
   #iterate the result
   link_result=get_dict(wordList,results)
   
except:
   import traceback
   traceback.print_exc()
db.close()


# Stich the Video 
from moviepy.editor import VideoFileClip, concatenate_videoclips
clip = []
for i in range(len(link_result)):
    temp = link_result[i].encode('UTF-8')
    video = VideoFileClip(link_result[i])
    clip.append(video)
final_clip = concatenate_videoclips(clip)
   #store the final video into a fix place
final_clip.write_videofile("D:/MySQL/Data/Uploads/result.mp4")


# Store the Final Video Position into the Database to be ready to be embed into the website
db = pymysql.connect(host='localhost',user='root',password='pass123',db='sign_language' )
cursor = db.cursor()

sql = """INSERT INTO sign_language.result(road)
   VALUES ("D:/MySQL/Data/Uploads/result.mp4")"""
try:
   #execute the sql sentence
   cursor.execute(sql)
   db.commit()
except:
   #if error, roll back
   db.rollback()

db.close()


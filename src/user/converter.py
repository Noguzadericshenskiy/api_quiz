import os
from os import path
from pydub import AudioSegment
import datetime

data = datetime.datetime.utcnow()
ts = str(int(data.timestamp()*1000000))
print(ts)
ts1 = str(int(datetime.datetime.utcnow().timestamp()*1000000))
print(ts1)


#
# def converter(path):
#     src = "simple.wav"
#     # dst = "output.mp3"
#     file_name = "../sound/output.mp3"
#     dst = os.path.join(path, file_name)
#     print(dst)
#     sound = AudioSegment.from_mp3(src)
#     sound.export(dst, format="wav")
#
#
# def create_link():
#     path = os.path.curdir
#
#     # patth_seve = f"http://{HOST}:{PORT}/record?id={record_id}&user={user_id}"
#     return os.path.join(path, "../sound")
#
#
# converter(create_link())


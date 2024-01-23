from pydub.utils import mediainfo


def get_file_duration(file):
    file_info = mediainfo(file)
    total_seconds = float(file_info.get('duration'))
    minutes = int(total_seconds//60)
    seconds = int(total_seconds%60)
    answer = f"{minutes}min {seconds}s"
    print(answer)
    
file_path = '/home/ankit/Music/Hothon Se Chhu Lo Tum.mp3'

get_file_duration(file_path)

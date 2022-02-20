from googleapiclient.discovery import build
import requests,json,random
api_key = 'AIzaSyBMlop7Dz3Y6vI-T96rdDUrYHVB_k8oY78'

youtube = build('youtube', 'v3', developerKey=api_key)

prefix = ['IMG ', 'IMG_', 'IMG-', 'DSC ']
postfix = [' MOV', '.MOV', ' .MOV']

def random_str(str_size):
    res = ""
    for i in range(str_size):
        x = random.randrange(0,25)
        c = chr(ord('a')+x)
        res += c
    return res

def search_youtube():
    search_response = youtube.search().list(
    q=random.choice(prefix) + str(random.randint(999, 9999)) + random.choice(postfix),
    # q=random_str(3),
    part='snippet',
    maxResults=3
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s' % (search_result['id']['videoId']))
    return (videos[random.randint(0, 2)])

def get_video():
    return "https://youtu.be/"+search_youtube()

def get_lyrics():
    url = 'https://a3odwonexi.execute-api.us-east-2.amazonaws.com/default/Bars_API'
    data = requests.get(url).content
    lit = json.loads(data.decode('ascii'))
    return lit['data']['lyric']

def response(type):
    read = False
    resp =[]
    for l in open(".//responses"):
        if l.startswith('#') or l[0].strip() == '':
            continue
        elif l.startswith('$'+type):
            read = True
            continue
        elif l.startswith('$'):
            read=False
        else:
            if read:
                resp.append(l.replace("\\n","\n"))
    return random.choice(resp)
	
def given(date):
    read = False
    resp =[]
    for l in open(".//advent.txt"):
        if l.contains('IO?') or l[0].strip() == '':
            continue
        elif l.startswith('$'+type):
            read = True
            continue
        elif l.startswith('$'):
            read=False
        else:
            if read:
                resp.append(l.replace("\\n","\n"))
    return random.choice(resp)

# coding=utf-8
import random;
from random_words import RandomWords
import string
import csv
import os
from pynamegenerator import generate_name #import來自資料夾中的另外一個程式
import time
import datetime

def generate_random_table(length): #產生長度為length的使用者資料
    userTable = []
    for i in range(100):
        name = random_chinese_name()
        account = random_account()
        pwd = random_password()
        user = [name, account, pwd]
        userTable.append(user)
    return userTable

def random_chinese_name(): #產生隨機中文姓名
    family = ["李", "王", "張", "劉", "陳", "楊", "黃", "趙", "周", "吳", "徐", "孫", "朱", "馬", "胡", "郭", "林", "何", "高", "梁", "鄭", "羅", "宋", "謝", "唐", "韓", "曹", "許", "鄧", "蕭", "馮", "曾", "程", "蔡", "彭", "潘", "袁", "於", "董", "餘", "蘇", "葉", "呂", "魏", "蔣", "田", "杜", "丁", "沈", "姜", "範", "江", "傅", "鐘", "盧", "汪", "戴", "崔", "任", "陸", "廖", "姚", "方", "金", "邱", "夏", "譚", "韋", "賈", "鄒", "石", "熊", "孟", "秦", "閻", "薛", "侯", "雷", "白", "龍", "段", "郝", "孔", "邵", "史", "毛", "常", "萬", "顧", "賴", "武", "康", "賀", "嚴", "尹", "錢", "施", "牛", "洪", "龔"]
    given = ["世", "中", "仁", "伶", "佩", "佳", "俊", "信", "倫", "偉", "傑", "儀", "元", "冠", "凱", "君", "哲", "嘉", "國", "士", "如", "娟", "婷", "子", "孟", "宇", "安", "宏", "宗", "宜", "家", "建", "弘", "強", "彥", "彬", "德", "心", "志", "忠", "怡", "惠", "慧", "慶", "憲", "成", "政", "敏", "文", "昌", "明", "智", "曉", "柏", "榮", "欣", "正", "民", "永", "淑", "玉", "玲", "珊", "珍", "珮", "琪", "瑋", "瑜", "瑞", "瑩", "盈", "真", "祥", "秀", "秋", "穎", "立", "維", "美", "翔", "翰", "聖", "育", "良", "芬", "芳", "英", "菁", "華", "萍", "蓉", "裕", "豪", "貞", "賢", "郁", "鈴", "銘", "雅", "雯", "霖", "青", "靜", "韻", "鴻", "麗", "龍"]
    return random.choice(family) + ''.join(random.choices(given, k = random.choice([1,2])));

def random_account(): #產生隨機帳號
    rw = RandomWords()
    n = random.randrange(1,3)
    
    if n==1:
        return ''.join(random.choices(rw.random_words(count=20), k = 1)) +''.join(random.choices( string.digits, k = random.randint(1,5))) 
    elif n==2:
        return ''.join(generate_name(language='en', gender=random.choices(['male', 'female']), size=1, type='array')) + ''.join(random.choices( string.digits, k = random.randint(1,5)))

def random_password(): #產生隨機密碼

    return ''.join(random.choices(string.ascii_letters+string.digits, k = random.choice([5,10])))

def seperate_user(UserTable): #將資料集分隔成老師、學生以及管理者
    split1 = int(0.8*len(UserTable))
    split2 = int(0.95*len(UserTable))

    random.shuffle(UserTable)
    student = UserTable[:split1]
    teacher = UserTable[split1:split2]
    admin = UserTable[split2:]

    return student, teacher, admin

def teacher_data(Teacher, Courses): #由於是老師決定上傳影片的Title以及Id，所以先產生屬於老師的table
    table = []
    video_info = []
    [teacher_videos, videos] = videoId(Teacher)  #隨機決定[每個老師上傳幾份影片, 影片的CourseId]
    for t in range(1,len(Teacher)+1):
            teached = random.choices(Courses, weights=[2,2,2,2,2,2,2,2,2]) #每個老師只會教授一種課程
            VideoId = randomtimes(teacher_videos[t] - teacher_videos[t-1]) #隨機產生影片錄製的時間
            for video in range(teacher_videos[t-1], teacher_videos[t]):
                table.append([Teacher[t-1][1], Teacher[t-1][2], ''.join(teached), videos[video]])
                video_info.append([VideoId[video - teacher_videos[t-1]]+'-'+''.join(teached), videos[video]]) #list,[所有影片的Title, CourseId]

    #print(video_title)
    return sorted(table, key=lambda x:x[2]), video_info

def videoId(Teacher): #隨機產生每位老師擁有的影片數量以及每個影片的CourseId
    teacher_videos = [0]
    total_video = 0
    for i in range(len(Teacher)):
        video = random.randint(1,20) #每位老師最多擁有20部影片
        teacher_videos.append(video+teacher_videos[i])
        total_video+=video
    videos = random.sample([j for j in range(1000,10000)], k=total_video) #影片的CourseId隨機取四位數，所以影片代碼跟老師或學生並沒有關聯

    return [teacher_videos, videos]

def randomtimes(n): #隨機產生時間
    dates = []
    sortDate = []
    stime = (2020,1,1,0,0,0,0,0,0)
    etime = (2023,12,31,23,59,59,0,0,0)

    start = time.mktime(stime)
    end = time.mktime(etime)

    for _ in range(n):
        t=random.randint(start, end)
        date_touple = time.localtime(t)
        sortDate.append(date_touple)

    sortDate.sort()
    for i in range(n):
        date = time.strftime("%Y-%m-%d",sortDate[i])
        #print(type(date))
        dates.append(date)
    return dates

def videos_data(video_infos, students): #將teacher_data funtion中的video_info list在進一步新增有哪些學生看過那些影片
    videos = []

    for video_info in video_infos:
        student = random.sample(students, k=len(students))
        for j in sorted(student, key=lambda x:x[1]):
            v = video_info[:]
            v.append(j[1])
            videos.append(v)
    return  videos


def student_data(Student, video_info):  #產生student table
    person_table = []
    table = []
    for s in Student:
        for v in video_info:
            if v[2] == s[1]:
                person_table.append([s[1], s[2], v[1]])
        person_table = sorted(person_table, key=lambda x:x[2])
        table = table + person_table
        person_table = []
        #print(table)
    return table

def video_watch_history(video_info): #產生影片觀看歷史
    VideoWatchHistory = []
    for video in video_info:
        Video = video[:]
        Video.append(random.randint(1,3600)) #每部影片最多六十分鐘 ，這裡以秒數計算
        VideoWatchHistory.append([Video[2], Video[1], Video[3]])

    return sorted(VideoWatchHistory, key=lambda x:x[0])

    


if __name__ == '__main__':
    try:
        os.mkdir('table',exist_ok=True)
    except:
        print("ExistError:Folder already exist.")
    
    userTable_headers = ['姓名', '帳號', '密碼']
    student_headers = ['帳號', '密碼', '觀看過的影片代碼']
    teacher_headers = ['帳號', '密碼', '授課課程', '課程影片代碼']
    video_headers = ['Title', 'CourseId', 'StudentAccount']
    Courses = ['CN', 'Eng', 'Math', 'Phys', 'Che', 'Bio', 'History', 'Geo', 'CSD'] #課程代號，[國, 英, 數, 物理, 化學, 生物, 歷史, 地理, 公民]
    VWH_headers = ['StudentAccount', 'CourseId', 'Time']
     
    userTable = generate_random_table(100)  #產生一百筆資料


    with open('table/userTable.csv','w',encoding='utf-8-sig',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(userTable_headers)
        writer.writerows(userTable)
        f.close()

    student, teacher, admin = seperate_user(userTable) #分割使用者
    teacher_teached, video_info = teacher_data(teacher, Courses) #[老師的table, 初步的videos資訊]
    videos = videos_data(video_info, student) #產生videos table
    student_learned = student_data(student, videos) #student table
    VideoWatchHistory = video_watch_history(videos) #產生影片觀看歷史的table
    
    

    with open('table/student.csv', 'w' ,encoding='utf-8-sig', newline='') as fs:
        writer = csv.writer(fs)
        writer.writerow(student_headers)
        writer.writerows(student_learned)
        fs.close()

    with open('table/teacher.csv', 'w' ,encoding='utf-8-sig', newline='') as ft:
        writer = csv.writer(ft)
        writer.writerow(teacher_headers)
        writer.writerows(teacher_teached)
        ft.close()

    with open('table/admin.csv', 'w' ,encoding='utf-8-sig', newline='') as fa:
        writer = csv.writer(fa)
        writer.writerow(userTable_headers[1:])
        for row in admin:
            writer.writerow(row[1:])
        fa.close()

    with open('table/videos.csv', 'w' , newline='') as fa:
        writer = csv.writer(fa)
        writer.writerow(video_headers)
        for row in videos:
            writer.writerow(row) 
        fa.close()

    with open('table/video_watch_history.csv', 'w' ,encoding='utf-8-sig', newline='') as fa:
        writer = csv.writer(fa)
        writer.writerow(VWH_headers)
        writer.writerows(VideoWatchHistory)
        fa.close()


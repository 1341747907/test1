import requests
import os
import re
import cv2
from threading import Thread,Lock
import matplotlib.pyplot as plt

path_cat=r'F:/Yanjiusheng/Yan1_shangxueqi/New_student_practice/Work5/cat'
path_dog=r'F:/Yanjiusheng/Yan1_shangxueqi/New_student_practice/Work5/dog'
class pachong(object):
    def __init__(self,):
        self._lock = Lock()

    def get_images_from_baidu(self,keyword, page_num, save_dir):
        self._lock.acquire()
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            # 请求的 url
            url = 'https://image.baidu.com/search/acjson?'
            n = 0
            for pn in range(0, 30 * page_num, 30):
                # 请求参数
                param = {'tn': 'resultjson_com',
                         # 'logid': '7603311155072595725',
                         'ipn': 'rj',
                         'ct': 201326592,
                         'is': '',
                         'fp': 'result',
                         'queryWord': keyword,
                         'cl': 2,
                         'lm': -1,
                         'ie': 'utf-8',
                         'oe': 'utf-8',
                         'adpicid': '',
                         'st': -1,
                         'z': '',
                         'ic': '',
                         'hd': '',
                         'latest': '',
                         'copyright': '',
                         'word': keyword,
                         's': '',
                         'se': '',
                         'tab': '',
                         'width': '',
                         'height': '',
                         'face': 0,
                         'istype': 2,
                         'qc': '',
                         'nc': '1',
                         'fr': '',
                         'expermode': '',
                         'force': '',
                         'cg': '',  # 这个参数没公开，但是不可少
                         'pn': pn,  # 显示：30-60-90
                         'rn': '30',  # 每页显示 30 条
                         'gsm': '1e',
                         '1618827096642': ''
                         }
                request = requests.get(url=url, headers=header, params=param)
                if request.status_code == 200:
                    print('Request success.')
                request.encoding = 'utf-8'
                # 正则方式提取图片链接
                html = request.text
                image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
                print(image_url_list)
                # # 换一种方式
                # request_dict = request.json()
                # info_list = request_dict['data']
                # # 看它的值最后多了一个，删除掉
                # info_list.pop()
                # image_url_list = []
                # for info in info_list:
                #     image_url_list.append(info['thumbURL'])

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                for image_url in image_url_list:
                    image_data = requests.get(url=image_url, headers=header).content
                    with open(os.path.join(save_dir, f'{n:06d}.jpg'), 'wb') as fp:
                        fp.write(image_data)
                    n = n + 1
        finally:
            self._lock.release()

class pa_chong(Thread):

    def __init__(self,name,keyword, page_num, save_dir):
        super().__init__()
        self._name=name
        self._keyword=keyword
        self._page_num = page_num
        self._save_dir = save_dir
    def run(self):
        self._name.get_images_from_baidu(self._keyword,self._page_num,self._save_dir)

def work1():
    name=pachong()
    t1 = pa_chong(name,'猫',10,'猫')
    t1.start()
    t2 = pa_chong(name,'狗',10,'狗')
    t2.start()
    t1.join()
    t2.join()
    print('Get images finished.')

def work2():
    image = cv2.imread('F:/Yanjiusheng/Yan1_shangxueqi/New_student_practice/Work5/cat/000000.jpg')
    image_suofang=cv2.resize(image, (200,200))
    rows, cols, chnl = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 60, 1)
    image_xuanzhuan = cv2.warpAffine(image, M, (cols, rows))
    image_fanzhuan1 = cv2.flip(image, 0)
    image_fanzhuan2 = cv2.flip(image, 1)
    image_fanzhuan3 = cv2.flip(image, -1)

    titles=['image','enlarge','rotated','x_flip','y_flip','xy_flip']
    images=[image,image_suofang,image_xuanzhuan,image_fanzhuan1,image_fanzhuan2,image_fanzhuan3]
    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.imshow(images[i])
        plt.title(titles[i])
    plt.show()
    #plt.subplot(2, 3, 1), plt.imshow(images[i])


def work3():
    b1=os.listdir(path_cat)
    for i in range(len(b1)):

        b1[i]=os.path.join(path_cat, b1[i])
        #b1[i]='F:/Yanjiusheng/Yan1_shangxueqi/新生训练/任务5/猫/%s'%b1[i]
        img = cv2.imread(b1[i],flags=1)
        name_cat='cat-%d'%i
        path=path_cat +'_g/%s.jpg' %name_cat
        #if not os.path.exists(path):
            #os.makedirs(path)
        cv2.imwrite(path, img)
    b2=os.listdir(path_dog)
    for i in range(len(b2)):
        b2[i]=os.path.join(path_dog, b2[i])
        img = cv2.imread(b2[i],1)
        name_dog="dog-%d"%i
        path=path_dog + '_g/%s.jpg' % name_dog
        cv2.imwrite(path, img)

if __name__ == '__main__':
    #work1()
    #work2()
    work3()

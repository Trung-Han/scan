import requests, os, json, sys, random
from pystyle import Colors, Colorate
from time import sleep
from datetime import datetime
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
tim = "\033[1;35m"
xanh = "\033[1;36m"
thanh = f'{do}[{trang}</>{do}] {trang}=> '
listToken = []
list_nv = []

def Server():
    response = requests.get('https://dhphuoc.click/api_key/server.php').json()
    if response['status'] == 'success': return 'LIVE' 
    else: return 'OFFLINE'

def Delay(value):
    while not(value <= 1):
        value -= 0.123
        print(f'''{trang}[{xanh}DHP07{trang}] [{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}] [{vang}X    {trang}]''', '               ', end = '\r')
        sleep(0.02)
        print(f'''{trang}[{xanh}DHP07{trang}] [{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}] [ {vang}X   {trang}]''', '               ', end = '\r')
        sleep(0.02)
        print(f'''{trang}[{xanh}DHP07{trang}] [{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}] [  {vang}X  {trang}]''', '               ', end = '\r')
        sleep(0.02)
        print(f'''{trang}[{xanh}DHP07{trang}] [{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}] [   {vang}X {trang}]''', '               ', end = '\r')
        sleep(0.02)
        print(f'''{trang}[{xanh}DHP07{trang}] [{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}] [    {vang}X{trang}]''', '               ', end = '\r')
        sleep(0.02)

def thanhngang(so):
    for i in range(so):
        print(trang+'-',end ='')
    print('')

def banner():
    os.system('cls' if os.name=='nt' else 'clear')
    print(f'''
            {xanh}██████╗ ██╗  ██╗██████╗  ██████╗ ███████╗
            {trang}██╔══██╗██║  ██║██╔══██╗██╔═████╗╚════██║
            {xanh}██║  ██║███████║██████╔╝██║██╔██║    ██╔╝
            {trang}██║  ██║██╔══██║██╔═══╝ ████╔╝██║   ██╔╝ 
            {xanh}██████╔╝██║  ██║██║     ╚██████╔╝   ██║  
            {trang}╚═════╝ ╚═╝  ╚═╝╚═╝      ╚═════╝    ╚═╝       ''')
    print(Colorate.Horizontal(Colors.white_to_blue,"         © Bản Quyền DHP07V2-TOOL ! Tool Gộp Siêu Lỏ !!!"))
    thanhngang(65)
    print(f'''{thanh}{luc}Admin{trang}: {vang}Đàm Hữu Phước
{thanh}{luc}Box Zalo{trang}: {do}https://zalo.me/g/ucvski448
{thanh}{luc}Web Thu Xu{trang}: {do}https://thucoin299.com/
{thanh}{luc}Web Tăng Tương Tác{trang}: {do}https://uplikesub.com/
{thanh}{luc}Bạn Đang Sử Dụng Tool{trang}: {vang}Tương Tác Chéo Facebook Token''')
    thanhngang(65)

class Facebook():
    def __init__(self, token):
        self.token = token
        
    def info(self):
        response = requests.get(f'https://dhphuoc.click/api/info.php?token={self.token}').json()
        return response
        
    def reaction(self, uid, type):
        response = requests.post(f'https://dhphuoc.click/api/camxuc.php?uid={uid}&type={type}&token={self.token}').json()
        return response
        
    def follow(self, uid):
        response = requests.post(f'https://dhphuoc.click/api/follow.php?uid={uid}&token={self.token}').json()
        return response

    def share(self, uid):
        response = requests.post(f'https://dhphuoc.click/api/share.php?uid={uid}&token={self.token}').json()
        return response
        
    def comment(self, uid, message):
        response = requests.post(f'https://dhphuoc.click/api/cmt.php?uid={uid}&message={message}&token={self.token}').json()
        return response
        
    def likepage(self, uid):
        response = requests.post(f'https://dhphuoc.click/api/page.php?uid={uid}&token={self.token}').json()
        return response

class TuongTacCheo():
    def __init__(self, token):
        try:
            self.session = requests.Session()
            self.response = self.session.post('https://tuongtaccheo.com/logintoken.php',headers={'Content-type': 'application/x-www-form-urlencoded'},data={'access_token': token})
            self.cookie = self.response.headers['Set-cookie']
            self.thongtin = self.response.json()
            self.headers = {
                'Host': 'tuongtaccheo.com',
                'accept': '*/*',
                'origin': 'https://tuongtaccheo.com',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                "cookie": self.cookie
            }
        except:
            pass

    def info(self):
        if self.thongtin['status'] == 'success':
            return self.thongtin
        else:
            return self.thongtin['mess']
        
    def cauhinh(self, id):
        response = self.session.post('https://tuongtaccheo.com/cauhinh/datnick.php',headers=self.headers, data={'iddat[]': id, 'loai': 'fb', }).text
        if response == '1':
            return {'status': "success", 'id': id}
        else:
            return {'error': 200}
        
    def getjob(self, nv):
        response = self.session.get(f'https://tuongtaccheo.com/kiemtien/{nv}/getpost.php',headers=self.headers)
        return response
    
    def nhanxu(self, id, nv):
        xu_truoc = self.session.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
        response = self.session.post(f'https://tuongtaccheo.com/kiemtien/{nv}/nhantien.php', headers=self.headers, data={'id': id}).json()
        xu_sau = self.session.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
        if 'mess' in response and int(xu_sau) > int(xu_truoc):
            parts = response['mess'].split()
            msg = parts[-2]
            return {'status': "success", 'msg': '+'+msg+' Xu', 'xu': xu_sau} 
        else:
            return {'error': response}

def addtoken():
    i = 0
    while True:
        i += 1
        token = input(f'{thanh}{luc}Nhập Token Facebook Số{vang} {i}{trang}: {vang}')
        if token == '' and i != 1:
            break
        try:
            fb = Facebook(token)
            info = fb.info()
            if info.get('status') == 'success':
                name = info['name']
                print(f'{thanh}{luc}Tên Facebook: {vang}{name}')
                thanhngang(65)
                listToken.append(token)
            else:
                print(f'{do}Token Facebook Die ! Vui Lòng Nhập Lại !!!')
                i -= 1
        except:
            print(f'{do}Token Facebook Die ! Vui Lòng Nhập Lại !!!')
            i -= 1

banner()
server = Server()
if server != 'LIVE': print(f'{thanh}{luc}Trạng Thái Server{trang}: {trang}[{do}{server}{trang}]'); os.remove(sys.argv[0]); sys.exit(); quit()
else:
    banner()
    if os.path.exists(f'tokenttcfb.json') == False:
        while True:
            token = input(f'{thanh}{luc}Nhập Access_Token TTC{trang}:{vang} ')
            print('\033[1;32mĐang Xữ Lý...','     ',end='\r')
            ttc = TuongTacCheo(token)
            checktoken = ttc.info()
            if checktoken.get('status') == 'success':
                users, xu = checktoken['data']['user'], checktoken['data']['sodu']
                print(f"{luc}Đăng Nhập Thành Công")
                with open('tokenttcfb.json','w') as f:
                    json.dump([token+'|'+users],f)
                    break
            else:
                print(f'{do}Đăng Nhập Thất Bại')
    else:
        token_json = json.loads(open('tokenttcfb.json','r').read())
        stt_token = 0
        for tokens in token_json:
            if len(tokens) > 5:
                stt_token += 1
                print(f'{thanh}{luc}Account {do}[{vang}{stt_token}{do}] {luc}Để Chạy Tài Khoản: {vang}{tokens.split('|')[1]}')
        thanhngang(65)
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Chọn Acc Tương Tác Chéo Để Chạy Tool')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Access_Token Tương Tác Chéo Mới')
        thanhngang(65)
        while True:
            chon = input(f'{thanh}{luc}Nhập: {vang}')
            thanhngang(65)
            if chon == '1':
                while True:
                    try:
                        tokenttcfb = int(input(f'{thanh}{luc}Nhập Số Acc: {vang}'))
                        thanhngang(65)
                        ttc = TuongTacCheo(token_json[tokenttcfb - 1].split("|")[0])
                        checktoken = ttc.info()
                        if checktoken.get('status') == 'success':
                            users, xu = checktoken['data']['user'], checktoken['data']['sodu']
                            print(f"{luc}Đăng Nhập Thành Công")
                            break
                        else:
                            print(f'{do}Đăng Nhập Thất Bại')
                    except:
                        print(f'{do}Số Acc Không Tồn Tại')
                break
            elif chon == '2':
                while True:
                    token = input(f'{thanh}{luc}Nhập Access_Token TTC{trang}: {vang}')
                    print('\033[1;32mĐang Xữ Lý...','     ',end='\r')
                    ttc = TuongTacCheo(token)
                    checktoken = ttc.info()
                    if checktoken.get('status') == 'success':
                        users, xu = checktoken['data']['user'], checktoken['data']['sodu']
                        print(f"{luc}Đăng Nhập Thành Công")
                        token_json.append(token+'|'+users)
                        with open('tokenttcfb.json','w') as f:
                            json.dump(token_json,f)
                        break
                    else:
                        print(f'{do}Đăng Nhập Thất Bại')
                break
            else:
                print(f'{do}Vui Long Nhập Chính Xác ')
    banner()
    if os.path.exists(f'tokenfb-ttc.json') == False:
        addtoken()
        with open('tokenfb-ttc.json','w') as f:
            json.dump(listToken, f)
    else:
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Sử Dụng Token Facebook Đã Lưu')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Token Facebook Mới')
        thanhngang(65)
        chon = input(f'{thanh}{luc}Nhập{trang}: {vang}')
        thanhngang(65)
        while True:
            if chon == '1':
                print(f'{luc}Đang Lấy Dữ Liệu Đã Lưu ','          ',end='\r')
                sleep(1)
                listToken = json.loads(open('tokenfb-ttc.json', 'r').read())
                break
            elif chon == '2':
                addtoken()
                with open('tokenfb-ttc.json','w') as f:
                    json.dump(listToken, f)
                break
            else:
                print(f'{do}Vui Lòng Nhập Đúng !!!')
    banner()
    print(f'{thanh}{luc}Tên Tài Khoản{trang}: {vang}{users}')
    print(f'{thanh}{luc}Xu Hiện Tại{trang}: {vang}{str(format(int(xu),","))}')
    print(f'{thanh}{luc}Số Token Facebook{trang}: {vang}{len(listToken)}')
    thanhngang(65)
    print(f'{thanh}{luc}Nhập {do}[{vang}1{do}]{luc} Để Chạy Nhiệm Vụ Like Vip')
    print(f'{thanh}{luc}Nhập {do}[{vang}2{do}]{luc} Để Chạy Nhiệm Vụ Like Thường')
    print(f'{thanh}{luc}Nhập {do}[{vang}3{do}]{luc} Để Chạy Nhiệm Vụ Cảm Xúc Vip')
    print(f'{thanh}{luc}Nhập {do}[{vang}4{do}]{luc} Để Chạy Nhiệm Vụ Cảm Xúc Thường')
    print(f'{thanh}{luc}Nhập {do}[{vang}5{do}]{luc} Để Chạy Nhiệm Vụ Share')
    print(f'{thanh}{luc}Nhập {do}[{vang}6{do}]{luc} Để Chạy Nhiệm Vụ Follow')
    print(f'{thanh}{luc}Nhập {do}[{vang}7{do}]{luc} Để Chạy Nhiệm Vụ Comment')
    print(f'{thanh}{luc}Nhập {do}[{vang}8{do}]{luc} Để Chạy Nhiệm Vụ Like Page')
    print(f'{thanh}{luc}Có Thể Chọn Nhiều Nhiệm Vụ {do}({vang}VD: 123...{do})')
    thanhngang(65)
    nhiemvu = str(input(f'{thanh}{luc}Nhập Số Để Chọn Nhiệm Vụ{trang}: {vang}'))
    for x in nhiemvu:
        list_nv.append(x)
    list_nv = [x for x in list_nv if x in ['1','2','3','4','5','6','7','8','9']]
    while(True):
        try:
            delay = int(input(f'{thanh}{luc}Nhập Delay Job{trang}: {vang}'))
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')
    while(True):
        try:
            JobbBlock = int(input(f'{thanh}{luc}Sau Bao Nhiêu Nhiệm Vụ Chống Block{trang}: {vang}'))
            if JobbBlock <= 1:
                print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')
    while(True):
        try:
            DelayBlock = int(input(f'{thanh}{luc}Sau {vang}{JobbBlock} {luc}Nhiệm Vụ Nghỉ Bao Nhiêu Giây{trang}: {vang}'))
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')
    while(True):
        try:
            JobBreak = int(input(f'{thanh}{luc}Sau Bao Nhiêu Nhiệm Vụ Chuyển Acc{trang}: {vang}'))
            if JobBreak <= 1:
                print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
            break
        except:
            print(f'{do}Vui Lòng Nhập Số')
    runidfb = input(f'{thanh}{luc}Bạn Có Muốn Ẩn Id Facebook Không? {do}({vang}y/n{do}){luc}: {vang}')
    thanhngang(65)
    stt = 0
    totalxu = 0
    xuthem = 0
    while True:
        if len(listToken) == 0:
            print(f'{do}Đã Xóa Tất Cả Token, Vui Lòng Nhập Lại !!!')
            addtoken()
            with open('tokenfb-ttc.json','w') as f:
                json.dump(listToken, f)
        for token in listToken:
            JobError, JobSuccess, JobFail = 0, 0, 0
            fb = Facebook(token)
            info = fb.info()
            if info.get('status') == 'success':
                namefb = info['name']
                idfb = str(info['id'])
                idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if runidfb.upper() =='Y' else idfb
            else:
                print(f'{do}Token Facebook Die ! Đã Xóa Ra Khỏi List !!!')
                listToken.remove(token)
                break
            cauhinh = ttc.cauhinh(idfb)
            if cauhinh.get('status') == 'success':
                print(f'{luc}Id Facebook{trang}: {vang}{idrun}{do} | {luc}Tên Tài Khoản{trang}: {vang}{namefb}')
            else:
                print(f'{luc}Chưa Cấu Hình Id Facebook{trang}: {vang}{idfb}{do} | {luc}Tên Tài Khoản{trang}: {vang}{namefb}')
                listToken.remove(token)
                break
            list_nv_default = list_nv.copy()
            while True:
                random_nv = random.choice(list_nv)
                if random_nv == '1': fields = 'likepostvipcheo'
                if random_nv == '2': fields = 'likepostvipre'
                if random_nv == '3': fields = 'camxucvipcheo'
                if random_nv == '4': fields = 'camxuccheo'
                if random_nv == '5': fields = 'sharecheo'
                if random_nv == '6': fields = 'subcheo'
                if random_nv == '7': fields = 'cmtcheo'
                if random_nv == '8': fields = 'likepagecheo'
                chuyen = False
                try:
                    getjob = ttc.getjob(fields)
                    if "idpost" in getjob.text or "idfb" in getjob.text:
                        print(luc+f" Đã Tìm Thấy {len(getjob.json())} Nhiệm Vụ {fields.title()}       ",end = "\r")
                        for x in getjob.json():
                            nextDelay = False
                            if random_nv == "1": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE"); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = 'LIKE'; id = x['idpost']
                            if random_nv == "2": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], "LIKE"); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = 'LIKE'; id = x['idpost']
                            if random_nv == "3": fb.reaction(x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb'], x['loaicx']); id_ = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']; type = x['loaicx']; id = x['idpost']
                            if random_nv == "4": fb.reaction(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], x['loaicx']); type = x['loaicx']; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                            if random_nv == "5": fb.share(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'SHARE'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                            if random_nv == "6": fb.follow(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'FOLLOW'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                            if random_nv == "7": fb.comment(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost'], json.loads(x["nd"])[0]); type = 'COMMENT'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                            if random_nv == "8": fb.likepage(x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']); type = 'LIKEPAGE'; id = x['idpost']; id_ = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                            nhanxu = ttc.nhanxu(id, fields)
                            if nhanxu.get('status') == 'success':
                                nextDelay, msg, xu, JobFail, timejob = True, nhanxu['msg'], nhanxu['xu'], 0, datetime.now().strftime('%H:%M:%S')
                                xutotal = msg.replace(' Xu','')
                                totalxu += int(xutotal)
                                stt+=1
                                JobSuccess += 1
                                print(f'{do}| {vang}{stt}{do} | {xanh}{timejob}{do} | {vang}{type.upper()}{do} | {trang}{id_}{do} | {vang}{msg}{do} | {luc}{str(format(int(xu),","))}')
                                if stt % 10 == 0:
                                    print(f'{trang}[{luc}Total Cookie Facebook: {vang}{len(listToken)}{trang}] [{luc}Total Coin: {vang}{str(format(int(totalxu),","))}{trang}] [{luc}Tổng Xu: {vang}{str(format(int(xu),","))}{trang}]')
                            else:
                                JobFail += 1
                                print(f'{trang}[{do}{JobFail}{trang}] {trang}[{do}ERROR{trang}] {trang}{id_}','            ',end="\r")
                            
                            if JobFail >= 20:
                                check = fb.info()
                                if 'error' in check:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Die Token, Đã Xoá Khỏi List')
                                    listToken.remove(token)
                                    chuyen = True
                                    break
                                else:
                                    print(do+f'Tài Khoản {vang}{namefb} {do}Đã Bị Block {fields.upper()}')
                                    JobFail = 0
                                    if nhiemvu in list_nv:
                                        list_nv.remove(nhiemvu)
                                    if list_nv:
                                        nhiemvu = random.choice(list_nv)
                                    else:
                                        print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Block Tất Cả Tương Tác')
                                        listToken.remove(token)
                                        chuyen = True
                                        list_nv = list_nv_default.copy()
                                    break

                            if JobSuccess != 0 and JobSuccess % int(JobBreak) == 0:
                                chuyen = True
                                break

                            if nextDelay == True:
                                if stt % int(JobbBlock)==0:
                                    Delay(DelayBlock)
                                else:
                                    Delay(delay)

                        if chuyen == True:
                            break
                    else:
                        if 'error' in getjob.text:
                            if getjob.json()['countdown']:
                                print(f'{do}Tiến Hành Get Job {fields.upper()}, COUNTDOWN: {str(round(getjob.json()["countdown"], 3))}'   ,end="\r")
                                sleep(1)
                                Delay(getjob.json()['countdown'])
                            else:
                                print(do+getjob.json()['error']+'          ',end="\r")
                                sleep(1)
                                Delay(getjob.json()['countdown'])
                except:
                    pass
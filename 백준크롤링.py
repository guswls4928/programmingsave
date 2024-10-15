from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pymysql
import time
import requests


def init():
    global con
    con = pymysql.connect(
    host='localhost',
    user='dna',
    password='dnalinux12345',
    db='acmicpc',
    charset='utf8',
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
    )
    
    global cur
    cur = con.cursor()
    
    sql_create()
    
    global acmicpc_list
    acmicpc_list = [['아이디', '처음 푼 문제', '최종 푼 문제']]
    
    sql = "SELECT * FROM USERLIST"
    cur.execute(sql)
    rows = cur.fetchall()
    for i in rows:
        res = [i['Id'], i['Solved_problem'], i['Current_sp']]
        acmicpc_list.append(res)
        
    global level_list
    level_list = ['Unrated', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']


def addlist(infolist):
    id = infolist[0].text
    solved_problem = infolist[1].text
    
    for i in range(len(acmicpc_list)):
        if(acmicpc_list[i][0] == id):
            acmicpc_list[i][2] = solved_problem
            return True
    
    acmicpc_list.append([id, solved_problem, solved_problem])


def userlist_extrac(person):
    url = "https://www.acmicpc.net/group/ranklist/17406"
    driver.get(url)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    main = soup.find("div", {"class": "table-responsive"})
    body = main.find("tbody")
    allinfo = body.find_all("tr")
    
    for link in allinfo:
        infolist = link.find_all("a")
        if(person == 'all'):
            addlist(infolist)
        elif(infolist[0].text == person):
            addlist(infolist)


def sql_create():
    try:
        sql = "SELECT * FROM USERLIST"
        cur.execute(sql)
    
    except:
        sql = """CREATE TABLE USERLIST(
                Id VARCHAR(50) NOT NULL,
                Solved_problem INT NOT NULL,
                Current_sp INT NOT NULL,
                PRIMARY KEY(Id));
                """
        cur.execute(sql)
        
        sql = """CREATE TABLE SOLVE_LIST(
                Id VARCHAR(50) NOT NULL,
                Init TEXT,
                Current TEXT,
                PRIMARY KEY(Id),
                FOREIGN KEY(Id) REFERENCES USERLIST(Id));
            """
        cur.execute(sql)
        
        sql = """CREATE TABLE PLIST(
                Id INT NOT NULL,
                Difficult VARCHAR(8),
                Tier INT,
                PRIMARY KEY(Id));
            """
        cur.execute(sql)


def problem_extrac(id):
    url = "https://www.acmicpc.net/user/{}".format(id)
    driver.get(url)
    print(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    main = soup.find("div", {"class": "problem-list"})
    allinfo = main.find_all("a")
    res = []
    
    for i in allinfo:
        res.append(i.text)
    
    time.sleep(3)
    
    return res


def table_control(person):
    for infolist in acmicpc_list[1:]:
        id = infolist[0]
        if(person == "all"):
            pass
        elif(person != id):
            continue
        
        solved_problem = infolist[1]
        current_sp = infolist[2]
        solve_list = problem_extrac(id)
        solve_list = ' '.join(s for s in solve_list)
        
        sql = "SELECT * FROM USERLIST WHERE Id='{}'".format(id)
        cur.execute(sql)
        res = cur.fetchall()
        try:
            id = res[0]['Id']
            sql = "UPDATE USERLIST SET Current_sp={} WHERE Id='{}'".format(current_sp,id)
            cur.execute(sql)
            sql = "UPDATE SOLVE_LIST SET Current='{}' WHERE Id='{}'".format(solve_list,id)
            cur.execute(sql)
        
        except:
            sql = "INSERT INTO USERLIST VALUES('{}',{},{})".format(id,solved_problem,solved_problem)
            cur.execute(sql)
            sql = "INSERT INTO SOLVE_LIST VALUES('{}','{}','{}')".format(id,solve_list,solve_list)
            cur.execute(sql)
    
    url = "https://www.acmicpc.net/group/ranklist/17406"
    driver.get(url)

#2606 1931 1086 10026 1927 2579 1541 1764
def member_manage(person):
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    userlist_extrac(person)
    
    table_control(person)
    
def member_problem_add(person, problem):
    for infolist in acmicpc_list[1:]:
        id = infolist[0]
        if(person != id):
            continue
        
        problem_list = set(map(int, problem.split()))
        fixed_num = infolist[1] - len(problem_list)
        
        sql = f"SELECT Init FROM SOLVE_LIST Where Id='{id}'"
    
        cur.execute(sql)
        
        res = cur.fetchall()
        
        init_data = set(map(int, res[0]['Init'].split()))
        fixed_data = [str(num) for num in (init_data - problem_list)]
        sql = f"UPDATE USERLIST SET Solved_problem={fixed_num} WHERE Id='{id}'"
        cur.execute(sql)
        sql = f"UPDATE SOLVE_LIST SET Init='{' '.join(s for s in fixed_data)}' WHERE Id='{id}'"
        cur.execute(sql)

def solveac_update():
    sql = "SELECT Current FROM SOLVE_LIST"
    
    cur.execute(sql)
    
    raws = cur.fetchall()
    
    solve_list = []
    
    for i in raws:
        try:
            res = list(map(int, i['Current'].split(' ')))
            solve_list = solve_list + res
        
        except:
            continue
    
    solve_list = list(set(solve_list))
    
    url = "https://solved.ac/api/v3/problem/lookup"

    for i in range(0, len(solve_list), 100):
        try:
            total = ','.join(map(str, solve_list[i:i+100]))
        
        except:
            total = ','.join(map(str, solve_list[i:]))
        
        querystring = {"problemIds":"{}".format(total)}
        
        headers = {"Accept": "application/json"}
        
        response = requests.get(url,headers=headers,params=querystring)
        
        res = response.json()
        
        for i in res:
            problemId = i['problemId']
            temp = i['level']
            
            if(not temp): continue
            
            level = {}
            level['difficult'] = level_list[temp//5 + 1] if temp%5 else level_list[temp//5]
            level['tier'] = 6 - temp%5 if temp%5 else 1
            
            try:
                sql = "INSERT INTO PLIST VALUES({},'{}',{})".format(problemId, level['difficult'], level['tier'])
                cur.execute(sql)
            except:
                pass


def query_ranking_by_solved_problem_count():
    sql = "SELECT * FROM USERLIST"
    
    cur.execute(sql)
    
    raws = cur.fetchall()
    
    ranking = {}
    for i in raws:
        id = i['Id']
        first = i['Solved_problem']
        current = i['Current_sp']
        res = current - first
        ranking[id] = res
    ranking = sorted(ranking.items(), key=lambda x:x[1], reverse=True)
    for i in ranking:
        if(i[1] == 0): break
        print(i)
        


def calculate_difficulty_weighted_score(req):
    high = {'Difficult':'Unrated', 'Tier':6, 'cnt':0}
    for i in req:
        sql = f"SELECT Difficult, Tier FROM PLIST WHERE Id = '{i}'"
        
        cur.execute(sql)
        
        raw = cur.fetchall()
        raw = raw[0]
        
        if(level_list.index(raw['Difficult']) > level_list.index(high['Difficult'])):
            high['Difficult'] = raw['Difficult']
            high['Tier'] = raw['Tier']
            high['cnt'] = 1
        elif(raw['Tier'] < high['Tier']):
            high['Tier'] = raw['Tier']
            high['cnt'] = 1
        elif(raw['Tier'] == high['Tier']):
            high['cnt'] += 1

    return high


def query_ranking_by_difficulty_weighted_score():
    sql = "SELECT * FROM SOLVE_LIST"  
    
    cur.execute(sql)
    
    raws = cur.fetchall()
    
    ranking = {}
    for i in raws:
        id = i['Id']
        first = []
        first = list(map(int, i['Init'].split()))
        current = list(map(int, i['Current'].split()))
        solve_list = [x for x in current if x not in first]
        ranking[id] = calculate_difficulty_weighted_score(solve_list)
    
    ranking = sorted(ranking.items(), key=lambda x:(-level_list.index(x[1]['Difficult']), x[1]['Tier'], -x[1]['cnt']))
    for i in ranking:
        if(i[1]['cnt'] == 0): break
        print(i)

def unrated_problem_count(req):
    cnt = 0
    for i in req:
        sql = f"SELECT Difficult FROM PLIST WHERE Id = '{i}'"
        
        cur.execute(sql)
        
        raw = cur.fetchall()
        raw = raw[0]
        
        if(raw['Difficult'] == 'Unrated'):
            cnt += 1
    
    return cnt

def query_ranking_by_solved_unrated_problem_count():
    sql = "SELECT * FROM SOLVE_LIST"
    
    cur.execute(sql)
    
    raws = cur.fetchall()
    
    ranking = {}
    for i in raws:
        id = i['Id']
        first = list(map(int, i['Init'].split()))
        current = list(map(int, i['Current'].split()))
        solve_list = [x for x in current if x not in first]
        ranking[id] = unrated_problem_count(solve_list)
        
    ranking = sorted(ranking.items(), key=lambda x:x[1], reverse=True)
    for i in ranking:
        if(i[1] == 0): break
        print(i)

def query(select_query):
    if select_query == '1':
        query_ranking_by_solved_problem_count()
    
    elif select_query == '2':
        query_ranking_by_difficulty_weighted_score()
        
    elif select_query == '3':
        query_ranking_by_solved_unrated_problem_count()
        
    elif select_query == '4':
        return
    
    else:
        print("올바르지 않은 입력")
        return


def change():
    for infolist in acmicpc_list[1:]:
        id = infolist[0]
        
        sql = f"SELECT Current_sp FROM USERLIST WHERE id='{id}'"
        cur.execute(sql)
        raw = cur.fetchall()
        sql = f"UPDATE USERLIST SET Solved_problem={raw[0]['Current_sp']} WHERE Id='{id}'"
        cur.execute(sql)
        
        sql = f"SELECT Current FROM SOLVE_LIST WHERE id='{id}'"
        cur.execute(sql)
        raw = cur.fetchall()
        sql = f"UPDATE SOLVE_LIST SET Init='{raw[0]['Current']}' WHERE Id='{id}'"
        cur.execute(sql)
    

def main():
    init()
    
    while(1):
        print("""
---------------------------------------------------------------------
수행할 작업을 선택하시오.
1. 멤버 관리
2. 문제 업데이트
3. 쿼리 실행
4. 초기화
5. 종료
---------------------------------------------------------------------
              """)
        cmd = input(">>")
        
        if(cmd == '1'):
            print("""
---------------------------------------------------------------------
수행할 작업을 선택하시오.
1. 멤버 추출
2. 멤버 문제 컨트롤
---------------------------------------------------------------------
              """)
            cmd = input(">>")
            if(cmd == '1'):
                print("""
---------------------------------------------------------------------
추출할 사람의 id를 입력하시오.
모두를 선택할 겨우 all
---------------------------------------------------------------------
                    """)
                person = input(">>")
                member_manage(person)
            elif(cmd == '2'):
                print("""
---------------------------------------------------------------------
컨트롤할 유저의 id를 입력하시오.
---------------------------------------------------------------------
                    """)
                person = input(">>")
                print("""
---------------------------------------------------------------------
추가할 문제 리스트를 띄어쓰기로 구분해 입력하시오.
---------------------------------------------------------------------
                    """)
                problem = input(">>")
                
                member_problem_add(person, problem)
        
        elif(cmd == '2'):
            solveac_update()
            print('업데이트 완료')
        
        elif(cmd == '3'):
            print("""
---------------------------------------------------------------------
실행할 쿼리를 선택하시오.
1. 많이 푼 순위
2. 어려운 문제 푼 순위
3. Unrated 문제 푼 순위
---------------------------------------------------------------------
                  """)
            select_query = input(">>")
            query(select_query)
        
        elif(cmd == '5'):
            print('정상적으로 종료되었습니다.')
            con.close()
            return
        
        elif(cmd == '4'):
            change()
            
        else:
            print('올바르지 않은 입력')
    
main()
        

"""
cd C:\Program Files\Google\Chrome\Application
chrome.exe --remote-debugging-port=9222 --user-data-dir="c:/chrometemp"
netstat -ano | findstr 9222
"""
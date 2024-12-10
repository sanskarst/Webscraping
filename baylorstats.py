from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

webpages = [
    'https://cfbstats.com/2024/team/51/index.html',
    'https://cfbstats.com/2023/team/51/index.html',
    'https://cfbstats.com/2022/team/51/index.html',
    'https://cfbstats.com/2021/team/51/index.html',
    'https://cfbstats.com/2020/team/51/index.html',
    'https://cfbstats.com/2019/team/51/index.html',
    'https://cfbstats.com/2018/team/51/index.html',
    'https://cfbstats.com/2017/team/51/index.html',
    'https://cfbstats.com/2016/team/51/index.html',
]

stats = {
    'Scoring Points Per Game': {'max':{'value':-float('inf'),'team': None},'min':{'value':float('inf'),'team': None}},
    'Passing Yards': {'max':{'value':-float('inf'),'team': None},'min':{'value':float('inf'),'team': None}},
    'Third Down Conversion %': {'max':{'value':-float('inf'),'team': None},'min':{'value':float('inf'),'team': None}},
    'Field Goal %': {'max':{'value':-float('inf'),'team': None},'min':{'value':float('inf'),'team': None}}

}

rivalteam, attendance  = [], {}

opponentrows = range(35,48)

def removerank(opponentname):
    for i in range(26):
        opponentname = opponentname.replace(str(i),'')
        opponentname = opponentname.replace('@ ','')
        opponentname = opponentname.replace('+ ','')
        opponentname = opponentname.replace(' ','')
    return opponentname

for x in webpages:
    page = urlopen(x)
    soup = BeautifulSoup(page, 'html.parser')
    statrows = soup.findAll('tr')
    title = soup.title
    sprgrow = statrows[1].findAll('td')
    pyrow = statrows[8].findAll('td')
    thirdrow = statrows[22].findAll('td')
    fgrow = statrows[28].findAll('td')
    spg  = float(sprgrow[1].text)
    py  = float(pyrow[1].text)
    thirddown  = float(thirdrow[1].text.replace("%",""))
    fg  = float(fgrow[1].text.replace("%",""))
    for row in opponentrows:
        try:
            if row >= len(statrows):
                continue
            antirow = statrows[row].findAll('td')
            opponentname = antirow[1].text.strip()
            opponentattendance = float(antirow[4].text.replace(',',''))
            
            if removerank(opponentname) in attendance:
                attendance[removerank(opponentname)] += opponentattendance
            else:
                attendance[removerank(opponentname)] = opponentattendance
            
        except Exception as e:
            continue        
            

    for stat, value in [("Scoring Points Per Game", spg), ("Passing Yards", py), ("Third Down Conversion %", thirddown), ("Field Goal %", fg)]:
        if value > stats[stat]["max"]["value"]:
            stats[stat]["max"] = {"value": value, "team": title}
        if value < stats[stat]["min"]["value"]:
            stats[stat]["min"] = {"value": value, "team": title}


for stat, data in stats.items():
    print(f"{stat.upper()}:")
    print(f"  Best: {data['max']['value']} From the {data['max']['team'].text.replace("cfbstats.com - ", '').replace(' Baylor Bears','')} Season")
    print(f"  Worst: {data['min']['value']} From the {data['min']['team'].text.replace("cfbstats.com - ", '').replace(' Baylor Bears','')} Season")

rivalteam = sorted(attendance.items(), key= lambda x: x[1],reverse=True)

top5rivals = rivalteam[:5]

from plotly.graph_objs import Bar
from plotly import offline
x = [team for team, _ in top5rivals]
y = [attendance for _, attendance in rivalteam]

graphdata = [
    {
        'type': 'bar',
        'x': x,
        'y': y,
        'marker':{
            'color': 'rgb(40,175,0)',
            'line': {'width': 1.5, 'color': 'rgb(40,175,0)'},
        },
        'opacity': 0.6

        }
]

my_layout = {
    'title': 'Biggest Rivalry Based on Attendance',
    'xaxis': {'title': 'Teams'},
    'yaxis': {'title': 'Attendance'},
    'plot_bgcolor': 'rgba(255, 240, 51, 1)'
}

fig = {'data': graphdata, 'layout': my_layout}

offline.plot(fig, filename= 'rivalryattendance.html')



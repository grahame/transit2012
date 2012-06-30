# Source:
# For the calculation of the contact times is made use of the algorithm and the elements of Meeus Jean, "Transit" (Willmann-Bell, 1989).
# The program code for calculating the contact time is based on code by Franco Martinelli and edited by Steven M. of Roode.
# The determination of the solar parallax goes back to the principle that in 1716 by Edmond Halley was formulated.

import math, sys, csv, json
from pprint import pprint
from itertools import combinations

degrees  = 180/math.pi
rad =  1/degrees

# 2004
elements_2004 = {
        'T0' : 8,
        '11' : -229.4542,
        '12' : 233.6932,
        '13' : 0.01512,
        '14' : -0.000079,
        '21' : -589.2948,
        '22' : -56.9904,
        '23' : 0.06953,
        '24' : 0.000071,
        '31' : 22.8860,
        '32' : 0.0036,
        '33' : -0.00001,
        '41' : 300.2378,
        '42' : 14.9980,
        '43' : 0.0,
        '51' : 22.7223,
        '52' : -0.0122,
        '53' : 0.0,
        '61' : 300.1687,
        '62' : 15.0684,
        '63' : 0.0,
        '71' : 1.0150844,
        '72' : 0.0000053,
        '73' : 0.0,
        '81' : 0.2888829,
        '82' : 0.0000006,
        '83' : 0.00000027
    }

elements_2012 = {
        'T0':2,
        '11':253.0583,
        '12':232.6966,
        '13':0.01583,
        '14':-0.000080,
        '21':507.0395,
        '22':-60.4263,
        '23':0.06675,
        '24':0.000076,
        '31':22.6775,
        '32':0.0042,
        '33':-0.00001,
        '41':210.3335,
        '42':14.9981,
        '43':0.0,
        '51':22.8183,
        '52':-0.0126,
        '53':0.0,
        '61':210.4097,
        '62':15.0682,
        '63':0.0,
        '71':1.0147447,
        '72':0.0000056,
        '73':0.0,
        '81':0.2887038,
        '82':0.0000011,
        '83':0.00000027
        }

def calculate_parallax(e, obs1, obs2):
    time=[0.] * 5
    elevation=[0.] * 5
    angle=[0.] * 5
    afstand=[0.] * 5

    def rhocosfi(Lat,Hgt):
        U=math.atan(math.tan(rad*Lat)*0.99664719)
        rhocfi=math.cos(U)+(Hgt/6378140)*math.cos(Lat*rad)
        return rhocfi

    def rhosinfi(Lat,Hgt):
        U=math.atan(math.tan(rad*Lat)*0.99664719)
        rhosfi=0.99664719*math.sin(U)+(Hgt/6378140)*math.sin(Lat*rad)
        return rhosfi

    def Sgn(n):
        if n < 0:
            return -1
        else:
            return 1

    def CornerRounding(a):
        I=math.floor(abs(a))
        F=abs(a)-I
        R=I%360
        if Sgn(a) > 0:
            return R+F
        else:
            return 360-(R+F)
        return Ag

    def FormatLD(afs):
        return (math.floor((afs)*1000))/1000

    def ElevationAzimuth(Lat,Decl,TA):
        TA=TA+360
        TA=CornerRounding(TA)
        if TA<180:
            AP=TA
        else:
            AP=360-TA
        D=math.sin(rad*Lat)*math.sin(rad*Decl)+math.cos(rad*Lat)*math.cos(rad*Decl)*math.cos(rad*AP)
        Alt=degrees*math.asin(D)
        D=(math.sin(rad*Decl)-math.sin(rad*Lat)*math.sin(rad*Alt))/(math.cos(rad*Lat)*math.cos(rad*Alt))
        Az=degrees*math.acos(D)
        if TA<180:
            Az=360-abs(Az)
        return Alt, Az

    def CalculateTime(e,Long,Lat,Par,Phase):
        Tau=0
        L=0
        fuso=0
        DET=67
        Hgt=10
        rsf=rhosinfi(Lat,Hgt)
        rcf=rhocosfi(Lat,Hgt)
        T=0
        for k in range(5):
            for rip in range(7):
                Xa=e['11']+e['12']*T+e['13']*(T*T)+e['14']*(T*T*T)
                Ya=e['21']+e['22']*T+e['23']*(T*T)+e['24']*(T*T*T)
                Xpa=e['12']+2*e['13']*T+3*e['14']*(T*T)
                Ypa=e['22']+2*e['23']*T+3*e['24']*(T*T)
                da=e['31']+e['32']*T+e['33']*(T*T)
                da=da*rad
                Ma=e['41']+e['42']*T+e['43']*(T*T)
                db=e['51']+e['52']*T+e['53']*(T*T)
                db=db*rad
                Mb=e['61']+e['62']*T+e['63']*(T*T)
                Ra=e['71']+e['72']*T+e['73']*(T*T)
                Dea=e['81']+e['82']*T+e['83']*(T*T)
                Ha=Ma-Long-0.00417807*DET
                Ha=rad*Ha
                Hb=Mb-Long-0.00417807*DET
                Hb=Hb*rad;	
                Zga=rsf*math.sin(da)+rcf*math.cos(Ha)*math.cos(da)
                Zgb=rsf*math.sin(db)+rcf*math.cos(Hb)*math.cos(db)
                Ra=Ra-Zga/23455
                Dea=Dea-Zgb/23455
                dx=-Par*rcf*((math.sin(Ha)/Ra)-(math.sin(Hb)/Dea))
                a=rsf*( (math.cos(da)/Ra) - (math.cos(db)/Dea) )
                b=-rcf*((math.sin(da)*math.cos(Ha))/Ra-(math.sin(db)*math.cos(Hb)/Dea))
                dy=Par*(a+b)
                dxp=-0.261*Par*rcf*(math.cos(Ha)/Ra-math.cos(Hb)/Dea)
                dyp=+0.261*Par*rcf*(math.sin(da)*math.sin(Ha)/Ra-math.sin(db)*math.sin(Hb)/Dea)
                Xa=Xa+dx
                Xpa=Xpa+dxp
                Ya=Ya+dy
                Ypa=Ypa+dyp
                sa=959.63/Ra
                sb=8.41/Dea
                if k == 0:
                    L=sa+sb
                elif k == 1:
                    L=sa-sb
                elif k == 2:
                    L=sa-sb
                elif k == 3:
                    L=sa-sb
                elif k == 4:
                    L=sa+sb
                n2=Xpa*Xpa+Ypa*Ypa
                n=math.sqrt(n2);	
                SM=(Xa*Ypa-Ya*Xpa)/(n*L)
                if ((SM*SM)>1) and (k!=3):
                    TC=9999
                if k == 0:
                    Tau=-(Xa*Xpa+Ya*Ypa)/n2-(L/n)*math.sqrt(1-SM*SM) 
                elif k == 1:
                    Tau=-((Xa*Xpa+Ya*Ypa)/n2)-((L/n)*math.sqrt(1-(SM*SM)))
                elif k == 2:
                    Tau=-((Xa*Xpa+Ya*Ypa)/n2)
                elif k == 3:
                    Tau=-((Xa*Xpa+Ya*Ypa)/n2)+((L/n)*math.sqrt(1-(SM*SM)))
                elif k == 4:
                    Tau=-((Xa*Xpa+Ya*Ypa)/n2)+((L/n)*math.sqrt(1-(SM*SM)))
                T=T+Tau
            TC=e['T0']+T+fuso
            TC=TC-DET/3600
            Alt, Az = ElevationAzimuth(Lat,da*degrees,Ha*degrees)
            ang=math.atan2(-Xa,Ya)
            if ang<0:
                ang=(ang+2*math.pi)
            time[k]=TC
            elevation[k]=Alt
            angle[k]=ang*degrees
            afstand[k]=math.sqrt((Xa*Xa)+(Ya*Ya))
        return time[Phase]

    assert(obs1.ctype == obs2.ctype)

    if obs1.ctype == "enter":
        fase = 1
    elif obs1.ctype == "left":
        fase = 3
    else:
        raise Exception("ctype invalid")
    time1=obs1.time
    time2=obs2.time
    waarneemverschil=time1-time2
    parzon=8.794148

    def calc_tm(obs):
        return CalculateTime(e,-obs.lng,obs.lat,parzon,fase)

    for n in range(5):
        timeA=calc_tm(obs1)
        timeB=calc_tm(obs2)
        rekenverschil=(timeA-timeB)
        parzon=((waarneemverschil/rekenverschil)*parzon)
    fout=((0.00278/waarneemverschil)*parzon)
    au=(math.floor(6378.14/((parzon/3600)*rad)))
    parallax = FormatLD(parzon)
    error=abs(FormatLD(fout))
    return au, parallax, error

class Observation:
    def __init__(self, doc_id, text, username, ctype, lat, lng, time, zone, time_source):
        self.doc_id = int(doc_id)
        self.text = text
        self.username = username
        self.ctype = ctype
        self.lat = float(lat)
        self.lng = float(lng)
        self.time = float(time) - float(zone)
        self.time_source = time_source

    def __repr__(self):
        secs = self.time * 3600.
        h = secs//3600
        secs -= h * 3600
        m = secs//60
        secs -= m * 60
        return "%s %s: %gN%gE %d:%d:%d `%s'" % (self.username, self.ctype[0], self.lat, self.lng, h, m, secs, self.text)

class Result:
    def __init__(self, obs1, obs2, res):
        self.obs1 = obs1
        self.obs2 = obs2
        self.lat = abs(obs1.lat - obs2.lat)
        self.au, self.parallax, self.error = res

    def __repr__(self):
        return "%s %s: %skm (%s %s)" % (self.obs1, self.obs2, self.au, self.parallax, self.error)

if __name__ == '__main__':
    year = sys.argv[1]
    data = sys.argv[2]

    if year == '2004':
        elements = elements_2004
    elif year == '2012':
        elements = elements_2012
    else:
        sys.exit(1)
    enter = []
    left = []
    with open(data) as fd:
        for row in csv.reader(fd):
            # later observations will override; this is good, people can correct typos
            o = Observation(*row)
            if o.ctype == "enter":
                enter.append(o)
            elif o.ctype == "left":
                left.append(o)
    def weed_dups(l):
        winning = {}
        l.sort(key=lambda o: o.doc_id)
        for o in l:
            winning[(o.username, o.lat, o.lng)] = o.doc_id
        winners = set(winning.values())
        r = []
        for obs in l:
            if obs.doc_id in winners:
                r.append(obs)
        return r
    enter = weed_dups(enter)
    left = weed_dups(left)

    def tweet_links(l):
        rv = []
        for obs in sorted(l, key=lambda obs: obs.time):
            rv.append([obs.username, 'https://twitter.com/%s/status/%s' % (obs.username, obs.doc_id)])
        return rv
    def pair_pick(l):
        for obs1, obs2 in combinations(l, 2):
            if abs(obs1.lat - obs2.lat) > 40:
                yield obs1, obs2
    results = []
    def calculate(it):
        for obs1, obs2 in it:
            try:
                res = Result(obs1, obs2, calculate_parallax(elements, obs1, obs2))
                results.append(res)
            except Exception as e:
                print("Exception with %s %s" % (obs1, obs2), file=sys.stderr)
                print(e, file=sys.stderr)
    calculate(pair_pick(enter))
    calculate(pair_pick(left))
    # averaging logic totally fell down, just use the best pair
    results = [t for t in results if t.au > 0 ]
    if len(results) > 0:
        best = max([t.lat for t in results])
        avg = [t.au for t in results if t.lat == best][0]
    else:
        avg = 0.0
    j = {}
    j['calculations'] = [str(t) for t in results]
    j['nenter'] = len(enter)
    j['nleft'] = len(left)
    j['result'] = avg
    j['enter_links'] = tweet_links(enter)
    j['left_links'] = tweet_links(left)
    json.dump(j, sys.stdout)



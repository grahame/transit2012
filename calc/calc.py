# Source:
# For the calculation of the contact times is made use of the algorithm and the elements of Meeus Jean, "Transit" (Willmann-Bell, 1989).
# The program code for calculating the contact time is based on code by Franco Martinelli and edited by Steven M. of Roode.
# The determination of the solar parallax goes back to the principle that in 1716 by Edmond Halley was formulated.

import math

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

def HMStoDec(h, m, s):
    return h + m/60. + s/3600.

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

def CalculateParallax(e):
    timeA1=HMStoDec(0, 0, 0)
    timeA2=HMStoDec(11, 3, 47)
    timeB1=HMStoDec(0, 0, 0)
    timeB2=HMStoDec(11, 10, 49)
    if timeA1>0:
        time1=timeA1
        time2=timeB1
        fase=1
    if timeA2>0:
        time1=timeA2
        time2=timeB2
        fase=3
    waarneemverschil=time1-time2
    parzon=8.794148
    for n in range(5):
        longitude=float("5.0")
        longitude=-longitude
        latitude=float("52.0")
        timeA=CalculateTime(e,longitude,latitude,parzon,fase)
        longitude=float("20.0")
        longitude=-longitude
        latitude=float("-30.0")
        timeB=CalculateTime(e,longitude,latitude,parzon,fase)
        rekenverschil=(timeA-timeB)
        parzon=((waarneemverschil/rekenverschil)*parzon)
    fout=((0.00278/waarneemverschil)*parzon)
    au=(math.floor(6378.14/((parzon/3600)*rad)))
    parallax = FormatLD(parzon)
    error=abs(FormatLD(fout))
    print(au)
    print(parallax)
    print(error)

if __name__ == '__main__':

CalculateParallax(elements_2004)



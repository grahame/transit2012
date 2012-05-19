# Source:
# For the calculation of the contact times is made ​​use of the algorithm and the elements of Meeus Jean, "Transit" (Willmann-Bell, 1989).
# The program code for calculating the contact time is based on code by Franco Martinelli and edited by Steven M. of Roode.
# The determination of the solar parallax goes back to the principle that in 1716 by Edmond Halley was formulated.

import math

degrees  = 180/math.pi
rad =  1/degrees

# 2004
ele_T0=8

ele11=-229.4542
ele12=233.6932
ele13=0.01512
ele14=-0.000079

ele21=-589.2948
ele22=-56.9904
ele23=0.06953
ele24=0.000071

ele31=22.8860
ele32=0.0036
ele33=-0.00001

ele41=300.2378
ele42=14.9980
ele43=0.0

ele51=22.7223
ele52=-0.0122
ele53=0.0

ele61=300.1687
ele62=15.0684
ele63=0.0

ele71=1.0150844
ele72=0.0000053
ele73=0.0

ele81=0.2888829
ele82=0.0000006
ele83=0.00000027

## 2012
## ele_T0=2
## 
## ele11=253.0583
## ele12=232.6966
## ele13=0.01583
## ele14=-0.000080
## 
## ele21=507.0395
## ele22=-60.4263
## ele23=0.06675
## ele24=0.000076
## 
## ele31=22.6775
## ele32=0.0042
## ele33=-0.00001
## 
## ele41=210.3335
## ele42=14.9981
## ele43=0.0
## 
## ele51=22.8183
## ele52=-0.0126
## ele53=0.0
## 
## ele61=210.4097
## ele62=15.0682
## ele63=0.0
## 
## ele71=1.0147447
## ele72=0.0000056
## ele73=0.0
## 
## ele81=0.2887038
## ele82=0.0000011
## ele83=0.00000027

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

def CalculateTime(Long,Lat,Par,Phase):
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
            Xa=ele11+ele12*T+ele13*(T*T)+ele14*(T*T*T)
            Ya=ele21+ele22*T+ele23*(T*T)+ele24*(T*T*T)
            Xpa=ele12+2*ele13*T+3*ele14*(T*T)
            Ypa=ele22+2*ele23*T+3*ele24*(T*T)
            da=ele31+ele32*T+ele33*(T*T)
            da=da*rad
            Ma=ele41+ele42*T+ele43*(T*T)
            db=ele51+ele52*T+ele53*(T*T)
            db=db*rad
            Mb=ele61+ele62*T+ele63*(T*T)
            Ra=ele71+ele72*T+ele73*(T*T)
            Dea=ele81+ele82*T+ele83*(T*T)
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
        TC=ele_T0+T+fuso
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

def CalculateParallax():
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
        print("args", longitude, latitude, parzon, fase)
        timeA=CalculateTime(longitude,latitude,parzon,fase)
        print("timeA %s"%timeA)
        longitude=float("20.0")
        longitude=-longitude
        latitude=float("-30.0")
        timeB=CalculateTime(longitude,latitude,parzon,fase)
        rekenverschil=(timeA-timeB)
        parzon=((waarneemverschil/rekenverschil)*parzon)
        print(parzon)
    fout=((0.00278/waarneemverschil)*parzon)
    au=(math.floor(6378.14/((parzon/3600)*rad)))
    parallax = FormatLD(parzon)
    error=abs(FormatLD(fout))
    print(au)
    print(parallax)
    print(error)

CalculateParallax()



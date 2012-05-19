
/* Source:
For the calculation of the contact times is made ​​use of the algorithm and the elements of Meeus Jean, "Transit" (Willmann-Bell, 1989).
The program code for calculating the contact time is based on code by Franco Martinelli and edited by Steven M. of Roode.
The determination of the solar parallax goes back to the principle that in 1716 by Edmond Halley was formulated.
*/

var degrees  = 180/Math.PI;
var rad =  1/degrees;

// 2004
var ele_T0=8

var ele11=-229.4542; 
var ele12=233.6932; 
var ele13=0.01512; 
var ele14=-0.000079;

var ele21=-589.2948; 
var ele22=-56.9904; 
var ele23=0.06953; 
var ele24=0.000071;

var ele31=22.8860; 
var ele32=0.0036; 
var ele33=-0.00001; 

var ele41=300.2378; 
var ele42=14.9980; 
var ele43=0.0; 

var ele51=22.7223; 
var ele52=-0.0122; 
var ele53=0.0; 

var ele61=300.1687; 
var ele62=15.0684; 
var ele63=0.0; 

var ele71=1.0150844; 
var ele72=0.0000053; 
var ele73=0.0; 

var ele81=0.2888829; 
var ele82=0.0000006; 
var ele83=0.00000027; 

/* 2012
var ele_T0=2

var ele11=253.0583; 
var ele12=232.6966; 
var ele13=0.01583; 
var ele14=-0.000080;

var ele21=507.0395; 
var ele22=-60.4263; 
var ele23=0.06675; 
var ele24=0.000076;

var ele31=22.6775; 
var ele32=0.0042; 
var ele33=-0.00001; 

var ele41=210.3335; 
var ele42=14.9981; 
var ele43=0.0; 

var ele51=22.8183; 
var ele52=-0.0126; 
var ele53=0.0; 

var ele61=210.4097; 
var ele62=15.0682; 
var ele63=0.0; 

var ele71=1.0147447; 
var ele72=0.0000056; 
var ele73=0.0; 

var ele81=0.2887038; 
var ele82=0.0000011; 
var ele83=0.00000027; 
*/

var time=new Array();
var elevation=new Array();
var angle=new Array();
var afstand=new Array();

function rhocosfi(Lat,Hgt)
{
    var U=Math.atan(Math.tan(rad*Lat)*0.99664719);
    var rhocfi=Math.cos(U)+(Hgt/6378140)*Math.cos(Lat*rad);
    return rhocfi;
}

function rhosinfi(Lat,Hgt)
{
    var U=Math.atan(Math.tan(rad*Lat)*0.99664719);
    var rhosfi=0.99664719*Math.sin(U)+(Hgt/6378140)*Math.sin(Lat*rad);
    return rhosfi;
}

function Sgn(n)
{	
    var S
    if (n<0){S=-1} else {S=1}
    return S
}

function CornerRounding(a)
{
    var Ag
    var Sgn
    if (a<0) {Sgn=-1} else {Sgn=1}
    var I=Math.floor(Math.abs(a))
    var F=Math.abs(a)-I
    var R=I%360
    if (Sgn>0) {Ag=R+F} else {Ag=360-(R+F)} 
    return Ag
}

function FormatLD(afs)
{
    var p=(Math.floor((afs)*1000))/1000
    return p
}

function HMStoDec(time)
{
    var eerstepunt=time.indexOf(".");
    var tweedepunt=time.indexOf(".",eerstepunt+1);
    var laatste=time.length;
    var hour=parseFloat(time.substring(0,eerstepunt));
    var minute=parseFloat(time.substring(eerstepunt+1,tweedepunt));
    var second=parseFloat(time.substring(tweedepunt+1,laatste+1));
    var decimaal=hour+(minute/60)+(second/3600);
    return decimaal
}

function ElevationAzimuth(Lat,Decl,TA)
{	
	TA=TA+360
	TA=CornerRounding(TA)
	if (TA<180) {AP=TA} else {AP=360-TA}
 	var D=Math.sin(rad*Lat)*Math.sin(rad*Decl)+Math.cos(rad*Lat)*Math.cos(rad*Decl)*Math.cos(rad*AP)
	Alt=degrees*Math.asin(D)
	var D=(Math.sin(rad*Decl)-Math.sin(rad*Lat)*Math.sin(rad*Alt))/(Math.cos(rad*Lat)*Math.cos(rad*Alt))
	Az=degrees*Math.acos(D)
	if (TA<180) {Az=360-Math.abs(Az)}
}

function CalculateTime(Long,Lat,Par,Phase)
{
    var Tau=0;
    var L=0;
    var fuso=0
    var DET=67
    var Hgt=10;
    var rsf=rhosinfi(Lat,Hgt);
    var rcf=rhocosfi(Lat,Hgt);
    var T=0;
    for (var k=1; k<=5; k++) { 
        for (var rip=1; rip<=6; rip++) {
            var Xa=ele11+ele12*T+ele13*(T*T)+ele14*(T*T*T);
            var Ya=ele21+ele22*T+ele23*(T*T)+ele24*(T*T*T);
            var Xpa=ele12+2*ele13*T+3*ele14*(T*T);
            var Ypa=ele22+2*ele23*T+3*ele24*(T*T);
            var da=ele31+ele32*T+ele33*(T*T);
            da=da*rad;
            var Ma=ele41+ele42*T+ele43*(T*T);
            var db=ele51+ele52*T+ele53*(T*T);
            db=db*rad;
            var Mb=ele61+ele62*T+ele63*(T*T);
            var Ra=ele71+ele72*T+ele73*(T*T);
            var Dea=ele81+ele82*T+ele83*(T*T);
            var Ha=Ma-Long-0.00417807*DET;
            Ha=rad*Ha;
            var Hb=Mb-Long-0.00417807*DET;
            Hb=Hb*rad;	
            var Zga=rsf*Math.sin(da)+rcf*Math.cos(Ha)*Math.cos(da);
            var Zgb=rsf*Math.sin(db)+rcf*Math.cos(Hb)*Math.cos(db);
            Ra=Ra-Zga/23455;
            Dea=Dea-Zgb/23455;
            var dx=-Par*rcf*((Math.sin(Ha)/Ra)-(Math.sin(Hb)/Dea));
            var a=rsf*( (Math.cos(da)/Ra) - (Math.cos(db)/Dea) );
            var b=-rcf*((Math.sin(da)*Math.cos(Ha))/Ra-(Math.sin(db)*Math.cos(Hb)/Dea));
            var dy=Par*(a+b);
            var dxp=-0.261*Par*rcf*(Math.cos(Ha)/Ra-Math.cos(Hb)/Dea);
            var dyp=+0.261*Par*rcf*(Math.sin(da)*Math.sin(Ha)/Ra-Math.sin(db)*Math.sin(Hb)/Dea);
            Xa=Xa+dx;
            Xpa=Xpa+dxp;
            Ya=Ya+dy;
            Ypa=Ypa+dyp;
            var sa=959.63/Ra;
            var sb=8.41/Dea;
            switch(k)
            {
                case 1:	L=sa+sb;
                break;
                case 2:	L=sa-sb;
                break;
                case 3:	L=sa-sb;
                break;
                case 4:	L=sa-sb;
                break;
                case 5:	L=sa+sb;
                break;
            }
            var n2=Xpa*Xpa+Ypa*Ypa;
            n=Math.sqrt(n2);	
            var SM=(Xa*Ypa-Ya*Xpa)/(n*L);
            if ( ((SM*SM)>1) && (k!=3)) {
                var TC=9999
            };
            switch(k)
            {
                case 1:	Tau=-(Xa*Xpa+Ya*Ypa)/n2-(L/n)*Math.sqrt(1-SM*SM) ;
                break;
                case 2:	Tau=-((Xa*Xpa+Ya*Ypa)/n2)-((L/n)*Math.sqrt(1-(SM*SM)));
                break;
                case 3:	Tau=-((Xa*Xpa+Ya*Ypa)/n2);
                break;
                case 4:	Tau=-((Xa*Xpa+Ya*Ypa)/n2)+((L/n)*Math.sqrt(1-(SM*SM)));
                break;
                case 5:	Tau=-((Xa*Xpa+Ya*Ypa)/n2)+((L/n)*Math.sqrt(1-(SM*SM)));
                break;
                }
            T=T+Tau; 
        }
        var TC=ele_T0+T+fuso;
        TC=TC-DET/3600;
        ElevationAzimuth(Lat,da*degrees,Ha*degrees);
        var ang=Math.atan2(-Xa,Ya);
        if (ang<0) {ang=(ang+2*Math.PI)};
        time[k]=TC;
        elevation[k]=Alt;
        angle[k]=ang*degrees
        afstand[k]=Math.sqrt((Xa*Xa)+(Ya*Ya));
    }
    return time[Phase]
}

function CalculateParallax()
{
    var timeA1=HMStoDec("0");
    var timeA2=HMStoDec("11.03.47");
    var timeB1=HMStoDec("0");
    var timeB2=HMStoDec("11.10.49");
    if (timeA1>0)
    {
        var time1=timeA1;
        var time2=timeB1;
        var fase=2
    }
    if (timeA2>0)
    {
        var time1=timeA2;
        var time2=timeB2;
        var fase=4
    }
    var waarneemverschil=time1-time2;
    var parzon=8.794148;
    for (var n=1; n<=5; n++)
    {
        var longitude=parseFloat("5.0");
        longitude=-longitude;
        var latitude=parseFloat("52.0");
        console.log("args " + longitude + " " + latitude + " " + parzon + " " + fase)
        var timeA=CalculateTime(longitude,latitude,parzon,fase);
        console.log("timeA "+timeA);
        var longitude=parseFloat("20.0");
        longitude=-longitude;
        var latitude=parseFloat("-30.0");
        var timeB=CalculateTime(longitude,latitude,parzon,fase);
        var rekenverschil=(timeA-timeB);
        var parzon=((waarneemverschil/rekenverschil)*parzon);
        console.log(parzon);
    }
    var fout=((0.00278/waarneemverschil)*parzon);;
    var au=(Math.floor(6378.14/((parzon/3600)*rad)));
    var parallax = FormatLD(parzon);
    var error=Math.abs(FormatLD(fout));
    console.log(au);
    console.log(parallax);
    console.log(error);
}

CalculateParallax();


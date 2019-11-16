import runpy
import random
import math
import csv

#Disini saya mendefinisikan per atribut (kecuali keputusan saya definisikan 1 bit saja) dengan 2 bit saja.
#suhu : 2bit, waktu : 2bit, cuaca : 2bit, kelembaban : 2bit, keputusan : 1bit


#import csvnya dulu 
def imp():
    data = []
    with open('data_latih.csv') as dat:
        read = csv.reader(dat)
        for row in read:
            data.append(row)
    return data

#import data uji nya belakangan nya hehe
def testing():
    data = []
    with open('data_uji_opsi_1.csv') as dat:
        read = csv.reader(dat)
        for row in read:
            data.append(row)
    return data

#buat bikin 1 kromosom
def indv():
    ind = []
    for i in range(9):
        x = random.randint(0,1)
        ind.append(x)
    return ind

#buat bikin populasi
def pop(jml):
    pop = []
    for i in range(jml):
        ind = indv()
        pop.append(ind)
    return pop

#buat translate suhu
def transTemp(data,i):
    if(data[i][0]=='normal'):
        suhu = [1,1]
    elif(data[i][0]=='rendah'):
        suhu = [0,1]
    elif(data[i][0]=='tinggi'):
        suhu = [1,0]
    return suhu

#buat translate waktu
def transHari(data,i):
    if(data[i][1]=='pagi'):
        hari = [1,1]
    if(data[i][1]=='siang'):
        hari = [1,0]
    if(data[i][1]=='sore'):
        hari = [0,1]
    if(data[i][1]=='malam'):
        hari = [0,0]
    return hari

#buat translate cuaca
def transLangit(data,i):
    if(data[i][2]=='berawan'):
        langit = [1,1]
    if(data[i][2]=='cerah'):
        langit = [1,0]
    if(data[i][2]=='rintik'):
        langit = [0,1]
    if(data[i][2]=='hujan'):
        langit = [0,0]
    return langit

#buat translate kelembaban
def transLembab(data,i):
    if(data[i][3]=='normal'):
        lembab = [1,1]
    elif(data[i][3]=='rendah'):
        lembab = [0,1]
    elif(data[i][3]=='tinggi'):
        lembab = [1,0]
    return lembab

#buat translate keputusan
def transDeci(data,i):
    if(data[i][4]=='ya'):
        dec = 1
    else:
        dec = 0
    return dec

#main program translate atau decode dari string jadi 2-bit biner
def translate(data):
    dec = []
    pop_csv = []
    for i in range(len(data)):
        suhu = transTemp(data,i)
        hari = transHari(data,i)
        langit = transLangit(data,i)
        lembab = transLembab(data,i)
        keputusan = transDeci(data,i)
        dec = suhu+hari+langit+lembab
        dec.append(keputusan)
        pop_csv.append(dec)
    return pop_csv

#buat ngitung fitness
def fitness(pop,pop_csv):
    cek = True
    fitneslist = []
    count = 0
    cek = True
    for i in range(len(pop)):
        for j in range(len(pop_csv)):
            if (pop[i][:2] == [1,1]):
                
                if(pop[i][2:4] == pop_csv[j][2:4]):
                   
                    if(pop[i][4:6] == pop_csv[j][4:6]):
                        
                        if(pop[i][6:8] == pop_csv[j][6:8]):
                            
                            if(pop[i][8:9] == pop_csv[j][8:9]):
                                count += 1  
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
                    
            elif (pop[i][:2] == [1,0]):

                if(pop[i][2:4] == pop_csv[j][2:4]):
                  
                    if(pop[i][4:6] == pop_csv[j][4:6]):
                        
                        if(pop[i][6:8] == pop_csv[j][6:8]):
                           
                            if(pop[i][8:9] == pop_csv[j][8:9]):
                                count += 1
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
                    

            elif (pop[i][:2] == [0,1]):
               
                if(pop[i][2:4] == pop_csv[j][2:4]):
                 
                    if(pop[i][4:6] == pop_csv[j][4:6]):
                      
                        if(pop[i][6:8] == pop_csv[j][6:8]):
                            
                            if(pop[i][8:9] == pop_csv[j][8:9]):
                                count += 1
                                
                            else:
                                cek = False
                                
                        else:
                            cek = False
                            
                    else:
                        cek = False
                        
                else:
                    cek = False
            else:
                cek = False
        fitneslist.append(count/80)

    return fitneslist

#milih orangtua pake roulette wheel 
def pilih_parent(fitness,pop):
    total=0
    for i in fitness:
        total += i
    idx_parent = []
    for j in range(2):
        r = random.random()
        idx = 0
        while (r>0) and (idx<19):
            r -= fitness[idx]/total
            idx = idx + 1
        idx_parent.append(idx)
    return idx_parent


def search(pop,index):
    i1 = index[0]   #i1 adalah variabel buat nampung index
    i2 = index[1]   #sama ini
    p1 = pop[i1]    #nah kalo ini buat ngeluarin kromosom bapak nya
    p2 = pop[i2]    #ini buat ibuknya
    return p1,p2

#crossover single point perkoro utek ku rakuat
#selain itu, proses pembuatan anak nya disini
def crossover(p1,p2):
    prob = random.random()
    anak1 =[]
    anak2 =[]
    cek = True
    if prob > 0.1:
        while (cek != False):
            a =random.randint(0,len(p1))
            b =random.randint(0,len(p1))
            if (a<b):
                tipotlist = [a,b]
                cek = False
            else:
                cek = True

        #buat anak pertama
        a =p1[:tipotlist[0]]
        b =p2[tipotlist[0]:tipotlist[1]]
        c =p1[(tipotlist[1]):len(p1)]


        #buat anak kedua
        d =p2[:tipotlist[0]]
        e =p1[tipotlist[0]:tipotlist[1]]
        f =p2[tipotlist[1]:len(p2)]

        anak1 = a+b+c       
        anak2 = d+e+f
        return anak1,anak2
        
    else :
        return p1,p2

#mutasi biasa
def mutasi(p1,p2):
    hasil_mutasi = []
    for i in range(len(p1)):
        chance = random.random()
        if chance < 0.1:
            p1[i]=random.randint(0,1)

    for j in range(len(p2)):
        chance1 = random.random()
        if chance1 < 0.1:
            p2[j]=random.randint(0,1)   
    hasil_mutasi.append(p1)
    hasil_mutasi.append(p2)
    return hasil_mutasi

def bestFitness(fitness):
   max = 0
   idx = 0
#    print(fitness)
   for i in range(len(fitness)):
     if fitness[i] > max:
        max = fitness[i]
        idx = i
   return max,idx 

def bestKromosom(max,fitnesslist,pop):
    idx=-1
    for i in range(len(fitnesslist)):
        if max == fitnesslist[i]:
            idx = i
    return pop[idx]

#masukin data ke csv nya + nerjemahin 
def encSuhu (data,i):
    if(data[i][:2]==[1,1]):
        suhu = "Normal"
    elif(data[i][:2]==[0,1]):
        suhu = "Tinggi"
    elif(data[i][:2]==[1,0]):
        suhu = "Rendah"
    else:
        suhu = 'unknown'
    return suhu

def encHari (data,i):
    if(data[i][2:4]==[1,1]):
        hari = "Pagi"
    elif(data[i][2:4]==[1,0]):
        hari = "Siang"
    elif(data[i][2:4]==[0,1]):
        hari = "Sore"
    elif(data[i][2:4]==[0,0]):
        hari = 'Malam'
    return hari

def encLangit(data,i):
    if(data[i][4:6]==[1,1]):
        langit = "Berawan"
    elif(data[i][4:6]==[1,0]):
        langit = "Cerah"
    elif(data[i][4:6]==[0,1]):
        langit = "Rintik"
    elif(data[i][4:6]==[0,0]):
        langit = 'Hujan'
    return langit

def encLembab(data,i):
    if(data[i][6:8]==[1,1]):
        lembab = "Normal"
    elif(data[i][6:8]==[0,1]):
        lembab = "Tinggi"
    elif(data[i][6:8]==[1,0]):
        lembab = "Rendah"
    else:
        lembab = 'unknown'
    return lembab

def encDecision(data,i):
    if(data[i][8:9]==[1]):
        decision = 'ya'
    else:
        decision = 'tidak'
    return decision


#untuk melihat keputusan dari anak anak kami, maaf kalau ada yang cacat 
def testPop(pop,test):
    testlist = []
    for i in range(len(pop)):
        for j in range(len(test)):
            if (pop[i][0]=='Tinggi'):                   
                if(pop[i][1] == test[j][1]):                  
                    if(pop[i][2] == test[j][2]):                       
                        if(pop[i][3] == test[j][3]):
                            decision = pop[i][4]
                            testlist.append([decision,i])
                        else:
                            decision = 'tidak tahu'                           
                    else:
                        decision = 'tidak tahu'                      
                else:
                    decision = 'tidak tahu'                   
            elif (pop[i][0]=='Normal'):
                if(pop[i][1] == test[j][1]):               
                    if(pop[i][2] == test[j][2]):                     
                        if(pop[i][3] == test[j][3]):
                            decision = pop[i][4]   
                            testlist.append([decision,i])
                        else:
                            decision = 'tidak tahu'                            
                    else:
                        decision = 'tidak tahu'                        
                else:
                    decision = 'tidak tahu'                   
            elif (pop[i][0]=='Rendah'):      
                if(pop[i][1] == test[j][1]):                
                    if(pop[i][2] == test[j][2]):                     
                        if(pop[i][3] == test[j][3]):                           
                            decision = pop[i][4] 
                            testlist.append([decision,i])                                                               
                        else:
                            decision = 'tidak tahu'                            
                    else:
                        decision = 'tidak tahu'                       
                else:
                    decision = 'tidak tahu'
            else:
                decision = 'tidak tahu' 
        
    return testlist







#main program atau proses elitism dan semuanya disini
data = imp() #--buat import data dari csv terus dimasukin ke array
ind = indv() #--buat generate 1 kromosom
#generate 1 populasi sama dengan 20
populasi = pop(20) #inisialisasi populasi awal sebanyak 20 kromosom
pop_csv=translate(data) #translating data dari csv
fit = fitness(populasi,pop_csv)
gen = 0
fitGlobal = []
bestGlobal = bestFitness(fit)
while gen <= 1000: #jumlahnya bisa diganti sesuka hati
    save = []
    #pembentukan populasi baru 
    for x in range (10):
        fit = fitness(populasi,pop_csv)
        idx = pilih_parent(fit,populasi)
        p1,p2 = search(populasi,idx)
        anak1,anak2 = crossover(p1,p2)
        hasil_mutasi = mutasi(anak1,anak2)
        save.append(hasil_mutasi[0])
        save.append(hasil_mutasi[1])
    #end
    popLokal = save                     #ngubah populasi awal jadi populasi baru (sementara)
    fitLokal = fitness(popLokal,pop_csv)#hitung fitness dari populasi yang baru dibuat
    bestLokal = bestFitness(fitLokal)   #ambil fitness terbaik untuk turnamen pentungan dengan fitnessglobal (bestGlobal)
    
    if  bestLokal[0] > bestGlobal[0]:   #nah ini pentungannya, kalo lokal dipentung joker, ya ga berubah globalnya hehe
        bestGlobal = bestLokal
        populasi = popLokal             #nah kalo menang si lokalnya, se populasi global yang kesimpen diganti
        fitGlobal = fitness(populasi,pop_csv) 
    print("generasi : ",gen)
    gen+=1
    
    


print("==========================Pemenang Turnamen Pentungan Kali ini==========================")
print("========================================================================================")
print('                     list populasi    : ',populasi)
print('                     fitness bagus    : ',fitGlobal)
print("                     fitness terbaik  : ",bestGlobal[0])
print("                     kromosom terbaik : ",populasi[bestGlobal[1]])
print("=========================================================================================")
print("================================Wassalamualaikum Wr. Wb.=================================")

#proses pembandingan data ujinya dimuali disini
encoding = encode(populasi)
data_test = testing()
keputusan = testPop(encoding,data_test)
print(keputusan)


with open("hasil hehehehe.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(keputusan)
print("==========================================================================================")
print("=======================================FIN================================================")






from flask import Flask, render_template, request, redirect, url_for, session,send_file
import os
import time
import json
import random

class Titik:
    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1

    def cetaktitik(self):
        print(self.y+1, ",", self.x+1)

    def titiksama(self, t):
        return (t.x == self.x) and (t.y == self.y)
    def to_dict(self):
        return self.__dict__

class Matrix:
    def setmatrix(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.isi = [["" for i in range(cols)] for i in range(rows)]

    def setIsian(self, z):
        k = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.isi[i][j] = z[k]
                k += 1

    def setIsianRandom(self, z):
        for i in range(self.rows):
            for j in range(self.cols):
                self.isi[i][j] = random.choice(z)

    def getCols(self):
        return self.cols

    def getRows(self):
        return self.rows

    def printMatrix(self):
        for row in self.isi:
            print(" ".join(row))

def input_func():
    buffer = 0
    bobot = []
    sequence = []
    m = Matrix()
    
    print("Select Input (Choose a number):")
    print("1. File txt")
    print("2. Keyboard")
    
    num = input("Enter a number: ")
    
    while num not in ["1", "2"]:
        print("Please choose between 1 or 2")
        num = input("Enter a number: ")
    
    if num == "1":
        file = input("Enter file name (without .txt): ")
        filename = "../test/" + file + ".txt"
        seqs=[]
        with open(filename, 'r') as fin:
            lines = fin.readlines()
            for i, line in enumerate(lines):
                if i == 0:
                    buffer = int(line)
                elif i == 1:
                    a, b = map(int, line.split())
                    m.setmatrix(a, b)
                elif 1 < i < m.getRows() + 2:
                    seqs += line.split()
                    if(i==m.getRows()+1):
                        m.setIsian(seqs)
                elif i == m.getRows() + 2:
                    count = int(line) 
                    for j in range(count * 2):
                        line = lines[i + j + 1].strip()
                        lineWords = []
                        if j % 2 == 0:
                            lineWords = line.split()
                            sequence.append(lineWords)
                        else:
                            bobot.append(int(line))
                        
    else:
        jumlah = int(input("Enter the number of tokens (2 minimum): "))
        while jumlah < 2:
            print("Invalid Number!")
            jumlah = int(input("Enter the number of tokens (2 minimum): "))
        
        sekuens = input("Enter {} tokens separated by space: ".format(jumlah)).split()
        
        buffer = int(input("Enter buffer length: "))
        row = int(input("Enter matrix row length: "))
        cols = int(input("Enter matrix column length: "))
        m.setmatrix(row, cols)
        jumlah_sekuens = int(input("Enter the number of sequences: "))
        maks_sekuens = int(input("Enter maximum length of sequence: "))
        
        m.setIsianRandom(sekuens)
        
        for _ in range(jumlah_sekuens):
            temp = []
            length = random.randint(2, maks_sekuens)
            for _ in range(length):
                temp.append(random.choice(sekuens))
            sequence.append(temp)
            bobot.append(random.randint(1, 60))
        
        print("\n\nMatrix generated!")
        m.printMatrix()
        
        print("\n\nSequence generated!")
        for i, seq in enumerate(sequence):
            print("Sequence", i+1)
            print(" ".join(seq))
            print("Weight:", bobot[i], "\n")

    return buffer, bobot, sequence, m

def arraytitiksama(t1, t2):
    for t in t1:
        if t.titiksama(t2):
            return True
    return False

def panjangaman(sequence, buf):
    size = 0
    for seq in sequence:
        if size + len(seq) <= buf:
            size += len(seq)
        else:
            return False
    return True

def cekkembar(sequence, buf):
    for seq in sequence:
        if seq == buf:
            return True
    return False

def kombisequens(sequence, temp, idx, index, index2, seqgab, bobot, bb, k, buf):
    if k == 0:
        if panjangaman(temp, buf) and not cekkembar(index, idx):
            temp2 = []
            maxi = 0
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    if i>0 and temp2[-1] == temp[i][j] and j==0:
                        continue
                    temp2.append(temp[i][j])
                maxi += bb[i]
            temp2.append(str(maxi))
            seqgab.append(temp2)
            index.append(idx)
        return

    for i in range(len(sequence)+1):
        if i not in index2:
            if (i==len(sequence) and len(temp)):
                temp.append(["bebas"])
                idx += str(i)
                index2.append(i)
                bb.append(0)

                kombisequens(sequence, temp, idx, index, index2, seqgab, bobot, bb, k - 1, buf)
                temp.pop()
                idx = idx[:-1]
                bb.pop()
                index2.pop()
            elif(i!=len(sequence)):
                temp.append(sequence[i])
                idx += str(i)
                index2.append(i)
                bb.append(bobot[i])

                kombisequens(sequence, temp, idx, index, index2, seqgab, bobot, bb, k - 1, buf)
                temp.pop()
                idx = idx[:-1]
                bb.pop()
                index2.pop()

def cekadatoken(m, token, bar, kol, pilihan):
    if pilihan == 1:
        for j in range(len(m.isi)):
            if m.isi[j][kol] == token or token == "bebas":
                return True
    elif pilihan == 2:
        for j in range(len(m.isi[bar])):
            if m.isi[bar][j] == token or token == "bebas":
                return True
    else:
        for j in range(1, len(m.isi)):
            if m.isi[j][kol] == token or token == "bebas":
                return True
    return False

def solve(buffer, bobot, sequence, m):
    idx = ""
    max_val = 0
    max_seq = []
    max_coords = []
    koor = []

    seqgab = []
    for k in range(1, len(sequence) + 1):
        temp = []
        kombisequens(sequence, temp, idx, [], [], seqgab, bobot, [], k, buffer)

    cnt = 0
    while cnt < len(seqgab):
        for i in range(m.cols):
            tidakcocok = False
            lok = 0
            if m.isi[0][i] == seqgab[cnt][0]:
                if (not cekadatoken(m, seqgab[cnt][1], lok, i, 1)):
                    tidakcocok = True
                else:
                    koor.append(Titik(0,i))
                    ada = True
                    done = False
                    total = 1
                    now = i
                    bebrow=-1
                    bebcol=-1
                    while total < len(seqgab[cnt]) - 1 and ada:
                        ada = False
                        if total % 2 == 1:
                            for z in range(m.rows):
                                if (m.isi[z][now] == seqgab[cnt][total] or seqgab[cnt][total] == "bebas") and len(koor)>0 and not arraytitiksama(koor,Titik(z, now)):
                                    if total == len(seqgab[cnt]) - 2 or cekadatoken(m, seqgab[cnt][total + 1], z, z, 2):
                                        if(seqgab[cnt][total] == "bebas"):
                                            seqgab[cnt][total] = m.isi[z][now]
                                            bebrow=cnt
                                            bebcol=total
                                        koor.append(Titik(z, now))
                                        now = z
                                        ada = True
                                        break
                        elif total % 2 == 0:
                            for z in range(m.cols):
                                if (m.isi[now][z] == seqgab[cnt][total] or seqgab[cnt][total] == "bebas") and  not arraytitiksama(koor,Titik(now, z)):
                                    if total == len(seqgab[cnt]) - 2 or ((total < len(seqgab) - 2) and cekadatoken(m, seqgab[cnt][total + 1], z, z, 1)):
                                        if(seqgab[cnt][total] == "bebas"):
                                            seqgab[cnt][total] = m.isi[now][z]
                                            bebrow=cnt
                                            bebcol=total
                                        koor.append(Titik(now, z))
                                        now = z
                                        ada = True
                                        break
                        if ada and (total == len(seqgab[cnt]) - 2):
                            done = True
                        if ada:
                            total += 1
                    if done:
                        total_weight = int(seqgab[cnt][-1])
                        if total_weight > max_val:
                            if max!=-999 and len(max_seq)>len(seqgab):
                                max_val = total_weight
                                max_seq = seqgab[cnt]
                                max_coords = koor
                                if bebrow!=-1:
                                    seqgab[bebrow][bebcol] == "bebas"
    
                            else:
                                max_val = total_weight
                                max_seq = seqgab[cnt]
                                max_coords = koor
                                if bebrow!=-1:
                                    seqgab[bebrow][bebcol] == "bebas"
                                
                    koor = []
            if (m.isi[0][i] != seqgab[cnt][0] or tidakcocok) and len(seqgab[cnt]) <= buffer:
                if cekadatoken(m, seqgab[cnt][0], 0, i, 3):
                    seqgab[cnt].insert(0, m.isi[0][i])
                    koor.append(Titik(0, i))
                    ada = True
                    done = False
                    total = 1
                    now = i
                    bebrow=-1
                    bebcol=-1
                    while total < len(seqgab[cnt]) - 1 and ada:
                        ada = False
                        if total % 2 == 1:
                            for z in range(m.rows):
                                if (m.isi[z][now] == seqgab[cnt][total] or seqgab[cnt][total] == "bebas") and len(koor)>0 and not arraytitiksama(koor,Titik(z, now)):
                                    if total == len(seqgab[cnt]) - 2 or cekadatoken(m, seqgab[cnt][total + 1], z, z, 2):
                                        if(seqgab[cnt][total] == "bebas"):
                                            seqgab[cnt][total] = m.isi[z][now]
                                            bebrow=cnt
                                            bebcol=total
                                        koor.append(Titik(z, now))
                                        now = z
                                        ada = True
                                        break
                        elif total % 2 == 0:
                            for z in range(m.cols):
                                if (m.isi[now][z] == seqgab[cnt][total] or seqgab[cnt][total] == "bebas") and  not arraytitiksama(koor,Titik(now, z)):
                                    if total == len(seqgab[cnt]) - 2 or ((total < len(seqgab) - 2) and cekadatoken(m, seqgab[cnt][total + 1], z, z, 1)):
                                        if(seqgab[cnt][total] == "bebas"):
                                            seqgab[cnt][total] = m.isi[now][z]
                                            bebrow=cnt
                                            bebcol=total
                                        koor.append(Titik(now, z))
                                        now = z
                                        ada = True
                                        break
                        if ada and total == len(seqgab[cnt]) - 2:
                            done = True
                        if not ada and bebrow!=-1:
                            seqgab[bebrow][bebcol] == "bebas"
                        if ada:
                            total += 1
                    if done:
                        total_weight = int(seqgab[cnt][-1])
                        if total_weight > max_val:
                            if max!=-999 and len(max_seq)>len(seqgab):
                                max_val = total_weight
                                seq_copy = seqgab[cnt].copy()
                                max_seq = seq_copy
                                max_coords = koor
                                if bebrow!=-1:
                                    seqgab[bebrow][bebcol] == "bebas"
                                
                            else:
                                max_val = total_weight
                                seq_copy = seqgab[cnt].copy()
                                max_seq = seq_copy
                                max_coords = koor
                                if bebrow!=-1:
                                    seqgab[bebrow][bebcol] == "bebas"
                                
                    koor = []
                    seqgab[cnt].pop(0)
        cnt += 1

    print("\nResult Calculated!")
    print("Maximum Weight:", max_val)
    sek = " ".join(max_seq[:-1])
    print(sek)
    print("Sequence:", " ".join(max_seq[:-1]))
    print("Coordinates:")
    for i in max_coords:
        i.cetaktitik()

    return max_val,sek,max_coords

def main():
    buffer = 0
    bobot = []
    sequence = []
    m = Matrix()

    buffer, bobot, sequence, m = input_func()
    solve(buffer, bobot, sequence, m)

def file_exists(file_path):
    return os.path.exists(file_path)

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        buffers =0
        bobot = []
        sequence = []
        sequencemax = ""
        m = Matrix()
        file = request.files['fileInput']
        if file:
            seqs = []
            lines = file.stream.readlines()
            for i, line in enumerate(lines):
                line = line.decode('utf-8').strip() 
                if i == 0:
                    buffer = int(line)
                elif i == 1:
                    a, b = map(int, line.split())
                    m.setmatrix(a, b)
                elif 1 < i < m.getRows() + 2:
                    seqs += line.split()
                    if i == m.getRows() + 1:
                        m.setIsian(seqs)
                elif i == m.getRows() + 2:
                    count = int(line)
                    for j in range(count * 2):
                        line = lines[i + j + 1].decode('utf-8').strip() 
                        lineWords = []
                        if j % 2 == 0:
                            lineWords = line.split()
                            sequence.append(lineWords)
                        else:
                            bobot.append(int(line))
            start_time = time.time()
            buffers,sequencemax,coordinate = solve(buffer, bobot, sequence, m)
            end_time = time.time()
            elapsed_time = (end_time - start_time)*1000

            if(sequencemax==""):
                sequencemax = "No Solution"

            koordinat = []
            for i in coordinate:
                koor = []
                koor.append(i.x)
                koor.append(i.y)
                koordinat.append(koor)
        
            session['buffers'] = buffers
            session['sekuense'] = sequence
            session['bobot'] = bobot
            session['sekuenses'] = sequencemax
            session['elapsed_time'] = elapsed_time
            session['matrix'] = m.isi
            session['coordinate'] = koordinat
            session['mode'] = "file"

            return redirect(url_for('result'))

@app.route('/manual_upload', methods=['POST'])
def manual_upload():
    buffers =0
    bobot = []
    sequence = []
    sequencemax = ""
    m = Matrix()
    
    jumlah = int(request.form['jumlah'])
    sekuens = request.form['sekuens'].split()
    buffer = int(request.form['buffer'])
    row = int(request.form['row'])
    cols = int(request.form['cols'])
    jumlah_sekuens = int(request.form['jumlah_sekuens'])
    maks_sekuens = int(request.form['maks_sekuens'])

    m.setmatrix(row, cols)
    m.setIsianRandom(sekuens)

    for _ in range(jumlah_sekuens):
        temp = []
        length = random.randint(2, maks_sekuens)
        for _ in range(length):
            temp.append(random.choice(sekuens))
        while temp in sequence:
            for _ in range(length):
                temp.append(random.choice(sekuens))
        sequence.append(temp)
        bobot.append(random.randint(1, 60))
        
    start_time = time.time()
    buffers,sequencemax,coordinate=solve(buffer, bobot, sequence, m)
    end_time = time.time()
    elapsed_time = (end_time - start_time)*1000

    if(sequencemax==""):
        sequencemax = "No Solution"

    koordinat = []
    for i in coordinate:
        koor = []
        koor.append(i.x)
        koor.append(i.y)
        koordinat.append(koor)

    session['sekuense'] = sequence
    session['bobot'] = bobot
    session['buffers'] = buffers
    session['sekuenses'] = sequencemax
    session['elapsed_time'] = elapsed_time
    session['matrix'] = m.isi
    session['coordinate'] = koordinat
    session['mode'] = "manual"

    return redirect(url_for('result'))

@app.route('/result')
def result():
    buffers = session.get('buffers')
    sequence = session.get('sekuenses')
    seq = session.get('sekuense')
    bobot = session.get('bobot')
    elapsed_time = session.get('elapsed_time')
    mode = session.get('mode')
    matrix = session.get('matrix')
    matrix = json.dumps(matrix)

    coordinate = session.get('coordinate')
    coordinate = json.dumps(coordinate)

    return render_template('result.html', buffers=buffers, sequence=sequence, elapsed_time=elapsed_time,matrix=matrix,coordinate=coordinate,seq=seq,bobot=bobot,mode=mode)

@app.route('/download', methods=['GET'])
def download():
    buffers = session.get('buffers')
    sequencemax = session.get('sekuenses')
    elapsed_time = session.get('elapsed_time')
    matrix = session.get('matrix')
    coordinate = session.get('coordinate')

    content = f"Buffers: {buffers}\n"
    content += f"Sequences: {sequencemax}\n"
    content += f"Elapsed Time: {elapsed_time} seconds\n"
    content += "Coordinates:\n"
    for coord in coordinate:
        content += f"{coord[1]+1}, {coord[0]+1}\n"

    save_path = os.path.join((os.path.dirname(app.root_path)), 'test', 'result.txt')
    
    with open(save_path, "w") as file:
        file.write(content)
    return send_file(save_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
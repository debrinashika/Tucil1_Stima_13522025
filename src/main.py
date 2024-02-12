import random

class Titik:
    def __init__(self, x1, y1):
        self.x = x1 + 1
        self.y = y1 + 1

    def cetaktitik(self):
        print(self.y, ",", self.x)

    def titiksama(self, t):
        return (t.x == self.x) and (t.y == self.y)

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
        filename = "test/" + file + ".txt"
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

def cekkembarint(sequence, buf):
    return buf in sequence

def kombisequens(sequence, temp, idx, index, index2, seqgab, bobot, bb, k, buf):
    if k == 0:
        if panjangaman(temp, buf) and not cekkembar(index, idx):
            temp2 = []
            maxi = 0
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    if i>0 and temp2[-1] == temp[i][j]:
                        continue
                    temp2.append(temp[i][j])
                maxi += bb[i]
            temp2.append(str(maxi))
            seqgab.append(temp2)
            index.append(idx)
        return

    for i, seq in enumerate(sequence):
        if i not in index2:
            temp.append(seq)
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
            if m.isi[j][kol] == token:
                return True
    elif pilihan == 2:
        for j in range(len(m.isi[bar])):
            if m.isi[bar][j] == token:
                return True
    else:
        for j in range(1, len(m.isi)):
            if m.isi[j][kol] == token:
                return True
    return False

def solve(buffer, bobot, sequence, m):
    idx = ""
    max_val = -999
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
            print(seqgab[cnt])
            if m.isi[0][i] == seqgab[cnt][0]:
                if (not cekadatoken(m, seqgab[cnt][1], lok, i, 1)):
                    tidakcocok = True
                else:
                    koor.append(Titik(0,i))
                    ada = True
                    done = False
                    total = 1
                    now = i
                    while total < len(seqgab[cnt]) - 1 and ada:
                        ada = False
                        if total % 2 == 1:
                            for z in range(m.rows):
                                if m.isi[z][now] == seqgab[cnt][total] and len(koor)>0 and not arraytitiksama(koor,Titik(z, now)):
                                    if total == len(seqgab[cnt]) - 2 or cekadatoken(m, seqgab[cnt][total + 1], z, z, 2):
                                        koor.append(Titik(z, now))
                                        now = z
                                        ada = True
                                        break
                        elif total % 2 == 0:
                            for z in range(m.cols):
                                if m.isi[now][z] == seqgab[cnt][total] and  not arraytitiksama(koor,Titik(now, z)):
                                    if total == len(seqgab[cnt]) - 2 or ((total < len(seqgab) - 2) and cekadatoken(m, seqgab[cnt][total + 1], z, z, 1)):
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
                                print(max_seq,max_val)
                                for j in max_coords:
                                    j.cetaktitik()
    
                            else:
                                max_val = total_weight
                                max_seq = seqgab[cnt]
                                max_coords = koor
                                print(max_seq,max_val)
                                for j in max_coords:
                                    j.cetaktitik()
                                
                    koor = []
            if (m.isi[0][i] != seqgab[cnt][0] or tidakcocok) and len(seqgab[cnt]) <= buffer:
                if cekadatoken(m, seqgab[cnt][0], 0, i, 3):
                    seqgab[cnt].insert(0, m.isi[0][i])
                    koor.append(Titik(0, i))
                    ada = True
                    done = False
                    total = 1
                    now = i
                    while total < len(seqgab[cnt]) - 1 and ada:
                        ada = False
                        if total % 2 == 1:
                            for z in range(m.rows):
                                if m.isi[z][now] == seqgab[cnt][total] and len(koor)>0 and not arraytitiksama(koor,Titik(z, now)):
                                    if total == len(seqgab[cnt]) - 2 or cekadatoken(m, seqgab[cnt][total + 1], z, z, 2):
                                        koor.append(Titik(z, now))
                                        now = z
                                        ada = True
                                        break
                        elif total % 2 == 0:
                            for z in range(m.cols):
                                if m.isi[now][z] == seqgab[cnt][total] and  not arraytitiksama(koor,Titik(now, z)):
                                    if total == len(seqgab[cnt]) - 2 or ((total < len(seqgab) - 2) and cekadatoken(m, seqgab[cnt][total + 1], z, z, 1)):
                                        koor.append(Titik(now, z))
                                        now = z
                                        ada = True
                                        break
                        if ada and total == len(seqgab[cnt]) - 2:
                            done = True
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
                                print(max_seq,max_val)
                                for j in max_coords:
                                    j.cetaktitik()
                                
                            else:
                                max_val = total_weight
                                seq_copy = seqgab[cnt].copy()
                                max_seq = seq_copy
                                max_coords = koor
                                print(max_seq,max_val)
                                for j in max_coords:
                                    j.cetaktitik() 
                    koor = []
                    seqgab[cnt].pop(0)
                    print("ini habis pop")
                    print(max_seq,max_val)
        cnt += 1

    print("\nResult Calculated!")
    print("Maximum Weight:", max_val)
    print(max_seq)
    print("Sequence:", " ".join(max_seq[:-1]))
    print("Coordinates:")
    for i in max_coords:
        i.cetaktitik()

def main():
    buffer = 0
    bobot = []
    sequence = []
    m = Matrix()

    buffer, bobot, sequence, m = input_func()
    solve(buffer, bobot, sequence, m)

if __name__ == "__main__":
    main()
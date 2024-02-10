#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <ctime>
#include <chrono>
#include <cstdlib>


using namespace std;

class Titik{
    public:
        int x;
        int y;

        Titik(int x1, int y1){
            this->x = x1+1;
            this->y = y1+1;
        }

        void cetaktitik(){
            std::cout<<y<<", "<<x<<endl;
        }

        bool titiksama(Titik t){
            return((t.x == this->x)&&(t.y == this->y) );
        }

};

class Matrix {
public:
    int cols;
    int rows;
    vector<vector<string>> isi;

    void setmatrix(int rows, int cols) {
        this->rows = rows;
        this->cols = cols;
        isi.resize(rows, vector<string>(cols)); // Inisialisasi vektor isi
    }

    void setIsian(vector<string> z) {
        int k = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                isi[i][j] = z[k];
                k++;
            }
        }
    }

    void setIsianRandom(vector<string> z) {
        int k = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                isi[i][j] = z[rand() % z.size()];
                k++;
            }
        }
    }

    int getCols() {
        return cols;
    }

    int getRows() {
        return rows;
    }

    void printMatrix() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                std::cout << isi[i][j] << " ";
            }
            std::cout << endl;
        }
    }
};

void input(int *buffer, vector<int> &bobot, vector<vector<string>> &sequence, Matrix &m) {
    string num, file, filename;
    vector<string> seqs;

    std::cout << "Select Input (Choose a number):" << endl;
    std::cout << "1. File txt" << endl;
    std::cout << "2. Keyboard" << endl;
    
    std::cout << "Enter a number: ";
    getline(cin, num);
    
    while(num!="2" && num!="1"){
        std::cout << "Please choose beetween 1 or 2"<<endl;
        std::cout << "Enter a number: ";
        getline(cin, num);
    }
    if (num == "1") {
        std::cout << "Enter file name (without .txt): ";
        getline(cin, file);
        filename = "../test/" + file + ".txt";
        ifstream fin(filename);

        if (!fin) {
            std::cout << "Unable to open file " << filename << endl;
            exit(1);
        }

        string line;
        int lines = 0; // Hitung jumlah baris
        while (getline(fin, line)) {
            if (lines == 0) {
                *buffer = stoi(line);
            } else if (lines == 1) {
                istringstream iss(line);
                int a, b;
                iss >> a >> b;
                m.setmatrix(a, b);
            } else if (lines < m.getRows() + 2) {
                istringstream iss(line);
                string code;
                while (iss >> code) {
                    seqs.push_back(code);
                    
                }
                if (lines == m.getRows() + 1) {
                    m.setIsian(seqs);
                }
            } else if (lines == m.getRows() + 2) {
                int count = stoi(line);
                for (int i = 0; i < count*2; ++i) {
                    vector<string> lineWords;
                    getline(fin, line);
                    istringstream iss(line);
                    string word;
                    if (i % 2 == 0) {
                        while (iss >> word) {
                            lineWords.push_back(word);
                        }
                        sequence.push_back(lineWords);
                    } else {
                        bobot.push_back(stoi(line));
                    }
                }
            }
            lines++;
        }
        fin.close();
    }
    else{
        string s,row,cols;
        int jumlah,jumlah_sekuens,maks_sekuens;
        std::cout << "Enter the number of tokens (2 minimum): ";
        getline(cin, s);
        jumlah = stoi(s);

        while(jumlah<2){
            std::cout << "Invalid Number!"<<endl;
            std::cout << "Enter the number of tokens (2 minimum): ";
            getline(cin, s);
            jumlah = stoi(s);
        }
        
        vector<string> sekuens;
        bool benar = true;
        while(benar){
            std::cout << endl << "Enter "<< jumlah<< " tokens: ";
            getline(cin, s);
            stringstream word(s);
            string temp;
            sekuens.clear();

            int cnt = 0;
            while (cnt<jumlah && word>>temp){
                sekuens.push_back(temp);
                cnt++;
            }

            if (cnt == jumlah){
                benar=false;
            }
            else{
                std::cout << "Invalid Input!";
            }
        }

        std::cout << endl << "Enter buffer length:  ";
        getline(cin, s);
        *buffer = stoi(s);

        std::cout << endl << "Enter matrix row length:  ";
        getline(cin, row);
        std::cout << endl << "Enter matrix collumn length:  ";
        getline(cin, cols);

        m.setmatrix(stoi(row),stoi(cols));

        std::cout << endl << "Enter the number of sequences: " ;
        getline(cin, s);
        jumlah_sekuens = stoi(s);

        std::cout << endl << "Enter maximum length of sequence:  ";
        getline(cin, s);
        maks_sekuens = stoi(s);

        //build matrix;
        m.setIsianRandom(sekuens);
        //build sekuens
        int cnt = 0;
        while(cnt<jumlah_sekuens){
            vector<string> temp;
            int t=0;
            int len = rand()%maks_sekuens;
            while(len<2){
                len = rand()%maks_sekuens;
            }
            while(t<len){
                temp.push_back(sekuens[rand()%sekuens.size()]);
                t++;
            }
            sequence.push_back(temp);
            cnt++;
        }

        // isi bobot random
        cnt = 0;
        while(cnt<jumlah_sekuens){
            bobot.push_back(rand()%60+1);
            cnt++;
        }
        
        cout<<endl<<endl;
        cout<<"Matrix generated!"<<endl;
        m.printMatrix();

        cout<<endl<<endl;
        cout<<"Sequence generated!"<<endl;
        for (int i = 0; i < jumlah_sekuens; i++) {
            cout<<"Sequence "<<i+1<<endl;
            for (int j = 0; j < sequence[i].size(); j++) {
                std::cout << sequence[i][j] << " ";
            }
            cout<<endl<<"Weight: "<<bobot[i]<<endl<<endl;
        }

    }
}

bool arraytitiksama(vector<Titik> t1, Titik t2){
    for (int j = 0; j < t1.size(); j++) {
        if(t1[j].titiksama(t2)){
            return true;
        }
    }
    return false;
}

bool panjangaman(vector<vector<string>> &sequence,int buf){
    int size=0;
    for (int j = 0; j < sequence.size(); j++) { 
        if(size+sequence[j].size()<=buf){
            size+=sequence[j].size();
        }
        else{
            return false;
        }
    }
    return true;
}

bool cekkembar(vector<string> &sequence,string buf){
    int i = 0;
    while ( i<sequence.size()) { 
        if(sequence[i]==buf){
            return true;
        }
       i++;
    }
    return false;
}

bool cekkembarint(vector<int> &sequence,int buf){
    int i = 0;
    while ( i<sequence.size()) { 
        if(sequence[i]==buf){
            return true;
        }
       i++;
    }
    return false;
}

void kombisequens(vector<vector<string>>& sequence, vector<vector<string>>& temp,string idx, vector<string> index, vector<int> index2, vector<vector<string>>& seqgab, vector<int> bobot, vector<int> bb,  int k, int buf) {

    if (k == 0) {
        if(panjangaman(temp,buf)&&!cekkembar(index,idx)){
            vector<string> temp2;
            int maxi = 0;
            bool adadobel = false;
            for (int i = 0; i < temp.size(); i++) {
                for (int j = 0; j < temp[i].size(); j++) { 
                    if (i>0&&temp2[(temp2.size())-1]==temp[i][j]){
                        continue;
                    }
                    temp2.push_back(temp[i][j]);
                }
                maxi+=bb[i];
            }

            temp2.push_back(to_string(maxi));
            seqgab.push_back(temp2);

            index.push_back(idx);
            //  for (int j = 0; j < temp2.size(); j++) {
            // cout << temp2[j] << " ";
        }
        // cout << endl;
        

        return;
    }

    for (int i = 0; i < sequence.size(); ++i) {
        if(!cekkembarint(index2,i)){
            temp.push_back(sequence[i]);
            idx.push_back(i);
            index2.push_back(i);
            bb.push_back(bobot[i]); 
           
            kombisequens(sequence,temp,idx,index,index2,seqgab, bobot,bb,k - 1,buf); 
            temp.pop_back();
            idx.pop_back();
            bb.pop_back();
            index2.pop_back();
        }
        else{
            continue;
        }
    }

}

bool cekadatoken(Matrix m, string token, int bar, int kol, int pilihan){
    bool ada = false;
    if (pilihan == 1){// cek vertikal
        int j = 0;
        while (j < m.isi.size() && !ada) { 
            if (m.isi[j][kol]==token){
                ada = true;
            }
            j++;
        }  
    }
    else if (pilihan == 2){// cek horizontal
        int j = 0;
        while (j < m.isi[bar].size() && !ada) { 
            if (m.isi[bar][j]==token){
                ada = true;
            }
            j++;
        } 
    }
    else{ // cek verti tanpa yg atas
        int j = 1;
        while (j < m.isi.size() && !ada) { 
            if (m.isi[j][kol]==token){
                ada = true;
            }
            j++;
        } 
    }
    return ada;
}

void solve(int *buffer, vector<int> &bobot, vector<vector<string>> &sequence, Matrix &m){
    int idx = 0;
    int max = -999;
    int jum = 1;

    vector<int> bb,titik,index;
    vector<string> bot,gabmax;
    vector<vector<string>> seqgab;
    vector<Titik> koor,koorfix;
    string bob;

    auto mulai = chrono::high_resolution_clock::now();

    for (int k = 1; k <= sequence.size(); k++) {
        vector<vector<string>> temp;
        kombisequens(sequence, temp, bob, bot, index, seqgab,bobot,bb, k,*buffer);
    }

    int cnt = 0;
    while(cnt<seqgab.size()){
        for(int i=0;i<m.cols;i++){
            bool tidakcocok = false;
            int lok = 0;
            if(m.isi[0][i]==seqgab[cnt][0]){ // cari lokasi pertama
                if(!cekadatoken(m,seqgab[cnt][1],lok,i,1)){
                    tidakcocok = true;
                }
                else{
                    koor.push_back(Titik(0,i));
                    bool ada = true;
                    bool done = false;
                    int total = 1;
                    int now = i;
                    while(total<seqgab[cnt].size()-1 && ada == true){
                        ada = false;
                        if (total%2==1){
                            for (int z = 0; z < m.rows; z++) { // cari vertikal
                                if(m.isi[z][now]==seqgab[cnt][total]&&koor.size()>0&&!arraytitiksama(koor,Titik(z,now))){
                                    if(total==seqgab[cnt].size()-2||cekadatoken(m,seqgab[cnt][total+1],z,z,2)){
                                        koor.push_back(Titik(z,now));
                                        // std::cout<<"1 ";
                                        // std::cout<<z<<" "<<now<<" "<<m.isi[z][now]<<endl;
                                        now = z;
                                        ada=true;
                                        break;
                                    }
                                }
                            }
                        }
                        else if (total%2==0){
                            for (int z = 0; z < m.cols; z++) {
                                if(m.isi[now][z]==seqgab[cnt][total]&&!arraytitiksama(koor,Titik(now,z))){
                                    if(total==seqgab[cnt].size()-2||((total<seqgab.size()-2)&&cekadatoken(m,seqgab[cnt][total+1],z,z,1))){
                                        koor.push_back(Titik(now,z));
                                        // std::cout<<"2 ";
                                        // std::cout<<now<<" "<<z<<" "<<m.isi[now][z]<<endl;
                                        now = z;
                                        ada=true;
                                        break;
                                    }
                                }
                                
                            }
                        }
                        if(ada&&total==seqgab[cnt].size()-2){
                            done =true;
                        }
                        if(ada){
                            total++;
                        }
                    }
                    if(done){
                        if(stoi(seqgab[cnt][(seqgab[cnt].size())-1])>max){
                            max = stoi(seqgab[cnt][(seqgab[cnt].size())-1]);
                            gabmax = seqgab[cnt];
                            koorfix = koor;
                        }
                    }
                    koor.clear();
                    }
                    seqgab[cnt].erase(seqgab[cnt].begin());
                

            }
            if((m.isi[0][i]!=seqgab[cnt][0]||tidakcocok)&&(seqgab[cnt].size()<=*buffer)){
                if(!cekadatoken(m,seqgab[cnt][0],i,i,3)){
                    continue;
                }
                else{
                    seqgab[cnt].insert(seqgab[cnt].begin(),m.isi[0][i]);
                    koor.push_back(Titik(0,i));
                    bool ada = true;
                    bool done = false;
                    int total = 1;
                    int now = i;
                    while(total<seqgab[cnt].size()-1 && ada == true){
                        ada = false;
                        if (total%2==1){
                            for (int z = 0; z < m.rows; z++) { // cari vertikal
                                if(m.isi[z][now]==seqgab[cnt][total]&&koor.size()>0&&!arraytitiksama(koor,Titik(z,now))){
                                    if(total==seqgab[cnt].size()-2||cekadatoken(m,seqgab[cnt][total+1],z,z,2)){
                                        koor.push_back(Titik(z,now));
                                        // std::cout<<"1 ";
                                        // std::cout<<z<<" "<<now<<" "<<m.isi[z][now]<<endl;
                                        now = z;
                                        ada=true;
                                        break;
                                    }
                                }
                            }
                        }
                        else if (total%2==0){
                            for (int z = 0; z < m.cols; z++) {
                                if(m.isi[now][z]==seqgab[cnt][total]&&!arraytitiksama(koor,Titik(now,z))){
                                    if(total==seqgab[cnt].size()-2||((total<seqgab.size()-2)&&cekadatoken(m,seqgab[cnt][total+1],z,z,1))){
                                        koor.push_back(Titik(now,z));
                                        // std::cout<<"2 ";
                                        // std::cout<<now<<" "<<z<<" "<<m.isi[now][z]<<endl;
                                        now = z;
                                        ada=true;
                                        break;
                                    }
                                }
                                
                            }
                        }
                        if(ada&&total==seqgab[cnt].size()-2){
                            done =true;
                        }
                        if(ada){
                            total++;
                        }
                    }
                    if(done){
                        if(stoi(seqgab[cnt][(seqgab[cnt].size())-1])>max){
                            if((max!=-999&&gabmax.size()>seqgab.size())){
                                max = stoi(seqgab[cnt][(seqgab[cnt].size())-1]);
                                gabmax = seqgab[cnt];
                                koorfix = koor;
                            }
                            else{
                                max = stoi(seqgab[cnt][(seqgab[cnt].size())-1]);
                                gabmax = seqgab[cnt];
                                koorfix = koor;
                            }
                        }
                    }
                    koor.clear();
                    }
                    seqgab[cnt].erase(seqgab[cnt].begin());
            }
        }
        cnt++;
    }

    std::cout <<endl<< "Result Calculated!"<<endl<<"Maximum Weight: " <<max<<endl;
    for (int j = 0; j < gabmax.size()-1; j++) {
        std::cout << gabmax[j] << " ";
    }
    std::cout << endl;
    for (int j = 0; j < koorfix.size(); j++) {
        koorfix[j].cetaktitik();
    }

    auto end = chrono::high_resolution_clock::now();
    double elapsed_time_ms = chrono::duration<double, milli>(end - mulai).count();
    std::cout << "executed in " << elapsed_time_ms << " ms" << endl;

    string sv;
    std::cout << "save it to a file? (y/n) " << endl;
    cin >> sv;

    while(sv!="y"&&sv!="n"){
        std::cout << "Invalid Input!" << endl;
        std::cout << "save it to a file? (y/n) " << endl;
        cin >> sv;
    }

    if(sv=="y"){
        string name,file;
        cout<< "Enter name file: ";
        cin >> name;
        file = "../test/" + name +".txt";

        ofstream fileout(file);

        fileout <<"Maximum Weight: " <<to_string(max)<<"\n";
        for (int j = 0; j < gabmax.size()-1; j++) {
        fileout << gabmax[j] << " ";
        }
        fileout << "\n";
        for (int j = 0; j < koorfix.size(); j++) {
            fileout<<to_string(koorfix[j].y)<<", "<<to_string(koorfix[j].x);
            fileout << "\n";
        }
        fileout << "executed in " << elapsed_time_ms << " ms" << endl;

        fileout.close();
    }
    else{
        cout<<"Okayy, Have a nice day ^^"<<endl;
    }
}
   

int main() {
    int buffer;
    vector<int> bobot;
    vector<vector<string>> sequence;
    Matrix m;

    input(&buffer, bobot, sequence, m);

    solve(&buffer, bobot, sequence, m);
    return 0;
}

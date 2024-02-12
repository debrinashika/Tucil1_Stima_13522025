#include <iostream>
#include <vector>

using namespace std;


class Matrix{
    private:
        int cols;
        int rows;
        vector<vector<int>> isi;
    public:
        Matrix(int rows, int cols){
            this->rows = rows;
            this->cols = cols;
        }
        void setIsian(vector<int> z){
            for(int i = 0; i < rows; i++) {
                for(int j = 0; j < cols; j++) {
                    isi[i][j] = z[j];
                } 
            }
        }
        int getCols() {
            return cols;
        }
        int getRows() {
            return rows;
        }
};
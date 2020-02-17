#include<stdio.h>
#include<stdlib.h>
#include<omp.h>
#define n 1080
int image[n][n];
int mask[3][3] = {{0, -2, 0},
                  {-2, 11, -2},
                  {0, -2, 0}} ;


void laplaceFilteringSerial(){
    int i, j, x, y;
    for(i=0;i<n; i++){
        for(j=0; j<n; j++){
            int sum = 0;
            for(x=0; x<3; x++){
                for(y=0; y<3; y++){
                    if((i==0 && x==0) || (i==n-1 && x==2) || (j==0 && y==0) || (j==n-1 && y==2)){
                        continue;
                    }
                    else{
                        sum += image[i-1+x][j-1+y] * mask[x][y];
                    }
                }
            }
            sum /= 16;
            image[i][j] = sum;
        }
    }
}

void laplaceFilteringParallel(){
    int i, j, x, y, sum;
    #pragma omp parallel for default (none) \
        shared (image, mask) private(i,j,x,y) reduction(+:sum)
            for(i=0;i<n; i++){
                for(j=0; j<n; j++){
                    sum = 0;
                    for(x=0; x<3; x++){
                        for(y=0; y<3; y++){
                            if((i==0 && x==0) || (i==n-1 && x==2) || (j==0 && y==0) || (j==n-1 && y==2)){
                                continue;
                            }
                            else{
                                sum += image[i-1+x][j-1+y] * mask[x][y];
                            }
                        }
                    }
                    sum /= 16;
                    image[i][j] = sum;
                }
            }
}

int main(){

    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            image[i][j] = 1;
        }
    }

    double timeTakenSerial = omp_get_wtime( );
    laplaceFilteringSerial();
    timeTakenSerial = omp_get_wtime( ) - timeTakenSerial;

    printf("Time taken: %14f\n", timeTakenSerial);

    double timeTakenParallel = omp_get_wtime( );
    laplaceFilteringParallel();
    timeTakenParallel = omp_get_wtime( ) - timeTakenParallel;

    printf("Time taken: %14f\n", timeTakenParallel);

    printf("Speedup : %14f\n", timeTakenSerial/timeTakenParallel);

    return 0;
}

#include<stdio.h>
#include<stdlib.h>
#include<omp.h>
#define n 1000
int room[n][n];


void heatDistributionSerial(){
    int i, j;
    for(i=1;i<n-1;i++){
        for(j=1;j<n-1;j++){
            room[i][j] = (room[i-1][j] + room[i][j+1] + room[i+1][j] + room[i][j-1]) / 4 ;
        }
    }
}

void heatDistributionParallel(){
    int i,j;
    #pragma omp parallel for default (none) \
        shared (room) private(i,j)
            for(i=1;i<n-1;i++){
                for(j=1;j<n-1;j++){
                    room[i][j] = (room[i-1][j] + room[i][j+1] + room[i+1][j] + room[i][j-1]) / 4 ;
                }
            }
}

int main(){

    int i, j;

    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            room[i][j] = 0;
        }
    }

    for(i=0; i<n; i++){
        room[i][0] = 20;
        room[i][n-1] = 20;
        room[n-1][i] = 20;
        room[0][i] = 20;
    }
    for(i=(int)(n*3)/10 ; i<(int)(n*7)/10 ; i++){
        room[0][i] = 100;
    }

    double timeTakenSerial = omp_get_wtime( );
    for(i=0;i<100;i++){
        heatDistributionSerial();
    }
    timeTakenSerial = omp_get_wtime( ) - timeTakenSerial;

    printf("Time taken: %14f\n", timeTakenSerial);

    double timeTakenParallel = omp_get_wtime( );
    for(i=0;i<100;i++){
        heatDistributionParallel();
    }
    timeTakenParallel = omp_get_wtime( ) - timeTakenParallel;

    printf("Time taken: %14f\n", timeTakenParallel);

    printf("Speedup : %14f\n", timeTakenSerial/timeTakenParallel);

    return 0;
}

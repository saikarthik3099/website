#include<stdio.h>
#include<stdlib.h>
#include<omp.h>
#define n 1000
float A[n][n+1], B[n][n+1], x[n];

void printMatrix(){
    int i,j;
    for(i=0;i<n;i++){
        for(j=0;j<=n;j++){
            printf("%f ",A[i][j]);
        }
        printf("\n");
    }
}

void printSol(){
	int i;
	for(i=0;i<n;i++){
		printf("%f\t",x[i]);
	}
	printf("\n");
}

void gaussionEliminationSerial(){
    int i,j,k;
    float c, sum = 0.0;

    for(j=0; j<n; j++) /* loop for the generation of upper triangular matrix*/
    {
        for(i=j+1; i<n; i++)
        {
            c=A[i][j]/A[j][j];
            for(k=0; k<=n; k++)
            {
                A[i][k]=A[i][k]-c*A[j][k];
            }
        }
    }

    x[n-1]=A[n-1][n]/A[n-1][n-1];

    for(i=n-2; i>=0; i--) /* this loop is for backward substitution*/
    {
        sum=0;
        for(j=i+1; j<n; j++)
        {
            sum=sum+A[i][j]*x[j];
        }
        x[i]=(A[i][n]-sum)/A[i][i];
    }
}

void gaussionEliminationParallel(){
    int i,j,k;
    float c, sum = 0.0;

    #pragma omp parallel for default (none) shared (A) private(i,j,k,c)
    for(j=0; j<n; j++) /* loop for the generation of upper triangular matrix*/
    {
        for(i=j+1; i<n; i++)
        {
            c=A[i][j]/A[j][j];
            for(k=0; k<=n; k++)
            {
                A[i][k]=A[i][k]-c*A[j][k];
            }
        }
    }
    
    x[n]=A[n-1][n]/A[n-1][n-1];

    #pragma omp parallel for default (none) shared (A,x) private(i,j,sum)
    for(i=n-2; i>=0; i--) /* this loop is for backward substitution*/
    {
        sum=0;
        for(j=i+1; j<n; j++)
        {
            sum=sum+A[i][j]*x[j];
        }
        x[i]=(A[i][n]-sum)/A[i][i];
    }
}

int main()
{
    int i,j;
    
    for(i=0; i<n; i++)
    {
        for(j=0; j<=n; j++)
        {
            B[i][j] = A[i][j] = 1 + rand()%100;
            
        }
    }
    
    double timeTakenSerial = omp_get_wtime( );
    gaussionEliminationSerial();
    timeTakenSerial = omp_get_wtime( ) - timeTakenSerial;

    //printSol();

    printf("Time taken Serial: %14f\n", timeTakenSerial);

    
    for(i=0; i<n; i++)
    {
        for(j=0; j<=n; j++)
        {
            A[i][j] = B[i][j];
        }
    }

    double timeTakenParallel = omp_get_wtime( );
    gaussionEliminationParallel();
    timeTakenParallel = omp_get_wtime( ) - timeTakenParallel;


    printf("Time taken Parallel: %14f\n", timeTakenParallel);

    printf("Speedup : %14f\n", timeTakenSerial/timeTakenParallel);
    
    return 0;
    
    
}

#include<stdio.h>
#include<omp.h>
#define N 10000
#define NUM_THREADS 4
int A[N][N],B[N],C[N];
int main()
{
	int i,j,k;
	double start_time,end_time,t_serial,t_parallel;
	for (i= 0; i< N; i++)
	{
        for (j= 0; j< N; j++)
		{
	            A[i][j] = 2;
		}
		B[i] = 2;
		C[i] = 0;
	}
	
//	serial code
	start_time = omp_get_wtime();
	for (i = 0; i < N; ++i)
	{
        for (j = 0; j < N; ++j)
		{
            C[i] += A[i][j] * B[j];
        }
    }
    end_time = omp_get_wtime();
    t_serial = end_time - start_time;
    printf("Time taken for serial code : %lf\n", t_serial);

//    parallel code
	start_time = omp_get_wtime();
	#pragma omp parallel for private(i,j) shared(A,B,C) num_threads(NUM_THREADS)
	for (i = 0; i < N; ++i)
	{
        for (j = 0; j < N; ++j)
		{
            C[i] += A[i][j] * B[j];
        }
    }
    end_time = omp_get_wtime();
    t_parallel = end_time - start_time;
    printf("Time taken for parallel code : %lf\n", t_parallel);
    printf("Speedup : %lf\n", t_serial/t_parallel);
    return 0;
}

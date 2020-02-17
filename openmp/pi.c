#include<stdio.h>
#include<omp.h>
#define NUM_THREADS 4
long num_steps = 1000000;
int main()
{
	double x,pi, sum = 0.0, d_sum[NUM_THREADS];
	double step,start_time,end_time,t_serial,t_parallel,aux;
	int i,id,nthrds,nthreads;
	step  = 1.0/(double)num_steps;
//	serial code
	start_time = omp_get_wtime();
	for(i = 0; i < num_steps; i++)
	{
		x = (i + 0.5)*step;
		sum += 4.0/(1.0 + x * x);
	}
	pi = step*sum;
	end_time = omp_get_wtime();
	t_serial = end_time - start_time;
	printf("Value of PI in serial code : %lf\n",pi);
	printf("Time taken by serial code : %lf\n\n",t_serial);
	
//	parallel code with critical section
	sum = 0.0;
	start_time = omp_get_wtime();
	#pragma omp parallel for private(i,x,aux) shared(sum) num_threads(NUM_THREADS)
	for(i = 0; i < num_steps; i++)
		{
			x = (i + 0.5)*step;
			aux = 4.0/(1.0 + x * x);
			#pragma omp critical
				sum += aux;
		}

	pi = step * sum;
	end_time = omp_get_wtime();
	t_parallel = end_time - start_time;
	printf("Value of PI in parallel code with CS : %lf\n",pi);
	printf("Time taken by parallel code with CS :%lf\n",t_parallel);
	printf("Speedup : %lf\n\n",t_serial/t_parallel);
	
//	parallel code without critical section
	start_time = omp_get_wtime();
	#pragma omp parallel private(i,id,nthrds,x) num_threads(NUM_THREADS)
	{
		id  = omp_get_thread_num();
		nthrds = omp_get_num_threads();
		if(id == 0) nthreads = nthrds;
		for(i = id, d_sum[id] = 0.0; i < num_steps; i = i + nthrds )
		{
			x = (i + 0.5)*step;
			d_sum[id] += 4.0/(1.0+x*x);
		}
	}
	for(i=0, pi=0.0;i<nthreads;i++)pi += d_sum[i] * step;
	end_time = omp_get_wtime();
	t_parallel = end_time - start_time;
	printf("Value of PI in parallel code without CS : %lf\n",pi);
	printf("Time taken by parallel code without CS :%lf\n",t_parallel);
	printf("Speedup : %lf\n\n",t_serial/t_parallel);
	
//	parallel code with reduction clause
	sum = 0.0;
	start_time = omp_get_wtime();
	#pragma omp parallel private(i,x) reduction(+:sum) num_threads(NUM_THREADS)
	{
		#pragma omp for
		for(i = 0; i < num_steps; i++)
		{
			x = (i + 0.5)*step;
			sum += 4.0/(1.0 + x * x);
		}
	
	}
	pi = step * sum;
	end_time = omp_get_wtime();
	t_parallel = end_time - start_time;
	printf("Value of PI in parallel code with reduction clause : %lf\n",pi);
	printf("Time taken by parallel code with reduction clause :%lf\n",t_parallel);
	printf("Speedup : %lf\n\n",t_serial/t_parallel);
	return 0;
}

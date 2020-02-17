#include<iostream>
#include<omp.h>
#define NUM_ITER 200
using namespace std;

unsigned count;
unsigned lastPrime;

void Primes(int N);
void ParallelPrimes(int N, int P);

bool *flags = NULL;

int main()
{
	int P,N;
	double start_time,end_time,t_serial,t_parallel;
	cout<<"Number of Processes : ";
	cin>>P;
	cout<<"\nProblem Size : ";
	cin>>N;
	cout<<endl;
	flags = new bool[(N-3)/2 + 1];
	
	//serial code
	start_time = omp_get_wtime();
	Primes(N);
	end_time = omp_get_wtime();
    t_serial = end_time - start_time;
    printf("Time taken for serial code : %lf\n", t_serial);
    
    //parallel code
    start_time = omp_get_wtime();
	ParallelPrimes(N,P);
	end_time = omp_get_wtime();
    t_parallel = end_time - start_time;
    printf("Time taken for parallel code : %lf\n", t_parallel);
    printf("Speedup : %lf\n", t_serial/t_parallel);
//	for(int i = 0; i < (N-3)/2 + 1; i++)
//	{
//		if(flags[i])
//		{
//			cout<<2*i + 3<<" ";
//		}
//	}
//	cout<<endl<<lastPrime<<endl;
	
	return 0;
}

void Primes(int N) {
  int i;
  int iter, prime;
  int div1, div2, rem;

  for (iter = 0; iter < NUM_ITER; ++iter)      
  {
    count = 0;
    lastPrime = 0;

    for (i = 0; i < (N-3)/2 + 1; ++i) {    /* For every odd number */
      prime = 2*i + 3;              

      /* Keep searching for divisor until rem == 0 (i.e. non prime),
         or we've reached the sqrt of prime (when div1 > div2) */

      div1 = 1;
      do {                            
        div1 += 2;            /* Divide by 3, 5, 7, ... */
        div2 = prime / div1;  /* Find the dividend */
        rem = prime % div1;   /* Find remainder */
      } while (rem != 0 && div1 <= div2); 

      if (rem != 0 || div1 == prime) {
        /* prime is really a prime */
        flags[i] = true;
        count++;                   
        lastPrime = prime;
      } else {
        /* prime is not a prime */
        flags[i] = false;         
      }
    }
  }
}

void ParallelPrimes(int N, int P) {
  int i;
  int iter, prime;
  int div1, div2, rem;

  for (iter = 0; iter < NUM_ITER; ++iter)      
  {
    count = 0;
    lastPrime = 0;
	#pragma omp parallel for num_threads(P) private(i,prime,div1,div2,rem) shared(N) lastprivate(lastPrime)
    for (i = 0; i < (N-3)/2 + 1; ++i) {    /* For every odd number */
      prime = 2*i + 3;              

      /* Keep searching for divisor until rem == 0 (i.e. non prime),
         or we've reached the sqrt of prime (when div1 > div2) */

      div1 = 1;
      do {                            
        div1 += 2;            /* Divide by 3, 5, 7, ... */
        div2 = prime / div1;  /* Find the dividend */
        rem = prime % div1;   /* Find remainder */
      } while (rem != 0 && div1 <= div2); 

      if (rem != 0 || div1 == prime) {
        /* prime is really a prime */
        flags[i] = true;
        count++;                   
        lastPrime = prime;
      } else {
        /* prime is not a prime */
        flags[i] = false;         
      }
    }
  }
}

#include<stdio.h> 
#include<stdlib.h>
#include<time.h>
#include<omp.h>
#define SIZE 25000
void swap(int* a, int* b) 
{ 
    int t = *a; 
    *a = *b; 
    *b = t; 
} 

int partition(int arr[], int low, int high){
	int i, j, temp, key;
	key = arr[low];
	i= low + 1;
	j= high;
	while(1){
		while(i < high && key >= arr[i])
    			i++;
		while(key < arr[j])
    			j--;
		if(i < j){
			temp = arr[i];
			arr[i] = arr[j];
			arr[j] = temp;
		}
		else{
			temp= arr[low];
			arr[low] = arr[j];
			arr[j]= temp;
			return(j);
		}
	}
}

void parQuickSort(int arr[], int low,int high)
{
	if (low < high) 
    {
        int pi = partition(arr, low, high);
        #pragma omp parallel sections
        {
        	#pragma omp section
        	parQuickSort(arr, low, pi - 1);
        	#pragma omp section
        	parQuickSort(arr, pi + 1, high);
		}
         
    } 
}

void quickSort(int arr[], int low, int high) 
{ 
    if (low < high) 
    {
        int pi = partition(arr, low, high); 
        quickSort(arr, low, pi - 1); 
        quickSort(arr, pi + 1, high); 
    } 
} 
  
int main() 
{ 
    int s_arr[SIZE],p_arr[SIZE]; 
    int n = SIZE;
    int i;
    double start_time,end_time,t_serial,t_parallel;
    srand(time(0));
	for(i = 0; i < n; i++)
	{
			s_arr[i] = rand() % SIZE;
			p_arr[i] = s_arr[i];
	}
	
	//serial code
	start_time = omp_get_wtime();
    quickSort(s_arr, 0, n-1);
    end_time = omp_get_wtime();
    t_serial = end_time - start_time;
    printf("Time taken for serial code : %lf\n", t_serial);
    
    //parallel code
    start_time = omp_get_wtime();
	parQuickSort(p_arr,0,n-1);
	end_time = omp_get_wtime();
    t_parallel = end_time - start_time;
    printf("Time taken for parallel code : %lf\n", t_parallel);
    printf("Speedup : %lf\n", t_serial/t_parallel);
    
    return 0; 
} 

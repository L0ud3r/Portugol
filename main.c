int fatorial(int min,int max){
	int res;
	res = min;
	for(i = min+1.0; i <= max; i++){
res = res*i;
	}
return res;
	}
	int main(){
	int a;
	int b;
	int c;
	a = 3.0;
	b = 10.0;
	c = 15.0;
	printf("%d", a);
	int d;
	d = 0.0;
	while(d <  b) {
printf("%d", d);
	d = d+1.0;
	}
if (a<b){
printf("ola");
	}
else {
	printf("adeus");
	}
	fatorial(1.0,3.0);
	}
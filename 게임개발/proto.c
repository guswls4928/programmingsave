#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int Othello(int L) {
  int a[L+2][L+2];
  int i,j,k,pn=1,cnt=0,pr=0;
  for (i=0; i<L+2; i++){
    for (j=0; j<L+2; j++)
      a[j][i]=0;
  }
  int rem=((L+2)/2);
  a[rem][rem]=2;
  a[rem-1][rem-1]=2;
  a[rem-1][rem]=1;
  a[rem][rem-1]=1;
  int n, m;
  while (cnt!=(L-3)){
    srand(time(0));
  	n=rand()%L+1;
	m=rand()%L+1;
	if (a[n][m]==0){
	  a[n][m]=5;
	  cnt++;
	}
  }
  while(1){
  	int cnt1=0, cnt2=0, cntc=0;
  	int x,y,k=1,wh=0;
    for (i=1; i<=L; i++){
      for (j=1; j<=L; j++){
        if (a[j][i]==0){
          wh=0;
          k=1;
          while (a[j-k][i-k]){
  			if (a[j-k][i-k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j-k][i-k]==3||a[j-k][i-k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;
          while (a[j][i-k]){
  			if (a[j][i-k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j][i-k]==3||a[j][i-k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;
          while (a[j+k][i-k]){
  			if (a[j+k][i-k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j+k][i-k]==3||a[j+k][i-k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;
          while (a[j-k][i]){
  			if (a[j-k][i]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j-k][i]==3||a[j-k][i]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;
          while (a[j+k][i]){
  			if (a[j+k][i]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j+k][i]==3||a[j+k][i]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;		
          while (a[j-k][i+k]){
  			if (a[j-k][i+k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j-k][i+k]==3||a[j-k][i+k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;
          while (a[j][i+k]){
  			if (a[j][i+k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j][i+k]==3||a[j][i+k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }
  		  if(a[j][i]==3)
  		   continue;
  		  k=1;
  		  wh=0;		
          while (a[j+k][i+k]){
  			if (a[j+k][i+k]==pn){
  	  		  if (wh){
  				a[j][i]=3;
				break;	
			  }
  			  else
  			    break;
			}
			else if(a[j+k][i+k]==3||a[j+k][i+k]==5)
			  break;
			else{
			  wh=1;
			  k++;
			}
  		  }		
		}
	  }
    }
    printf("\n");
    for (i=1; i<=L; i++){
      for (j=1; j<=L; j++)
        printf("%d",a[j][i]);
      printf("\n");
    }
    printf("\n");
    for (i=1; i<=L; i++){
      for (j=1; j<=L; j++){
      	if(a[j][i]==1)
      	  cnt1++;
      	else if(a[j][i]==2)
      	  cnt2++;
      	else if(a[j][i]==3)
      	  cntc++;
	  }
    }
  	while (1){
	  if(cntc){
	  	printf("%d�÷��̾���� �����Դϴ�.\n",pn);
  	 	printf("���� ���� ��ǥ�� �Է��ϼ��� : ");
  	  	scanf("%d%d",&x,&y);
  	  	pr=0;
  	  	if (a[x][y]!=3)
  	      printf("�װ����� ���� ���� �� �����ϴ�.\n");
  	  	else
  	      break;
	  }
	  else{
		pr++;
		if(pr>=2){
		  if(cnt1>cnt2)
			return 1;
		  else if(cnt2>cnt1)
		    return 2;
		  else
		    return 0;
		}    
	  	if (pn==1){
		  pn=2;
		  break;
		}	  
		else if(pn==2){
		  pn=1;
		  break;
		}	  
      }
	}
  	a[x][y]=pn;
    for (i=1; i<=L; i++){
      for (j=1; j<=L; j++){
      	if(a[j][i]==3)
      	  a[j][i]==0;
	  }
    }
    while (a[x-k][y-k]){
	  if (a[x-k][y-k]==pn){
  		if (wh){
		  for(i=1; i<k; i++)
			a[x-i][y-i]=pn;
		  break;
		}
		else
		  break;
	  }
	  else if (a[x-k][y-k]==5)
	    break;
	  else{
		wh=1;
		k++;
	  }
	}
  	k=1;
  	wh=0;
  	while (a[x][y-k]){
	  if (a[x][y-k]==pn){
  	    if (wh){
		  for(i=1; i<k; i++)
			a[x][y-i]=pn;
		  break;	
		}
	  	else
	      break;
	  }
	  else if (a[x][y-k]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
    }
  	k=1;
  	wh=0;
  	while (a[x+k][y-k]){
	  if (a[x+k][y-k]==pn){
	    if (wh){
		  for(i=1; i<=k; i++)
			a[x+i][y-i]=pn;
		  break;	
	  	}
	    else
	      break;
	  }
	  else if (a[x+k][y-k]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
    }
  	k=1;
  	wh=0;
 	while (a[x-k][y]){
	  if (a[x-k][y]==pn){
	  	if (wh){
		  for(i=1; i<=k; i++)
			a[x-i][y]=pn;
		  break;	
	  	}
	  	else
	      break;
	  }
	  else if (a[x-k][y]==5)
	    break;
	  else{
		wh=1;
		k++;
	  }
  	}
  	k=1;
  	wh=0;
  	while (a[x+k][y]){
	  if (a[x+k][y]==pn){
	  	if (wh){
		  for(i=1; i<=k; i++)
			a[x+i][y]=pn;
		  break;
	  	}
	  	else
	      break;
	  }
	  else if (a[x+k][y]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
    }
  	k=1;
  	wh=0;		
  	while (a[x-k][y+k]){
	  if (a[x-k][y+k]==pn){
	  	if (wh){
		  for(i=1; i<=k; i++)
			a[x-i][y+i]=pn;
		  break;	
	  	}
	    else
	      break;
	  }
	  else if (a[x-k][y+k]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
  	}
  	k=1;
  	wh=0;
  	while (a[x][y+k]){
	  if (a[x][y+k]==pn){
	  	if (wh){
		  for(i=1; i<=k; i++)
			a[x][y+i]=pn;
		  break;	
	  	}
	  	else
	      break;
	  }
	  else if (a[x][y+k]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
    }
  	k=1;
  	wh=0;		
  	while (a[x+k][y+k]){
	  if (a[x+k][y+k]==pn){
	  	if (wh){
		  for(i=1; i<=k; i++)
			a[x+i][y+i]=pn;
		  break;	
	  	}
	  	else
	      break;
	  }
	  else if (a[x+k][y+k]==5)
	    break;
	  else{
	  	wh=1;
	  	k++;
	  }
    }
    for (i=1; i<=L; i++){
      for (j=1; j<=L; j++){
	  	if (a[j][i]==3)
	  	  a[j][i]=0;
	  }
    }
  	if (pn==1)
  	  pn=2;
  	else
  	  pn=1;
  }
}


int main(){
  int L,result;
  printf("���� ���̸� �Է��ϼ���(6�̻��� ¦��, 8�� ��õ) : ");
  scanf("%d",&L);
  result=Othello(L);
  if (result)
  	printf("%d�÷��̾���� ����ϼ̽��ϴ�.",result);
  else
    printf("���º��Դϴ�.");
  scanf("%d",&L);
}

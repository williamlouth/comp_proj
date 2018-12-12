#include <iostream>
#include <fstream>
#include <math.h>
#include <cmath>
#include <ctime>
#include <iomanip>

#include <vector>

#include "block.h"
#include "type_class.h"


int main()
{
	std::cout << std::setprecision (17);
	/*
	std::cout << "Hello world!";
	float test_array [5][2];
	test_array[0][0] = 2.3;
	test_array[1][2] = 5;
	std::cout << a<< "\n";
	std::cout << a[1][2];
	std::cout << a[0][0];
	std::cout << a[3][0],'\n';
*/
	

	std::cout << "bill";
	double multiple = 3;
	double dist = (1.0/multiple)*pow(10,-3);
	double p = 0.5*pow(10,9);
	
	int height_a =multiple;
	int width_a = multiple*14;
	int height_b = multiple*2;
	int width_b = multiple*20;
	
	int wfmm = 1;
	int hfmm = 30;
	int sfmm = 2;
	int number_f = 25;
	
	int width_f = wfmm*multiple;
	int height_f = hfmm*multiple;
	int seperation_f = sfmm*multiple;

	int height_c = multiple*4;
	int width_c = (width_f * number_f) + (seperation_f*(number_f-1));


	std::vector <block*> block_vector;
	block_vector.resize(3+number_f);
	
	if(width_c<width_b)
	{
		std::cout << "width_c less than width_b";
		return 1;
	}	
	block *a = new block(width_a,height_a,150,p,dist);
	block *b = new block(width_b,height_b,240,0,dist);
	block *c = new block(width_c,height_c,248,0,dist);

	std::cout << "bob";
	block_vector[0] = a;
	block_vector[1] = b;
	block_vector[2] = c;

	std::vector <block*> fins_vector;
	fins_vector.resize(number_f);
	for(int i=0;i<number_f;i++)
	{
		block *d = new block(width_f,height_f,248,0,dist);
		block_vector[3+i] = d;
		fins_vector[i] = d;
	}
	/*block a(28,2,150,1e-9,1e-3);;
	block b(30,2,240,1,1);;
	block c(32,3,248,1,1);;
*/
	a->type_change(b,true,int((width_b-width_a)/2)+1,int((width_b+width_a)/2)-2,1,width_a);
	b->type_change(a,0,1,width_a,int((width_b-width_a)/2)+1,int((width_b+width_a)/2));
	
	b->type_change(c,1,int((width_c-width_b)/2)+1,int((width_c+width_b)/2)-2,1,width_b);
	c->type_change(b,0,1,width_b,int((width_c-width_b)/2)+1,int((width_c+width_b)/2));
	for(int i = 0; i<number_f;i++)
	{
	    	fins_vector[i]->type_change(c,0,1+(width_f+seperation_f)*i,((width_f+seperation_f)*i)+width_f,1,width_f);
	        c->type_change(fins_vector[i],1,1,width_f,(width_f+seperation_f)*i+1,(width_f+seperation_f)*(i)+width_f);
	}



	
	//a->type_change(b,1,0,28,1,29);
	//b->type_change(a,0,0,28,1,29);

	//b->type_change(c,1,0,28,1,29);
	//c->type_change(b,0,0,28,1,29);
	
	double stop_error = 5.0/pow(10,8);
	stop_error = 1e-8;
	stop_error = (1e-7/4014)*((height_a*width_a)+(height_b*width_b)+(height_c*width_c));
	//stop_error = (1e-7/1e2)*(height_a*width_a);
	std::cout << stop_error;
	double before = 10000000000;
	long double after  = 10000000000;
	double error = 1;

	//for(int i = 0;i<1;i++)

	int count_2 =0;
	for(int i=0;i<1000;i++)
	{
		count_2 +=1;
		//std::cout << a->points[4][1]<< "\n";
		std::cout << i<< "\n";
		before = after;
		a->edge_maker();
		a->sor();
		b->edge_maker();
		b->sor();
		c->edge_maker();
		c->sor();
		for(int j=0;j<fins_vector.size();j++)
		{
			fins_vector[j]->edge_maker();
			fins_vector[j]->sor();
		}
	}




	int console_count = 0;
	std::clock_t start;
	start = std::clock();
	int the_count = 0;
	while(std::abs(error) > stop_error)
	//for(int i=0;i<0;i++)
	{
		the_count +=1;
		if(console_count > 1000)
		{
			console_count = 0;
			std::cout << error << "\n";
		}
		console_count +=1;
		before = after;
		a->edge_maker();
		a->sor();
		b->edge_maker();
		b->sor();
		c->edge_maker();
		c->sor();
		for(int j=0;j<number_f;j++)
		{
			fins_vector[j]->edge_maker();
			fins_vector[j]->sor();
		}


		after=0;
		//for(int i=0;i<block_vector.size();i++)
		for(int i=0;i<3;i++)
		{
			for(int j=1;j<block_vector[i]->height-1;j++)
			{
				for(int k=1;k<block_vector[i]->width-1;k++)
				{
					after += block_vector[i]->points[j][k];
					//after += a->points[j][k];
				}
			}
		}
			
		/*{
			for(int j=1;j<a->height-1;j++)
			{
				for(int k=1;k<a->width-1;k++)
				{
					//after += block_vector[i]->points[j][k];
					after += a->points[j][k];
				}
			}
		}*/
		error = std::abs(after-before)/before;
	}

	std::cout << "Time: " << ((std::clock() - start)/(double)(CLOCKS_PER_SEC/1000))/1000 << " s" << "\n";
		
	double max = 0;
	for(int i=1;i<a->height-1;i++)
	{
		for(int j=1;j<a->width-1;j++)
		{
			if(a->points[i][j] > max)
			{
				max = a->points[i][j];
			}
		}
	}
	std::cout << "\n" <<"max a " << max << "\n";
	std::cout << "\n" << a->points[0][1];
	std::ofstream myfile;
	myfile.open("acpp.csv");
	for(int i = 0;i<height_a+2;i++)
	{
		for(int j=0;j<width_a+2;j++)
		{
			myfile << a->points[i][j] <<",";
		}
		myfile<< '\n';
	}
	myfile.close();
	
	std::ofstream myfileb;
	myfileb.open("bcpp.csv");
	for(int i = 0;i<height_b+2;i++)
	{
		for(int j=0;j<width_b+2;j++)
		{
			myfileb << b->points[i][j] <<",";
		}
		myfileb<< '\n';
	}
	myfileb.close();

	std::ofstream myfilec;
	myfilec.open("ccpp.csv");
	for(int i = 0;i<height_c+2;i++)
	{
		for(int j=0;j<width_c+2;j++)
		{
			myfilec << c->points[i][j] <<",";
		}
		myfilec<< '\n';
	}
	myfilec.close();

	std::ofstream myfilef1;
	myfilef1.open("f1cpp.csv");
	for(int i = 0;i<height_f+2;i++)
	{
		for(int j=0;j<width_f+2;j++)
		{
			myfilef1 << block_vector[3]->points[i][j] <<",";
		}
		myfilef1<< '\n';
	}
	myfilef1.close();

	std::ofstream myfilef2;
	myfilef2.open("f2cpp.csv");
	for(int i = 0;i<height_f+2;i++)
	{
		for(int j=0;j<width_f+2;j++)
		{
			myfilef2 << block_vector[4]->points[i][j] <<",";
		}
		myfilef2<< '\n';
	}
	myfilef2.close();
	

	//std::cout << a->points[1,2] - 2*dist*1.31*pow(a->points[1,1]-Ta,4/3)/kappa;
	//std::cout << "\n" <<"hehehehe" <<  a->points[1][2]- 2*dist*1.31*pow(a->points[1][1]-Ta,4.0/3)/kappa << "\n" ;
	//std::cout << "\n" <<"hehehehe" <<  pow((a->points[1][1]-Ta),4.0/3) << "\n" ;
	//std::cout << "\n" <<"hehehehe" <<  a->points[1][1]-Ta << "\n" ;
	//std::cout << "here";
	//std::cout << "\n" << block_vector[3]->bot_type[0]->position;
	//std::cout << "\n" << block_vector[3]->bot_type[1]->position;
	//std::cout << "\n" << block_vector[3]->bot_type[2]->position;
	
	//std::cout << "\n" << block_vector[3]->bot_type[0]->block_reference->points[1][1];
	//std::cout << "\n" << block_vector[3]->bot_type[1]->block_reference->points[1][1];
	//std::cout << "\n" << block_vector[3]->bot_type[2]->block_reference->points[1][1];
	
	//std::cout << "\n \n" << c->points[1][1];
	//std::cout << "\n" << block_vector[3]->points[7][1];
	std::cout << "\n" <<"count_2 " << count_2;

	return 0;
}




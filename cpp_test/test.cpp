#include <iostream>
#include <fstream>
#include <math.h>

#include <vector>

#include "block.h"
#include "type_class.h"

/*class block 
{
	public:
		block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist);
		std::vector <std::vector<float> > points;
		std::vector <type_class> top_type;
		int width;
		int height;
		float kappa;
		float tot_power;
		float dist;




};

block::block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist)
{
	width = in_width+2; //1 layer round edge to hold imaginary points
	height= in_height+2;
	points.resize(width,std::vector<float>(height));
	for(int i=0;i<width;i++)
	{
		for(int j=0;j<height;j++)
		{
			points[i][j] = 30.0;
			std::cout << points[i][j] << '\n';
		}
	}
}

class type_class
{
	public:
		block* block_reference;
		int position;
};
*/
int main()
{
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
	

	float multiple = 3;
	float dist = (1/multiple)*pow(10,-3);
	std::cout <<"\n hi \n" << dist << "\n ho \n";
	float p = 0.5*pow(10,9);
	
	int height_a =multiple;
	int width_a = multiple*14;
	int height_b = multiple*2;
	int width_b = multiple*20;
	
	int wfmm = 1;
	int hfmm = 30;
	int sfmm = 10;
	int number_f = 3;
	
	int width_f = wfmm*multiple;
	int height_f = hfmm*multiple;
	int seperation_f = sfmm*multiple;

	int height_c = multiple*4;
	int width_c = (width_f * number_f) + (seperation_f*(number_f-1));
	
	//std::cout << "\n" << width_c;
	//std::cout << "\n" << width_b;
	if(width_c<width_b)
	{
		std::cout << "width_c less than width_b";
		return 1;
	}	
	block *a = new block(width_a,height_a,150,0,dist);
	//block *b = new block(width_b,height_b,240,0,dist);
	//block *c = new block(width_c,height_c,248,0,dist);

	//std::vector <block*> fins_vector;
	//fins_vector.resize(number_f);
	//for(int i=0;i<number_f;i++)
	//{
	//	block *d = new block(width_f,height_f,248,0,dist);
	//	fins_vector[i] = d;
	//}
	/*block a(28,2,150,1e-9,1e-3);;
	block b(30,2,240,1,1);;
	block c(32,3,248,1,1);;
*/
	//a->type_change(b,true,int((width_b-width_a)/2)+1,int((width_b+width_a)/2)-2,1,width_a-2);
/*	b->type_change(a,0,1,width_a-2,int((width_b-width_a)/2)+1,int((width_b+width_a)/2)-2);
	
	b->type_change(c,1,int((width_c-width_b)/2)+1,int((width_c+width_b)/2)-2,1,width_b-2);
	c->type_change(b,0,1,width_b-2,int((width_c-width_b)/2)+1,int((width_c+width_b)/2)-2);
	for(int i = 0; i<number_f;i++)
	{
	    fins_vector[i]->type_change(c,0,(width_f+seperation_f)*i,((width_f+seperation_f)*i)+width_f-1,1,width_f-2);
	    c->type_change(fins_vector[i],1,1,width_f,(width_f+seperation_f)*i,(width_f+seperation_f)*(i)+width_f-1);
	}

*/

	/*
	a->type_change(b,1,0,28,1,29);
	b->type_change(a,0,0,28,1,29);

	b->type_change(c,1,0,28,1,29);
	c->type_change(b,0,0,28,1,29);
	*/

	for(int i = 0;i<20000;i++)
	{
		a->edge_maker();
		a->solver();
		//b->edge_maker();
		//b->solver();
		//c->edge_maker();
		//c->solver();
		//for(int j=0;j<number_f;j++)
		//{
		//	fins_vector[j]->edge_maker();
		//	fins_vector[j]->solver();
		//}
	}

	//a->edge_maker();
	/*(std::cout << '\n' << b.height << '\n';;
	std::cout << '\n' << "hello" << '\n';;
	//std::cout << b.points[1][2]<<'\n';;
	std::cout << b.points[0][0]<<'\n';;
//	std::cout << b.top_type[0].block_reference<<'\n';;
*/	
	
	std::ofstream myfile;
	myfile.open("a.csv");
	for(int i = 0;i<height_a+2;i++)
	{
		for(int j=0;j<width_a+2;j++)
		{
			myfile << a->points[i][j] <<",";
		}
		myfile<< '\n';
	}
	myfile.close();
	
	return 0;
}




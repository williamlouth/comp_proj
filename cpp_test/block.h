#ifndef BLOCK_H
#define BLOCK_H

#include <iostream>
#include <vector>

class type_class;

class block 
{
	static const float omega = 1.15;
	static const float Ta  = 20;
	//float omega = 1.75;
	public:
		block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist);
		std::vector <std::vector<float> > points;
		std::vector <type_class*> top_type;
		std::vector <type_class*> bot_type;
		int width;
		int height;
		float kappa;
		float tot_power;
		float dist;
		void type_change(block* connected_block,bool top_bot,int block_start_index,int block_end_index,int points_start,int points_end);
		void solver();
		void edge_maker();

		//float omega = 1.75;





};
/*
block::block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist)
{
	std::cout << "\n bill \n";
	width = in_width+2; //1 layer round edge to hold imaginary points
	height= in_height+2;
	points.resize(width,std::vector<float>(height));
	//top_type[0].block_reference = self;
	top_type[0]->position = 0;
	for(int i=0;i<width;i++)
	{
		for(int j=0;j<height;j++)
		{
			points[i][j] = 30.0;
			std::cout << points[i][j] << '\n';
		}
	}
}*/
#endif

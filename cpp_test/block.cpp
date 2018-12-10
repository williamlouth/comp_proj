#include <math.h>

#include "block.h"
#include "type_class.h"


/*
class block 
{
	public:
		block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist);
		std::vector <std::vector<float> > points;
		std::vector <type_class> top_type;
		std::vector <type_class> bot_type;
		int width;
		int height;
		float kappa;
		float tot_power;
		float dist;




};
*/
block::block(int in_width,int in_height,float in_kappa,float in_tot_power,float in_dist)
{
	width = in_width+2; //1 layer round edge to hold imaginary points
	height= in_height+2;
	points.resize(height,std::vector<float>(width));
	kappa = in_kappa;
	tot_power = in_tot_power;
	dist = in_dist;
	

	//type_class a;
	

	top_type.resize(width-2);
	bot_type.resize(width-2);
	/*std::cout << "bob";
	top_type.resize(width);
	std::cout << "\n size top_type " << top_type.size() << "\n";
	std::cout << "hmm \n";
	std::cout << a->position;
	//
	std::cout << "\n hesr";
	std::cout << "\n hes2";

	top_type.push_back(a);
	//top_type[0] = &a;
	std::cout << "\n what";*/
	for(int j=0;j<width-2;j++)
	{
		type_class *a = new type_class(this);
		type_class *b = new type_class(this);
		top_type[j] = a;
		bot_type[j] = b;
	}

	
	//top_type.push_back(this*,0);
	//std::cout << top_type;
	//top_type[0].block_reference = self;
	//top_type[0]->position = 0;
	for(int i=0;i<height;i++)
	{
		for(int j=0;j<width;j++)
		{
			points[i][j] = 30.0;
			//std::cout << points[i][j] << '\n';
		}
	}
}


void block::type_change(block* connected_block,bool top_bot,int block_start_index,int block_end_index,int points_start,int points_end)
{
	
	if(top_bot == true)
	{
		int i = points_end-points_start;
		for(int j = 0;j<i;j++)
		{
			top_type[j+points_start]->block_reference = connected_block;
			top_type[j+points_start]->position = block_start_index+i;
		}
	}
	else
	{
		int i = points_end-points_start;
		for(int j = 0;j<i;j++)
		{
			bot_type[j+points_start]->block_reference = connected_block;
			bot_type[j+points_start]->position = block_start_index+i;
		}
	}


	return;
}


void block::solver()
{
	for(int i=1;i<height-1;i++)
	{
		for(int j=1;j<width-1;j++)
		{
			points[i][j] = points[i][j]*(1-omega) + omega*0.25*(points[i-1][j]+points[i+1][j]+points[i][j+1]+points[i][j-1]+dist*dist*tot_power/kappa);
			points[i][j] = points[i][j]*(1-omega) +omega*0.25*(points[i-1][j]+points[i+1][j]+points[i][j+1]+points[i][j-1]+dist*dist*tot_power/kappa);

			//std::cout << points[i][j];
		}
	}
}



void block::edge_maker()
{
	for(int i=1;i<height-1;i++)
	{
		points[i][0] = points[i][2] - 2*dist*1.31*pow((points[i][1] - Ta),4/3)/kappa;
		points[i][width-1] = points[i][width-3] - 2*dist*1.31*pow((points[i][width-2] - Ta),4/3)/kappa;
		//std::cout << points[width-1][j];
	}
	for(int j=1;j<width-1;j++)
	{
		if(top_type[j-1]->block_reference == this)
		{
			points[0][j] = points[2][j] - 2.0*dist*1.31*pow((points[1][j] - Ta),4.0/3.0)/kappa;
			
		}		
		else
		{
			points[0][j] = top_type[j-1]->block_reference->points[top_type[j-1]->block_reference->height -2][top_type[j-1]->position];
			
		}
		if(bot_type[j-1]->block_reference == this)
		{
			
			points[height-1][j] = points[height-3][j] - 2*dist*1.31*pow((points[height-2][j] - Ta),4.0/3.0)/kappa;

		}		
		else
		{
			points[height-1][j] = bot_type[j-1]->block_reference->points[1][bot_type[j-1]->position];
		}
	}
}





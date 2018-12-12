#ifndef BLOCK_H
#define BLOCK_H

#include <iostream>
#include <vector>

class type_class;

class block 
{
	static const long double omega = 1;
	static const long double Ta  = 20;
	//float omega = 1.75;
	public:
		block(int in_width,int in_height,long double in_kappa,long double in_tot_power,long double in_dist);
		std::vector <std::vector<long double> > points;
		std::vector <type_class*> top_type;
		std::vector <type_class*> bot_type;
		int width;
		int height;
		long double kappa;
		long double tot_power;
		long double dist;
		void type_change(block* connected_block,bool top_bot,int block_start_index,int block_end_index,int points_start,int points_end);
		void jacobi();
		void sor();
		void edge_maker();

		//float omega = 1.75;





};

#endif

#include "type_class.h"
#include "block.h"
#include <iostream>

/*class type_class
{
	public:
		type_class();
		block* block_reference;
		int position;
};
*/
type_class::type_class(block* start_block)
{
	block_reference = start_block;
	position = 0;
	//std::cout << "\n  position " << position << "\n";
}



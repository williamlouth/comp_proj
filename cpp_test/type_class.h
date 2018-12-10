#ifndef TYPE_CLASS_H
#define TYPE_CLASS_H
class block;

class type_class
{
	public:
		type_class(block* start_block);
		block* block_reference;
		int position;
};



#endif

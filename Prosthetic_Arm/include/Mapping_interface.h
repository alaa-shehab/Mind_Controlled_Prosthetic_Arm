/******************************************************/
/******************************************************/
/**********      AUTHOR: Raghad Mohamed      **********/
/**********      Layer: Library              **********/
/**********      SWC: Mapping                **********/
/**********      Date: 2-10-2020             **********/
/**********      Version: 1.00               **********/
/******************************************************/
/******************************************************/

#ifndef MAPPING_INTERFACE_H_
#define MAPPING_INTERFACE_H_

typedef struct {

	s32 InputRangeMinimum;
	s32 InputRangeMaximum;
	s32 OutputRangeMinimum;
	s32 OutputRangeMaximum;

}MAP_T;


s32 Map_s32(MAP_T * Copy_puMAP_T_Map_config, s32 Copy_s32InputValue);



#endif

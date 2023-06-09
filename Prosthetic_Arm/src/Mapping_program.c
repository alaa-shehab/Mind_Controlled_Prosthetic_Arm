/******************************************************/
/******************************************************/
/**********      AUTHOR: Raghad Mohamed      **********/
/**********      Layer: Library              **********/
/**********      SWC: Mapping                **********/
/**********      Date: 2-10-2020             **********/
/**********      Version: 1.00               **********/
/******************************************************/
/******************************************************/

#include "STD_TYPES.h"

#include "Mapping_interface.h"

s32 Map_s32(MAP_T * Copy_puMAP_T_Map_config, s32 Copy_s32InputValue) {

	s32 Local_s32Output;
	s32 Local_OutputDif = Copy_puMAP_T_Map_config ->OutputRangeMaximum - Copy_puMAP_T_Map_config -> OutputRangeMinimum;
	s32 Local_InputDif  = Copy_puMAP_T_Map_config ->InputRangeMaximum  - Copy_puMAP_T_Map_config -> InputRangeMinimum;
	s32 Local_Input_Calc = Copy_s32InputValue - Copy_puMAP_T_Map_config -> InputRangeMinimum;

	Local_s32Output = (s32) ( (Local_OutputDif * Local_Input_Calc) / Local_InputDif);
	Local_s32Output = (s32) (Local_s32Output + Copy_puMAP_T_Map_config -> OutputRangeMinimum);
	return Local_s32Output;



}

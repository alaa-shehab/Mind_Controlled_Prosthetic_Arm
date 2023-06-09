#include "STD_TYPES.h"
#include "BIT_MATH.h"
#include "Mapping_interface.h"

#include "RCC_interface.h"
#include "GPIO_interface.h"
#include "TIMERS_interface.h"

#include "Servo_interface.h"
#include "Servo_config.h"
#include "Servo_private.h"

MAP_T ServoAngleMap = {0, 100, 650, 3000};
//MAP_T ServoAngleMap = {0, 180, 2500, 19000};

Servo_t  Servo_attach(u8 Copy_u8Port,u8 Copy_u8Pin) {

	Servo_t servo = {Copy_u8Port, Copy_u8Pin, 0, 0, YES};
	GPIO_u8SetPinMode(servo.ServoPort, servo.ServoPin, GPIO_PIN_MODE_AF_PP_10MHZ);


	switch(Copy_u8Port) {
	case(GPIO_PORTA):
			switch(Copy_u8Pin){
			case(GPIO_PIN0): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL1; break;
			case(GPIO_PIN1): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL2; break;
			case(GPIO_PIN2): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL3; break;
			case(GPIO_PIN3): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL4; break;
			case(GPIO_PIN6): servo.ServoTimer = TIMER3; servo.ServoChannel = CHANNEL1; break;
			case(GPIO_PIN7): servo.ServoTimer = TIMER3; servo.ServoChannel = CHANNEL2; break;
			default: break;
			}
			break;
	case(GPIO_PORTB):
			switch(Copy_u8Pin){
			case(GPIO_PIN0): servo.ServoTimer = TIMER3; servo.ServoChannel = CHANNEL3; break;
			case(GPIO_PIN1): servo.ServoTimer = TIMER3; servo.ServoChannel = CHANNEL4; break;
			case(GPIO_PIN3): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL2; break;
			case(GPIO_PIN4): servo.ServoTimer = TIMER3; servo.ServoChannel = CHANNEL1; break;
			case(GPIO_PIN5): servo.ServoTimer = TIMER2; servo.ServoChannel = CHANNEL2; break;
			default: break;
			}
			break;
	}

	return servo;

}



void Servo_init(void) {

	TIMER2_init();
	TIMER3_init();

}

//21500
void Servo_setAngle(Servo_t Servo, u16 Copy_u16Angle) {

	u16 Local_u16MappedValue = Map_s32(&ServoAngleMap, Copy_u16Angle);
	TIMERS_setCompareMatchValue(Servo.ServoTimer, Servo.ServoChannel, Local_u16MappedValue);
//	TIMERS_setCompareMatchValue(Servo.ServoTimer, Servo.ServoChannel, 2010);


}


void Servo_rotateRight(Servo_t Servo) {

	TIMERS_setCompareMatchValue(Servo.ServoTimer, Servo.ServoChannel, 2010);


}

void Servo_rotateLeft(Servo_t Servo) {

	TIMERS_setCompareMatchValue(Servo.ServoTimer, Servo.ServoChannel, 21500);


}




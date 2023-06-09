/*
 * main.c
 *
 *  Created on: 27 Dec 2022
 *      Author: es-RaghadAly2023
 */

#include "STD_TYPES.h"
#include "DELAY_interface.h"

#include "RCC_interface.h"
#include "GPIO_interface.h"
#include "TIMERS_interface.h"
#include "USART_interface.h"
#include "NVIC_interface.h"
#include "Servo_interface.h"

void main(void) {

	RCC_voidInit();
	RCC_u8EnablePeripheralClock(GPIOA);
	RCC_u8EnablePeripheralClock(GPIOB);
	RCC_u8EnablePeripheralClock(GPIOC);

	RCC_u8EnablePeripheralClock(USART1);
	RCC_u8EnablePeripheralClock(USART2);

	NVIC_voidEnableInterrupt(NVIC_USART1);

	RCC_u8EnablePeripheralClock(TIM2);
	RCC_u8EnablePeripheralClock(TIM3);

	Servo_t little_finger_servo = Servo_attach(GPIO_PORTA, GPIO_PIN6);
	Servo_t ring_finger_servo = Servo_attach(GPIO_PORTA, GPIO_PIN7);
	Servo_t middle_finger_servo = Servo_attach(GPIO_PORTB, GPIO_PIN0);
	Servo_t index_finger_servo = Servo_attach(GPIO_PORTB, GPIO_PIN1);
	Servo_t thumb_servo = Servo_attach(GPIO_PORTA, GPIO_PIN1);
	Servo_t wrist_servo = Servo_attach(GPIO_PORTA, GPIO_PIN0);

	USART_voidInit();

	GPIO_u8SetPinMode(GPIO_PORTA, USART1_TX_PIN, GPIO_PIN_MODE_AF_PP_10MHZ);
	GPIO_u8SetPinMode(GPIO_PORTA, USART1_RX_PIN, GPIO_PIN_MODE_FLOATING_INPUT);

	GPIO_u8SetPinMode(GPIO_PORTA, USART2_TX_PIN, GPIO_PIN_MODE_AF_PP_10MHZ);
	GPIO_u8SetPinMode(GPIO_PORTA, USART2_RX_PIN, GPIO_PIN_MODE_FLOATING_INPUT);


	Servo_init();

	u8 Local_u8ReceivedData = 0;

	USART_u8SendDataSynchronous(USART_SERIAL2, 'H');
	USART_u8SendDataSynchronous(USART_SERIAL2, 'i');


	while (1) {



		USART_u8ReceiveDataSynchronous(USART_SERIAL2, &Local_u8ReceivedData);
		if (Local_u8ReceivedData == 'a') {
			Servo_setAngle(wrist_servo, 180);

		} else if (Local_u8ReceivedData == 'b') {
			Servo_setAngle(wrist_servo, 0);

		}

	}
}

# i-cube_lrwan notes
* icube-lrwan lorawan library supports different IDEs and toolchains using for embedded systems development. This library contains preconfigured project files for multiple toolchains like EWARM (IAR Embedded Workbench for ARM), MDK-ARM (Keil Microcontroller Development Kit for ARM) and STM32CubeIDE.
* The SubGHz_Phy project in the cube-lrwan STM32 library is a reference project designed to provide a hardware abstraction layer for the Sub-GHz radio frequency (RF) hardware, such as the Semtech SX1276/1278 (used in STM32WL and external radios with STM32).When to Use SubGHz_Phy
   * Point-to-Point Communication: If your application only needs two devices communicating directly without a LoRaWAN gateway.
   * Custom Protocols: When building a proprietary protocol stack that doesn't adhere to LoRaWAN specifications.
   * Radio Evaluation: For testing and evaluating Sub-GHz performance parameters.
* The LoRaWAN_AT_Master and LoRaWAN_AT_Slave projects are reference implementations In the I-CUBE-LRWAN library provided by STMicroelectronics. designed to demonstrate AT-command-based communication over LoRaWAN. 
* The LoRaWAN_End_Node project is a reference implementation in the I-CUBE-LRWAN library which is a fully functional implementation of a LoRaWAN end device that interacts with a LoRaWAN network server using the LoRaWAN protocol stack.
* find where is data sending file and portion of code in icube-lrwan lorawan library
    * it seems like present in LoRaWAN/App/lora_app.c
* where to add credentials
    * seems like LoRaWAN/App/se-identity.h
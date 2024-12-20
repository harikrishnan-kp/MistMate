# i-cube_lrwan notes
* icube-lrwan lorawan library supports different IDEs and toolchains using for embedded systems development. This library contains preconfigured project files for multiple toolchains like EWARM (IAR Embedded Workbench for ARM), MDK-ARM (Keil Microcontroller Development Kit for ARM) and STM32CubeIDE.
* find where is data sending file and portion of code in icube-lrwan lorawan library
    * it seems like present in LoRaWAN/App/lora_app.c
* mbedTLS in the I-CUBE-LRWAN library is a lightweight, portable cryptographic library provided by Arm, integrated into the stack to handle security features required by the LoRaWAN protocol and related applications. It provides a collection of cryptographic primitives and protocols essential for secure communication in IoT systems.
* to change APB/OTA edit keys etc.
    * reference project/.../LoRaWAN_End_Node/LoRaWAN/App/se-identity.h
* to change frequency plan: 
    * reference project/.../LoRaWAN_End_Node/LoRaWAN/App/lora_app.h
* details of regional parameters and frequency plans
    * Middlewares/Third_Party/LoRaWAN/Mac     
* drivers,middlewares,utilities folder contain support for many hardwares it is a common resource application layer
* in every projects applictaion layer is the only thing which is changing. 
* stmcubeide does not copy common utilities files to apllication layer in a projject.instead it resolve by linking the files by adding file paths to makefile.(changing make file is automatically done by stmcubeIDE)

## Example projects
* The LoRaWAN_End_Node project is a reference implementation in the I-CUBE-LRWAN library which is a fully functional implementation of a LoRaWAN end device that interacts with a LoRaWAN network server using the LoRaWAN protocol stack.
* The LoRaWAN_AT_Master and LoRaWAN_AT_Slave projects are reference implementations In the I-CUBE-LRWAN library provided by STMicroelectronics. designed to demonstrate AT-command-based communication over LoRaWAN. 
* The SubGHz_Phy project in the cube-lrwan STM32 library is a reference project designed to provide a hardware abstraction layer for the Sub-GHz radio frequency (RF) hardware, such as the Semtech SX1276/1278 (used in STM32WL and external radios with STM32).When to Use SubGHz_Phy
   * Point-to-Point Communication: If your application only needs two devices communicating directly without a LoRaWAN gateway.
   * Custom Protocols: When building a proprietary protocol stack that doesn't adhere to LoRaWAN specifications.
   * Radio Evaluation: For testing and evaluating Sub-GHz performance parameters.

## Driver layer
* HAL, BSP and CMSIS are the foundational layers of drivers.
* CMSIS (Cortex Microcontroller Software Interface Standard):
    * it is a software framework developed by Arm that provides a standardized interface for ARM Cortex-M-based microcontrollers.
    * It abstracts core-level functionality, making it easier to develop applications that are portable across different microcontroller vendors.
    * Provides access to ARM Cortex-M core-specific features, such as interrupts, system timers, and CPU registers.
    * CMSIS it is essential for the proper functioning of HAL and BSP. It also provides additional capabilities like DSP libraries and precise control over the core that HAL and BSP do not offer.
* HAL (Hardware Abstraction Layer):
    * it is a layer of software provided by microcontroller vendors (such as STMicroelectronics for STM32 devices) that abstracts the hardware specific details of peripherals. 
    * HAL simplifies the process of firmware development by providing high-level APIs for configuring and operating hardware peripherals such as GPIO, UART, SPI, I2C, ADC and more, without needing to directly manipulate hardware registers.
* BSP (Board Support Package): 
    * it is a layer of software designed to abstract the hardware-specific details of the STM32 microcontroller and its peripherals.
    * Provides drivers and APIs for board-specific components like LEDs, buttons, and external sensors.
    * Builds on HAL to simplify interaction with onboard peripherals.
    * The BSP ensures that the same LoRaWAN stack and application code can run on different STM32 boards without significant modification.

    <img src=../img/driver_dif.png>
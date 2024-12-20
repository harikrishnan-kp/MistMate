# STM32Cube IDE Notes
## Some hidden files in project repo
* **.cproject and .project** : These are part of the project management system in STM32CubeIDE, which is based on Eclipse.
   * .cproject : This is an Eclipse-based file that stores configuration data for your C/C++ project, such as compiler settings, include paths, and build options.
   * .project : Another Eclipse file, which defines general project metadata such as the project name, type, and linked resources.

* **.launch** : This file contains debug or run configurations. It is used to define how the IDE should interact with the microcontroller during debugging or execution. It stores parameters such as:
   * The debugging interface (e.g., ST-LINK)
   * Memory mappings
   * Reset configurations

* **.settings Folder** : This folder contains various configuration files, often used by Eclipse-based IDEs to store workspace-specific settings. Examples include:
   * Compiler-specific settings
   * Code formatting rules
   * Build configurations

* **.mxproject** : this file works in conjunction with the .ioc file to define project-specific settings in STM32CubeMX, the .mxproject file is in XML format and stores project-related metadata.which may include:
   * The STM32CubeMX version used.
   * IDE settings (e.g., whether the project is for STM32CubeIDE or another toolchain).
   * Build toolchain and environment preferences.
   * Information about the project's name, paths, and configurations.
# Verilog Gadget for Sublime Text
==================================

Use **Command Palette (ctrl+shift+p)** or **Right-Click (context menu)** to run.
The context menu only can be seen for .v, .vh, .sv, .svh file.
You can see `View Log` command of context menu only for .log file.

* **Verilog Gadget: Instantiate Module**
	- Parse module ports in currently open file
	- Generate its instance text
	- Copy generated text to clipboard
	- Paste the text on where you want
	- Support Verilog-1995, Verilog-2001 style ports and parameters
```Verilog
	e.g)
		module test #(parameter WIDTH = 3)(input [WIDTH - 1:0] a, output [WIDTH - 1:0] b);
		endmodule

		--> generate
		test #(.WIDTH(WIDTH)) inst_test (.a(a), .b(b));
```

* **Verilog Gadget: Generate Testbench**
	- Parse module ports in currently open file
	- Generate a simple testbench with its instance and signals
	- Testbench will be generated as a systemverilog file
	- Support Verilog-1995, Verilog-2001 style ports and parameters
```Verilog
	e.g)
		module test #(parameter WIDTH = 3)(input [WIDTH - 1:0] a, output [WIDTH - 1:0] b);
		endmodule

		--> generate
		`timescale 1ns/1ps

		module tb_test (); /* this is automatically generated */
			logic rstb;
			logic clk;
			...
			parameter WIDTH = 3;
			...
			logic [WIDTH - 1:0] a;
			logic [WIDTH - 1:0] b;

			test #(.WIDTH(WIDTH)) inst_test (.a(a), .b(b));

			initial begin
			...
		endmodule
```

* **Verilog Gadget: Insert Template**
	- Insert user-template text from the file specified in settings
	- Multiple templates are possible
```json
	e.g)
		In settings :

		"templates": [
			[ "Default", "D:/Temp/verilog_template.v" ],
			[ "FSM", "D:/Temp/verilog_fsm_template.v" ]
		]
```

* **Verilog Gadget: Insert Header**
	- Insert header-description from the file specified in settings
	- {DATE} will be replaced with current date
	- {YEAR} will be replaced with this year
	- {TIME} will be replaced with current time
	- {FILE} will be replaced with current file name
	- {TABS} will be replaced with current tab size
	- {SUBLIME_VERSION} will be replaced with current sublime text version
```Verilog
	e.g)
		In settings :

		"header": "D:/Temp/verilog_header.v"

		//
		// -----------------------------------------------------------------------------
		// Copyright (c) 2014-{YEAR} All rights reserved
		// -----------------------------------------------------------------------------
		// Author : yongchan jeon (Kris) poucotm@gmail.com
		// File   : {FILE}
		// Create : {DATE} {TIME}
		// Editor : sublime text{SUBLIME_VERSION}, tab size ({TABS})
		// -----------------------------------------------------------------------------

		--> after insertion

		//
		// -----------------------------------------------------------------------------
		// Copyright (c) 2014-2016 All rights reserved
		// -----------------------------------------------------------------------------
		// Author : yongchan jeon (Kris) poucotm@gmail.com
		// File   : abc.v
		// Create : 2016-06-03 22:34:43
		// Editor : sublime text3, tab size (3)
		// -----------------------------------------------------------------------------
```

* **Verilog Gadget: Repeat Code with Numbers**
	- Select codes to be repeated, it may include Python's format symbol like {...}
	- Run 'Repeat Code with Numbers' command (default key map : ctrl+f12)
	- Type a range in the input panel as the following : [from]~[to],[step]
	`(e.g. 0 ~ 10 or 0 ~ 10, 2 or 10 ~ 0, -1 ...)`
	- The codes will be repeated with incremental or decremental numbers
	- In order to repeat line by line, the codes should include start of next line (\n:line feed)
	- Python's format symbol supports variable formats : binary, hex, leading zeros, ...
	- To use '{' as is, you should type twice as '{{'
	- Refer to Python's format symbol here, [https://www.python.org/dev/peps/pep-3101/](https://www.python.org/dev/peps/pep-3101/)
	- For **sublime text 2 (python 2.x)**, you should insert index behind of ':' in curly brackets like `foo {0:5b} bar {1:3d}`
```Verilog
	e.g)
		case (abc)
			5'b{:05b} : def <= {:3d};

		--> select `	5'b{:05b} : def <= {:3d};`, run the command and type the range 0~10
		case (abc)
			5'b{:05b} : def <= {:3d};
			5'b00000 : def <=   0;
			5'b00001 : def <=   1;
			5'b00010 : def <=   2;
			5'b00011 : def <=   3;
			5'b00100 : def <=   4;
			5'b00101 : def <=   5;
			5'b00110 : def <=   6;
			5'b00111 : def <=   7;
			5'b01000 : def <=   8;
			5'b01001 : def <=   9;
			5'b01010 : def <=  10;
```

* **Verilog Gadget: View Log**
	- It highlights Error/Warning syntax (Monokai theme base)
	- It is possible to go to Error/Warning positions of files in a log by double-click
	- For relative path, it automatically searches a base directory near the log file
	- Open `xxx.log` file and run `View Log` by righ-click (context menu)
	- Summary will be shown in the output panel ("log_panel": true in settings)
	- The output panel can be toggled by ctrl+f11 (default)
	- Only errors can be displayed in the output panel ("error_only: true in settings")
	- Log syntaxs will be continuosly updated for various vendor's tools (Synopsys, Cadence, Mentor, Xilinx, Altera,...)

   ![Image of Verilog Gadget](https://raw.githubusercontent.com/poucotm/Links/master/image/view_log.png)

## issues

When you have an issue, tell me through [https://github.com/poucotm/Verilog-Gadget/issues](https://github.com/poucotm/Verilog-Gadget/issues), or send me an e-mail poucotm@gmail.com, yongchan.jeon@samsung.com
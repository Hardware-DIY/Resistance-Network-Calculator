# Resistance-Network-Calculator
This Python program selects 1-3 resistors from a given list to form a two-terminal network, aiming to match a user-specified resistance value.Users can define resistor values via CSV files, set the number of resistors, specify tolerance, and choose if each resistor can only be used once.

#Features:
Precision Resistance Calculation: Achieve nearly any desired resistance using a limited set of resistors.
Combination of Measured Resistors: Combine several precisely measured but low-accuracy resistors to achieve an accurate target resistance.
Customizable Resistor Values: Define resistor types via CSV files in the data folder.
Configurable Parameters:
Number of Resistors: Choose how many resistors (1-3) to use in the calculation.
Tolerance: Specify the acceptable precision for the target resistance value.
Single Use Option: Restrict each resistor value to be used only once in a combination.

#How to Use:
Define Resistor Values: Populate the data folder with CSV files containing the resistor values.
Specify Target Resistance: Input the desired resistance value.
Set Parameters: Configure the number of resistors, tolerance, and whether each resistor can be used only once.
Get Results: The program will suggest resistor combinations and display the corresponding circuit diagrams.

程序功能：从给定的阻值列表中选取1-3个电阻，组成二端电阻网络，并使得这个电阻网络的等效阻值尽可能接近用户指定的数值。程序考虑到了全部的7种不同的电阻连接方式，并会在点击一条结果后显示对应的连接示意图。此程序可以帮你用有限种类的电阻得到几乎任意一个阻值，也可以用于将几个经过精确测量但精度较差的电阻组合起来得到精准的阻值。电阻的种类可以通过data文件夹下的csv文件定义。

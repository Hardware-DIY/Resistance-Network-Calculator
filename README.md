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

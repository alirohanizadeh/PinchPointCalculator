# Pinch Point Calculator 

This project contain a UI that can collect user input containing hot and cold kind of data of supply temp, target temp, FCP, h, and deltaT min, then calculate hot scale, cold scale, factors, Qhmin, Qcmin, Amin, pinch point, and also plot GCC and CC.

## Installation

To install this project, you need to have Python 3 and pip installed on your system. Then, you can clone this repository using the following command:

```bash
git clone https://github.com/alirohanizadeh/PinchPointCalculator.git

Next, you need to install the required dependencies using the following command:

pip install -r requirements.txt

Usage
To run this project, you can use the following command:

python main.py

This will launch the UI. 
![UI_Page1]([0](images/Example.jpg)
You can then enter the data for the hot and cold streams in the input fields and click "Add" to add them to the list, when you are done with the temperature stream now you have to add deltaT min. 
![UI_Page1]([1](images/UI_Page1.png)
now you can use the "Save and Calculate" button to reach the next page and see the results. 
![UI_Page2]([2](images/UI_Page2.png)
The UI will display the results and you can use the "GCC Plot" and "CC Plot" buttons to graph GCC and CC. 

![UI_Page1]([3](images/GCC_Plot.png)

![UI_Page1]([4](images/CC_Plot.png)

Dependencies
This project depends on the following Python libraries:

•  PyQt5: A GUI framework for building the UI

•  NumPy: A library for scientific computing

•  Matplotlib: A library for plotting graphs 

Contributing
If you want to contribute to this project, please follow these steps:

•  Fork this repository

•  Create a new branch with a descriptive name

•  Make your changes and commit them

•  Push your branch to your fork

•  Open a pull request and describe your changes

Contact
If you have any questions or feedback, please contact me at ali.rohanizadeh@gmail.com.
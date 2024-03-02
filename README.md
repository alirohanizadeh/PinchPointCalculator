# Pinch Point Calculator  

The pinch point is the point of closest temperature approach between the hot and cold streams in the heat exchanger network (HEN). It determines the minimum energy requirement and the maximum heat recovery of the network. The grand composite curve (GCC) and the composite curve (CC) are graphical tools that show the temperature and enthalpy profiles of the hot and cold streams in the network. They can be used to identify the pinch point, the utility requirements, and the heat exchanger matches.

The input parameters are:

•  Supply temp: The inlet temperature of the hot or cold stream in °C. The typical range is from 0 to 500 °C.

•  Target temp: The outlet temperature of the hot or cold stream in °C. The typical range is from 0 to 500 °C.

•  FCP: The flowrate times the heat capacity of the hot or cold stream in kW/°C. The typical range is from 0 to 1000 kW/°C.

•  h: The overall heat transfer coefficient of the heat exchanger in kW/m^2 °C. The typical range is from 0 to 1000 kW/m^2 °C.

•  deltaT min: The minimum temperature difference allowed between the hot and cold streams in the network in °C. The typical range is from 1 to 30 °C.

The output parameters are:

•  Hot scale: The scaling factor for the hot stream in °C. It is calculated as deltaT min / 2.

•  Cold scale: The scaling factor for the cold stream in °C. It is calculated as -deltaT min / 2.

•  Factors: The factors for each stream that are used to plot the GCC and CC. They are calculated as FCP * (target temp - supply temp) for the hot streams and -FCP * (target temp - supply temp) for the cold streams.

•  Qhmin: The minimum hot utility requirement of the network in kW. It is calculated as the sum of the factors of the hot streams minus the sum of the factors of the cold streams.

•  Qcmin: The minimum cold utility requirement of the network in kW. It is calculated as the maximum of zero and the negative of Qhmin.

•  Amin: The minimum heat transfer area of the network in m^2. It is calculated as the sum of the factors of the streams divided by the h value.

•  Pinch point: The pinch temperature of the network in °C. It is calculated as the supply temp of the hot stream with the lowest supply temp plus the hot scale, or the target temp of the cold stream with the highest target temp plus the cold scale, whichever is lower.

•  GCC and CC: The graphs that show the temperature and enthalpy profiles of the hot and cold streams in the network. They are plotted using the factors and the scaled temperatures of the streams.

The UI allows the user to enter the data for the hot and cold streams in the input fields and click "Add" to add them to the list. The UI validates the input data and shows an error message if the data is invalid or incomplete. When the user is done with the temperature stream, they have to add deltaT min. Then, they can use the "Save and Calculate" button to reach the next page. The UI displays the results and the user can use the "GCC Plot" and "CC Plot" buttons to graph GCC and CC.

The following image show an example of the HEN problem with two hot streams and two cold streams:
![Exapmle]([0](images/Example.jpg) 

The following screenshots show the UI and the results for the related problem:
![UI_Page1]([1](images/UI_Page1.png) 
![UI_Page2]([2](images/UI_Page2.png) 
![GCC_Plot]([3](images/GCC_Plot.png) 
![CC_Plot]([4](images/CC_Plot.png)

## Installation

To install this project, you need to have Python 3 and pip installed on your system. Then, you can clone this repository using the following command:

```bash
git clone https://github.com/alirohanizadeh/PinchPointCalculator.git 
```

Next, you need to install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
Usage
To run this project, you can use the following command:
```bash
python main.py
```
This will launch the UI.  

## Dependencies
This project depends on the following Python libraries:

•  PyQt5: A GUI framework for building the UI

•  NumPy: A library for scientific computing

•  Matplotlib: A library for plotting graphs 

## Contributing
If you want to contribute to this project, please follow these steps:

•  Fork this repository

•  Create a new branch with a descriptive name

•  Make your changes and commit them

•  Push your branch to your fork

•  Open a pull request and describe your changes

### Contact
If you have any questions or feedback, please contact me at ali.rohanizadeh@gmail.com.
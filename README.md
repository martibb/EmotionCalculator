# EmotionCalculator
EmotionCalculator is a web application that allows the user to classify a specific emotion using the James Russel valence-arousal domain.

![The Application working in PCA Components mode after a submit operation.](https://user-images.githubusercontent.com/112756894/213936360-2c614f04-b2da-48b9-a29f-24f3ca3caed9.png)

*The Application working in PCA Components mode after a submit operation.*

## The idea and the dataset used
The idea is to use for that purpose a set of data obtained from research conducted on 32 people while having a conversation on social issues. These people, of various genres, ages, and ethnicities, were equipped with sensors that allow us to know different biometric information such as heart rate and brain signals. The emotions they felt have been discussed at the end using a numeric rate with two integer values from 1 to 5: valence and arousal. These values can be used to identify the specific emotion in the valence-arousal domain: the James Russel model as mentioned before.

The dataset is called **K-EmoCon**. It's not public, so the application considers the presence of a folder called *data* inside the *App* folder with the dataset in question which is not present in this repository.

## Data mining
Before developing the application we did a **preprocessing** phase to clean the data and to obtain a single table to work on, and then we proceeded with a **classification**. We compared different classifiers, and we concluded that Random Forest is the best one in this case. We also worked with the *Principal Component Analysis* model, using as aggregation criterion of the features the similarity of sensors signals. Also a **Feature Importance analysis** has been conducted.
The code is available in **preprocessing.py**, **classification.py**, and **program.py**; **corrplot.png** shows the Correlation Matrix.

## Developing
The EmotionCalculator app has been built using HTML, CSS, and Javascript with the usage of Flask to run the python scripts used specifically for the application.
It works in two modes: the **General mode** (with a slider per feature) and the **PCA Components mode** (with a slider per column obtained after the aggregation with Principal Component Analysis). It is possible to *set the value of each slider* by scrolling the slider with the mouse, or by editing its numerical value visible below it: after selecting it, it is necessary to enter the desired value and then press the enter key. The *Submit* button allows the sliders’ set values to be used to **predict Valence and Arousal** using the model. In addition, the submit operation also allows you to get the **corresponding emotion** in the right pane of the Valence and Arousal sliders, and the **graphs related to the Feature Importance Analysis**, which you can view by clicking on the *Feature Importance* button. For more instruction about the usage, a button *Instruction Manual* has been added to the application interface.

For more information about the overall topic of predicting emotions using sensors data, valence-arousal domain, data mining phase, or the application itself, read the *Technical Report* in the Documentation folder.

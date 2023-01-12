/**************** Constants and variables ****************/

/* Constant where the valence-arousal domain has been mapped in a [1,5] domain: */
const valenceArousalDomain = {
  1: {
    1: "boredom",
    2: "disappointment",
    3: "sadness",
    4: "fear",
    5: "anger"
  },
  2: {
    1: "relaxation",
    2: "frustration",
    3: "relaxation",
    4: "anxiety",
    5: "anger"
  },
  3: {
    1: "contentment",
    2: "neutrality",
    3: "calm",
    4: "enthusiasm",
    5: "excitement"
  },
  4: {
    1: "happiness",
    2: "love",
    3: "happiness",
    4: "enthusiasm",
    5: "excitement"
  },
  5: {
    1: "contentment",
    2: "love",
    3: "happiness",
    4: "enthusiasm",
    5: "excitement"
  }
}

/* Constant where the instruction text parts has been stored: */
const instruction = [  "The idea is to use a set of data obtained from a research conducted on 32 people " +
    "while having a conversation on social issues. These people, of various genres, age and ethnicities, were " +
    "equipped with sensors who allow us to know different biometric information such as heart rate and brain " +
    "signals. The emotions they felt have been discussed at the end using a numeric rate with two integer values " +
    "from 1 to 5: valence and arousal. These values can be used to identify the specific emotion on the " +
    "valence-arousal domain: the James Russel model.",

    "Through this web app you can regulate the value of each sensor using the correspondent slider and " +
    "see the relative values of valence and arousal in the horizontal sliders below, and the emotion they felt " +
    "according to James Russel Model. You can use your mouse or you can write the value you want to give to that " +
    "sensor using the keyboard: click on the current value of the sensor, then change the number and press Enter. " +
    "You should see the slider properly visually updated. Press Submit to see the result of the components " +
    "combination.",

    "If you click on PCA Components button, you will get the sliders of the components obtained with Principal " +
    "Component Analysis (PCA). This is the \"PCA Components Mode\". You can use these slider in the same way of the " +
    "general ones: set the components value and then see valence, arousal and correspondent emotion clicking on " +
    "Submit button. If you want to came back to the previous mode, click on the Close PCA Component Mode button.",

    "A feature importance analysis was conducted on general and raw data. You can see the plots obtained with a " +
    "click on Other Features button. Depending on the mode you are in, you will see plots processed with all the " +
    "sensors or with the components resulted from PCA Analysis. Thanks for using our web app. Enjoy! " +
    "From EmotionCalculator Developers."
]

/* Variable to use when the instruction are shown to navigate the text parts: */
let currentInstructionPart;

/* Variable to set to true when PCA Components mode is active and the PCA Components are shown: */
let PCAMode = false;

/* Initializing the "Other Features" button to show, when clicked, the feature importance plot: */
let buttonOther = document.getElementById("other");
buttonOther.addEventListener("click", openOtherFeaturesBlock);



/**************** "Other Features" Button Properties ****************/

/******** Function to open the "Other Features" block with the feature importance plots. ********/
function openOtherFeaturesBlock() {

    /* Creation of all the proper html structures: */
    let otherFeaturesBlock = document.createElement("div");
    otherFeaturesBlock.id = "otherFeatDiv";

    let header = document.createElement("HEADER");

    let cancel = document.createElement("button");
    cancel.className = "cancel";
    cancel.textContent = "X";
    cancel.addEventListener("click", closeOtherFeaturesBlock)
    header.appendChild(cancel);

    otherFeaturesBlock.appendChild(header);

    /* Call of the function to apply the "overlay effect": */
    applyOverlayEffect(otherFeaturesBlock);

    /* Distinction of the plots that will be loaded based on the current mode. */
    if(PCAMode == false)
        loadPlots(otherFeaturesBlock, "general");
    else
        loadPlots(otherFeaturesBlock, "PCA");
}

/******** Function to load the proper feature importance plots on the "Other Features" block. ********/
function loadPlots(otherFeaturesBlock, mode) {

    /* First plot html structures: */
    let plotsDiv = document.createElement("div");
    plotsDiv.className = "plotDiv";
    otherFeaturesBlock.appendChild(plotsDiv);

    /* Creation of the img object of the first plot: */
    let generalFeatureImportancePlot = document.createElement("img");
    generalFeatureImportancePlot.src = "./static/img/" + mode + "FI.png";
    generalFeatureImportancePlot.className = "plot";
    plotsDiv.appendChild(generalFeatureImportancePlot);

    /* Creation of the title of the first plot: */
    let generalPlotTitle = document.createElement("h3");
    generalPlotTitle.innerText = mode + " feature importance plot";
    generalPlotTitle.className = "plotTitle";
    plotsDiv.appendChild(generalPlotTitle);

    /* Second plot html structures: */
    plotsDiv = document.createElement("div");
    plotsDiv.className = "plotDiv";
    otherFeaturesBlock.appendChild(plotsDiv);

    /* Creation of the img object of the second plot: */
    let rowFeatureImportancePlot = document.createElement("img");
    rowFeatureImportancePlot.src = "./static/img/" + mode + "RowFI.png";
    rowFeatureImportancePlot.className = "plot";
    plotsDiv.appendChild(rowFeatureImportancePlot);

    /* Creation of the title of the second plot: */
    let rowPlotTitle = document.createElement("h3");
    rowPlotTitle.innerText = "row " + mode + " feature importance plot";
    rowPlotTitle.className = "plotTitle";
    plotsDiv.appendChild(rowPlotTitle);
}

/******** Function to visualize a block at the center of the page with position fixed. ********/
function applyOverlayEffect(block) {

    let overlayEffect = document.createElement("div");
    overlayEffect.id = "overlay";
    overlayEffect.appendChild(block);
    let body = document.getElementsByTagName("body")[0];
    body.appendChild(overlayEffect);
}

/******** Function to remove the "Other Features" block after the click on "X" button. ********/
function closeOtherFeaturesBlock() {

    let otherFeaturesBlock = document.getElementById("otherFeatDiv");
    otherFeaturesBlock.remove();

    let overlay = document.getElementById("overlay");
    overlay.remove();
}



/**************** "PCA Components" Button Properties ****************/
let buttonPCA = document.getElementById("PCAButton");

/******** Function to switch to PCA Mode ********/
function switchToPCAComponents() {

    /* If this is the first time the user press the button, perform an Ajax request and update the proper structures. */
    if(oldComponentsProperties=="") {

        performAjaxRequest('PCA', "", function(dataset) {

            /* Saving general components properties to retrieve them the next time. */
            oldComponentsProperties = componentsProperties;
            componentsProperties = dataset;

            handleModeChange();
        });
    }

    /* If this is not the first time: */
    else {

        /* Retrieve general components properties and save PCA ones. */
        PCA_tmp = componentsProperties;
        componentsProperties = oldComponentsProperties;
        oldComponentsProperties = PCA_tmp;

        handleModeChange();
    }
}

/******** Function to clean the components board and to fill with the other ones. ********/
function handleModeChange() {

    /* Cleaning of the components board: */
    const componentsBoard = document.getElementById("componentsBoard");
    componentsBoard.innerHTML = "";

    /* Call of the proper functions to load the new sliders and to apply all of the logic and design properties: */
    loadSliders();
    applySlidersProperties();

    /* Handling of the PCA Components button giving the possibility to close the PCA Components mode: */
    buttonPCA.textContent = "Close PCA Components Mode";
    buttonPCA.removeEventListener("click", switchToPCAComponents);
    buttonPCA.addEventListener("click", closePCAComponentsMode);

    PCAMode = true;
}

/******** Function to close the PCA Components mode. ********/
function closePCAComponentsMode() {

    /* Cleaning of the components board: */
    const componentsBoard = document.getElementById("componentsBoard");
    componentsBoard.innerHTML = "";

    /* Call of the proper functions to load the previous sliders: */
    loadSliders();

    /* Handling of the Close PCA Components Mode button giving the possibility to open the PCA Components mode: */
    buttonPCA.textContent = "PCA Components";
    buttonPCA.removeEventListener("click", closePCAComponentsMode);
    buttonPCA.addEventListener("click", switchToPCAComponents);

    PCAMode = false;
}

/******** Function to create a component slider. ********/
function createSlider(min, max, name) {

    let component = document.createElement("div");
    component.className = "component";
    let sliderDiv = document.createElement("div");
    sliderDiv.className = "sliderDiv";

    /* Creation of a slider with min, max, name and step fixed. The initial value is the mean value: */
    let rangeInput = document.createElement("input");
    rangeInput.type = "range";
    rangeInput.classList.add("vertical", "slider");
    rangeInput.min = min;
    rangeInput.max = max;
    rangeInput.name = name;
    rangeInput.step = 1;
    rangeInput.setAttribute("value", (min+max)/2);
    sliderDiv.appendChild(rangeInput);
    component.appendChild(sliderDiv);

    /* Creation of the label to show the sensor/component name: */
    let label = document.createElement("label");
    label.className = "componentName";
    label.innerText = name;
    component.appendChild(label);

    /* Creation of the input to show the current value: */
    let input = document.createElement("input");
    input.min = min;
    input.max = max;
    input.type = "number";
    input.className = "value";
    input.id = "span" + name;
    component.appendChild(input);

    return component;
}


/**************** "Submit" Button Properties ****************/

/******** Function to handle the submit operations. ********/
function submit() {

    /* Getting components sliders values: */
    let inputsRange = document.getElementsByClassName("vertical");
    let slidersList = {}
    for (const component of inputsRange) {
        slidersList[component.name] = component.value;
    }

    /* Sending sliders values and current mode to server: */
    let classificationType = ( PCAMode == false )? "General Submit" : "PCA Submit";
    performAjaxRequest(classificationType, slidersList, function(labels) {

        /* Update of the valence and arousal sliders with the model prediction: */
        updateOutputSliders(labels);

        /* Update of the emotion field with the correspondent emotion: */
        updateEmotion(labels);
    });
}

/******** Function to update the valence and arousal sliders with the new values predicted. ********/
function updateOutputSliders(labels) {

    let outputSliders = document.getElementsByClassName("outputSlider");
    let output = document.getElementsByClassName("output value");

    for (let i=0; i<2; i++) {

        outputSliders[i].value = labels[0][i];
        output[i].innerHTML = labels[0][i];

        /* Visual update of the slider: */
        let min = outputSliders[i].min;
        let max = outputSliders[i].max;
        let percentage = (labels[0][i] - min) / (max - min) * 100;
        let color = "linear-gradient(90deg, rgba(48, 87, 144, 1) " + percentage + "%, rgb(187, 200, 214, 1) " + percentage + "%)";
        outputSliders[i].style.background = color;
    }
}

/******** Function to update the emotion field with the emotion related to the values of arousal and valence. ********/
function updateEmotion(labels) {

    /* Getting the emotion word from the valence-arousal domain mapped in the variable valenceArousalDomain: */
    let valence = labels[0][0];
    let arousal = labels[0][1];
    let emotionWord = valenceArousalDomain[valence][arousal];

    let emotionP = document.getElementById("emotion");
    emotionP.innerText = emotionWord;

    /* Handling the effect of new emotion predicted: the word comes out as red and slowly turns blue. */
    emotionP.style.animationName = "colorChange";
    emotionP.style.animationDuration = "2s";
    emotionP.style.animationDirection = "forward";
    setTimeout(function() {

        emotionP.style.animationName = "none";
        emotionP.style.color = "#181874";
    },2000);
}


/**************** "Instruction Manual" Button Properties ****************/

/******** Function to show the instruction block. ********/
function showInstruction() {

    let instructionBlock = document.createElement("div");
    instructionBlock.id = "instructionBlock";

    let header = document.createElement("HEADER");

    /* Creation of the cancel button to close the instruction block: */
    let cancel = document.createElement("button");
    cancel.className = "cancel";
    cancel.textContent = "X";
    cancel.addEventListener("click", closeInstructionBlock)
    header.appendChild(cancel);

    instructionBlock.appendChild(header);

    /* Creation of the instruction text area: */
    let p = document.createElement("p");
    p.className = "details instructionP";
    currentInstructionPart = 0;
    p.innerText = instruction[currentInstructionPart];
    instructionBlock.appendChild(p);

    let controlButtonsDiv = createInstructionButtons();
    instructionBlock.appendChild(controlButtonsDiv);

    applyOverlayEffect(instructionBlock);
}

/******** Function to create the instruction buttons to navigate back and forward the instruction texts. ********/
function createInstructionButtons() {

    let controlButtonsDiv = document.createElement("div");
    controlButtonsDiv.id = "controlButtonsDiv";

    /* Creation of the "Back" button to show the previous part of the instruction: */
    let back = document.createElement("button");
    back.className = "cancel";
    back.id = "backButton";
    back.textContent = "Back";
    back.disabled = true;
    back.style.color = "lightgray";
    back.addEventListener("click", function() {

        previousPartOfInstruction();
    });
    controlButtonsDiv.appendChild(back);

    /* Creation of the "Continue reading" button to show the next part of the instruction: */
    let next = document.createElement("button");
    next.className = "cancel";
    next.id = "nextButton";
    next.textContent = "Continue reading";
    next.addEventListener("click", function() {

        nextPartOfInstruction();
    });
    controlButtonsDiv.appendChild(next);

    return controlButtonsDiv;
}

/******** Function to show the previous part of the instruction. ********/
function previousPartOfInstruction() {

    let p = document.getElementsByClassName("details instructionP")[0];

    /* If the part of the instruction the user want to see is the first one, the "Back" button have to be disabled: */
    if(currentInstructionPart==1) {

        let backButton = document.getElementById("backButton");
        backButton.disabled = true;
        backButton.style.color = "lightgray";
    }
    /* If the part of the instruction the user want to see is the penultimate one, the "Continue Reading" button have
    to be enabled: */
    else if(currentInstructionPart==3) {

        let nextButton = document.getElementById("nextButton");
        nextButton.disabled = false;
        nextButton.addEventListener("mouseover", function() {

            nextButton.style.color = "gray";
        })
        nextButton.addEventListener("mouseleave", function() {

            nextButton.style.color = "lightgray";
        })
    }

    /* Update of the current instruction part: */
    currentInstructionPart--;
    p.textContent = instruction[currentInstructionPart];
}

/******** Function to show the next part of the instruction. ********/
function nextPartOfInstruction() {

    let p = document.getElementsByClassName("details instructionP")[0];

    /* If the part of the instruction the user want to see is not the first one, the "Back" button have to be
    enabled: */
    if(currentInstructionPart==0) {

        let backButton = document.getElementById("backButton");
        backButton.disabled = false;

        backButton.addEventListener("mouseover", function() {

            backButton.style.color = "gray";
        })
        backButton.addEventListener("mouseleave", function() {

            backButton.style.color = "lightgray";
        })
    }
    /* If the part of the instruction the user want to see is the last one, the "Continue reading" button have to be
    disabled: */
    else if(currentInstructionPart==2) {

        let nextButton = document.getElementById("nextButton");
        nextButton.disabled = true;
        nextButton.style.color = "lightgray";
    }

    currentInstructionPart++;
    p.textContent = instruction[currentInstructionPart];
}

/******** Function to close the instruction block. ********/
function closeInstructionBlock() {

    let instructionBlock = document.getElementById("instructionBlock");
    instructionBlock.remove();

    let overlay = document.getElementById("overlay");
    overlay.remove();
}

/**************** Ajax Request Function ****************/
function performAjaxRequest(type, values_list, callback) {

      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/process_request");
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onload = function() {
        if (xhr.status === 200) {

            /* Handling the response: */
            const response = JSON.parse(xhr.responseText);
            const result = response.result;
            callback(result);
        }
      };

      /* Handling the request and the related parameters depending on the type and components mode: */
      if(type=="General Submit" || type=="PCA Submit")
        xhr.send(JSON.stringify({ type: type,  values: values_list }));
      else
        xhr.send(JSON.stringify({ type: type }));
}
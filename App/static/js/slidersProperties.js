/* Variables to be used to store sensors/components properties when switching to or from PCA mode: */
let oldComponentsProperties = "";

/* Calling function to load valence and arousal sliders: */
createValenceAndArousalSliders();

/******** Function to load valence and arousal sliders. ********/
function createValenceAndArousalSliders() {

    let verticalSlider = document.getElementsByClassName("vertical");

    let arousalMin = componentsProperties["arousal"]["min"];
    let arousalMax = componentsProperties["arousal"]["max"];
    let valenceMin =  componentsProperties["valence"]["min"];
    let valenceMax = componentsProperties["valence"]["max"];

    let arousalSlider = createRangeInput("arousalOutput", arousalMin, arousalMax);
    let valenceSlider = createRangeInput("valenceOutput", valenceMin, valenceMax);

    let highArousalImage = document.getElementById("highArousalEmoticon");
    highArousalImage.insertAdjacentElement("beforebegin", arousalSlider);

    let highValenceImage = document.getElementById("highValenceEmoticon");
    highValenceImage.insertAdjacentElement("beforebegin", valenceSlider);
}

/******** Function to load components sliders. ********/
function loadSliders() {

    /* Cleaning of the components board: */
    const componentsBoard = document.getElementById("componentsBoard");
    componentsBoard.innerHTML = "";

    /* Creation of every slider using componentsProperties variable passed by the server: */
    for (const key in componentsProperties) {

        /* If the key is 'valence' or 'arousal', skip the iteration: only the sensors/components sliders are loaded
         with this function: */
        if(key=="valence" || key=="arousal")
            continue;

        let slider = createSlider(Number(componentsProperties[key]['min']), Number(componentsProperties[key]['max']), key);
        componentsBoard.appendChild(slider);
    }

    /* Call of the proper function to apply all of the logic and design properties: */
    applySlidersProperties();
}

/******** Function to create a range input to build valence and arousal sliders. ********/
function createRangeInput(name, min, max) {

    /* Creation of a slider with min, max, name and step fixed. The initial value is the mean value: */
    let rangeInput = document.createElement("input");
    rangeInput.type = "range";
    rangeInput.name = name;
    rangeInput.classList.add("outputSlider", "slider");
    rangeInput.min = min;
    rangeInput.max = max;
    rangeInput.disabled = "true";
    rangeInput.setAttribute("value", (min+max)/2);

    /* Application of the automatic update property of the span which represents the value of the slider every time it
    is updated */
    let span = document.getElementsByClassName("output value");
    i = ( name == "valenceOutput" )? 0:1;
    span[i].textContent = rangeInput.value;
    rangeInput.addEventListener('change', () => {

      span[i].textContent = rangeInput.value;
    });

    return rangeInput;
}

/******** Function to apply the sliders logic and design properties. ********/
function applySlidersProperties() {

    let input = document.getElementsByClassName("value");
    let verticalSlider = document.getElementsByClassName("vertical");

    /* Application of the properties to all the sensors/components sliders: */
    for(let i=0; i<verticalSlider.length; i++) {

        applyInputProperties(input[i],verticalSlider[i]);

        /* Definition of a listener to update the slider every time the cursor is moved from a position to another using
         the mouse: */
        verticalSlider[i].addEventListener("mousemove", function() {

            /* If there is an error message, remove it: */
            p = document.getElementById("error" + verticalSlider[i].name);
                if(p)
                    p.remove();

            /* Update the slider with the new value: */
            visualUpdateSlider(verticalSlider[i]);
        })
    }

}

/******** Function to apply properties to a specific input of a slider. ********/
function applyInputProperties(input, slider) {

    /* The input object below the slider have to be updated every time the correspondent slider is updated: */
    input.value = slider.value;
    slider.oninput = function() {

        input.value = slider.value;
    }
    /* The input object below the slider can be updated manually from the user using the keyboard: */
    input.addEventListener("change", function() {

        let value = Number(this.value);
        /* If the added number is outside the allowed range: */
        if (value < this.min || value > this.max) {

            let p = document.getElementById("error" + slider.name);
            if(p)
                return;

            /* Adding the error message: */
            handleErrorMessage(slider);
        }
        /* If the added number is inside the allowed range: */
        else {

            /* If there is an error message, remove it: */
            p = document.getElementById("error" + slider.name);
            if(p)
                p.remove();

            /* Update the slider with the new value: */
            slider.value = input.value;
            visualUpdateSlider(slider);
        }
    });
}

/******** Function used to create the error message in case of input value outside the range. ********/
function handleErrorMessage(slider) {

    /* Creation of the message: */
    p = document.createElement("p");
    p.id = "error" + slider.name;
    p.className = "error";
    p.innerText = "Error: Value is outside the allowed range: [" + slider.min + "," + slider.max + "].";

    let sliderDiv = slider.parentElement;
    let component = sliderDiv.parentElement;
    component.appendChild(p);
}

/******** Function to update the slider value, min, max and visual aspect. ********/
function visualUpdateSlider(verticalSlider) {

    let value = verticalSlider.value;
    let min = verticalSlider.min;
    let max = verticalSlider.max;

    /* Design handling of the selected part of the slider: */
    let percentage = (value - min) / (max - min) * 100;
    let color = "linear-gradient(90deg, rgba(48, 87, 144, 1) " + percentage + "%, rgb(187, 200, 214, 1) " + percentage + "%)";
    verticalSlider.style.background = color;
}
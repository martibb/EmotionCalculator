var slider = document.getElementsByClassName("slider");
var verticalSlider = document.getElementsByClassName("vertical");
var output = document.getElementsByClassName("value");


for(let i=0; i<slider.length; i++) {

    output[i].innerHTML = slider[i].value;
    
    slider[i].oninput = function() {

        output[i].innerHTML = this.value;
    }
}

for(let i=0; i<verticalSlider.length; i++) {

    output[i].innerHTML = verticalSlider[i].value;
    
    verticalSlider[i].addEventListener("mousemove", function() {

        var x = verticalSlider[i].value;
        var color = "linear-gradient(90deg, rgba(48, 87, 144, 1) " + x + "%, rgb(187, 200, 214, 1) " + x + "%)";
        verticalSlider[i].style.background = color;
    })
}

var button = document.getElementById("other");

button.addEventListener("click", openOtherFeaturesBlock)

function openOtherFeaturesBlock() {

    let otherFeaturesBlock = document.createElement("div");
    otherFeaturesBlock.id = "otherFeatDiv";

    let header = document.createElement("HEADER");

    let cancel = document.createElement("button");
    cancel.id = "cancel";
    cancel.textContent = "X";
    cancel.addEventListener("click", closeOtherFeaturesBlock)

    header.appendChild(cancel);

    otherFeaturesBlock.appendChild(header);

    applyOverlayEffect(otherFeaturesBlock);
}

function applyOverlayEffect(block) {

    let overlayEffect = document.createElement("div");
    overlayEffect.id = "overlay";
    overlayEffect.appendChild(block);
    let body = document.getElementsByTagName("body")[0];
    body.appendChild(overlayEffect);
}

function closeOtherFeaturesBlock() {

    let otherFeaturesBlock = document.getElementById("otherFeatDiv");
    otherFeaturesBlock.remove();

    let overlay = document.getElementById("overlay");
    overlay.remove();
}
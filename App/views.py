from flask import Blueprint, render_template, request, jsonify
from classify import get_components_properties, classify, PCA_classify, compute_row_feature_importance

views = Blueprint(__name__, "views")


@views.route('/')
def index():
    results = get_components_properties("general")
    return render_template('index.html', results=results)


@views.route("/process_request", methods=["POST"])
def process_request():
    type = request.json["type"]

    if type == "PCA":
        result = get_components_properties(type)
    elif type == "General Submit":
        components_value = request.json["values"]
        result = classify(components_value)
        compute_row_feature_importance("General", components_value)
        result = result.tolist()
    else: # type: "PCA Submit"
        components_value = request.json["values"]
        print(components_value)
        result = PCA_classify(components_value)
        compute_row_feature_importance("PCA", components_value)
        result = result.tolist()

    return jsonify({"result": result})

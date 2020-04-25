from simpletransformers.classification import ClassificationModel
from numpy import exp, sum

flairs = ['AskIndia', 'Business/Finance', 'Coronavirus', 'Food',
       'Non-Political', 'Photography', 'Policy/Economy', 'Politics',
       'Science/Technology', 'Sports', '[R]eddiquette']
    
def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return exp(x)/sum(exp(x), axis=0)

def predict(text):
    model = ClassificationModel(
        "distilbert", 
        './models/DistilBERT/', 
        use_cuda=False, 
        num_labels=11
    )

    prediction, raw_outputs = model.predict([text])
    top_3 = raw_outputs.argsort()[0][-3:]
    confidence = softmax(raw_outputs[0])
    index = confidence.argsort()[-3:]
    return [flairs[prediction[0]], flairs[top_3[1]], flairs[top_3[0]]], [confidence[index[-1]], confidence[index[-2]], confidence[index[-3]]]
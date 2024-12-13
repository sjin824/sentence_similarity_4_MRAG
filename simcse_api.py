from flask import Flask, request, jsonify
from nltk.tokenize import sent_tokenize
from simcse import SimCSE
import numpy as np
import time

app = Flask(__name__)

# Load the SimCSE model (global load to avoid repeated initialization)
model = SimCSE("princeton-nlp/sup-simcse-roberta-large")

def select_candidate_sentences(fulltext):
    """
    Producer function: Generate candidate sentences based on input fulltext.
    Yields sentences one by one for consumers to process.
    Criteria:
    a) If len(sentences) <= 10; select all sentences.
    b) If len(sentences) <= 100; select top-10 sentences.
    c) If len(sentences) > 100; select 1/10 of sentences.
    """
    # Tokenize sentences
    sentences = sent_tokenize(fulltext)

    # Compute similarity scores
    sent_sim_scores_by_simcse = model.similarity(sentences, [fulltext])
    sent_ids_select_by_simcse = np.argsort(-sent_sim_scores_by_simcse.reshape(1, -1)).tolist()[0]

    # Determine candidate length based on rules
    if len(sentences) <= 10:
        cand_sent_ids = sent_ids_select_by_simcse
    elif len(sentences) <= 100:
        cand_sent_ids = sent_ids_select_by_simcse[:10]
    else:
        cand_length = int(len(sentences) / 10)
        cand_sent_ids = sent_ids_select_by_simcse[:cand_length]

    # Yield sentences one by one (producer behavior)
    for idx in cand_sent_ids:
        yield sentences[idx]

@app.route('/produce_sentences', methods=['POST'])
def api_produce_sentences():
    """
    API Endpoint: Acts as a producer to stream candidate sentences one by one.
    Input JSON:
        {"fulltext": "your input text here"}
    Output JSON (streamed response):
        [{"sentence": "sentence1"}, {"sentence": "sentence2"}, ...]
    """
    from flask import Response

    try:
        # Parse input JSON
        data = request.get_json()
        fulltext = data.get("fulltext", "")
        if not fulltext:
            return jsonify({"error": "No input text provided."}), 400

        def sentence_stream():
            for sentence in select_candidate_sentences(fulltext):
                time.sleep(0.1)  # Simulate delay for streaming
                yield f"{{\"sentence\": \"{sentence}\"}}\n"

        return Response(sentence_stream(), mimetype="application/json")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask API server
    app.run(host="0.0.0.0", port=5000, debug=True)

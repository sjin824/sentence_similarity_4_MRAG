from flask import Flask, request, jsonify
from nltk.tokenize import sent_tokenize
from simcse import SimCSE
import numpy as np

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
    # Descending order indexing based on the Similarity scores
    sent_ids_select_by_simcse = np.argsort(-sent_sim_scores_by_simcse.reshape(1, -1)).tolist()[0] 

    # Candidate sentence id selection based on length
    if len(sentences) <= 10:
        cand_sent_ids = sent_ids_select_by_simcse
    elif len(sentences) <= 100:
        cand_sent_ids = sent_ids_select_by_simcse[:10]
    else:
        cand_length = int(len(sentences) / 10)
        cand_sent_ids = sent_ids_select_by_simcse[:cand_length]
        
    # Candidate sentence ids, sentences and scores
    cand_sent = [sentences[i] for i in cand_sent_ids]
    cand_sent_sim_scores = [float(sent_sim_scores_by_simcse[i][0]) for i in cand_sent_ids]
    return cand_sent_ids, cand_sent, cand_sent_sim_scores


@app.route('/produce_sentences', methods=['POST'])
def api_produce_sentences():
    """
    API Endpoint: Select candidate sentences based on fulltext and return JSON.
    """
    try:
        # Parse input JSON
        data = request.get_json()
        fulltext = data.get("fulltext", "")
        if not fulltext:
            return jsonify({"error": "No input text provided."}), 400

        # Select candidate sentences
        ids, sentences, similarity_scores = select_candidate_sentences(fulltext)

        # Prepare JSON response
        response = {
            "ids": ids,
            "sentences": sentences,
            "similarity_scores": similarity_scores
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask API server
    app.run(host="0.0.0.0", port=5001, debug=True)
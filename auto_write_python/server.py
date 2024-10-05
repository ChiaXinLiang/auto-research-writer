from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Simulated storage for references and outlines
references = {}
outlines = {}

# Endpoint to get reference ids from a query
@app.route('/get_reference_ids_from_query', methods=['POST'])
def get_reference_ids():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    # Simulated retrieval of reference IDs
    reference_id = str(uuid.uuid4())
    references[reference_id] = {'topic': topic, 'title': f'Title for {topic}', 'abstract': f'Abstract for {topic}'}

    return jsonify({'reference_id': reference_id})

# Endpoint to generate a rough outline for a reference
@app.route('/generate_rough_outline', methods=['POST'])
def generate_rough_outline():
    data = request.get_json()
    reference_id = data.get('reference_id')
    if not reference_id or reference_id not in references:
        return jsonify({'error': 'Valid reference_id is required'}), 400

    # Simulated outline generation
    reference = references[reference_id]
    outline_id = str(uuid.uuid4())
    outline = {
        'reference_id': reference_id,
        'title': reference['title'],
        'abstract': reference['abstract'],
        'outline': f'Generated outline for {reference["title"]}'
    }
    outlines[outline_id] = outline

    return jsonify({'outline_id': outline_id, 'outline': outline})

# Endpoint to get all outlines
@app.route('/get_outlines', methods=['GET'])
def get_outlines():
    return jsonify({'outlines': list(outlines.values())})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
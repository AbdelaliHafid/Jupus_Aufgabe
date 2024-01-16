from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import heapq

# Create the application instance
app = Flask(__name__)

# tuple of (priority, data)
queue = []


@app.route('/api/endpoint', methods=['POST'])
def api_endpoint():
    try:
        # Get the parameters from the request
        key = request.json.get('key')
        timestamp = request.json.get('timestamp')
        location = request.json.get('location')
        document = request.json.get('document')

        # Validate the parameters
        if not key or len(key) != 32:
            return jsonify({'error': 'Invalid key parameter :'}), 400

        if not timestamp:
            return jsonify({'error': 'Missing timestamp parameter'}), 400

        if not location or location not in ['EU', 'USA']:
            return jsonify({'error': 'Invalid location parameter'}), 400

        if not document:
            return jsonify({'error': 'Missing document parameter'}), 400

        # Convert the local timestamp to UTC
        try:
            local_dt = datetime.fromtimestamp(int(timestamp))
            if location == 'EU':
                utc_dt = local_dt - timedelta(hours=1)  # EU = UTC+1
            else:  # location == 'USA'
                utc_dt = local_dt + timedelta(hours=5)  # USA = UTC-5
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format'}), 400

        # Store the document in the queue
        document.update({'key': key, 'timestamp': utc_dt, 'location': location})
        heapq.heappush(queue, (-utc_dt.timestamp(), document))

        return jsonify({'message': 'Document stored successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500

@app.route('/api/endpoint/pop', methods=['GET'])
def get_top_document():
    if queue:
        return jsonify(heapq.heappop(queue)[1])
    else:
        return jsonify({'error': 'No documents in the queue'}), 400

@app.route('/api/endpoint/all', methods=['GET'])
def get_all_documents():
    return jsonify([item[1] for item in sorted(queue, reverse=True)])



# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(debug=True)




 #class Main:
   # @staticmethod
    #def run():
        #app.run(debug=True)


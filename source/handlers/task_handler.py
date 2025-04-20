from flask import jsonify
from source.cerebras_ai_command import process_ai_command

def handle_task_request(request):
    try:
        # Get the raw request data
        data = request.get_json()
        user_input = data.get('input')
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
            
        # Process the input using your existing AI command processor
        result = process_ai_command(user_input)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 
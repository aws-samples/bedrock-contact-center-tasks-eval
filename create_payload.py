def model_payloads(input_text, model_id):
    # Define the base payload
    payload = {}

    # Check model ID and create payload accordingly
    if model_id == 'amazon.titan-text-express-v1':
        payload = {
            "inputText": input_text,
        }
    elif model_id == 'cohere.command-text-v14':
        payload = {
            "prompt": input_text,
            "max_tokens": 100,
            "temperature": 0.8,
        }
    elif model_id == 'anthropic.claude-instant-v1':
        payload = {
            "prompt": "\n\nHuman: " + input_text + "\n\nAssistant:",
            "max_tokens_to_sample": 300,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 1,
        }

    return payload
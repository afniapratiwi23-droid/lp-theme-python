from flask import Flask, render_template, request, jsonify
from generator import ContentExtractor, ThemeRenderer, GeminiExtractor, GeminiCopywriter, DesignExtractor
import os
from dotenv import load_dotenv

import logging

# Configure logging
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Index page accessed")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    logging.info("Generate request received")
    data = request.json
    html_input = data.get('html')
    api_key = data.get('api_key')
    
    # Fallback to env var if not provided
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    style = data.get('style', 'pink_curhat') # Default to pink_curhat
    custom_prompt = data.get('custom_prompt', '') # Custom style description
    rewrite_copywriting = data.get('rewrite_copywriting', False) # Default to False
    generate_variants = data.get('generate_variants', False) # Check for variants request
    reference_url = data.get('reference_url')
    
    print(f"\n=== GENERATE REQUEST ===")
    logging.info(f"API Key provided: {'Yes' if api_key else 'No'}")
    logging.info(f"HTML length: {len(html_input)} chars")
    logging.info(f"Style: {style}, Custom Prompt: {custom_prompt[:50] if custom_prompt else 'None'}")
    if reference_url:
        logging.info(f"Reference URL: {reference_url}")
    
    if not html_input:
        return jsonify({'error': 'HTML content is required'}), 400
    
    try:
        # Use GeminiCopywriter if API key provided (generates complete HTML with copywriting)
        if api_key:
            # Extract design tokens if reference URL provided
            design_tokens = None
            if reference_url:
                print(f"Extracting design from: {reference_url}")
                extractor = DesignExtractor(reference_url, api_key)
                design_tokens = extractor.extract()
                if design_tokens:
                    print("✓ Design tokens extracted")

            # Normal Single Generation
            print(f"Using GeminiCopywriter (AI-powered) - Style: {style}, Rewrite: {rewrite_copywriting}")
            copywriter = GeminiCopywriter(html_input, api_key, style, rewrite_copywriting, custom_prompt, design_tokens)
            result_html = copywriter.generate()
            
            # Clean up markdown code blocks if present
            if result_html.startswith('```html'):
                result_html = result_html.replace('```html', '', 1)
            if result_html.endswith('```'):
                result_html = result_html.replace('```', '', 1)
            
            print("✓ Gemini generation completed")
            return jsonify({'html': result_html})
        else:
            # Fallback to extraction + rendering (BeautifulSoup)
            print("Using BeautifulSoup (fallback)")
            extractor = ContentExtractor(html_input)
            extracted_data = extractor.extract()
            
            renderer = ThemeRenderer()
            result_html = renderer.render(extracted_data, 'premium')
            
            print("✓ BeautifulSoup extraction completed")
            return jsonify({'html': result_html})
            
    except Exception as e:
        print(f"ERROR in /generate: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=False, port=8080)

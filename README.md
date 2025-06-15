# Career Guidance Assistant

An AI-powered career guidance assistant that helps users explore career paths, understand required skills, and make informed career decisions.

## Features

- Career path exploration
- Skills and education requirements
- Industry insights
- Personalized career recommendations
- Interactive career guidance

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd career-guidance-assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Together API key:
   - Sign up for a Together AI account at [https://www.together.ai](https://www.together.ai)
   - Get your API key from the Together AI dashboard
   - Create a `.env` file in the project root:
   ```
   TOGETHER_API_KEY=your_api_key_here
   ```

5. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501

## API Key Configuration

The application requires a Together AI API key to function properly. Follow these steps to set up your API key:

1. Visit [Together AI](https://www.together.ai) and create an account
2. Navigate to your dashboard and find your API key
3. Create a `.env` file in the project root directory
4. Add your API key to the `.env` file:
   ```
   TOGETHER_API_KEY=your_api_key_here
   ```
5. Make sure the `.env` file is in your `.gitignore` to keep your API key secure

## Usage

1. Start the Streamlit application using `streamlit run streamlit_app.py`
2. The web interface will open in your browser
3. Enter your career-related questions or interests in the chat interface
4. Get personalized career guidance and recommendations
5. Explore different career paths and their requirements

## Example Queries

- "I want to become a software developer"
- "What skills do I need for a career in marketing?"
- "Tell me about careers in healthcare"
- "How can I transition into data science?"

## Troubleshooting

If you encounter any issues:

1. Make sure your Together API key is correctly set in the `.env` file
2. Verify that all dependencies are installed correctly
3. Check that you're running the correct file (`streamlit_app.py`)
4. Ensure your virtual environment is activated
5. Try refreshing the browser if the Streamlit interface doesn't load properly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

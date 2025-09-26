# AI-Powered MCQ Generator with Google Gemini & LangChain

An intelligent application that leverages Google's Gemini Pro model through the LangChain framework to automatically generate and evaluate Multiple Choice Quizzes from user-provided documents.

## 🚀 Live Demo & Preview

![Live Demo](https://storage.googleapis.com/project-idx-public/assets/images/placeholder.gif)
*(Note: This is a placeholder. It is highly recommended to replace this with a screen recording (GIF or MP4) of your actual application.)*

## ✨ Key Features

*   **Dynamic Document Upload:** Accepts `.pdf` and `.txt` files as source material for quiz generation.
*   **Customizable Quiz Parameters:** Users can specify the number of questions, the subject, and the difficulty level (tone) of the quiz.
*   **AI-Powered Quiz Generation:** Utilizes Google's `gemini-1.5-flash-latest` model to understand the context of the document and create relevant multiple-choice questions.
*   **Intelligent Question Evaluation:** After generation, a second AI-powered chain reviews the quiz for grammatical correctness, complexity, and suitability for the target audience.
*   **Modern LangChain Implementation:** Built using the latest LangChain Expression Language (LCEL) for creating robust and readable AI chains, not legacy components.
*   **Interactive Web Interface:** A clean and user-friendly interface built with Streamlit.

## 🛠️ Tech Stack

This project is built with a modern, industry-standard stack for GenAI application development.

### Backend & Core Logic:
*   **Python 3.11**
*   **LangChain:** The core framework for orchestrating the LLM calls and building the sequential generation/evaluation chain.
*   **LangChain Expression Language (LCEL):** Used for its composability and modern features, ensuring the application is built with current best practices.
*   **Google Gemini Pro:** The Large Language Model (`gemini-1.5-flash-latest`) used for content generation and analysis.

### Frontend:
*   **Streamlit:** For creating the interactive web-based user interface.

### Development Environment:
*   **Google Project IDX:** A cloud-based IDE with a Nix-powered environment for reproducible builds.
*   **Nix:** For declarative and reproducible environment management, ensuring all dependencies are handled correctly.

## 📂 Project Structure

A well-organized and modular folder structure is used to ensure the code is maintainable and scalable.

```
/gen-ai-portfolio
│
├── .idx/
│   └── dev.nix           # Nix environment configuration for Project IDX
│
├── mcq-generator/
│   ├── src/
│   │   └── mcqgenerator/
│   │       ├── __init__.py
│   │       ├── MCQGenerator.py # Core LangChain logic (prompts and LCEL chain)
│   │       ├── utils.py        # Utility functions (file reading, data parsing)
│   │       └── logger.py       # Logging configuration
│   │
│   ├── StreamlitAPP.py       # Main Streamlit application file
│   └── test.py                 # (Optional) For testing components
│
├── .env                    # For storing API keys (MUST NOT be committed to Git)
├── requirements.txt        # List of all Python packages for pip
└── README.md               # You are here!
```

## ⚙️ Setup & Installation

Follow these instructions to set up and run the project in your own environment.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/gen-ai-portfolio.git
    cd gen-ai-portfolio
    ```

2.  **Set Up the Environment**
    This project uses a `.nix` file for easy setup within Google's Project IDX. If you are using IDX, the environment will build automatically based on the `dev.nix` file.

    For other environments:
    *   Ensure you have Python 3.11 installed.
    *   Create and activate a virtual environment:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Configure API Keys**
    The application requires an API key from Google AI Studio to use the Gemini model.
    *   Create a file named `.env` in the root directory of the project.
    *   Go to Google AI Studio and create an API key.
    *   Add the key to your `.env` file:
        ```
        GOOGLE_API_KEY="your-gemini-api-key-here"
        ```

4.  **Run the Application**
    Once the setup is complete, you can start the Streamlit application.
    ```bash
    streamlit run mcq-generator/StreamlitAPP.py
    ```
    Your browser should open a new tab with the running application.

## 🔗 Reference Documentation

*   [Google Gemini API](https://ai.google.dev/docs)
*   [LangChain](https://python.langchain.com/docs/get_started/introduction)
*   [Streamlit](https://docs.streamlit.io/)
*   [Nix Environment for IDX](https://developers.google.com/idx/guides/customize-idx-env)


## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 👤 About The Author

Hi, I'm **Yash Desai** 👋

**Generative AI & LLM Engineer | Java • Python • Spring Boot | Exploring DevOps & SDET | Building Scalable AI Solutions**

With a strong foundation in Java backend engineering and a growing expertise in Generative AI, I specialize in building intelligent, production-ready applications that merge the robustness of enterprise systems with the innovation of Large Language Models (LLMs).

I thrive on designing solutions that are scalable, impactful, and deployment-ready—bridging backend reliability with AI innovation to deliver real-world value for businesses and communities.

<p align="left">
  <a href="https://www.linkedin.com/in/your-linkedin-profile" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/your-github-username" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

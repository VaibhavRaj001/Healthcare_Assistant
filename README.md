# Healthcare Assistant App

https://youtu.be/Lgf8j1j91ao

## Overview
This Healthcare Assistant App is designed to provide personalized meal plans and recipes based on dietary preferences, nutritional needs, local seasonal ingredients, and user likes/dislikes. The app utilizes Gen AI Rag for advanced natural language processing and Pathway for structured data retrieval.

## Features
- **Personalized Meal Plans:** Tailored meal plans based on user preferences.
- **Recipe Suggestions:** Recipes generated based on selected criteria.
- **Nutritional Information:** Detailed nutritional breakdown of meals and recipes.
- **Ingredient Substitutions:** Options for ingredient substitutions based on availability or dietary restrictions.
- **User Preferences:** Customizable settings for dietary preferences and allergies.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- **Operating System:** Windows 10 or later
- **Docker:** Installed and configured
- **Python:** Installed (if needed for development purposes)
- **WSL:** Windows Subsystem for Linux (for Windows users)
- **pip:** Installed (for managing Python packages)

## Installation

### Docker Setup
1. **Clone the repository:**
    ```sh
    git clone https://github.com/VaibhavRaj001/Healthcare_Assistant.git
    cd your-repo-name
    ```

2. **Create a `.env` file in the project directory and add your OpenAI API key:**
    ```sh
    echo "OPENAI_API_KEY=your-openai-api-key" > .env
    ```

3. **Build and run the Docker container:**
    ```sh
    docker compose up --build
    ```

4. **Access the app:**
    Open your web browser and navigate to `http://localhost:8501` to access the Healthcare Assistant App.

## Usage
- Follow the on-screen instructions to input your dietary preferences, nutritional needs, and any specific likes or dislikes.
- Generate personalized meal plans and recipes.
- Review the nutritional information and make any necessary adjustments or substitutions.

## Contributing
To contribute to this project, follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Video Demonstration
For a video demonstration of the app, please check out the following link: [Video Demonstration](https://youtu.be/Lgf8j1j91ao)

## Contact
If you have any questions or need further assistance, please feel free to contact me at [vaibhavraj73400@gmail.com].


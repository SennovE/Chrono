# Chrono
# Chrono

**Chrono** is a Python-based web application designed to help users create both individual and team schedules for the day based on natural language input. Leveraging the GPT API, Chrono generates personalized schedules, allowing users to efficiently manage their time and tasks.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

Chrono offers a robust set of features to streamline daily planning and task management:

### 1. Task Calendar

- **Daily Task Blocks**: Visualize tasks as blocks on a calendar by day.
- **Manual & Automated Entry**: Add tasks manually or generate a full-day schedule using natural language prompts.
- **Customizable Generation Parameters**: Tailor schedule generation based on personal preferences for each day.
- **Customization Options**: Personalize the calendar's background and task block appearance.

### 2. Deadlines Page

- **Deadline Management**: View deadlines organized by day through a list of cards.
- **Automated Deadline Generation**: Create deadlines using free-form text input.
- **Manual Addition**: Add specific deadlines manually as needed.

### Additional Features

- **Default Settings**: Configure default schedule generation settings.
- **Template Creation**: Compose and save schedule templates for recurring use.
- **Multiple Calendars**: Manage several calendars (e.g., individual and team) within the application.
- **Progress Tracking**: Mark tasks as completed or incomplete and monitor progress over time.

## Demo

![Chrono Demo](path_to_demo_image.png)

*Screenshot of Chrono's Task Calendar and Deadlines Page.*

## Installation

Follow these steps to set up Chrono on your local machine:

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Git**

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/chrono.git
   cd chrono
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add your GPT API key:

   ```env
   GPT_API_KEY=your_openai_api_key
   ```

5. **Run Database Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   Open your browser and navigate to `http://localhost:8000`.

## Usage

### Generating a Schedule

1. Navigate to the **Task Calendar** page.
2. Click on the **Generate Schedule** button.
3. Enter your daily objectives or preferences in the text prompt.
4. Adjust generation parameters as needed.
5. Click **Generate** to create a schedule for the day.

### Managing Deadlines

1. Go to the **Deadlines** page.
2. To add a deadline, click **Add Deadline** and enter the details manually or use the **Generate Deadline** option with a text prompt.
3. Deadlines will appear as cards organized by their respective dates.

### Customizing Calendars

1. Access the **Settings** page.
2. Choose to create a new calendar (e.g., Team Calendar).
3. Customize the appearance and default settings for each calendar.
4. Switch between calendars as needed to manage different schedules.

### Tracking Progress

- Mark tasks as **Completed** or **Incomplete** directly from the calendar or deadlines page.
- View progress indicators to monitor your daily or team productivity.

## Configuration

Chrono allows extensive customization to fit your workflow:

- **Default Settings**: Set default preferences for schedule generation under the **Settings** page.
- **Templates**: Create and save schedule templates for recurring use, enhancing consistency in planning.
- **Customization**: Personalize the calendar's appearance, including background themes and task block styles.

## Contributing

Contributions are welcome! Please follow these steps to contribute to Chrono:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your code follows the project's coding standards and includes relevant tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact [your.email@example.com](mailto:your.email@example.com).

---

*Happy Scheduling with Chrono!*

# AdVizor - Ad Performance Analytics Dashboard

AdVizor is a powerful Django-based web application that provides real-time analytics and visualization for advertising campaign performance data. This dashboard helps marketing teams and advertisers track, analyze, and optimize their advertising campaigns through intuitive visualizations and filtering capabilities.

## Features

- **Interactive Dashboard**
  - Real-time data visualization
  - Key performance metrics at a glance
  - Dynamic filtering capabilities
  - Custom date range selection
  - Record count indicators for time ranges

- **Performance Metrics**
  - Total clicks tracking
  - Click-through rate (CTR) analysis
  - Conversion rate monitoring
  - Performance by ad type
  - Geographic performance analysis
  - Ad topic effectiveness

- **Data Visualization**
  - Daily clicks trend charts
  - Performance comparison graphs
  - Geographic distribution maps
  - Topic performance analysis

## Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AdVizor
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

## 🚀 Getting Started

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Dashboard: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

## Data Import

1. **Prepare your CSV data**
   - Ensure your CSV file contains the required columns:
     - click_time
     - ad_type
     - location
     - ad_topic
     - clicks
     - impressions
     - ctr
     - conversion_rate

2. **Import data through the admin interface**
   - Log in to the admin interface
   - Navigate to the Advertisement section
   - Use the "Import" button to upload your CSV file

## Using the Dashboard

1. **Filtering Data**
   - Use the date range filter to select specific time periods
   - Filter by ad type, location, and ad topic
   - Use the custom date range option for precise date selection
   - View record counts for each time range

2. **Analyzing Performance**
   - Monitor key metrics in the top cards
   - Analyze trends in the daily clicks chart
   - Compare performance across different ad types
   - Review geographic distribution of performance
   - Evaluate ad topic effectiveness

## Customization

1. **Adding New Metrics**
   - Add fields to the Advertisement model in `models.py`
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

2. **Modifying Visualizations**
   - Edit the dashboard template in `dashboard/templates/dashboard.html`
   - Update chart configurations in the JavaScript section

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Contact

Javian Ng - https://www.linkedin.com/in/javianngzh/

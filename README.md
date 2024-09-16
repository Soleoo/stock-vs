# Stock-VS

Stock-VS is an advanced inventory management software that uses cutting-edge technologies such as facial recognition for user verification, QR code generation and reading for equipment, interactive dashboards, and value prediction using Machine Learning.

## Features

- **Inventory Management**: Complete control of inventory, including adding, removing, and updating items.
- **Facial Recognition**: User verification through facial recognition to ensure data security and integrity.
- **QR Codes**: Generation and reading of QR codes to facilitate the identification and tracking of equipment.
- **Dashboards**: Real-time data visualization through interactive dashboards.
- **Value Prediction**: Use of Machine Learning algorithms to predict future values and assist in decision-making.

## Installation

### Prerequisites

- python
- django

### Installation Steps

1. Clone the repository:
    
    ```bash
    git clone https://github.com/soleoo/stock-vs.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd stock-vs
    ```
3. Install the dependencies:

    ```bash
    python 3.9.19
    pip install -r requirements.txt
    ```
4. Migrate models

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Start the application:
    
    ```bash
    python manage.py runserver
    ```
    

## Usage

### Inventory Management

- Add, remove, and update items in the inventory through the user interface or API.

### Facial Recognition

- Configure facial recognition to verify users before allowing access to sensitive features.

### QR Codes

- Generate QR codes for new equipment and use the reading functionality to track items.

### Dashboards

- Access dashboards to view real-time data about the inventory.

### Value Prediction

- Use the prediction feature to gain insights into future values and make informed decisions.

## Contribution

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Name**: Soléo
- **Email**: [ms.soleo@gmail.com](mailto:ms.soleo@gmail.com)
- **GitHub**: [Soleoo](https://github.com/soleoo)

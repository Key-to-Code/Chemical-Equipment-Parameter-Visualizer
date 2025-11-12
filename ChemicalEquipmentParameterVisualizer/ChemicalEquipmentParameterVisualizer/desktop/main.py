import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
                             QMessageBox, QTabWidget, QComboBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')

class EquipmentVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        self.datasets = []
        self.current_dataset = None
        
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        title_label = QLabel('Chemical Equipment Parameter Visualizer')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; padding: 10px;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        button_layout = QHBoxLayout()
        
        self.upload_button = QPushButton('Upload CSV File')
        self.upload_button.clicked.connect(self.upload_csv)
        button_layout.addWidget(self.upload_button)
        
        self.refresh_button = QPushButton('Refresh History')
        self.refresh_button.clicked.connect(self.load_datasets)
        button_layout.addWidget(self.refresh_button)
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.currentIndexChanged.connect(self.dataset_selected)
        button_layout.addWidget(self.dataset_combo)
        
        self.pdf_button = QPushButton('Download PDF Report')
        self.pdf_button.clicked.connect(self.download_pdf)
        self.pdf_button.setEnabled(False)
        button_layout.addWidget(self.pdf_button)
        
        main_layout.addLayout(button_layout)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_tab.setLayout(self.summary_layout)
        self.tabs.addTab(self.summary_tab, 'Summary')
        
        self.data_tab = QWidget()
        self.data_layout = QVBoxLayout()
        self.data_tab.setLayout(self.data_layout)
        self.tabs.addTab(self.data_tab, 'Data Table')
        
        self.charts_tab = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_tab.setLayout(self.charts_layout)
        self.tabs.addTab(self.charts_tab, 'Charts')
        
        self.setup_summary_tab()
        self.setup_data_tab()
        self.setup_charts_tab()
    
    def setup_summary_tab(self):
        self.summary_label = QLabel('No dataset loaded')
        self.summary_label.setStyleSheet('font-size: 14px; padding: 20px;')
        self.summary_layout.addWidget(self.summary_label)
    
    def setup_data_tab(self):
        self.data_table = QTableWidget()
        self.data_layout.addWidget(self.data_table)
    
    def setup_charts_tab(self):
        self.figure = Figure(figsize=(12, 5))
        self.canvas = FigureCanvas(self.figure)
        self.charts_layout.addWidget(self.canvas)
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': (os.path.basename(file_path), f, 'text/csv')}
                    response = requests.post(f'{API_BASE_URL}/upload/', files=files)
                    
                    if response.status_code == 201:
                        QMessageBox.information(self, 'Success', 'File uploaded successfully!')
                        self.load_datasets()
                    else:
                        error_msg = response.json().get('error', 'Unknown error')
                        QMessageBox.warning(self, 'Error', f'Upload failed: {error_msg}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to upload file: {str(e)}')
    
    def load_datasets(self):
        try:
            response = requests.get(f'{API_BASE_URL}/datasets/')
            if response.status_code == 200:
                self.datasets = response.json()
                self.dataset_combo.clear()
                
                if self.datasets:
                    for dataset in self.datasets:
                        self.dataset_combo.addItem(dataset['name'], dataset['id'])
                else:
                    self.dataset_combo.addItem('No datasets available', None)
            else:
                QMessageBox.warning(self, 'Error', 'Failed to load datasets')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to connect to server: {str(e)}')
    
    def dataset_selected(self, index):
        dataset_id = self.dataset_combo.itemData(index)
        if dataset_id:
            self.load_dataset_details(dataset_id)
            self.pdf_button.setEnabled(True)
        else:
            self.pdf_button.setEnabled(False)
    
    def load_dataset_details(self, dataset_id):
        try:
            response = requests.get(f'{API_BASE_URL}/datasets/{dataset_id}/')
            if response.status_code == 200:
                self.current_dataset = response.json()
                self.display_summary()
                self.display_data_table()
                self.display_charts()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to load dataset details')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def display_summary(self):
        dataset = self.current_dataset
        summary_text = f"""
        <h2>{dataset['name']}</h2>
        <p><b>Uploaded:</b> {dataset['uploaded_at']}</p>
        
        <h3>Summary Statistics:</h3>
        <ul>
            <li><b>Total Equipment Count:</b> {dataset['total_count']}</li>
            <li><b>Average Flowrate:</b> {dataset['avg_flowrate']:.2f}</li>
            <li><b>Average Pressure:</b> {dataset['avg_pressure']:.2f}</li>
            <li><b>Average Temperature:</b> {dataset['avg_temperature']:.2f}</li>
        </ul>
        
        <h3>Equipment Type Distribution:</h3>
        <ul>
        """
        
        for eq_type, count in dataset['type_distribution'].items():
            summary_text += f"<li><b>{eq_type}:</b> {count}</li>"
        
        summary_text += "</ul>"
        
        self.summary_label.setText(summary_text)
    
    def display_data_table(self):
        csv_data = self.current_dataset['csv_data']
        
        if csv_data:
            headers = list(csv_data[0].keys())
            self.data_table.setColumnCount(len(headers))
            self.data_table.setRowCount(len(csv_data))
            self.data_table.setHorizontalHeaderLabels(headers)
            
            for row_idx, row_data in enumerate(csv_data):
                for col_idx, header in enumerate(headers):
                    item = QTableWidgetItem(str(row_data[header]))
                    self.data_table.setItem(row_idx, col_idx, item)
            
            self.data_table.resizeColumnsToContents()
    
    def display_charts(self):
        dataset = self.current_dataset
        self.figure.clear()
        
        ax1 = self.figure.add_subplot(1, 2, 1)
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [dataset['avg_flowrate'], dataset['avg_pressure'], dataset['avg_temperature']]
        colors = ['#3498db', '#e74c3c', '#f39c12']
        
        ax1.bar(params, values, color=colors, alpha=0.7)
        ax1.set_title('Average Values by Parameter')
        ax1.set_ylabel('Value')
        ax1.grid(True, alpha=0.3)
        
        ax2 = self.figure.add_subplot(1, 2, 2)
        type_dist = dataset['type_distribution']
        
        if type_dist:
            labels = list(type_dist.keys())
            sizes = list(type_dist.values())
            colors_pie = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6']
            
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_pie[:len(labels)], startangle=90)
            ax2.set_title('Equipment Type Distribution')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def download_pdf(self):
        if self.current_dataset:
            dataset_id = self.current_dataset['id']
            try:
                response = requests.get(f'{API_BASE_URL}/datasets/{dataset_id}/generate_pdf/', stream=True)
                
                if response.status_code == 200:
                    file_path, _ = QFileDialog.getSaveFileName(
                        self, 'Save PDF Report', f"{self.current_dataset['name']}_report.pdf", 
                        'PDF Files (*.pdf)'
                    )
                    
                    if file_path:
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        QMessageBox.information(self, 'Success', f'PDF saved to {file_path}')
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to generate PDF')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to download PDF: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = EquipmentVisualizerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

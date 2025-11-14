import boto3
import random
import time
from datetime import datetime

# CloudWatch-Client erstellen
cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')  # Frankfurt-Region

# Namespace für unsere Demo-Metriken
NAMESPACE = "WebshopDemo"

# Initialisierung der akkumulierten Metriken
total_tickets_sold = 0

# Manuell festgelegter Wert für AbandonedCarts
fixed_abandoned_carts = 42  # Beispielwert, den du nach Bedarf ändern kannst

print("🚀 Sende jetzt Demo-Metriken an CloudWatch ... (alle 60 Sekunden)")

while True:
    # Zufällige Demo-Daten erzeugen
    page_views = random.randint(50, 800)
    tickets_sold_increment = random.randint(0, 3)
    
    total_tickets_sold += tickets_sold_increment

    current_train_capacity = random.randint(40, 80)

    # Metriken an CloudWatch senden
    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=[
            {'MetricName': 'PageViews', 'Value': page_views, 'Unit': 'Count'},
            {'MetricName': 'TicketsSold', 'Value': total_tickets_sold, 'Unit': 'Count'},
            {'MetricName': 'AbandonedCarts', 'Value': fixed_abandoned_carts, 'Unit': 'Count'},
            {'MetricName': 'CurrentTrainCapacity', 'Value': current_train_capacity, 'Unit': 'Percent'}
        ]
    )

    # Konsolenausgabe
    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
          f"Views={page_views}, Sold={total_tickets_sold}, Abandoned={fixed_abandoned_carts}, "
          f"TrainCapacity={current_train_capacity}%")

    # Alle 60 Sekunden neue Werte senden
    time.sleep(1)

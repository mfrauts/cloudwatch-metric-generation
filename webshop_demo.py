import boto3
import random
import time
from datetime import datetime

# CloudWatch-Client erstellen
cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')  # Frankfurt-Region

# Namespace für unsere Demo-Metriken
NAMESPACE = "WebshopDemo"

# Initialisierung der akkumulierten Metriken
total_tickets_sold = 20
total_furka_tickets_sold = 0
total_mattherhorn_gotthard_pass_2 = 0
total_mattherhorn_gotthard_pass_3 = 0
total_mattherhorn_gotthard_pass_5 = 0

# Manuell festgelegter Wert für AbandonedCarts
fixed_abandoned_carts = 42  # Beispielwert, den du nach Bedarf ändern kannst

print("🚀 Sende jetzt Demo-Metriken an CloudWatch ... (alle 60 Sekunden)")

while True:
    # Zufällige Demo-Daten erzeugen
    page_views = random.randint(50, 600)
    tickets_sold_increment = random.randint(0, 3)
    furka_tickets_sold_increment = random.randint(1, 2)

    total_tickets_sold += tickets_sold_increment
    total_furka_tickets_sold += furka_tickets_sold_increment
    total_mattherhorn_gotthard_pass_2 += random.randint(1, 3)
    total_mattherhorn_gotthard_pass_3 += random.randint(1, 2)
    total_mattherhorn_gotthard_pass_5 += random.randint(1, 1)

    current_train_capacity = random.randint(40, 80)

    # Parkplatzauslastung Täsch basierend auf current_train_capacity
    parking_capacity_tasch = current_train_capacity * 0.8  # Beispiel: 80% der Zugkapazität

    # Systemauslastung basierend auf current_train_capacity
    systemauslastung = current_train_capacity * 0.9  # Beispiel: 90% der Zugkapazität

    # Metriken an CloudWatch senden
    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=[
            {'MetricName': 'PageViews', 'Value': page_views, 'Unit': 'Count'},
            {'MetricName': 'TicketsSold', 'Value': total_tickets_sold, 'Unit': 'Count'},
            {'MetricName': 'AbandonedCarts', 'Value': fixed_abandoned_carts, 'Unit': 'Count'},
            {'MetricName': 'CurrentTrainCapacity', 'Value': current_train_capacity, 'Unit': 'Percent'},
            {'MetricName': 'ParkingCapacityTasch', 'Value': parking_capacity_tasch, 'Unit': 'Percent'},
            {'MetricName': 'FurkaTicketsSold', 'Value': total_furka_tickets_sold, 'Unit': 'Count'},
            {'MetricName': 'MatterhornGotthardPass2', 'Value': total_mattherhorn_gotthard_pass_2, 'Unit': 'Count'},
            {'MetricName': 'MatterhornGotthardPass3', 'Value': total_mattherhorn_gotthard_pass_3, 'Unit': 'Count'},
            {'MetricName': 'MatterhornGotthardPass5', 'Value': total_mattherhorn_gotthard_pass_5, 'Unit': 'Count'},
            {'MetricName': 'Systemauslastung', 'Value': systemauslastung, 'Unit': 'Percent'}  # Systemauslastung in Prozent
        ]
    )

    # Konsolenausgabe
    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
          f"Views={page_views}, Sold={total_tickets_sold}, Abandoned={fixed_abandoned_carts}, "
          f"TrainCapacity={current_train_capacity}%, ParkingTasch={parking_capacity_tasch}%, "
          f"FurkaTickets={total_furka_tickets_sold}, "
          f"MatterhornPass2={total_mattherhorn_gotthard_pass_2}, "
          f"MatterhornPass3={total_mattherhorn_gotthard_pass_3}, "
          f"MatterhornPass5={total_mattherhorn_gotthard_pass_5}, "
          f"Systemauslastung={systemauslastung}%")

    # Alle 60 Sekunden neue Werte senden
    time.sleep(5)
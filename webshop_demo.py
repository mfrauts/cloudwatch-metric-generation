import boto3
import random
import time
from datetime import datetime

# Create CloudWatch and CloudWatch Logs clients using the same credentials
region = 'eu-central-1'  # Frankfurt-Region
cloudwatch = boto3.client('cloudwatch', region_name=region)
logs_client = boto3.client('logs', region_name=region)

# Log Group and Log Stream Names
LOG_GROUP = "WebshopDemoLogs"
LOG_STREAM = "WebshopDemoStream"

# Create Log Group if it doesn't exist
try:
    logs_client.create_log_group(logGroupName=LOG_GROUP)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass

# Create Log Stream if it doesn't exist
try:
    logs_client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass

# Namespace for metrics
NAMESPACE = "WebshopDemo"

# Initialize metrics
total_tickets_sold = 20
total_furka_tickets_sold = 0
total_mattherhorn_gotthard_pass_2 = 0
total_mattherhorn_gotthard_pass_3 = 0
total_mattherhorn_gotthard_pass_5 = 0
error_count = 0  # Initialize Error Count

# Fixed value for AbandonedCarts
fixed_abandoned_carts = 42  # Example value

print("🚀 Sending demo metrics to CloudWatch... (every 5 seconds)")

# Sequence token for logs
sequence_token = None

while True:
    # Generate random demo data
    page_views = random.randint(50, 600)
    tickets_sold_increment = random.randint(0, 3)
    furka_tickets_sold_increment = random.randint(1, 2)
    error_count_increment = random.randint(0, 1)  # Random error count

    total_tickets_sold += tickets_sold_increment
    total_furka_tickets_sold += furka_tickets_sold_increment
    total_mattherhorn_gotthard_pass_2 += random.randint(1, 3)
    total_mattherhorn_gotthard_pass_3 += random.randint(1, 2)
    total_mattherhorn_gotthard_pass_5 += random.randint(1, 1)
    error_count += error_count_increment

    current_train_capacity = random.randint(40, 80)

    # Parking capacity Täsch based on current_train_capacity
    parking_capacity_tasch = current_train_capacity * 0.8  # Example: 80% of train capacity

    # System load based on current_train_capacity
    systemauslastung = current_train_capacity * 0.9  # Example: 90% of train capacity

    # Send metrics to CloudWatch
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
            {'MetricName': 'Systemauslastung', 'Value': systemauslastung, 'Unit': 'Percent'},
            {'MetricName': 'ErrorCount', 'Value': error_count, 'Unit': 'Count'}  # Error Count
        ]
    )

    # Console output
    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
          f"Views={page_views}, Sold={total_tickets_sold}, Abandoned={fixed_abandoned_carts}, "
          f"TrainCapacity={current_train_capacity}%, ParkingTasch={parking_capacity_tasch}%, "
          f"FurkaTickets={total_furka_tickets_sold}, "
          f"MatterhornPass2={total_mattherhorn_gotthard_pass_2}, "
          f"MatterhornPass3={total_mattherhorn_gotthard_pass_3}, "
          f"MatterhornPass5={total_mattherhorn_gotthard_pass_5}, "
          f"Systemauslastung={systemauslastung}%, "
          f"ErrorCount={error_count}")

    # Create log message
    log_message = (f"Exception in thread \"main\" java.lang.RuntimeException: Simulated error\n"
                   f"\tat com.example.MyClass.method(MyClass.java:10)\n"
                   f"\tat com.example.MyClass.main(MyClass.java:5)\n"
                   f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                   f"Error Count: {error_count}\n")

    # Send log message to CloudWatch Logs
    try:
        if sequence_token:
            response = logs_client.put_log_events(
                logGroupName=LOG_GROUP,
                logStreamName=LOG_STREAM,
                logEvents=[
                    {
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'message': log_message
                    }
                ],
                sequenceToken=sequence_token
            )
        else:
            response = logs_client.put_log_events(
                logGroupName=LOG_GROUP,
                logStreamName=LOG_STREAM,
                logEvents=[
                    {
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'message': log_message
                    }
                ]
            )
        sequence_token = response['nextSequenceToken']
    except logs_client.exceptions.InvalidSequenceTokenException as e:
        sequence_token = e.response['expectedSequenceToken']
    except Exception as e:
        print(f"Error sending log message: {e}")

    time.sleep(5)
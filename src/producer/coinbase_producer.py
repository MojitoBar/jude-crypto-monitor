import json
import websocket
import os
import time
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable
from datetime import datetime

class CoinbaseProducer:
    def __init__(self):
        self.init_kafka_producer()
        
        # 구독할 암호화폐 목록
        self.subscribe_message = {
            "type": "subscribe",
            "product_ids": ["BTC-USD", "ETH-USD"],  # BTC와 ETH 가격 모니터링
            "channels": ["ticker"]
        }

    def init_kafka_producer(self, max_retries=5, retry_interval=5):
        """Kafka 프로듀서 초기화 (재시도 로직 포함)"""
        for i in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092'),
                    value_serializer=lambda x: json.dumps(x).encode('utf-8')
                )
                self.create_topic()
                print("Successfully connected to Kafka")
                return
            except NoBrokersAvailable:
                if i < max_retries - 1:  # 마지막 시도가 아니면
                    print(f"Failed to connect to Kafka. Retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
                else:
                    raise  # 모든 재시도 실패시 예외 발생

    def on_message(self, ws, message):
        """웹소켓으로부터 메시지를 받았을 때 처리"""
        try:
            data = json.loads(message)
            
            if data.get('type') == 'ticker':
                # 필요한 데이터만 추출
                price_data = {
                    'product_id': data.get('product_id'),
                    'price': float(data.get('price', 0)),
                    'time': data.get('time'),
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                # Kafka로 메시지 전송
                self.producer.send('crypto-prices', price_data)
                print(f"Sent to Kafka: {price_data}")
        
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(self, ws, error):
        """에러 발생시 처리"""
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """웹소켓 연결이 닫혔을 때 처리"""
        print("WebSocket Connection Closed")

    def on_open(self, ws):
        """웹소켓 연결이 열렸을 때 처리"""
        print("WebSocket Connection Opened")
        # 구독 메시지 전송
        ws.send(json.dumps(self.subscribe_message))

    def start(self):
        """프로듀서 시작"""
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            "wss://ws-feed.exchange.coinbase.com",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def create_topic(self):
        """Kafka 토픽 생성"""
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
            )
            
            topic = NewTopic(
                name='crypto-prices',
                num_partitions=1,
                replication_factor=1
            )
            
            admin_client.create_topics([topic])
            print("Topic created successfully")
        except Exception as e:
            print(f"Topic already exists or error occurred: {e}")

if __name__ == "__main__":
    print("Starting Coinbase Producer...")
    producer = CoinbaseProducer()
    producer.start() 
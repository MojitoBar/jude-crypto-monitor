from kafka import KafkaConsumer
import json
import logging
from time import time
from datetime import datetime
from collections import defaultdict

def process_price_alerts():
    consumer = KafkaConsumer(
        'crypto-prices',
        bootstrap_servers=['kafka:29092'],
        group_id='price-alert-group',
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # 각 코인의 가격 기록을 저장할 딕셔너리
    price_history = defaultdict(list)  # {product_id: [(timestamp, price), ...]}
    last_alert = defaultdict(float)  # 마지막 경고 시점을 저장
    
    # 가격 변동 임계값 (%)
    THRESHOLD = 0.1
    # 비교 시간 간격 (초)
    INTERVAL = 60

    for message in consumer:
        current_time = time()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = message.value
        product_id = data['product_id']
        current_price = float(data['price'])
        
        # 현재 가격 기록 추가
        price_history[product_id].append((current_time, current_price))
        
        # 1분 이상 된 기록 제거
        price_history[product_id] = [
            (ts, price) for ts, price in price_history[product_id] 
            if current_time - ts <= INTERVAL
        ]
        
        # 1분 전 가격이 있는 경우에만 비교
        if len(price_history[product_id]) > 1:
            oldest_price = price_history[product_id][0][1]  # 가장 오래된 가격
            oldest_time = datetime.fromtimestamp(price_history[product_id][0][0]).strftime('%H:%M:%S')
            price_change = ((current_price - oldest_price) / oldest_price) * 100
            
            # # 모든 변동을 INFO로 로깅
            # logging.info(f"[{current_datetime}] 1min Price Change: {product_id} changed by {price_change:.2f}% "
            #             f"(${oldest_price:.2f} at {oldest_time} -> ${current_price:.2f})")
            
            # 임계값 이상 변동이고 마지막 경고로부터 1분이 지났을 때만 WARNING
            if abs(price_change) >= THRESHOLD and (current_time - last_alert[product_id]) >= INTERVAL:
                logging.warning(f"[{current_datetime}] SIGNIFICANT 1min PRICE CHANGE: {product_id} changed by {price_change:.2f}%!")
                last_alert[product_id] = current_time
        else:
            # 첫 가격 기록
            logging.info(f"[{current_datetime}] Initial price for {product_id}: ${current_price:.2f}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'  # 기본 로그 포맷을 제거하고 우리가 정의한 포맷만 사용
    )
    process_price_alerts() 
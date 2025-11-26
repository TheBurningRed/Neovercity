from queue import Queue
import time
import random

# Створити чергу заявок
queue = Queue()
request_id = 0


def generate_request():
    global request_id
    request_id += 1
    request = f"Request-{request_id}"
    queue.put(request)
    print(f"[GENERATED] {request}")


def process_request():
    if not queue.empty():
        request = queue.get()
        print(f"[PROCESSED] {request}")
    else:
        print("[INFO] Черга порожня")


def main():
    print("Press Ctrl+C to stop the program\n")
    try:
        while True:
            # Випадково генеруємо 0–2 нових заявки
            for _ in range(random.randint(0, 2)):
                generate_request()

            process_request()

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram stopped.")


if __name__ == "__main__":
    main()

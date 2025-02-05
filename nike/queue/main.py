import queue
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Thiết lập kết nối MySQL
db_url = f"mysql+pymysql://root:10051998@database:3306/nike?charset=utf8mb4"
engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=40)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo một hàng đợi
task_queue = queue.Queue()

# Hàm xử lý tác vụ từ hàng đợi
def worker():
    # Kết nối với MySQL trong mỗi worker
    session = session_factory()
    try:
        while True:
            task = task_queue.get()  # Lấy tác vụ từ hàng đợi (blocking)
            if task is None:
                break  # Dừng worker nếu gặp giá trị None
            print(f"Processing task: {task}")
            print(f"Task {task} inserted into database")
            print(f"Task {task} completed")
            task_queue.task_done()  # Đánh dấu tác vụ đã hoàn thành
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()  # Đóng kết nối khi worker kết thúc

while True:
    # Thêm các tác vụ vào hàng đợi
    for task in range(10):  # Thêm 10 tác vụ
        task_queue.put(task)
        print(f"Added task {task} to the queue")

    # Khởi động các worker
    # num_worker_threads = 3  # Số lượng worker
    # threads = []
    # for i in range(num_worker_threads):
    threading.Thread(target=worker).start()
    # threads.append(t)
    print("All tasks completed and workers stopped.")
    time.sleep(20)

# Đợi cho đến khi tất cả các tác vụ được xử lý
# task_queue.join()

# Dừng các worker
# for _ in range(num_worker_threads):
#     task_queue.put(None)  # Gửi tín hiệu dừng cho các worker
# for t in threads:
#     t.join()  # Đợi tất cả các worker kết thúc

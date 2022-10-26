import threading

def f():
  threading.Timer(5.0, f).start()  # Перезапуск через 5 секунд
  print("Hello!")

f()
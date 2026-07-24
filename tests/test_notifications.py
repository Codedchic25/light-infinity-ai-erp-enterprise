from fastapi import BackgroundTasks
from app.shared.notifications import send_order_email, check_and_send_stock_sms


def test_background_tasks_registration():
    """Verifica daca sarcinile asincrone sunt adaugate corect in coada FastAPI."""
    # Initializam managerul nativ de sarcini din FastAPI
    tasks = BackgroundTasks()

    # Adaugam task-urile in coada
    tasks.add_task(send_order_email, "test@infinity.ai", 101, 45.90)
    tasks.add_task(check_and_send_stock_sms, "Ceara de Soia Flocoane", -5.0)

    # Validam matematic ca exista exact 2 sarcini programate sa ruleze in fundal
    assert len(tasks.tasks) == 2
    assert tasks.tasks[0].func == send_order_email
    assert tasks.tasks[1].func == check_and_send_stock_sms


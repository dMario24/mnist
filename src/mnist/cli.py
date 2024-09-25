import typer
from mnist.worker import send_line_noti

def run_noti():
  typer.run(send_line_noti)
from mnist.worker import prediction, get_job_img_task, send_line_noti

def test_prediction():
    r = prediction(file_path='/a/b/c/d.png', num=2)
    assert r in range(10)


def test_get_job_img_task():
    r = get_job_img_task()
    assert True


def test_send_line_noti():
    send_line_noti("abc.png", 1)
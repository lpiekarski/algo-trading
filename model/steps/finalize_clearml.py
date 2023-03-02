def finalize_clearml(
        task,
        **kwargs):
    if task is not None:
        task.close()

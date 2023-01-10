from clearml import Task


def initialize_clearml(
        model,
        clearml_project,
        clearml_access_key,
        clearml_secret_key,
        **kwargs):
    web_server = 'https://app.clear.ml'
    api_server = 'https://api.clear.ml'
    files_server = 'https://files.clear.ml'

    Task.set_credentials(web_host=web_server,
                         api_host=api_server,
                         files_host=files_server,
                         key=clearml_access_key,
                         secret=clearml_secret_key)

    task = Task.init(project_name=clearml_project, task_name=model)
    task.mark_started()
    return dict(task=task)

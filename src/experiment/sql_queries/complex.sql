SELECT * FROM er1.task
LEFT JOIN er1.user_on_task ON task.name = user_on_task.task_name
LEFT JOIN er1.attachment ON task.name = attachment.task_name
LEFT JOIN er1.subtask ON task.name = subtask.task_name
WHERE er1.task.name = 'mBBQTeapSXoVFtjLmHmO';

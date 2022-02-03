# ! Запросы для создания форинов в проекте

# TRUNCATE TABLE public.projectstatuses CASCADE;
# INSERT INTO public.projectstatuses (name) VALUES ('Черновик'),('На согласовании'),('Утвержден'),('Отклонен'),('В работе'),('Приостановлен'),('Завершен');

# TRUNCATE TABLE public.taskstatuses CASCADE;
# INSERT INTO public.taskstatuses (name) VALUES ('Черновик'),('В работе'),('Приостановлена'),('Завершена')

# TRUNCATE TABLE public.assignmentstatuses CASCADE;
# INSERT INTO public.assignmentstatuses (name) VALUES ('Черновик'),('Назначено'),('В работе'),('Приостановлено'),('Завершено')

# ! Тестовый проект



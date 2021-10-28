CREATE TABLE IF NOT EXISTS public.task
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    assignees text,
    description text NOT NULL,
    due_date date NOT NULL,
    completed boolean NOT NULL DEFAULT FALSE,
    created_at timestamp NOT NULL DEFAULT NOW()
);
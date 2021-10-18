CREATE TABLE IF NOT EXISTS public.task
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    assignee text,
    description text NOT NULL,
    due_date date,
    completed boolean NOT NULL DEFAULT FALSE,
    created_at timestamp NOT NULL DEFAULT NOW()
);
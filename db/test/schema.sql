CREATE TABLE IF NOT EXISTS public.task
(
    id serial PRIMARY KEY,
    assignee text,
    description text NOT NULL,
    due_date date,
    created_at timestamp NOT NULL DEFAULT NOW()
);
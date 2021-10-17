BEGIN;
TRUNCATE TABLE public.task;

INSERT INTO
  public.task (assignee, description, due_date)
VALUES
  ('Martha Nielsen', 'Clean the kitchen', '2021-10-02'),
  ('Ulrich Nielsen', 'Do the laundry', '2021-10-02'),
  ('Katharina Nielsen', 'Cook a communal meal', '2021-10-05'),
  ('Magnus Nielsen', 'Clean and tidy the bedrooms', '2021-10-02'),
  ('Jonas Kahnwald', 'Vacuum and mop the floors', '2021-09-25'),
  ('Hannah Kahnwald', 'Clean out the fridge', '2021-09-25'),
  ('Hannah Kahnwald', 'Tidy and sweep the living room', '2021-09-25'),
  ('Mikhael Kahnwald', 'Tidy the studio', '2021-09-25'),
  ('Mikhael Kahnwald', 'Water the indoor plants', '2021-09-25'),
  ('Adam Kahnwald', 'Vacuum and tidy the basement', '2021-09-25');

COMMIT;
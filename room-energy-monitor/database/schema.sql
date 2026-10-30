-- Room Energy Monitor — Supabase schema
-- Run this in your Supabase project's SQL Editor (Project -> SQL Editor -> New query)

create table if not exists occupancy (
    id bigint generated always as identity primary key,
    person_present boolean not null,
    ts timestamptz not null default now()
);

create table if not exists power_readings (
    id bigint generated always as identity primary key,
    watts real not null,
    ts timestamptz not null default now()
);

create table if not exists waste_events (
    id bigint generated always as identity primary key,
    started_at timestamptz not null,
    ended_at timestamptz not null,
    watts real not null,
    kwh real not null,
    cost real not null
);

-- Single-row table that stores whether the (simulated) power has been manually cut
create table if not exists system_state (
    id int primary key default 1,
    power_cut boolean not null default false,
    constraint single_row check (id = 1)
);

insert into system_state (id, power_cut)
values (1, false)
on conflict (id) do nothing;

-- Helpful indexes for "give me the latest reading" queries
create index if not exists idx_occupancy_ts on occupancy (ts desc);
create index if not exists idx_power_readings_ts on power_readings (ts desc);

-- For a hackathon demo, disable Row Level Security so the anon key can read/write freely.
-- (In a real production app you would write proper RLS policies instead.)
alter table occupancy disable row level security;
alter table power_readings disable row level security;
alter table waste_events disable row level security;
alter table system_state disable row level security;

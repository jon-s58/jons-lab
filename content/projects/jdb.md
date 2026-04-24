+++
title = "JDB"
description = "A database written from scratch using Rust."
weight = 2

[extra]
category = "Database"
scale = "Open Source"
stage = "In Progress"
tech = ["Rust", "Databases", "Tokio"]
github = "https://github.com/jon-s58/jdb"
+++

A relational database written from scratch in Rust.

<!-- more -->

JDB is a learning-first database project — built to understand how modern relational systems actually work, from bytes on disk up to SQL. The long-term goal is PostgreSQL wire-protocol compatibility, wrapped in a clean, workspace-based Rust architecture.

## Key Features
- **Storage layer** — slotted-page design, buffer pool, and B+ tree indexes.
- **SQL layer** — parser, planner, and execution engine.
- **Server** — PostgreSQL-compatible wire protocol with connection and session management.
- **CLI** — a `psql`-like interactive shell.

## Technical Implementation
Written in Rust with Tokio for async I/O. The project is laid out as a Cargo workspace with separate crates for storage, SQL, core, server, CLI, and benchmarking — each with a single clear responsibility. Progress and design decisions are documented in the *Building a Database From Scratch* blog series.

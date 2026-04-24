+++
title = "Astra"
description = "A math and deep-learning crate written from scratch using Rust."
weight = 2

[extra]
category = "ML / Math Crate"
scale = "Open Source"
tech = ["Rust", "Deep Learning", "Math"]
github = "https://github.com/jon-s58/astra"
+++

A math and deep-learning crate written from scratch in Rust.

<!-- more -->

Astra is a personal exploration into the math behind modern deep learning, built up from first principles. Instead of wrapping an existing framework, every piece — from tensor ops to the training loop — is written from scratch in Rust, with no ML dependencies.

## Key Features
- **Tensors** — generic, n-dimensional tensor type with the core math operations.
- **Dense networks** — trainable fully-connected layers with standard activations.
- **Convolutional networks** — trainable 2D convolutional layers built on cross-correlation primitives.

## Technical Implementation
Written in Rust to deepen my understanding of the linear algebra and calculus that power neural networks, and to sharpen my Rust skills along the way. The focus is on *how things work under the hood* rather than chasing feature parity with the big frameworks — so the code stays small, readable, and something I can reason about end to end.

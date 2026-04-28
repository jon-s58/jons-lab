+++
title = "Mesh to BREP - The Challenge"
date = 2026-04-21
[taxonomies]
tags = ["Rust", "C++", "Incudo", "Machine Learning"]
[extra]
reading_time = 10
+++
What are Meshes? What are BREPs? Why is converting one to the other important, and why is it so hard?

<!-- more -->

We are diving deep into the world of mechanical engineering, 3D printing, and manufacturing. There is an unsolved problem at the intersection of these fields: converting a **mesh** into a **BREP**. Before we get into why it's hard, we need to understand what these two representations actually are.

## What is a Mesh?

A **polygon mesh** represents a 3D object's surface using a collection of vertices, edges, and faces. It's typically composed of simple shapes - most commonly triangles - which are then stitched together to approximate curves. The resolution of a mesh determines how detailed and smooth the model appears.

Imagine a teapot. How do we render it on screen in a video game? How do we represent it? The most common approach is to stitch together thousands - if not millions - of tiny triangles into the shape. The more triangles, the better the detail.

This faceted structure makes meshes computationally lightweight to draw on screen, making them ideal for video games, simulations, and visual effects. However, once we step into the world of precision, this becomes a limiting feature - and that's where BREPs come in.

## What is a BREP?

**Boundary Representation** (BREP) defines a 3D model mathematically using geometric boundaries - precisely calculated surfaces (NURBS), curves, and points. Instead of approximating a shape with flat polygons, a BREP maintains infinite precision: curves stay perfectly smooth no matter how much you zoom in.

This exact mathematical definition also allows for the inclusion of solid properties, enabling software to accurately calculate a model's physical volume and mass.

## When to Use Each?

- **Meshes** are the standard format for video games, visual effects, and 3D animation - anywhere rendering speed matters more than precision.
- **BREPs** are the essential format for CAD (Computer-Aided Design), mechanical engineering, and 3D printing - anywhere precision and physical accuracy are non-negotiable.

## What happens when we scan something physical, get our result as a mesh, and we want to manufacture it?

Well, a mesh usually isn't accurate enough for manufacturing, and it carries no design intent — no features, no parameters, no editable history. Which means we need to convert it into a BREP. And this is where things fall apart.

Imagine you 3D scan a broken bracket from a vintage machine. You get back a mesh: a few hundred thousand triangles approximating its surface. To remanufacture that part — or to modify it, simulate it, or feed it into a CAD-driven workflow — you need a BREP. You need to know "this region is a cylinder of radius 8mm", "this is a planar face", "these two faces meet at a fillet of radius 2mm". The mesh knows none of this. It only knows triangles.

## Why is it so hard?

Going from a BREP to a mesh is straightforward — you sample the math and tessellate. Going the other way is a different beast entirely. A few of the reasons:

- **Loss of intent.** A mesh is the *output* of a shape. The cylinder, the fillet, the chamfer — those concepts are gone. All that's left is a faceted approximation. Recovering them is a guessing game.
- **Surface segmentation.** Before you can fit a surface, you need to know which triangles belong to which surface. A faceted cylinder and a faceted set of small planes can look identical locally. Getting the boundaries right is its own hard problem.
- **Primitive fitting under noise.** Real-world scans are noisy. Triangles wobble. Edges are rounded by the scanner. Fitting a clean NURBS surface or a perfect cylinder through noisy data without overfitting or underfitting is delicate.
- **Topology reconstruction.** Even after you fit surfaces, you need to stitch them into a watertight, manifold solid with consistent edges and vertices. One bad junction and the BREP is invalid for downstream CAD operations.
- **Feature recognition.** A good BREP isn't just geometry — it's geometry with semantic structure. Holes, pockets, ribs, fillets. Recovering these from triangles is closer to computer vision than to geometry processing.

Each of these is hard on its own. Chained together, with each step's errors feeding into the next, they compound into a problem that has resisted a clean general solution for decades.

## The state of the solutions today

The honest answer is: there is no good general-purpose solution.

What exists today falls into two camps. On one side, semi-automatic commercial tools — Geomagic Design X, Ansys SpaceClaim, Autodesk's reverse-engineering tooling — where an engineer manually drapes surfaces, picks regions, and guides the software through reconstruction. They work, but they are expensive, slow, and require expert operators. On the other side, a body of academic research — ParseNet, ComplexGen, Point2CAD, and friends — which show promising results on clean datasets but tend to break on real scans, complex assemblies, or anything outside the distribution they were trained on.

For a problem this central to manufacturing, 3D printing, and digital fabrication, the gap between what's needed and what's available is striking.

## Where this is going

This is the problem I've been working on. The project is called **Incudo** (you may have seen it referenced as CADKit while it was still finding its name). It's a CAD processing engine built in Rust and C++, with mesh-to-BREP reconstruction as one of its core targets — alongside the rest of the geometry pipeline that production CAD work needs.

I'm not going to say much about the approach yet. The point of this post is the problem, not the answer. But over the next few entries in this series, I'll go deeper into each of the sub-problems above — segmentation, fitting, topology, features — and gradually build up to what Incudo is actually doing about them.

If you work in CAD, manufacturing, or 3D scanning and you've felt this pain, stick around.

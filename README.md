# Productivity AI — Personal Machine Learning Dashboard

A full-stack **machine learning application** that tracks daily habits, stores data in a database, and predicts productivity using a trained model.

Built with **Streamlit + Random Forest + SQLite**, this project simulates a real-world data product with persistent learning and interactive analytics.

---

## Live Demo

👉 https://predictivehabit.streamlit.app/

---

## Overview

This project analyzes how daily habits impact productivity and uses machine learning to predict future performance.

Users input daily behavior and receive:

- Productivity prediction
- Real-time analytics dashboard
- orrelation insights
- Persistent data storage (SQLite)

---

## Features

- Machine Learning prediction (Random Forest Regressor)
- Interactive dashboard (Streamlit)
- Persistent database (SQLite)
- Continuous learning (model retrains with new data)
- Seed data for cold start problem
- CSV migration support (legacy data import)
- Correlation analysis between habits and productivity

---

## Tech Stack

- Python 
- Streamlit 
- Pandas 
- Scikit-learn 
- SQLite 

---

## Machine Learning Pipeline

### Input Features (X):
- Sleep hours
- Study (0/1)
- Exercise (0/1)
- Caffeine intake
- Mood score

### Target Variable (y):
- Productivity score (0–10)

### Model:
- Random Forest Regressor
- Handles non-linear relationships and feature interactions

---

## Why Random Forest?

Random Forest was chosen because:

- It captures complex non-linear patterns
- Works well with small datasets
- Handles feature interactions automatically
- More robust than linear regression


# Loyalty, Please

A decision-making game based on selectorate theory.

## 🎮 Play the Game

👉 [https://loyalty-please-game.streamlit.app/](https://loyalty-please-game.streamlit.app/)
---

## 🧠 About

In this game, you play as the leader of an authoritarian regime.

Your goal is to maintain power for 10 turns by managing:

- State resources
- Elite loyalty
- Public anger
- Coup risk

Your decisions will determine whether your regime survives—or collapses.

---

## 🎯 Learning Objective
This game is developed for the lecture on "Economic System" (経済体制論) at Keio University.
This game is designed to help students understand:

- Selectorate Theory
- Trade-offs between private goods and public goods
- Political survival under authoritarian rule
- The dynamics of coups and mass unrest

Reference for the selectorate theory:  
De Mesquita, B. B., Smith, A., Siverson, R. M., & Morrow, J. D. (2005). The logic of political survival. MIT press.


Note: This game is developed for the lecture on "Economic System" (経済体制論) at Keio University.
---
## Project Structure
streamlit_app.py   # UI (Streamlit)
game_logic.py      # Game rules & mechanics
events.py          # Event definitions
requirements.txt   # Dependencies

---
## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run streamlit_app.py

<div align="center">

<img src="assets/banner.svg" alt="habit-tracker-cli - a simple command-line habit tracker" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-28c840?style=for-the-badge)
![Type](https://img.shields.io/badge/type-CLI-34d399?style=for-the-badge)

</div>

A simple command-line habit tracker written in Python. No dependencies, just Python 3.8+.

## 🚀 Usage

```bash
python habit.py add "drink water"     # add a habit
python habit.py done "drink water"    # mark it done today
python habit.py list                  # show all habits with streaks
python habit.py remove "drink water"  # delete a habit
```

### Example output

```text
[x] drink water               streak:   3  total: 5
[ ] read                      streak:   0  total: 2
```

## 💾 Data

Data is stored in `~/.habits.json`. Set the `HABITS_FILE` environment variable to use another location.

## 🧪 Tests

```bash
python -m unittest test_habit.py
```

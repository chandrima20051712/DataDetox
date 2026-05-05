import numpy as np
import pandas as pd


def generate_sample_data(n=250, seed=42):
    rng = np.random.default_rng(seed)

    genders = rng.choice(["Male", "Female"], size=n, p=[0.55, 0.45])
    education = rng.choice(["Bachelors", "Masters", "PhD"], size=n, p=[0.55, 0.35, 0.10])

    age = rng.normal(loc=29, scale=6, size=n).round().astype(int)
    age = np.clip(age, 21, 50)

    experience = np.clip((age - 21) * rng.uniform(0.25, 0.75, size=n) + rng.normal(2, 1.5, size=n), 0, 25)
    experience = np.round(experience, 1)

    test_score = np.clip(np.random.normal(68, 12, size=n), 35, 98).round(1)
    interview_score = np.clip(
        0.45 * test_score + np.random.normal(35, 10, size=n) + np.where(genders == "Male", 2.0, -1.5),
        30, 99
    ).round(1)

    edu_bonus = np.select(
        [education == "Bachelors", education == "Masters", education == "PhD"],
        [0, 4, 7],
        default=0
    )

    composite = (
        0.42 * test_score
        + 0.38 * interview_score
        + 0.7 * experience
        + edu_bonus
        + np.where(genders == "Male", 2.5, -2.5)
    )

    hired = np.where(composite > np.percentile(composite, 55), "Hired", "Rejected")

    df = pd.DataFrame({
        "ApplicantID": [f"A{i:04d}" for i in range(1, n + 1)],
        "Gender": genders,
        "Age": age,
        "Education": education,
        "ExperienceYears": experience,
        "TestScore": test_score,
        "InterviewScore": interview_score,
        "Hired": hired
    })

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[20, 25, 30, 35, 40, 60],
        labels=["21-25", "26-30", "31-35", "36-40", "41+"],
        include_lowest=True
    ).astype(str)

    for col, frac in {
        "Age": 0.04,
        "Education": 0.06,
        "ExperienceYears": 0.05,
        "InterviewScore": 0.04
    }.items():
        idx = rng.choice(df.index, size=max(1, int(n * frac)), replace=False)
        df.loc[idx, col] = np.nan

    return df


if __name__ == "__main__":
    df = generate_sample_data()
    df.to_csv("sample_hiring_data.csv", index=False)
    print("sample_hiring_data.csv created successfully.")
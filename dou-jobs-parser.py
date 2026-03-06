import requests
from bs4 import BeautifulSoup
import csv


BASE_URL = "https://jobs.dou.ua/vacancies/?search=python"


def get_vacancies(level=None):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(BASE_URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("li", class_="l-vacancy")

    vacancies = []

    for job in jobs:

        title_tag = job.find("a", class_="vt")
        title = title_tag.text.strip()
        link = title_tag["href"]

        company_tag = job.find("a", class_="company")
        company = company_tag.text.strip() if company_tag else "Unknown"

        city_tag = job.find("span", class_="cities")
        city = city_tag.text.strip() if city_tag else "Remote"

        # фильтр по уровню
        if level:
            if level.lower() not in title.lower():
                continue

        vacancies.append({
            "title": title,
            "company": company,
            "city": city,
            "link": link
        })

    return vacancies


def save_to_csv(vacancies):

    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["Title", "Company", "City", "Link"])

        for job in vacancies:
            writer.writerow([
                job["title"],
                job["company"],
                job["city"],
                job["link"]
            ])


def main():

    level = input("Enter level (junior/middle/senior or press enter): ")

    jobs = get_vacancies(level)

    print(f"\nFound {len(jobs)} vacancies\n")

    for job in jobs:
        print(job["title"])
        print(job["company"])
        print(job["city"])
        print(job["link"])
        print("-" * 40)

    save_to_csv(jobs)

    print("\nVacancies saved to jobs.csv")


if __name__ == "__main__":
    main()
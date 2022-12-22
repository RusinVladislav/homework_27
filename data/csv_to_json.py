import csv
import json

# передаем названия всех файлов для конвертирования
NAME_FILES_ADS_CSV = ['ad.csv', 'category.csv']
NAME_FILES_USERS_CSV = ['location.csv', 'user.csv']

AMOUNT_FILES = len(NAME_FILES_ADS_CSV)

# передаем название нашего "app" для подстановки его в начало названия модели
NAME_APP_ADS = 'ads.'
NAME_APP_USER = 'users.'

# создаем файлы с раcширением "json"
NAME_FILES_JSON_AD = [name.replace('csv', 'json') for name in NAME_FILES_ADS_CSV]
NAME_FILES_JSON_USER = [name.replace('csv', 'json') for name in NAME_FILES_USERS_CSV]

# в названии моделей в начале добавляем NAME_APP а в конце удаляем букву "s"
NAME_MODELS_AD = [NAME_APP_ADS + name.replace('.csv', '') for name in NAME_FILES_ADS_CSV]
NAME_MODELS_USER = [NAME_APP_USER + name.replace('.csv', '') for name in NAME_FILES_USERS_CSV]


def convert_file(csv_file, json_file, model):
    with open(csv_file, encoding='UTF-8') as csv_f:
        result = []
        for row in csv.DictReader(csv_f):
            record = {"model": model, "pk": row["id"]}
            del row['id']

            if "price" in row:
                row['price'] = int(row['price'])

            if "is_published" in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if "location_id" in row:
                row["locations"] = [row["location_id"]]
                del row["location_id"]

            record["fields"] = row
            result.append(record)

        with open(json_file, "w", encoding='UTF-8') as json_f:
            json_f.write(json.dumps(result, ensure_ascii=False))


for i in range(AMOUNT_FILES):
    convert_file(NAME_FILES_ADS_CSV[i], NAME_FILES_JSON_AD[i], NAME_MODELS_AD[i])
    convert_file(NAME_FILES_USERS_CSV[i], NAME_FILES_JSON_USER[i], NAME_MODELS_USER[i])

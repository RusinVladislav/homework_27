import csv
import json

# передаем названия всех файлов для конвертирования
NAME_FILES_CSV = ['ads.csv', 'categories.csv']
AMOUNT_FILES = len(NAME_FILES_CSV)

# передаем название нашего "app" для подстановки его в начало названия модели
NAME_APP = 'ads.'

# создаем файлы с раcширением "json"
NAME_FILES_JSON = [name.replace('csv', 'json') for name in NAME_FILES_CSV]

# в названии моделей в начале добавляем NAME_APP а в конце удаляем букву "s"
NAME_MODELS = [NAME_APP + name.replace('.csv', '')[:-1] for name in NAME_FILES_CSV]


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

            record["fields"] = row
            result.append(record)

        with open(json_file, "a", encoding='UTF-8') as json_f:
            json_f.write(json.dumps(result, ensure_ascii=False))


for i in range(AMOUNT_FILES):
    convert_file(NAME_FILES_CSV[i], NAME_FILES_JSON[i], NAME_MODELS[i])

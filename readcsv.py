import csv

def readCSV(fileName, colName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csvdata = []
        for row in reader:
            info = {}
            for col in colName:
                info[col] = row[col]
            csvdata.append(info)
        return csvdata

if __name__ == "__main__":
    colName = ["name","security_provider_type","displayName","password"]
    print(readCSV('Users-NFT.csv', colName))